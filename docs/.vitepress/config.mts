import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Math for CS, visually',
  description: 'A self-study companion to MIT 6.1200J Mathematics for Computer Science',
  base: '/math/',
  cleanUrls: true,
  markdown: { math: true },
  // Light by default; the toggle in the nav still switches to dark and remembers the choice.
  appearance: { initialValue: 'light' } as any,
  themeConfig: {
    nav: [
      { text: 'Start here', link: '/guide/start-here' },
      { text: 'Course map', link: '/guide/course-map' },
    ],
    sidebar: [
      {
        text: 'Guide',
        items: [
          { text: 'Start here', link: '/guide/start-here' },
          { text: 'How these lessons teach', link: '/guide/how-to-learn' },
          { text: 'Course map', link: '/guide/course-map' },
        ],
      },
      {
        text: 'Unit 1 · Proofs',
        items: [
          { text: 'L1 · 1.1–1.7 Propositions and proofs', link: '/lessons/01-proofs' },
          { text: 'L1 · 3.1–3.3 Propositional logic', link: '/lessons/03-1-propositional-logic' },
          { text: 'L1 · 3.6 Quantifiers', link: '/lessons/03-6-quantifiers' },
          { text: 'L2 · 5.1 Ordinary induction', link: '/lessons/05-1-induction' },
        ],
      },
    ],
    outline: { level: [2, 3] },
    socialLinks: [{ icon: 'github', link: 'https://github.com/karthikeyan993/math' }],
  },
})
