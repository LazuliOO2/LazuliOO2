"""Build local SVG panels and README. Python standard library only."""
from pathlib import Path
from html import escape as esc
import json
import textwrap

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
CYAN, GREEN, TEXT, MUTED = '#00f0ff', '#4edea3', '#dbfcff', '#b9cacb'
BG, PANEL, INSET, BORDER = '#051424', '#122131', '#010f1f', '#273647'

def rect(x, y, w, h, fill=PANEL, stroke=BORDER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" stroke="{stroke}"/>'

def text(x, y, value, size=14, color=TEXT, mono=True, weight=400):
    font = 'Consolas,DejaVu Sans Mono,monospace' if mono else 'Segoe UI,Arial,sans-serif'
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{font}" font-size="{size}" font-weight="{weight}">{esc(str(value))}</text>'

def line(x1,y1,x2,y2,color=CYAN):
    return f'<path d="M{x1} {y1}H{x2}V{y2}" fill="none" stroke="{color}" stroke-width="1.5"/>'

def svg(name,w,h,body,title):
    out=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="title"><title id="title">{esc(title)}</title>{rect(0.5,0.5,w-1,h-1,BG)}{body}</svg>\n'
    (ASSETS/f'{name}.svg').write_text(out,encoding='utf-8')

def picture(name,alt,mobile=False):
    img=f'<img src="assets/{name}.svg" width="100%" alt="{esc(alt,quote=True)}">'
    return f'<picture>\n  <source media="(max-width: 600px)" srcset="assets/{name}-mobile.svg">\n  {img}\n</picture>' if mobile else img

def section(n,anchor,label,sub):
    body=rect(16,16,35,35,INSET)+text(23,39,f'{n:02}',16,CYAN)+text(65,29,sub,11,GREEN)+text(65,52,label,21,TEXT,True,700)
    svg(anchor+'-label',800,70,body,label)
    # Compact label avoids shrinking terminal typography on narrow screens.
    body=text(16,23,f'{n:02} // {sub}',10,GREEN)+text(16,48,label,17,TEXT,True,700)
    svg(anchor+'-label-mobile',380,64,body,label)
    return f'<a name="{anchor}"></a>\n\n'+picture(anchor+'-label',f'{n:02} // {label}',True)+'\n\n'

def build():
    d=json.loads((ASSETS/'profile-data.json').read_text(encoding='utf-8'))
    t=json.loads((ASSETS/'telemetry.json').read_text(encoding='utf-8'))
    login=t['login']
    for mobile in (False,True):
        w=380 if mobile else 800
        suffix='-mobile' if mobile else ''
        b=''.join(f'<circle cx="{20+i*14}" cy="22" r="4" fill="{c}"/>' for i,c in enumerate(['#ffb4ab','#00a572',GREEN]))
        b+=text(16,52,'DRL-SYSTEM // OBSERVE-CORE',13,CYAN)+text(16,75,'ENGINEERING CONTROL CENTER',10,MUTED)
        if not mobile: b+=text(564,51,'BRAZIL / UTC-3',13,GREEN)+text(564,75,'SOFTWARE · DATA · CLOUD',11,MUTED)
        svg('header'+suffix,w,94,b,'DRL-System — engineering control center')

        h=540 if mobile else 345
        b=rect(16,16,w-32,30,INSET)+text(28,36,'01 // PROFILE_SCAN.EXE',12,CYAN)
        x,y=(24,78) if mobile else (278,85)
        # Wireframe monogram echoes the original terminal glyph.
        if not mobile:
            b+=rect(24,66,226,253,INSET)
            b+='<g transform="translate(85 85)" fill="none" stroke="#00f0ff"><rect width="100" height="100" rx="5" stroke-dasharray="4 3" opacity=".5"/><path d="M25 20H55C80 20 80 48 55 48H25V20M25 48H56C83 48 83 80 56 80H25V48" stroke-width="2"/><path d="M10 50H90" opacity=".4"/><circle cx="50" cy="50" r="3" fill="#00f0ff"/></g>'
            for i,v in enumerate(['> software_engineering.core','> data_ml_pipeline.engine','> cloud_devops.runtime']): b+=text(36,224+i*27,v,11,GREEN)
            b+=text(36,305,'READY_FOR_DEPLOYMENT',11,CYAN)
        b+=text(x,y,'SYSTEM OPERATOR SPECIFICATION',10,CYAN)
        b+=text(x,y+37,'DIOGO DOS REIS LAGO',25 if mobile else 29,TEXT,False,700)
        for i,v in enumerate(['Software Engineer','Data & Machine Learning','Cloud & DevOps']): b+=text(x,y+69+i*25,v,16,GREEN if i==0 else MUTED,False)
        b+=rect(x,y+137,w-x-24,67,PANEL)+text(x+12,y+161,'Software Engineering Student',13,TEXT,False)+text(x+12,y+187,'Brazil [BR] // UTC-3',12,CYAN)
        b+=text(x,y+233,'Building, learning and shipping.',15,TEXT,False)
        if mobile:
            for i,v in enumerate(['AVAILABLE_FOR_WORK','BUILDING_AT_SCALE','CONTINUOUS_LEARNING']):
                b+=rect(24,341+i*43,332,32,PANEL)+text(36,362+i*43,'● '+v,12,GREEN if i==0 else CYAN)
            b+=text(24,494,'Full Stack · Data Pipelines',13,MUTED,False)+text(24,517,'Cloud Infra',13,MUTED,False)
        svg('profile-terminal'+suffix,w,h,b,'Diogo dos Reis Lago; Software Engineer; Data & Machine Learning; Cloud & DevOps; Software Engineering Student; Brazil UTC-3. Building, learning and shipping.')

        steps=[('CODE','Clean Arch / Typing'),('LOCAL TESTS','PyTest / Unit Matrix'),('MERGE REQUEST','Code Review & Lint'),('DEPLOY','Docker / Registry'),('CLOUD','AWS / Clusters'),('VALIDATION','Prometheus / Health')]
        b=text(20,29,'SERPRO_DATA_SCIENCE // DELIVERY PIPELINE',11,CYAN)
        for i,(name,desc) in enumerate(steps):
            x,y=(24,52+i*91) if mobile else (20+(i%3)*260,54+(i//3)*117)
            if mobile and i<5: b+=line(190,y+71,190,y+91)
            b+=rect(x,y,332 if mobile else 240,71)+text(x+12,y+21,f'{i+1:02} / {name}',13,GREEN if i==5 else TEXT,True,700)+text(x+12,y+47,desc,11,MUTED)
            b+=f'<path d="M{x+12} {y+60}h{308 if mobile else 216}" stroke="{GREEN}"/>'
        if not mobile:
            b+=line(260,88,280,88)+line(520,88,540,88)
            b+='<path d="M660 125V149H140V171M260 205H280M520 205H540" fill="none" stroke="#00f0ff"/>'
        svg('mission-pipeline'+suffix,w,610 if mobile else 265,b,'CODE → LOCAL TESTS → MERGE REQUEST → DEPLOY → CLOUD → VALIDATION. Workflow architecture, not live execution status.')

        b=''.join(f'<path d="M{xx} 0V{680 if mobile else 335}" stroke="{BORDER}" opacity=".18"/>' for xx in range(0,w,24))
        def node(x,y,ww,title,lines):
            q=rect(x,y,ww,86,INSET)+text(x+14,y+25,title,12,CYAN,True,700)
            for i,v in enumerate(lines): q+=text(x+14,y+48+i*19,v,11,MUTED,False)
            return q
        if mobile:
            b+=node(24,20,332,'SOFTWARE ENGINEERING CORE',['Full Stack · Data Pipelines · Cloud Infra'])
            b+=line(16,63,16,590)
            for i,(title,lines) in enumerate([('BACKEND & SYSTEMS',['Go · Python · Node · Redis','APIs · concurrency · async workers']),('DATA & MACHINE LEARNING',['Scikit · TensorFlow · spaCy · Pandas','Reinforcement learning · ETL · NLP']),('CLOUD ARCHITECTURE',['AWS · Docker · GCP · VPC','Containers · networking · storage'])]):
                y=143+i*127;b+=line(16,y+43,24,y+43)+node(24,y,332,title,lines)
            b+=line(16,63,24,63)+line(16,590,24,590)+node(24,547,332,'DEVOPS & PLATFORM ENGINEERING',['Reliability · GitHub Actions · delivery','Container runtimes · telemetry'])
        else:
            b+=node(240,16,320,'SOFTWARE ENGINEERING CORE',['Full Stack · Data Pipelines · Cloud Infra'])
            b+='<path d="M400 102V120M140 136V120H660V136M400 120V136M140 222V240H660V222M400 222V254" stroke="#00f0ff" fill="none"/>'
            b+=node(20,136,240,'BACKEND & SYSTEMS',['Go · Python · Node · Redis','APIs · concurrency · async workers'])
            b+=node(280,136,240,'DATA & MACHINE LEARNING',['Scikit · TensorFlow · spaCy · Pandas','Reinforcement learning · ETL · NLP'])
            b+=node(540,136,240,'CLOUD ARCHITECTURE',['AWS · Docker · GCP · VPC','Containers · networking · storage'])
            b+=node(240,254,320,'DEVOPS & PLATFORM ENGINEERING',['Reliability · GitHub Actions · delivery','Container runtimes · telemetry'])
        svg('engineering-map'+suffix,w,654 if mobile else 357,b,'Software Engineering Core branches into Backend & Systems, Data & Machine Learning and Cloud Architecture, converging in DevOps & Platform / Reliability Engineering.')

        b=text(20,28,'GITHUB REST API // PUBLIC SNAPSHOT',11,CYAN)
        metrics=[('PUBLIC_REPOS',t['public_repos']),('PULL_REQUESTS',t['pull_requests']),('REPO_STARS',t['stars']),('FOLLOWERS',t['followers'])]
        for i,(label,value) in enumerate(metrics):
            x,y=(20+(i%2)*180,48+(i//2)*103) if mobile else (20+i*195,48)
            b+=rect(x,y,160 if mobile else 175,87)+text(x+12,y+24,label,11,MUTED)+text(x+12,y+64,f'{value:,}',30,GREEN)
        base=279 if mobile else 170
        b+=text(20,base,'PRIMARY LANGUAGE / REPOSITORY COUNT',10,CYAN)
        total=sum(t['languages'].values())
        for i,(language,count) in enumerate(t['languages'].items()):
            y=base+29+i*28
            b+=text(20,y,language,12,TEXT)+rect(151,y-11, max(1,(w-239)*count/max(total,1)),10,GREEN,GREEN)+text(w-63,y,str(count),12,MUTED)
        end=base+len(t['languages'])*28+40
        b+=text(20,end,'@'+login+' / '+t['fetched_at'][:10]+' UTC',11,MUTED)
        svg('github-telemetry'+suffix,w,end+22,b,f"GitHub snapshot for {login}: {t['public_repos']} public repositories; {t['pull_requests']} authored public pull requests; {t['stars']} stars on owned public repositories; {t['followers']} followers. Primary languages by non-fork repository count.")

        b=''
        for i,m in enumerate(d['modules']):
            x,y=(16,16+i*161) if mobile else (16+(i%2)*392,16+(i//2)*161)
            ww=348 if mobile else 376
            b+=rect(x,y,ww,145)+text(x+14,y+26,m['name'],13,CYAN,True,700)
            b+=text(x+14,y+49,'● INSTALLED',10,GREEN)
            lines=textwrap.wrap(' · '.join(m['tags']),width=38 if mobile else 41)
            for j,v in enumerate(lines): b+=text(x+14,y+76+j*23,v,12,TEXT)
            b+=f'<path d="M{x+14} {y+131}h{ww-28}" stroke="{BORDER}"/>'
        svg('tech-stack'+suffix,w,982 if mobile else 499,b,'Installed modules: '+ '; '.join(m['name']+': '+', '.join(m['tags']) for m in d['modules']))

    svg('footer-terminal',800,72,text(20,29,'$ exit // DRL-NODE',14,CYAN)+text(20,53,'Building, learning and shipping.',13,MUTED,False)+text(632,43,'PROMPT_READY',12,GREEN),'Session complete. Building, learning and shipping.')
    svg('footer-terminal-mobile',380,94,text(16,27,'$ exit // DRL-NODE',13,CYAN)+text(16,52,'Building, learning and shipping.',13,MUTED,False)+text(16,77,'PROMPT_READY',11,GREEN),'Session complete. Building, learning and shipping.')
    md='<!-- Generated by scripts/build.py. Edit assets/profile-data.json for projects, modules and study areas. -->\n\n'
    md+=picture('header','DRL-System // Observe-Core — Engineering Control Center',True)+'\n\n'
    md+='<p align="center">'+ ' · '.join(f'<a href="#{a}">{v}</a>' for a,v in [('profile','PROFILE'),('mission','MISSION'),('stack','STACK'),('projects','PROJECTS'),('graph','MAP'),('metrics','METRICS'),('exploring','EXPLORING'),('contact','CONTACT')])+'</p>\n\n'
    md+='<a name="profile"></a>\n\n'+picture('profile-terminal','Diogo dos Reis Lago — Software Engineer; Data & Machine Learning; Cloud & DevOps. Software Engineering Student. Brazil // UTC-3. Building, learning and shipping.',True)+'\n\n'
    md+='<p align="center"><code>AVAILABLE_FOR_WORK</code> · <code>BUILDING_AT_SCALE</code> · <code>CONTINUOUS_LEARNING</code><br>Full Stack · Data Pipelines · Cloud Infra</p>\n\n'
    md+='<p align="center"><a href="#contact">[ ESTABLISH_CONNECTION ]</a> &nbsp; <a href="#projects">[ VIEW_REPOSITORIES ]</a></p>\n\n'
    md+=section(2,'mission','CURRENT_MISSION','ACTIVE ASSIGNMENT')
    md+='**Data Science Intern · SERPRO**  \nSerpro — Serviço Federal de Processamento de Dados  \n`Cloud` · `ML` · `Infrastructure`\n\nEnterprise scale data processing & model deployment. CI/CD Continuous Delivery — automated testing, container runtime & telemetry.\n\n'
    md+=picture('mission-pipeline','Pipeline: CODE → LOCAL TESTS → MERGE REQUEST → DEPLOY → CLOUD → VALIDATION.',True)+'\n\n'
    md+=section(3,'stack','TECH_ARSENAL','RUNTIME_ENVIRONMENT // INSTALLED_MODULES')
    md+=picture('tech-stack','Installed modules: Frontend, Backend, Data & ML, Database, Cloud & DevOps, Testing & QA. Expand below for all technologies and module descriptions.',True)+'\n\n<details>\n<summary>Inspect installed modules / technologies & responsibilities</summary>\n\n<table>\n'
    for m in d['modules']:
        md+='<tr><td>\n<p><strong><samp>'+esc(m['name'])+'</samp></strong> &nbsp; <samp>[INSTALLED]</samp></p>\n<p>'+esc(m['description'])+'</p>\n<p>'+' · '.join('<code>'+esc(tag)+'</code>' for tag in m['tags'])+'</p>\n</td></tr>\n'
    md+='</table>\n\n</details>\n\n'+section(4,'projects','SELECTED_PROJECTS','CURATED ARTIFACTS // REPOSITORY_NODES')
    for i,p in enumerate(d['projects'],1):
        md+='<table>\n<tr><td>\n<p><samp>┌─ REPOSITORY_NODE_'+f'{i:02}'+' ── '+esc(p['category'][1])+'</samp></p>\n'
        md+='<p><samp>'+esc(p['category'][0].split(' // ',1)[-1])+'</samp></p>\n'
        title=esc(p['name'])
        if p['url']: title=f'<a href="{esc(p["url"],quote=True)}">{title}</a>'
        md+='<p><strong>'+title+'</strong></p>\n<p>'+esc(p['description'])+'</p>\n<p>'+' · '.join('<code>'+esc(tag)+'</code>' for tag in p['tags'])+'</p>\n'
        md+=f'<p><a href="{esc(p["url"],quote=True)}">[ OPEN_REPOSITORY ]</a></p>\n' if p['url'] else '<p><code>REPOSITORY_URL_REQUIRED</code></p>\n'
        md+='</td></tr>\n</table>\n\n'
    md+=section(5,'graph','ENGINEERING_MAP','SYSTEM_TOPOLOGY')+picture('engineering-map','Software Engineering Core → Backend & Systems / Data & Machine Learning / Cloud Architecture → DevOps & Platform Engineering, with a focus on reliability.',True)+'\n\n'
    md+='<details>\n<summary>Inspect topology / architecture notes</summary>\n\n'
    md+='**Backend & Systems:** High throughput APIs, Golang concurrency, async workers & microservices. Go · Python · Node · Redis.\n\n**Data & Machine Learning:** Reinforcement learning, ETL pipelines, NLP parsers & predictive analytics. Scikit · TensorFlow · spaCy · Pandas.\n\n**Cloud Architecture:** Containers, auto-scaling environments, secure networking & storage. AWS · Docker · GCP · VPC.\n\n**DevOps & Reliability Engineering:** Continuous delivery (GitHub Actions), containerized runtimes, telemetry metrics, and high uptime operations.\n\n</details>\n\n'
    md+=section(6,'metrics','SYSTEM_METRICS','GITHUB_TELEMETRY')+picture('github-telemetry',f"GitHub @{login}: {t['public_repos']} public repos, {t['pull_requests']} authored public PRs, {t['stars']} repository stars, {t['followers']} followers. Snapshot {t['fetched_at']}.",True)+'\n\n'
    md+=f'<details>\n<summary>Inspect telemetry / source & scope</summary>\n\nSnapshot: **{t["fetched_at"]}** · [@{login}](https://github.com/{login}) · [Source data](assets/telemetry.json).\n\n'
    md+='Public repositories include forks. Pull requests count public PRs authored by this account, across all states; they do not imply approval or merge. Stars are summed across owned public repositories. Languages count the primary language of each non-fork public repository with a detected language; they do not measure proficiency or lines of code.\n\n'
    md+='Commits, contributions and streak are omitted because this snapshot does not provide reliable totals.\n\n</details>\n\n'
    md+=section(7,'exploring','CURRENTLY_EXPLORING','ASYNC_THREADS // ACTIVE_DAEMONS')+'<table>\n'
    for i,p in enumerate(d['exploring']):
        status='INITIALIZING' if i==3 else 'RUNNING'
        md+='<tr><td><p><samp>'+esc(p['name'])+'</samp><br><samp>['+status+']</samp></p><p>'+esc(p['description'])+'</p></td></tr>\n'
    md+='</table>\n\n'+section(8,'contact','ESTABLISH_CONNECTION','COMMAND_DISPATCH // CLI_SHELL')
    md+='<table>\n'
    for cmd,label,url in [('github --profile','github.com/'+login,'https://github.com/'+login),('linkedin --connect','linkedin.com/in/diogodoreislago','https://linkedin.com/in/diogodoreislago'),('mail --protocol=smtp','contact@diogolago.dev','mailto:contact@diogolago.dev'),('ping --portfolio','dev.diogolago.tech','https://dev.diogolago.tech')]:
        md+=f'<tr><td><samp>$ {cmd}</samp><br><a href="{url}">{label}</a></td></tr>\n'
    md+='</table>\n\n'+picture('footer-terminal','DRL-Node // Prompt ready. Building, learning and shipping.',True)+'\n'
    (ROOT/'README.md').write_text(md,encoding='utf-8')

if __name__=='__main__': build()
