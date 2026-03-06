#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《硅基黎明》EPUB 文件 - 简化版
"""

import os
import zipfile
import markdown
import uuid
from datetime import datetime

def read_chapter(filepath):
    """读取章节文件并转换为 HTML"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 过滤 Markdown 分隔线 ---
    lines = content.split('\n')
    filtered_lines = [line for line in lines if line.strip() != '---']
    content = '\n'.join(filtered_lines)
    
    # Markdown 转 HTML
    html_content = markdown.markdown(content, extensions=['extra'])
    return html_content

def create_container_xml():
    """创建 container.xml"""
    return '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>'''

def create_content_opf(chapters):
    """创建 content.opf"""
    manifest_items = []
    spine_items = []
    
    for i, (filename, title) in enumerate(chapters, 1):
        manifest_items.append(f'    <item id="chapter{i:03d}" href="text/chapter_{i:03d}.xhtml" media-type="application/xhtml+xml"/>')
        spine_items.append(f'    <itemref idref="chapter{i:03d}"/>')
    
    content = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="uid">silicon-dawn-2026</dc:identifier>
    <dc:title>硅基黎明</dc:title>
    <dc:language>zh</dc:language>
    <dc:creator>梁先生</dc:creator>
    <dc:date>{datetime.now().strftime("%Y-%m-%d")}</dc:date>
    <meta property="dcterms:modified">{datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}</meta>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="style" href="style/style.css" media-type="text/css"/>
{chr(10).join(manifest_items)}
  </manifest>
  <spine toc="ncx">
{chr(10).join(spine_items)}
  </spine>
</package>'''
    return content

def create_toc_ncx(chapters):
    """创建 toc.ncx"""
    nav_points = []
    for i, (filename, title) in enumerate(chapters, 1):
        nav_points.append(f'''    <navPoint id="navpoint{i}" playOrder="{i}">
      <navLabel><text>{title}</text></navLabel>
      <content src="text/chapter_{i:03d}.xhtml"/>
    </navPoint>''')
    
    content = f'''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="silicon-dawn-2026"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>硅基黎明</text></docTitle>
  <navMap>
{chr(10).join(nav_points)}
  </navMap>
</ncx>'''
    return content

def create_nav_xhtml(chapters):
    """创建 nav.xhtml"""
    nav_items = []
    for i, (filename, title) in enumerate(chapters, 1):
        nav_items.append(f'      <li><a href="text/chapter_{i:03d}.xhtml">{title}</a></li>')
    
    content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>目录</title>
  <style>
    body {{ font-family: sans-serif; }}
    ol {{ list-style-type: none; padding-left: 0; }}
    li {{ margin: 0.5em 0; }}
    a {{ text-decoration: none; color: #333; }}
  </style>
</head>
<body>
  <nav epub:type="toc">
    <h1>目录</h1>
    <ol>
{chr(10).join(nav_items)}
    </ol>
  </nav>
</body>
</html>'''
    return content

def create_style_css():
    """创建 CSS 样式"""
    return '''body { font-family: "SimSun", "宋体", serif; line-height: 1.8; margin: 5%; }
h1 { text-align: center; color: #333; margin-top: 2em; }
h2 { text-align: center; color: #666; margin-top: 1.5em; }
h3 { color: #444; margin-top: 1.2em; }
p { text-indent: 2em; margin: 0.8em 0; }
blockquote { border-left: 3px solid #ccc; margin: 1em 0; padding-left: 1em; color: #666; }
pre { background: #f5f5f5; padding: 1em; overflow-x: auto; white-space: pre-wrap; }
code { background: #f5f5f5; padding: 0.2em 0.4em; }
hr { border: none; border-top: 1px solid #ddd; margin: 2em 0; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th, td { border: 1px solid #ddd; padding: 0.5em; text-align: left; }
th { background: #f5f5f5; }'''

def create_epub():
    """创建 EPUB 文件"""
    base_dir = '/home/admin/.openclaw/workspace/novel-projects/硅基黎明'
    chapters_dir = os.path.join(base_dir, 'chapters')
    exports_dir = os.path.join(base_dir, 'exports')
    
    # 读取所有章节
    chapters = []
    chapter_files = sorted([f for f in os.listdir(chapters_dir) if f.startswith('chapter-') and f.endswith('.md')])
    
    for filename in chapter_files:
        filepath = os.path.join(chapters_dir, filename)
        chapter_num = int(filename.split('-')[1].split('.')[0])
        title = f'第{chapter_num:03d}章'
        chapters.append((filename, title))
        print(f'已读取章节：{filename}')
    
    # 创建 EPUB 文件
    epub_path = os.path.join(exports_dir, '硅基黎明.epub')
    
    with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED) as epub:
        # mimetype (必须第一个，不压缩)
        epub.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        
        # META-INF/container.xml
        epub.writestr('META-INF/container.xml', create_container_xml())
        
        # content.opf
        epub.writestr('content.opf', create_content_opf(chapters))
        
        # toc.ncx
        epub.writestr('toc.ncx', create_toc_ncx(chapters))
        
        # nav.xhtml
        epub.writestr('nav.xhtml', create_nav_xhtml(chapters))
        
        # style/style.css
        epub.writestr('style/style.css', create_style_css())
        
        # 章节文件
        for i, (filename, title) in enumerate(chapters, 1):
            filepath = os.path.join(chapters_dir, filename)
            html_content = read_chapter(filepath)
            xhtml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{title}</title>
  <link rel="stylesheet" type="text/css" href="../style/style.css"/>
</head>
<body>
{html_content}
</body>
</html>'''
            epub.writestr(f'text/chapter_{i:03d}.xhtml', xhtml_content.encode('utf-8'))
    
    print(f'\n✅ EPUB 生成完成：{epub_path}')
    return epub_path

if __name__ == '__main__':
    create_epub()
