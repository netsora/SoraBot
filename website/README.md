---
home: true
modules:
  - BannerBrand
  - Blog
  - MdContent
  - Footer
bannerBrand:
  bgImage: '/bg.svg'
  title: SoraBot
  description: 林汐ᴮᴼᵀ 使用 & 开发 文档。
  tagline: SoraBot 继续坚持简洁、好用的风格，数据防丢失，插件易管理，指令不会与其它机器人碰撞。你只需要输入指令，其他请交给我。
  buttons:
    - { text: '快速开始', link: '/docs' }
    - { text: '关于', link: '/blogs/about/introduce.html', type: 'plain' }
  socialLinks:
    - { icon: 'LetterQq', link: 'http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=A9oTio04Frz8oX0WgbPWM9OszLcF5RHT&authKey=D84U3cnB2Lax1qgww4psT1OgEU1iOOKW4evsdhnQuHtV3QFedQGNNLm1kK2Mfj15&noverify=0&group_code=817451732'}
    - { icon: 'LogoGithub', link: 'https://github.com/netsora/SoraBot' }
    - { icon: 'LogoDiscord', link: 'https://discord.gg/YRVwvYt58X'}
blog:
  socialLinks:
    - { icon: 'LetterQq', link: 'http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=A9oTio04Frz8oX0WgbPWM9OszLcF5RHT&authKey=D84U3cnB2Lax1qgww4psT1OgEU1iOOKW4evsdhnQuHtV3QFedQGNNLm1kK2Mfj15&noverify=0&group_code=817451732'}
    - { icon: 'LogoGithub', link: 'https://github.com/netsora' }
    - { icon: 'LogoDiscord', link: 'https://discord.gg/YRVwvYt58X'}
isShowTitleInHome: true
actionText: About
actionLink: /blogs/about/introduce.md
---

<!-- Google tag (gtag.js) -->
<script>
    const Analytics_ID = process.env.ANALYTICS_ID;
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${Analytics_ID}`;
    
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-ZM7QTC95DS');
</script>

