import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "林汐",
  lang: "zh_Hans",
  head: [['link', { rel: 'icon', href: 'https://raw.githubusercontent.com/netsora/SoraBot/master/resources/logo.jpg' }]],
  description: "基于 Nonebot2 和 go-cqhttp 开发，超可爱的林汐酱",
  lastUpdated: true,
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    logo: 'https://raw.githubusercontent.com/netsora/SoraBot/master/resources/logo.jpg',
    nav: [
      { text: '首页', link: '/home' },
      { text: '模块列表', link: '/module/' },
      { text: '开发指南', link: '/develop/forward/prepare' },
      {
        text: '关于我们',
        items: [
            { text: '关于', link: '/about/about'},
            { text: '贡献指南', link: '/about/contribute'},
            { text: '赞助', link: 'https://afdian.net/@netsora', target: '_blank'}
        ]
      }
    ],

    sidebar: {
        '/module/': [
            {
              text: '索引',
              items: [
                { text: '导航', link: '/module/' },
              ]
            },
            {
                text: '基础',
                collapsed: true,
                items: [
                  { text: '更新', link: '/module/' },
                ]
              },
          ],
        '/develop/': [
            {
                text: '起步',
                items: [
                    { text: '介绍', link:'/develop/forward/introduction' },
                    { text: '准备工作', link:'/develop/forward/prepare' },
                ]
            },
            {
                text: '配置',
                items: [
                    { text: '配置林汐', link: '/develop/setting/set-sora' },
                    { text: '配置Go-cqhttp', link: '/develop/setting/set-gocq'}
                ]
            }
        ],
        '/about/': [
            {
                text: '关于我们',
                items: [
                    { text: '关于', link:'/about/about' },
                    { text: '贡献指南', link:'/about/contribute' },
                    { text: '赞助', link: 'https://afdian.net/@netsora'}
                ]
            }
        ],
    },

    socialLinks: [
      { icon: 'discord', link: 'https://discord.com/invite/YRVwvYt58X'},
      { icon: 'github', link: 'https://github.com/netsora/SoraBot' },
    ],

    footer: {
        message: 'Released under the AGPL-3.0 License.',
        copyright: 'Copyright © 2023-present Evan You'
      }
  },
  
})
