import re, html as h

with open('SKILL.md', 'r', encoding='utf-8') as f:
    md = f.read()

lines = md.split('\n')
out = []
in_code = False
in_list = False
in_quote = False
in_para = False
in_yaml = False

for line in lines:
    if line.strip() == '---' and not in_code:
        if not in_yaml:
            in_yaml = True
            continue
        else:
            in_yaml = False
            out.append('<hr class=frontmatter>')
            continue
    if in_yaml:
        key_val = re.match(r'^(\w+):\s*(.+)$', line)
        if key_val:
            out.append('<div class=frontmatter-line><span class=fm-key>{}</span>: <span class=fm-val>{}</span></div>'.format(
                key_val.group(1), h.escape(key_val.group(2))))
        continue

    if line.startswith('```'):
        if in_code:
            out.append('</code></pre>')
            in_code = False
        else:
            out.append('<pre><code>')
            in_code = True
        continue
    if in_code:
        out.append(h.escape(line))
        continue

    if line.startswith('# '):
        if in_para: out.append('</p>'); in_para = False
        if in_list: out.append('</ul>'); in_list = False
        if in_quote: out.append('</blockquote>'); in_quote = False
        out.append('<h1>{}</h1>'.format(h.escape(line[2:])))
    elif line.startswith('## '):
        if in_para: out.append('</p>'); in_para = False
        if in_list: out.append('</ul>'); in_list = False
        if in_quote: out.append('</blockquote>'); in_quote = False
        out.append('<h2>{}</h2>'.format(h.escape(line[3:])))
    elif line.startswith('### '):
        if in_para: out.append('</p>'); in_para = False
        if in_list: out.append('</ul>'); in_list = False
        if in_quote: out.append('</blockquote>'); in_quote = False
        out.append('<h3>{}</h3>'.format(h.escape(line[4:])))
    elif line.startswith('#### '):
        if in_para: out.append('</p>'); in_para = False
        if in_list: out.append('</ul>'); in_list = False
        if in_quote: out.append('</blockquote>'); in_quote = False
        out.append('<h4>{}</h4>'.format(h.escape(line[5:])))
    elif line.startswith('> '):
        if not in_quote:
            if in_para: out.append('</p>'); in_para = False
            if in_list: out.append('</ul>'); in_list = False
            out.append('<blockquote>')
            in_quote = True
        content = h.escape(line[2:])
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', content)
        out.append('<p>{}</p>'.format(content))
    elif line.startswith('- '):
        if not in_list:
            if in_para: out.append('</p>'); in_para = False
            if in_quote: out.append('</blockquote>'); in_quote = False
            out.append('<ul>')
            in_list = True
        content = h.escape(line[2:])
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', content)
        content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
        out.append('<li>{}</li>'.format(content))
    elif line.startswith('---'):
        if in_para: out.append('</p>'); in_para = False
        if in_list: out.append('</ul>'); in_list = False
        if in_quote: out.append('</blockquote>'); in_quote = False
        out.append('<hr>')
    elif line.strip() == '':
        if in_para: out.append('</p>'); in_para = False
        if in_list: out.append('</ul>'); in_list = False
        if in_quote: out.append('</blockquote>'); in_quote = False
    else:
        if not in_para and not in_list and not in_quote:
            out.append('<p>')
            in_para = True
        processed = h.escape(line)
        processed = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', processed)
        processed = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', processed)
        processed = re.sub(r'`([^`]+)`', r'<code>\1</code>', processed)
        processed = processed.replace('⚙️', '<span class=tag-mech>⚙️ 通用</span>')
        processed = processed.replace('👤', '<span class=tag-personal>👤 进化猫</span>')
        out.append(processed)

if in_para: out.append('</p>')
if in_list: out.append('</ul>')
if in_quote: out.append('</blockquote>')

css = """
*{box-sizing:border-box}
body{font-family:"Inter","PingFang SC",system-ui,sans-serif;max-width:840px;margin:40px auto;padding:24px 32px;line-height:1.78;color:#1a1a1a;background:#fafaf8}
h1{font-size:30px;border-bottom:2.5px solid #002FA7;padding-bottom:14px;margin-top:0}
h2{font-size:21px;margin-top:42px;color:#002FA7;border-bottom:1px solid #e8e8e4;padding-bottom:8px}
h3{font-size:17px;margin-top:32px;color:#333}
h4{font-size:15px;margin-top:24px;color:#555}
code{background:#eee;padding:2px 6px;border-radius:3px;font-size:13px;font-family:"Cascadia Code",monospace}
pre{background:#1a1a2e;color:#cdd6f4;padding:18px 20px;border-radius:10px;overflow-x:auto;font-size:13px;line-height:1.55}
pre code{background:none;padding:0;color:inherit}
blockquote{background:#fffde7;border-left:3.5px solid #ffc107;padding:10px 18px;margin:14px 0;border-radius:0 6px 6px 0}
blockquote p{margin:4px 0;color:#5d4037}
li{margin:5px 0}
hr{border:none;border-top:1px solid #e0e0dc;margin:28px 0}
hr.frontmatter{border:none;border-top:1px dashed #ccc;margin:16px 0 24px}
strong{color:#002FA7}
a{color:#002FA7}
.tag-mech{display:inline-block;background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 8px;border-radius:10px;margin-right:4px;font-weight:600}
.tag-personal{display:inline-block;background:#e3f2fd;color:#1565c0;font-size:11px;padding:1px 8px;border-radius:10px;margin-right:4px;font-weight:600}
.frontmatter-line{font-size:13px;color:#888;margin:2px 0;font-family:"Cascadia Code",monospace}
.fm-key{color:#002FA7;font-weight:600}
.fm-val{color:#555}
@media(prefers-color-scheme:dark){body{background:#0d1117;color:#c9d1d9}h2{color:#58a6ff;border-bottom-color:#21262d}h3{color:#c9d1d9}code{background:#161b22}blockquote{background:#161b22;border-left-color:#d29922}blockquote p{color:#c9d1d9}hr{border-top-color:#30363d}strong{color:#58a6ff}a{color:#58a6ff}.tag-mech{background:#1b3a1b;color:#7dcc7d}.tag-personal{background:#1a2d4a;color:#79b8ff}.frontmatter-line{color:#666}.fm-key{color:#58a6ff}.fm-val{color:#999}}
"""

html = '<!DOCTYPE html><html><head><meta charset=utf-8><title>进化猫写作技能</title><style>{}</style></head><body>\n{}\n</body></html>'.format(
    css, '\n'.join(out))

with open('SKILL.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('OK: SKILL.html written')
