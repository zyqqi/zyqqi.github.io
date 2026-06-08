"""
fix_links.py — 修复作品集 HTML 中的绝对 file:// 链接
=======================================================
用法：
    python fix_links.py  能力全景_浅色版.html  about.html  index.html ...

功能：
  ① 把 file:///D:/hhha/作品集/插图/xxx.html#hash  →  xxx.html#hash
  ② 如果目标就是当前文件，进一步缩成  #hash
  ③ 跨页面链接变成相对路径（about.html, skills.html …）
  ④ 在 </body> 前注入一段 JS，让所有页内锚点链接平滑滚动

修复后的文件会覆盖原文件（自动备份为 .bak）。
"""

import re, sys, os, shutil
from urllib.parse import unquote

# ── 要处理的基路径前缀（按你的实际路径调整） ──
BASE_PREFIXES = [
    'file:///D:/hhha/%E4%BD%9C%E5%93%81%E9%9B%86/%E6%8F%92%E5%9B%BE/',
    'file:///D:/hhha/作品集/插图/',
]

# ── 页内平滑滚动脚本 ──
SMOOTH_SCROLL_JS = '''
<!-- 页内锚点平滑滚动（fix_links.py 注入） -->
<script>
document.addEventListener('click', function(e) {
  var a = e.target.closest('a[href^="#"]');
  if (!a) return;
  var id = a.getAttribute('href').slice(1);
  var target = document.getElementById(id);
  if (target) {
    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    history.replaceState(null, '', '#' + id);
  }
}, true);
</script>
'''


def fix_html(filepath):
    """修复单个 HTML 文件中的所有 file:// 链接。"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html  # 用于比较是否有变化
    
    # 当前文件名（解码后），用于判断同页链接
    current_name = os.path.basename(filepath)
    # URL 编码版本（手动处理中文）
    from urllib.parse import quote
    current_name_encoded = quote(current_name, safe='')
    
    # ── Step 1: 去掉 file:// 基路径前缀 ──
    for prefix in BASE_PREFIXES:
        html = html.replace(prefix, '')
    
    # ── Step 2: 同页链接 → 只保留 #hash ──
    # 处理 URL 编码版本的文件名
    # 例如 %E8%83%BD%E5%8A%9B...%88.html#t-cad → #t-cad
    pattern_encoded = re.compile(
        r'href="' + re.escape(current_name_encoded) + r'(#[^"]*)"',
        re.IGNORECASE
    )
    html = pattern_encoded.sub(r'href="\1"', html)
    
    # 处理解码版本的文件名
    pattern_decoded = re.compile(
        r'href="' + re.escape(current_name) + r'(#[^"]*)"',
        re.IGNORECASE
    )
    html = pattern_decoded.sub(r'href="\1"', html)
    
    # ── Step 3: 清理残留的 file:// 链接（兜底） ──
    def clean_file_url(match):
        url = match.group(1)
        decoded = unquote(url)
        # 提取最后的文件名（可能带 #hash）
        name = decoded.split('/')[-1]
        return f'href="{name}"'
    
    html = re.compile(r'href="(file:///[^"]+)"').sub(clean_file_url, html)
    
    # ── Step 4: 注入平滑滚动 JS（如果还没有） ──
    if 'fix_links.py' not in html and '</body>' in html:
        html = html.replace('</body>', SMOOTH_SCROLL_JS + '\n</body>')
    
    # ── 写回 ──
    if html != original:
        # 备份
        bak = filepath + '.bak'
        if not os.path.exists(bak):
            shutil.copy2(filepath, bak)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # 统计修改数量
        diff_count = sum(1 for a, b in zip(original, html) if a != b)
        print(f'  ✔ {filepath}  — 已修复（备份 → {bak}）')
    else:
        print(f'  · {filepath}  — 无需修改')


def main():
    if len(sys.argv) < 2:
        print('用法: python fix_links.py  文件1.html  [文件2.html ...]')
        print('  或: python fix_links.py  *.html')
        sys.exit(1)
    
    import glob
    files = []
    for arg in sys.argv[1:]:
        files.extend(glob.glob(arg))
    
    if not files:
        print('未找到匹配的文件。')
        sys.exit(1)
    
    print(f'准备修复 {len(files)} 个文件...\n')
    for f in files:
        if f.endswith('.bak'):
            continue
        fix_html(f)
    
    print('\n完成！原文件已备份为 .bak')
    print('提示：修复后请在浏览器里测试所有页面的跳转和图片加载。')


if __name__ == '__main__':
    main()
