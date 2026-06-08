/**
 * ============================================================
 *  protect.js — 张雅琦作品集 · 内容保护脚本
 * ============================================================
 *  使用方法：在需要保护的页面 </body> 前加一行
 *    <script src="protect.js"></script>
 * ============================================================
 */
(function () {
  'use strict';

  /* ========== 1. 注入保护 CSS ========== */
  var css = document.createElement('style');
  css.textContent = [

    /* 禁止全局文字选中 —— 仅作用于 body，不污染 * */
    'body {',
    '  -webkit-user-select: none !important;',
    '  -moz-user-select: none !important;',
    '  -ms-user-select: none !important;',
    '  user-select: none !important;',
    '}',
    'img {',
    '  -webkit-user-drag: none;',
    '  -webkit-touch-callout: none;',
    '}',

    /* ---- 浮层 · 全屏暗色 ---- */
    '#zyq-overlay {',
    '  position:fixed; inset:0; z-index:99999;',
    '  display:flex; align-items:center; justify-content:center;',
    '  background:#1C1711;',
    '  opacity:0; animation:zyqIn .6s ease forwards;',
    '}',
    '@keyframes zyqIn  { to{opacity:1} }',
    '@keyframes zyqOut { to{opacity:0} }',
    '#zyq-overlay.hide { animation:zyqOut .5s ease forwards }',

    /* ---- 内容容器 ---- */
    '#zyq-inner {',
    '  max-width:460px; width:88%; text-align:center;',
    '  transform:translateY(24px); opacity:0;',
    '  animation:zyqUp .7s ease .2s forwards;',
    '}',
    '@keyframes zyqUp { to{transform:translateY(0);opacity:1} }',

    /* 英文名 */
    '#zyq-inner .zyq-en {',
    "  font-family:'Archivo',sans-serif;",
    '  font-size:clamp(22px,4vw,30px); font-weight:800;',
    '  letter-spacing:6px; color:#fff;',
    '  margin:0 0 8px;',
    '}',
    '#zyq-inner .zyq-en span { color:#C1121F }',

    /* 中文"作品集" */
    '#zyq-inner .zyq-cn {',
    "  font-family:'Noto Serif SC','Noto Sans SC',serif;",
    '  font-size:13px; letter-spacing:8px; color:rgba(255,255,255,.35);',
    '  margin:0 0 40px;',
    '}',

    /* 分割 · 菱形 */
    '#zyq-inner .zyq-diamond {',
    '  display:flex; align-items:center; justify-content:center;',
    '  gap:14px; margin-bottom:36px;',
    '}',
    '#zyq-inner .zyq-diamond i {',
    '  width:38px; height:1px; background:rgba(255,255,255,.12);',
    '}',
    '#zyq-inner .zyq-diamond b {',
    '  width:6px; height:6px; border:1px solid #C1121F;',
    '  transform:rotate(45deg); flex-shrink:0;',
    '}',

    /* 正文段落 */
    '#zyq-inner p {',
    "  font-family:'Noto Sans SC',sans-serif;",
    '  font-size:13px; line-height:2.2; color:rgba(255,255,255,.55);',
    '  letter-spacing:.5px; margin:0 0 36px;',
    '}',
    '#zyq-inner p em {',
    '  font-style:normal; color:rgba(255,255,255,.85); font-weight:500;',
    '}',

    /* 按钮 */
    '#zyq-inner button {',
    "  font-family:'Archivo',sans-serif;",
    '  font-size:11px; font-weight:700; letter-spacing:3px;',
    '  padding:13px 40px; border:1px solid #C1121F;',
    '  background:transparent; color:#C1121F; cursor:pointer;',
    '  transition:all .3s ease;',
    '}',
    '#zyq-inner button:hover {',
    '  background:#C1121F; color:#fff;',
    '}',

    /* 底部版权 */
    '#zyq-inner .zyq-foot {',
    "  font-family:'Archivo',sans-serif;",
    '  font-size:9px; letter-spacing:2px; color:rgba(255,255,255,.2);',
    '  margin-top:44px; line-height:1.8;',
    '}'

  ].join('\n');
  document.head.appendChild(css);


  /* ========== 2. 关闭浮层：从 DOM 彻底移除 + 唤醒页面 ========== */
  function closeOverlay() {
    var ov = document.getElementById('zyq-overlay');
    if (!ov) return;
    ov.classList.add('hide');
    ov.addEventListener('animationend', function () {
      ov.parentNode.removeChild(ov);          // 从 DOM 彻底删除
      /* 触发 scroll + resize 让页面的 IntersectionObserver 重新检测 */
      window.dispatchEvent(new Event('scroll'));
      window.dispatchEvent(new Event('resize'));
      /* 额外：如果页面用了 scroll-triggered 动画，滚一点再滚回来确保触发 */
      window.scrollBy(0, 1);
      requestAnimationFrame(function () { window.scrollBy(0, -1); });
    }, { once: true });
  }
  /* 挂到全局以便按钮 onclick 调用 */
  window.__zyqClose = closeOverlay;


  /* ========== 3. 创建浮层 HTML ========== */
  var ov = document.createElement('div');
  ov.id = 'zyq-overlay';
  ov.innerHTML = [
    '<div id="zyq-inner">',

    '  <div class="zyq-en">ZHANG <span>YAQI</span></div>',
    '  <div class="zyq-cn">作 品 集</div>',

    '  <div class="zyq-diamond"><i></i><b></b><i></i></div>',

    '  <p>',
    '    本站所有内容均为<em>张雅琦</em>原创，受中华人民共和国著作权法保护。',
    '    为保护原创权益，本站已禁止右键操作、文本复制、图片保存及源代码查看。',
    '    未经本人书面授权，任何个人或组织不得以任何形式转载、复制、进行二次创作或引用。',
    '  </p>',

    '  <button onclick="window.__zyqClose()">进 入 浏 览</button>',

    '  <div class="zyq-foot">© 2026 ZHANG YAQI · ALL RIGHTS RESERVED</div>',

    '</div>'
  ].join('\n');
  document.body.appendChild(ov);


  /* ========== 4. 禁止右键 ========== */
  document.addEventListener('contextmenu', function(e){ e.preventDefault(); return false; }, false);


  /* ========== 5. 禁止选中 / 复制 / 剪切 ========== */
  document.addEventListener('selectstart', function(e){ e.preventDefault(); return false; }, false);
  document.addEventListener('copy', function(e){ e.preventDefault(); return false; }, false);
  document.addEventListener('cut',  function(e){ e.preventDefault(); return false; }, false);


  /* ========== 6. 禁止图片拖拽（带节流，避免干扰页面渲染） ========== */
  var lockTimer = null;
  function lockImg(){
    var imgs = document.querySelectorAll('img:not([data-zyq])');
    for(var i=0;i<imgs.length;i++){
      imgs[i].setAttribute('draggable','false');
      imgs[i].setAttribute('data-zyq','1');            // 标记已处理
      imgs[i].addEventListener('dragstart',function(e){e.preventDefault();},false);
    }
  }
  lockImg();
  var MO = window.MutationObserver || window.WebKitMutationObserver;
  if(MO){
    new MO(function(){
      if(lockTimer) return;
      lockTimer = setTimeout(function(){ lockImg(); lockTimer=null; }, 200);
    }).observe(document.body,{childList:true,subtree:true});
  }


  /* ========== 7. 屏蔽快捷键 ========== */
  document.addEventListener('keydown', function(e){
    if(e.key==='F12'||e.keyCode===123){ e.preventDefault(); return false; }
    if(e.ctrlKey||e.metaKey){
      var k = e.key ? e.key.toLowerCase() : '';
      if(k==='u'||k==='s'||k==='a'||k==='c'||k==='p'){ e.preventDefault(); return false; }
      if(e.shiftKey&&(k==='i'||k==='j'||k==='c')){ e.preventDefault(); return false; }
    }
  }, false);


  /* ========== 8. 禁止拖拽 ========== */
  document.addEventListener('dragstart', function(e){ e.preventDefault(); return false; }, false);

})();
