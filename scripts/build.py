"""Generate GitHub-compatible SVG panels and README. Python standard library only."""
import json
import textwrap
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'assets'
DATA = json.loads((A / 'profile.json').read_text(encoding='utf-8-sig'))
TELEMETRY = json.loads((A / 'telemetry.json').read_text(encoding='utf-8-sig'))
GREEN, CYAN, WHITE, MUTED, PURPLE = '#39ff88', '#37dfff', '#e6f1f5', '#94aab9', '#b599ff'

def txt(x, y, value, size=16, color=WHITE, weight='400', mono=True):
    font = 'Consolas,monospace' if mono else 'Segoe UI,Arial,sans-serif'
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{font}" font-size="{size}" font-weight="{weight}">{escape(str(value))}</text>'

def lines(x, y, value, width, size=16, color=MUTED, step=25):
    rows = textwrap.wrap(value, width=width)
    return ''.join(txt(x, y+i*step, row, size, color, mono=False) for i, row in enumerate(rows))

def line(x1,y1,x2,y2,color='#203943'):
    return f'<path d="M{x1} {y1}H{x2}" stroke="{color}"/>' if y1==y2 else f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}"/>'

def rect(x,y,w,h,fill='#0d1820',stroke='#203943',radius=4):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'

def panel(name, w, h, body, title):
    grid = ''.join(line(x,1,x,h-1,'#101c23') for x in range(20,w,40))
    grid += ''.join(line(1,y,w-1,y,'#101c23') for y in range(20,h,40))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>'
    svg += rect(1,1,w-2,h-2,'#080d12') + f'<g opacity="0.5">{grid}</g>'
    svg += f'<path d="M1 26V1H72 M{w-72} {h-1}H{w-1}V{h-26}" stroke="{GREEN}" stroke-width="2" fill="none"/>'
    svg += body + '</svg>'
    (A / f'{name}.svg').write_text(svg, encoding='utf-8')

def top(w, code, title):
    return txt(24,31,code,12,GREEN)+txt(24,64,title,22,WHITE,'700')+line(24,82,w-24,82)

def picture(name, alt):
    return f'<picture>\n  <source media="(max-width: 600px)" srcset="assets/{name}-mobile.svg">\n  <img src="assets/{name}.svg" width="100%" alt="{escape(alt, quote=True)}">\n</picture>'

