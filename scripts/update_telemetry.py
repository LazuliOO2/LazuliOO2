"""Refresh public GitHub data without dependencies or credentials; rebuild separately."""
import json
import os
import re
from datetime import datetime, timezone, timedelta, date
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
username=json.loads((ROOT/'assets/profile.json').read_text(encoding='utf-8'))['username']

def get(url, api=True):
    headers={'User-Agent':'profile-command-center','Accept':'application/vnd.github+json' if api else 'text/html'}
    if api and os.environ.get('GITHUB_TOKEN'): headers['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
    with urlopen(Request(url,headers=headers),timeout=30) as response:
        content=response.read().decode('utf-8')
    return json.loads(content) if api else content

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__(); self.days={}; self.labels={}; self.active=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='td' and 'data-date' in a: self.days[a['id']]=a['data-date']
        if tag=='tool-tip': self.active=a.get('for'); self.labels[self.active]=''
    def handle_data(self,data):
        if self.active: self.labels[self.active]+=data
    def handle_endtag(self,tag):
        if tag=='tool-tip': self.active=None

repos=[]
page=1
while True:
    batch=get(f'https://api.github.com/users/{username}/repos?per_page=100&page={page}')
    repos+=batch
    if len(batch)<100: break
    page+=1
user=get(f'https://api.github.com/users/{username}')
languages={}
for repo in repos:
    if not repo['fork']:
        for lang,count in get(repo['languages_url']).items(): languages[lang]=languages.get(lang,0)+count
calendar=Calendar()
calendar.feed(get(f'https://github.com/users/{username}/contributions',False))
today=datetime.now(timezone.utc).date()
days=[]
for ident,day in calendar.days.items():
    label=calendar.labels.get(ident,'')
    match=re.search(r'\b(No|[\d,]+) contributions? on',label)
    if not match: raise ValueError('GitHub calendar format changed; previous snapshot preserved.')
    if day<=today.isoformat(): days.append({'date':day,'count':0 if match[1]=='No' else int(match[1].replace(',',''))})
days.sort(key=lambda d:d['date'])
if len(days)<31: raise ValueError('Incomplete contribution calendar; previous snapshot preserved.')
for prev,nxt in zip(days,days[1:]):
    if date.fromisoformat(nxt['date'])-date.fromisoformat(prev['date'])!=timedelta(days=1): raise ValueError('Calendar has missing days.')
longest=run=0
for day in days:
    run=run+1 if day['count'] else 0
    longest=max(longest,run)
current=0
tail=days[:-1] if days[-1]['date']==today.isoformat() and days[-1]['count']==0 else days
for day in reversed(tail):
    if not day['count']: break
    current+=1
data={'date':today.isoformat(),'repositories':len(repos),'stars':sum(r['stargazers_count'] for r in repos),'followers':user['followers'],'languages':languages,'contributions':days,'current_streak':current,'longest_streak':longest}
target=ROOT/'assets/telemetry.json'
temporary=target.with_suffix('.tmp')
temporary.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
temporary.replace(target)
print('Public telemetry refreshed:',today)
