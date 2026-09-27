"""Optional visual review. Requires Pillow and resvg-py; not needed to publish."""
import io
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageFont
import resvg_py

root=Path(__file__).resolve().parents[1]
readme=(root/'README.md').read_text(encoding='utf-8')
for src in re.findall(r'(?:src|srcset)="(assets/[^"]+)"',readme):
    assert (root/src).is_file(),src
assert not re.search(r'<(?:style|script|iframe)\b|style=',readme)
count=0
for path in (root/'assets').glob('*.svg'):
    node=ET.parse(path).getroot()
    width=float(node.attrib['width'])
    height=float(node.attrib['height'])
    for text in node.findall('{http://www.w3.org/2000/svg}text'):
        size=int(text.attrib['font-size'])
        mono='Consolas' in text.attrib['font-family']
        bold=text.attrib.get('font-weight')=='700'
        fontfile=('consolab.ttf' if bold else 'consola.ttf') if mono else ('segoeuib.ttf' if bold else 'segoeui.ttf')
        font=ImageFont.truetype('C:/Windows/Fonts/'+fontfile,size)
        end=float(text.attrib['x'])+font.getlength(text.text or '')
        assert end < width-12,(path.name,text.text,end,width)
        assert float(text.attrib['y']) < height-8,(path.name,text.text)
    count+=1
out=root/'docs'/'previews'
out.mkdir(exist_ok=True)
for mobile in (False,True):
    suffix='-mobile' if mobile else ''
    names=['header','profile-scan','tech-stack','projects-label','project-card-backend','project-card-frontend','project-card-fullstack','project-card-workbench','telemetry','activity','mission','contact-label','footer']
    images=[]
    for name in names:
        images.append(Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_path=str(root/'assets'/f'{name}{suffix}.svg')))).convert('RGB'))
        if name=='contact-label':
            buttons=Image.new('RGB',(420 if mobile else 900,112 if mobile else 60),'#0d1117')
            for i,label in enumerate(['github','linkedin','e-mail','portfolio']):
                button=Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_path=str(root/'assets'/f'contact-{label}.svg'),width=180))).convert('RGB')
                buttons.paste(button,(24+(i%2)*192,8+(i//2)*52) if mobile else (72+i*192,8))
            images.append(buttons)
    canvas=Image.new('RGB',(images[0].width,sum(i.height for i in images)+12*(len(images)-1)),'#0d1117')
    y=0
    for img in images:
        canvas.paste(img,(0,y)); y+=img.height+12
    canvas.save(out/('mobile.png' if mobile else 'desktop.png'))
print(f'Validated {count} SVGs, text bounds, README image paths and forbidden HTML. Rendered desktop and mobile previews.')