for mobile in (False, True):
    w = 420 if mobile else 900
    suffix = '-mobile' if mobile else ''
    b = txt(24,32,'DRL / DEVELOPER COMMAND CENTER',12,GREEN)
    b += line(24,48,w-24,48)
    for i,s in enumerate(['[ SYSTEM BOOT ]','> INITIALIZING DEVELOPER PROFILE...', '> LOADING PROJECTS...','> CONNECTING TO GITHUB...','> SYSTEM ONLINE ✓']):
        b += txt(24,78+i*23,s,13,GREEN if i in (0,4) else MUTED)
    b += txt(24,244,'DIOGO' if mobile else DATA['name'],48 if mobile else 56,WHITE,'700',False)
    if mobile:
        b += txt(24,293,'REIS LAGO',48,WHITE,'700',False)
    y=327 if mobile else 282
    b += txt(24,y,'SOFTWARE ENGINEERING',15,CYAN)
    b += txt(24,y+28,'Full Stack / Backend / AI / DevOps',13,MUTED)
    b += line(24,y+49,w-24,y+49)
    b += txt(24,y+76,'01 OPERATOR  /  04 PROJECT NODES',12,GREEN)
    if not mobile:
        for r in (45,70,95):
            b += f'<circle cx="770" cy="136" r="{r}" fill="none" stroke="#203943"/>'
        b += f'<path d="M655 136H885 M770 21V251 M709 197L831 75" stroke="{CYAN}" opacity="0.4"/>'
        b += txt(739,147,'DRL',28,GREEN,'700')
        b += f'<circle cx="831" cy="75" r="5" fill="{GREEN}"/>'
    panel('header'+suffix,w,y+100,b,'Diogo Reis Lago / Developer Command Center')

    b=top(w,'01 / IDENTITY MODULE','PROFILE_SCAN.exe')
    fields=[('ROLE',['Software Engineering Student','Full Stack Developer']),('FOCUS',['Backend • Full Stack • AI • DevOps']),('LOCATION',['Belo Horizonte - MG - Brazil']),('STATUS',['AVAILABLE / BUILDING / LEARNING'])]
    y=115
    for label, values in fields:
        b+=txt(24,y,label,12,CYAN)
        for j,v in enumerate(values): b+=txt(24,y+26+j*23,v,15,WHITE)
        y+=52+23*len(values)
    if not mobile:
        b+=rect(570,110,300,250)
        for i,s in enumerate(['     ┌──────────┐','     │  ▪    ▪  │','     │    ──    │','     └────┬─────┘','    ┌─────┴──────┐','    │  </ DRL >  │','    └────────────┘']):
            b+=txt(590,143+i*25,s,18,GREEN)
        b+=txt(600,341,'HUMAN BEHIND THE CODE',12,MUTED)
    panel('profile-scan'+suffix,w,y+6,b,'Perfil profissional: estudante de Engenharia de Software e desenvolvedor Full Stack')

    b=top(w,'02 / INSTALLED MODULES','TECH_STACK.sys')
    for i,(label,stack,desc) in enumerate(DATA['stack']):
        x=24 if mobile else 24+(i%2)*438
        y=104+(i if mobile else i//2)*116
        cw=372 if mobile else 414
        b+=rect(x,y,cw,102)
        b+=txt(x+16,y+25,label,13,CYAN)
        b+=txt(x+16,y+54,stack,14,WHITE,mono=False)
        b+=txt(x+16,y+79,desc,12,MUTED)
    panel('tech-stack'+suffix,w,816 if mobile else 468,b,'Tecnologias por categoria; ferramentas utilizadas e áreas em desenvolvimento')

    for n,p in enumerate(DATA['projects'],1):
        k='REPO_'+p['key']+'_'
        b=txt(24,32,f'PROJECT_0{n} / {p["category"]}',13,GREEN)
        b+=line(24,49,w-24,49)
        b+=txt(24,91,p[k+'NAME'],30,WHITE,'700',False)
        b+=lines(24,125,p[k+'DESCRIPTION'],44 if mobile else 93,17,step=25)
        sy=210 if mobile else 185
        b+=txt(24,sy,'STACK /',11,CYAN)
        b+=txt(24,sy+26,p[k+'STACK'],14,WHITE,mono=False)
        b+=rect(24,sy+47,w-48,40,'#10271f','#235d42')
        b+=txt(40,sy+73,'ACCESS REPOSITORY →',14,GREEN,'700')
        panel('project-card-'+p['asset']+suffix,w,sy+108,b,p[k+'NAME']+' — '+p[k+'DESCRIPTION']+' Stack: '+p[k+'STACK'])

    b=top(w,'04 / PUBLIC SIGNALS','GITHUB_TELEMETRY')
    b+=txt(24,109,'SNAPSHOT / '+TELEMETRY['date']+' UTC',12,CYAN)
    stats=[('PUBLIC REPOS',TELEMETRY['repositories']),('REPO STARS',TELEMETRY['stars']),('FOLLOWERS',TELEMETRY['followers'])]
    for i,(label,value) in enumerate(stats):
        x=24+i*(124 if mobile else 285)
        b+=txt(x,160,value,36,GREEN,'700')+txt(x,184,label,11,MUTED)
    b+=line(24,204,w-24,204)+txt(24,233,'LANGUAGE DISTRIBUTION / BYTES',12,CYAN)
    langs=sorted(TELEMETRY['languages'].items(),key=lambda item:item[1],reverse=True)[:5]
    total=sum(TELEMETRY['languages'].values())
    for i,(label,value) in enumerate(langs):
        y=265+i*48
        b+=txt(24,y,label,14,WHITE)+txt(w-88,y,f'{value/total:.1%}',13,MUTED)
        b+=rect(24,y+11,w-48,6,'#152831','#152831',2)
        b+=rect(24,y+11,round((w-48)*value/total,1),6,GREEN if i%2==0 else CYAN,GREEN if i%2==0 else CYAN,2)
    b+=txt(24,523,'PUBLIC CODE / NOT A SKILL RATING',11,MUTED)
    panel('telemetry'+suffix,w,549,b,'GitHub: '+str(TELEMETRY['repositories'])+' repositórios públicos; distribuição de linguagens por bytes. Snapshot '+TELEMETRY['date'])

    contributions=TELEMETRY.get('contributions',[])
    if contributions:
        recent=contributions[-31:]
        b=top(w,'04.1 / CONTRIBUTION SIGNAL','ACTIVITY_LOG')
        b+=txt(24,113,f'{sum(d["count"] for d in recent)} CONTRIBUTIONS / LAST 31 DAYS',13,GREEN)
        chartw=w-48
        peak=max(1,max(d['count'] for d in recent))
        for i,d in enumerate(recent):
            bh=100*d['count']/peak
            b+=rect(round(24+i*chartw/31,2),round(242-bh,2),round(chartw/31-3,2),max(2,round(bh,2)),GREEN if d['count'] else '#203943','none',1)
        b+=txt(24,270,recent[0]['date'],12,MUTED)+txt(w-110,270,recent[-1]['date'],12,MUTED)
        b+=line(24,291,w-24,291)
        b+=txt(24,324,f'CURRENT STREAK / {TELEMETRY["current_streak"]} DAYS',14,CYAN)
        b+=txt(24,351,f'LONGEST IN WINDOW / {TELEMETRY["longest_streak"]} DAYS',14,MUTED)
        panel('activity'+suffix,w,378,b,'Contribuições diárias nos últimos 31 dias e sequências do calendário público; snapshot '+TELEMETRY['date'])

    b=top(w,'05 / EXECUTION QUEUE','CURRENT_MISSION')
    missions=['Building scalable systems','Exploring applied AI','Improving backend architecture','Learning DevOps & Cloud','Shipping useful projects']
    for i,s in enumerate(missions): b+=txt(24,120+i*36,'> '+s,15,GREEN if i==0 else WHITE)
    panel('mission'+suffix,w,296,b,'Missão atual: sistemas escaláveis, IA aplicada, arquitetura backend, DevOps e entrega de projetos')
    b=txt(24,35,'> SESSION STATUS: ACTIVE',14,GREEN)+txt(24,65,'> SYSTEM: ONLINE',14,WHITE)+txt(24,95,'> LAST MODULE: PORTFOLIO',14,WHITE)+txt(24,125,'> CONNECTION AVAILABLE',14,CYAN)
    b+=line(24,147,w-24,147)+txt(24,178,'[ END OF TRANSMISSION ]',12,MUTED)
    panel('footer'+suffix,w,200,b,'Sessão ativa. Sistema online. Conexão disponível.')
    for name,number,title in [('projects-label','03','PROJECT_NETWORK'),('contact-label','06','ESTABLISH_CONNECTION')]:
        panel(name+suffix,w,96,top(w,number+' / COMMAND CENTER',title),title)

for label,key in [('GITHUB','GITHUB_URL'),('LINKEDIN','LINKEDIN_URL'),('E-MAIL','EMAIL_URL'),('PORTFOLIO','PORTFOLIO_URL')]:
    panel('contact-'+label.lower(),200,48,txt(15,30,label+' ↗',15,GREEN,'700'),label)

readme='<!-- Generated by scripts/build.py. Edit assets/profile.json, then run python scripts/build.py. -->\n\n'
readme+=picture('header','DIOGO REIS LAGO — Software Engineering • Full Stack • Backend • AI • DevOps')+'\n\n'
readme+='<p align="center"><a href="#profile">PROFILE</a> · <a href="#stack">STACK</a> · <a href="#projects">PROJECTS</a> · <a href="#telemetry">TELEMETRY</a> · <a href="#contact">CONTACT</a></p>\n\n'
readme+='<a name="profile"></a>\n\n'+picture('profile-scan','ROLE: Software Engineering Student / Full Stack Developer. FOCUS: Backend, Full Stack, AI, DevOps. LOCATION: Belo Horizonte - MG - Brazil. STATUS: Available / Building / Learning.')+'\n\n'
readme+='Sou **Diogo Reis Lago**, estudante de Engenharia de Software e desenvolvedor Full Stack. Construo aplicações web e exploro a integração entre backend, dados e inteligência artificial, com foco em código organizado, aprendizado contínuo e soluções úteis.\n\n'
readme+='<a name="stack"></a>\n\n'+picture('tech-stack','TECH_STACK.sys — Backend, Frontend, Database, DevOps / Cloud, AI / Data e Tools.')+'\n\n'
readme+='<details>\n<summary>Inspect modules / tecnologias em texto</summary>\n\n'
for label,stack,desc in DATA['stack']: readme+=f'- **{label}:** {stack}. {desc}.\n'
readme+='\n</details>\n\n<a name="projects"></a>\n\n'+picture('projects-label','PROJECT_NETWORK — quatro repositórios selecionados')+'\n\n'
for p in DATA['projects']:
    k='REPO_'+p['key']+'_'
    readme+=f'<!-- {k}URL / {k}NAME / {k}DESCRIPTION / {k}STACK: edit assets/profile.json -->\n'
    readme+=f'<a href="{escape(p[k+"URL"],quote=True)}">\n'+picture('project-card-'+p['asset'],p[k+'NAME']+' — '+p[k+'DESCRIPTION']+' Stack: '+p[k+'STACK']+'. Abrir repositório.')+'\n</a>\n\n'
readme+='<a name="telemetry"></a>\n\n'+picture('telemetry','GITHUB_TELEMETRY — repositórios, estrelas, seguidores e linguagens. Snapshot: '+TELEMETRY['date'])+'\n\n'
if TELEMETRY.get('contributions'): readme+=picture('activity','ACTIVITY_LOG — contribuições nos últimos 31 dias e streak do calendário público. Snapshot: '+TELEMETRY['date'])+'\n\n'
readme+='<details>\n<summary>Inspect telemetry / origem e escopo</summary>\n\n'
readme+=f'Snapshot: **{TELEMETRY["date"]} UTC**. [Dados utilizados](assets/telemetry.json) · [Contribuições no GitHub](https://github.com/{DATA["username"]}?tab=overview).\n\n'
readme+='Estatísticas da API pública do GitHub. Linguagens representam bytes dos repositórios públicos próprios, excluindo forks; não medem proficiência. Os cinco maiores valores são exibidos; as porcentagens consideram todas as linguagens, incluindo notebooks. Repositórios públicos incluem forks; estrelas são somadas nesses repositórios.\n\n'
readme+='Atividade e streak usam o calendário público do GitHub. A sequência atual admite o dia de hoje ainda sem contribuições; a maior sequência se limita à janela coletada. Os painéis são snapshots, atualizados pelo comando documentado no [guia de personalização](docs/CUSTOMIZATION.md).\n\n</details>\n\n'
readme+=picture('mission','CURRENT_MISSION — Building scalable systems; Exploring applied AI; Improving backend architecture; Learning DevOps & Cloud; Shipping useful projects.')+'\n\n'
readme+='<a name="contact"></a>\n\n'+picture('contact-label','ESTABLISH_CONNECTION')+'\n\n<p align="center">\n'
for label,key in [('GITHUB','GITHUB_URL'),('LINKEDIN','LINKEDIN_URL'),('E-MAIL','EMAIL_URL'),('PORTFOLIO','PORTFOLIO_URL')]:
    readme+=f'  <a href="{escape(DATA["contacts"][key],quote=True)}"><img src="assets/contact-{label.lower()}.svg" width="180" alt="{label}"></a>\n'
email_url=DATA['contacts']['EMAIL_URL']
readme+=f'</p>\n\n<p align="center"><a href="{escape(email_url,quote=True)}">{escape(email_url.removeprefix("mailto:"))}</a></p>\n\n'
readme+=picture('footer','SESSION STATUS: ACTIVE / SYSTEM: ONLINE / LAST MODULE: PORTFOLIO / CONNECTION AVAILABLE / END OF TRANSMISSION')+'\n'
(ROOT/'README.md').write_text(readme,encoding='utf-8')
print('README and SVG panels generated.')
