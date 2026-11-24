import { defineConfig } from 'vitepress'

const repo = 'https://github.com/net-packet/Hybrid_SQLiteFTS5-Karpathy_Wiki'

// The site is served from /Hybrid_SQLiteFTS5-Karpathy_Wiki/ on GitHub Pages.
// Without `base`, every asset and every internal link is emitted as /assets/...
// and resolves to the domain root, which is a 404. This must match the repo name.
const base = '/Hybrid_SQLiteFTS5-Karpathy_Wiki/'

export default defineConfig({
  base,
  cleanUrls: true,
  themeConfig: {
    socialLinks: [{ icon: 'github', link: repo }]
  },
  locales: {
    root: {
      label: 'English',
      lang: 'en',
      title: 'Hybrid Archive',
      description: 'SQLite FTS5 + Karpathy-style wiki for Persian and English documents',
      themeConfig: {
        nav: [
          { text: 'Guide', link: '/guide/install' },
          { text: 'Reference', link: '/reference/Home' },
          { text: 'Repair', link: '/reference/layer4/Debug-Playbook' }
        ],
        sidebar: [
          {
            text: 'Guide',
            items: [
              { text: 'Install', link: '/guide/install' },
              { text: 'First ingest', link: '/guide/ingest' },
              { text: 'CLI', link: '/guide/cli' },
              { text: 'Architecture', link: '/guide/architecture' }
            ]
          },
          {
            text: 'Reference (full wiki)',
            items: [
              { text: 'Home', link: '/reference/Home' },
              { text: 'Why hybrid', link: '/reference/layer1/Why-Hybrid' },
              { text: 'Three layers', link: '/reference/layer1/Three-Layers' },
              { text: 'Data model', link: '/reference/layer1/Data-Model' },
              { text: 'DB: files', link: '/reference/layer2/DB-Files' },
              { text: 'DB: chunks', link: '/reference/layer2/DB-Chunks' },
              { text: 'DB: FTS5', link: '/reference/layer2/DB-FTS' },
              { text: 'Persian folding', link: '/reference/layer2/Persian-Normalize' },
              { text: 'Query router', link: '/reference/layer2/Query-Router' },
              { text: 'CLI reference', link: '/reference/layer2/CLI-Reference' },
              { text: 'Collections', link: '/reference/layer3/Collections' },
              { text: 'Wiki page contract', link: '/reference/layer3/Wiki-Page-Contract' },
              { text: 'Lint', link: '/reference/layer3/Wiki-Lint' },
              { text: 'Debug playbook', link: '/reference/layer4/Debug-Playbook' },
              { text: 'Verify checklist', link: '/reference/layer4/Verify-Checklist' },
              { text: 'Non-goals', link: '/reference/layer1/Non-Goals' }
            ]
          }
        ]
      }
    },
    fa: {
      label: 'فارسی',
      lang: 'fa-IR',
      link: '/fa/',
      title: 'آرشیو ترکیبی',
      description: 'آرشیو اسناد با SQLite FTS5 و ویکی به سبک کارپاتی',
      themeConfig: {
        nav: [
          { text: 'راهنما', link: '/fa/guide/install' },
          { text: 'مرجع', link: '/reference/Home' }
        ],
        sidebar: [
          {
            text: 'راهنما',
            items: [
              { text: 'نصب', link: '/fa/guide/install' },
              { text: 'اولین افزودن', link: '/fa/guide/ingest' },
              { text: 'خط فرمان', link: '/fa/guide/cli' },
              { text: 'معماری', link: '/fa/guide/architecture' }
            ]
          }
        ]
      }
    }
  }
})
