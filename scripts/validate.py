"""Validate source paths, anchors, SVG safety and preserved project content."""
from html.parser import HTMLParser
from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]

class Readme(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors=set()
        self.links=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        assert tag not in {'script','style','svg','iframe','object','embed','button'},tag
        assert not any(k in {'style','class','id'} or k.startswith('on') for k in attrs),attrs
        if tag=='a':
            if 'name' in attrs: self.anchors.add(attrs['name'])
            if 'href' in attrs: self.links.append(attrs['href'])
        if tag in {'img','source'}:
            src=attrs.get('src',attrs.get('srcset'))
            assert src and (ROOT/src).is_file(),src
            if tag=='img': assert attrs.get('alt') and attrs.get('width')=='100%'

def main():
    md=(ROOT/'README.md').read_text(encoding='utf-8')
    p=Readme();p.feed(md)
    assert len(p.anchors)==8
    for href in p.links:
        if href.startswith('#'): assert href[1:] in p.anchors,href
    count=0
    for path in (ROOT/'assets').glob('*.svg'):
        root=ET.parse(path).getroot();assert root.get('viewBox')
        assert root.find('{http://www.w3.org/2000/svg}title') is not None
        for el in root.iter():
            assert el.tag.split('}')[-1] not in {'script','foreignObject','image','animate'}
            assert not any(k.startswith('on') or 'href' in k for k in el.attrib)
        count+=1
    from html import unescape
    plain=unescape(md)
    data=json.loads((ROOT/'assets/profile-data.json').read_text(encoding='utf-8'))
    for project in data['projects']:
        assert project['name'] in plain and project['description'] in plain
        for tag in project['tags']: assert tag in plain
    assert md.count('REPOSITORY_URL_REQUIRED')==sum(not p['url'] for p in data['projects'])
    assert 'github.com/diogolago' not in md
    print(f'OK: {count} SVGs, 8 anchors, local image paths, alt text, 5 complete project descriptions; no active content.')

if __name__=='__main__': main()
