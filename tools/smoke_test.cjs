#!/usr/bin/env node
// Browser smoke test: build first (npm run build), then
//   node tools/smoke_test.cjs [screenshot-dir]
// Serves docs/.vitepress/dist, opens every lesson in Chromium, drives each
// interactive component, and fails on any console or page error, or if a
// component doesn't respond the way it should.
const { chromium } = require('playwright')
const { spawn } = require('child_process')
const fs = require('fs')
const path = require('path')

const ROOT = path.resolve(__dirname, '..')
const PORT = 4179
const BASE = `http://localhost:${PORT}/math`
const shots = process.argv[2]
const lessons = fs.readdirSync(path.join(ROOT, 'docs/lessons')).filter((f) => f.endsWith('.md')).map((f) => f.replace(/\.md$/, ''))

const problems = []
const expect = (cond, msg) => { if (!cond) problems.push(msg) }

async function waitForServer() {
  try { await fetch(`${BASE}/`); throw new Error(`port ${PORT} is already in use; stop the old server first`) } catch (e) { if (e.message.includes('already')) throw e }
  for (let i = 0; i < 60; i++) {
    try { const r = await fetch(`${BASE}/`); if (r.ok) return } catch {}
    await new Promise((r) => setTimeout(r, 500))
  }
  throw new Error('preview server did not start')
}

// Per-component interactions. Each returns after checking the visible result.
const drive = {
  async PrimeStreak(page, el) {
    await el.getByRole('button', { name: 'Lock in my bet' }).click()
    for (let i = 0; i < 5; i++) await el.getByRole('button', { name: 'Run 10' }).click()
    const text = await el.innerText()
    expect(text.includes('p(40) = 1681 = 41 × 41') && text.includes('40 tests in a row passed'),
      'PrimeStreak: batches should stop at the first failure, n = 40 = 41 × 41')
  },
  async FactorSigns(page, el) {
    await el.locator('input[type=range]').fill('1')
    expect((await el.innerText()).includes('That\'s the whole proof'), 'FactorSigns: x = 1 should be inside the band')
    await el.locator('input[type=range]').fill('2.5')
    expect((await el.innerText()).includes('One factor is negative'), 'FactorSigns: x = 2.5 should have one negative factor')
    await el.locator('input[type=range]').fill('-2.5')
    expect((await el.innerText()).includes('Two factors are negative'), 'FactorSigns: x = -2.5 should have two negative factors')
  },
  async PartyGraph(page, el) {
    await el.locator('summary').click()
    await el.getByRole('button', { name: 'Load the pentagon' }).click()
    expect((await el.innerText()).includes('a counterexample for 5 people'), 'PartyGraph: pentagon should be a counterexample')
  },
  async TruthTable(page, el) {
    await el.getByRole('button', { name: 'Check' }).click()
    expect((await el.innerText()).includes('wrong or blank'), 'TruthTable: empty table should report blanks')
    await el.getByRole('button', { name: 'Show the answer' }).click()
    expect((await el.locator('.after').count()) === 1, 'TruthTable: explanation should appear after reveal')
  },
  async WasonCards(page, el) {
    const cards = el.locator('.card')
    await cards.nth(0).click(); await cards.nth(3).click()
    await el.getByRole('button', { name: 'Check my picks' }).click()
    expect((await el.innerText()).includes('Correct.'), 'WasonCards: A and 7 should be marked correct')
  },
  async EquivalenceChecker(page, el) {
    await el.getByRole('button', { name: 'Equivalent', exact: true }).click()
    expect((await el.locator('table').count()) === 1, 'EquivalenceChecker: table should appear after predicting')
    await el.locator('input').first().fill('P AND')
    expect((await el.innerText()).includes('formula ends early'), 'EquivalenceChecker: bad formula should show an error')
  },
  async QuantifierGame(page, el) {
    await el.getByRole('button', { name: 'True' }).click()
    // Statement 1 is ∀x ∃y. x + y = 4: the opponent picks x, we answer 4 − x.
    const moves = await el.locator('.moves').innerText()
    const x = Number(moves.match(/x = (\d)/)[1])
    await el.locator('.viz-controls').getByRole('button', { name: String(4 - x), exact: true }).click()
    expect((await el.innerText()).includes('You win this round'), 'QuantifierGame: y = 4 − x should win statement 1')
  },
  async QuantifierGrid(page, el) {
    await el.getByRole('button', { name: 'x = y' }).click()
    expect((await el.innerText()).includes('Done.'), 'QuantifierGrid: the diagonal should satisfy the challenge')
  },
}

;(async () => {
  // Run vitepress directly (not via npx) in its own process group, so killing
  // the group really stops it. A leftover server would serve a stale build.
  const bin = path.join(ROOT, 'node_modules/.bin/vitepress')
  const server = spawn(bin, ['preview', 'docs', '--port', String(PORT), '--strictPort'], { cwd: ROOT, stdio: 'ignore', detached: true })
  try {
    await waitForServer()
    const browser = await chromium.launch()
    for (const lesson of lessons) {
      const page = await browser.newPage({ viewport: { width: 1100, height: 900 }, deviceScaleFactor: 1 })
      page.on('console', (m) => { if (m.type() === 'error') problems.push(`${lesson}: console error: ${m.text()}`) })
      page.on('pageerror', (e) => problems.push(`${lesson}: page error: ${e.message}`))
      await page.goto(`${BASE}/lessons/${lesson}`, { waitUntil: 'networkidle' })
      expect(await page.locator('h1').count() === 1, `${lesson}: no h1`)
      expect(await page.locator('mjx-container').count() > 0, `${lesson}: no rendered maths`)
      for (const [name, fn] of Object.entries(drive)) {
        const els = page.locator(`[data-viz="${name}"]`)
        const n = await els.count()
        for (let i = 0; i < n; i++) {
          try { await fn(page, els.nth(i)) } catch (e) { problems.push(`${lesson}: ${name} #${i + 1}: ${e.message.split('\n')[0]}`) }
          if (shots) await els.nth(i).screenshot({ path: path.join(shots, `${lesson}--${name}-${i + 1}.png`) }).catch(() => {})
        }
        if (n) console.log(`  ${lesson}: drove ${n} × ${name}`)
      }
      // Revealed slots must not blow up maths (a global `svg { width: 100% }` once did).
      const tallest = await page.evaluate(() => Math.max(0, ...[...document.querySelectorAll('mjx-container svg')].map((e) => e.getBoundingClientRect().height)))
      expect(tallest < 200, `${lesson}: a MathJax formula renders ${Math.round(tallest)}px tall (CSS stretching it?)`)
      if (shots) await page.screenshot({ path: path.join(shots, `${lesson}.png`), fullPage: true })
      await page.close()
    }
    // Phone width: no horizontal scroll on any lesson.
    const phone = await browser.newPage({ viewport: { width: 390, height: 844 } })
    for (const lesson of lessons) {
      await phone.goto(`${BASE}/lessons/${lesson}`, { waitUntil: 'networkidle' })
      const overflow = await phone.evaluate(() => document.documentElement.scrollWidth - window.innerWidth)
      expect(overflow <= 1, `${lesson}: ${overflow}px horizontal scroll at phone width`)
    }
    await browser.close()
  } finally {
    try { process.kill(-server.pid) } catch {}
  }
  if (problems.length) {
    console.log(`\n${problems.length} problem(s):\n  ✗ ` + problems.join('\n  ✗ '))
    process.exit(1)
  }
  console.log(`\nSmoke test passed for ${lessons.length} lessons.`)
})()
