import { defineUserConfig } from "vuepress";
import recoTheme from "vuepress-theme-reco";

const Valine_ID = process.env.VALINE_ID;
const Valine_Key = process.env.VALINE_KEY

export default defineUserConfig({
  title: "林汐 の 文档",
  description: "SoraBot的使用与开发文档",
  head: [['link', { rel: 'icon', href: '/logo.png' }]],
  theme: recoTheme({
    style: "@vuepress-reco/style-default",
    logo: "/logo.png",
    author: "mute.",
    authorAvatar: "/head.png",
    docsRepo: "https://github.com/netsora/SoraBot",
    docsBranch: "master",
    docsDir: "website",
    lastUpdatedText: "",
    // series 为原 sidebar
    series: {
      '/blogs/about/': [
        'introduce.md',
        'about',
        'contribute'
      ],
      '/docs/module/': [
        {
          text: "索引",
          children: ['']
        },
        {
          text: "基础",
          children: ['/docs/module/base/help', '/docs/module/base/status', '/docs/module/base/repo', '/docs/module/base/broadcast', '/docs/module/base/manager']
        },
        {
          text: "工具",
          children: ['/docs/module/tools/music', '/docs/module/tools/roll', '/docs/module/tools/ciphertext', '/docs/module/tools/code', '/docs/module/tools/thesaurus']
        }
      ],
      // '/docs/module/bilibili/': [
      //   "base.md",
      //   "action",
      //   "follow_up",
      //   "anchor",
      //   "anime",
      //   "list",
      //   "hot"
      // ],
      '/blogs/develop/': [
        {
          text: "起步",
          children: ['/blogs/develop/foreword/introduction', '/blogs/develop/foreword/prepare']
        },
        {
          text: "配置",
          children: ['/blogs/develop/set/set-sora', '/blogs/develop/set/set-gocq']
        },
        {
          text: "部署",
          children: ['/blogs/develop/deploy/docker']
        }
      ]
    },
    navbar: [
      { text: '主页', link: '/docs/index.html', icon: 'Home'},
      { text: '功能', link: '/docs/module/index.md', icon: 'Document'},
      { text: '开发指南', link: '/blogs/develop/foreword/prepare.md', icon: 'Compass'},
      { text: '关于',
        children: [
          { text: '关于', link: '/blogs/about/introduce.md' },
          { text: '反馈', link: 'https://support.qq.com/product/426080' },
          { text: '赞助', link: 'https://afdian.net/a/linxi-bot' }
        ]
      },
      { text: '留言板', link: '/blogs/message-board.html', icon: 'Chat'}
    ],
    bulletin: {
      body: [
        {
          type: "text",
          content: `🎉🎉🎉 林汐先已经接近 1.0 版本，在发布 1.0 版本之前不会再有大的更新，大家可以尽情尝鲜了，并且希望大家在 QQ 群和 GitHub 踊跃反馈使用体验，我会在第一时间响应。`,
          style: "font-size: 12px;",
        },
        {
          type: "hr",
        },
        {
          type: "title",
          content: "QQ 群",
        },
        {
          type: "text",
          content: `
          <ul>
            <li>QQ群：413820772</li>
            <li>开发群：817451732</li>
          </ul>`,
          style: "font-size: 12px;",
        },
        {
          type: "hr",
        },
        {
          type: "title",
          content: "GitHub",
        },
        {
          type: "text",
          content: `
          <ul>
            <li><a href="https://github.com/netsora/SoraBot/issues">Issues<a/></li>
            <li><a href="https://github.com/orgs/netsora/discussions">Discussions<a/></li>
          </ul>`,
          style: "font-size: 12px;",
        },
        {
          type: "hr",
        },
        {
          type: "buttongroup",
          children: [
            {
              text: "打赏",
              link: "https://afdian.net/a/linxi-bot",
            },
          ],
        },
      ],
    },
    // valineConfig 配置与 1.x 一致
    commentConfig: {
      type: 'valine',
      options: {
        appId: Valine_ID, // your appId
        appKey: Valine_Key, // your appKey
        placeholder: '填写邮箱可以收到回复提醒哦！',
        verify: true, // 验证码服务
        hideComments: false, // 全局隐藏评论，默认 false
        recordIP: true,
      }
    },
  }),
  // debug: true,
});
