"""Fetch public, auditable GitHub metrics; preserve previous data on any failure."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import urllib.request
from build import build

ROOT = Path(__file__).resolve().parents[1]
LOGIN = 'LazuliOO2'

def get(path):
    headers={'User-Agent':'DRL-profile-telemetry','Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
    if os.environ.get('GH_TOKEN'): headers['Authorization']='Bearer '+os.environ['GH_TOKEN']
    with urllib.request.urlopen(urllib.request.Request('https://api.github.com/'+path,headers=headers),timeout=30) as response:
        return json.load(response)

def main():
    user=get('users/'+LOGIN)
    repos=[]
    for page in range(1,1001):
        batch=get(f'users/{LOGIN}/repos?type=owner&per_page=100&page={page}')
        repos.extend(batch)
        if len(batch)<100: break
    else: raise RuntimeError('Pagination did not complete')
    prs=get(f'search/issues?q=author:{LOGIN}+type:pr+is:public&per_page=1')
    if prs.get('incomplete_results'): raise RuntimeError('Incomplete PR search; keeping previous snapshot')
    if len(repos)!=user['public_repos']: raise RuntimeError('Repository count changed during collection; retry later')
    languages=Counter(r['language'] for r in repos if not r['fork'] and r['language'])
    data={'login':user['login'],'fetched_at':datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
          'public_repos':user['public_repos'],'pull_requests':prs['total_count'],
          'followers':user['followers'],'stars':sum(r['stargazers_count'] for r in repos),
          'languages':dict(sorted(languages.items(),key=lambda x:(-x[1],x[0]))),
          'sources':[f'https://api.github.com/users/{LOGIN}',f'https://api.github.com/users/{LOGIN}/repos?type=owner&per_page=100',f'https://api.github.com/search/issues?q=author:{LOGIN}+type:pr+is:public'],
          'repositories':[{'name':r['name'],'url':r['html_url'],'fork':r['fork'],'primary_language':r['language'],'stars':r['stargazers_count']} for r in repos]}
    target=ROOT/'assets/telemetry.json'
    temp=target.with_suffix('.tmp')
    temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temp.replace(target)
    build()
    print(f"Updated @{LOGIN}: {len(repos)} public repositories, {prs['total_count']} authored public PRs")

if __name__=='__main__': main()
