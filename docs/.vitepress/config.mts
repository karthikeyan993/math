import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Math for CS, visually',
  description: 'A self-study companion to MIT 6.1200J Mathematics for Computer Science',
  base: '/math/',
  cleanUrls: true,
  markdown: { math: true },
  appearance: 'dark',
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
        text: 'Part I · Proofs',
        items: [
          { text: '5.1 Ordinary induction', link: '/lessons/05-1-induction' },
        ],
      },
    ],
    outline: { level: [2, 3] },
    socialLinks: [{ icon: 'github', link: 'https://github.com/karthikeyan993/math' }],
  },
})
