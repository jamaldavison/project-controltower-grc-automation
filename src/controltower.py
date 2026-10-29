"""Offline fictional ITGC evidence metadata assurance demo. No production systems."""
import csv, json, argparse
from collections import Counter
from datetime import datetime
from pathlib import Path
REQUIRED={'record_id','control_id','control_domain','system','owner','due_date','evidence_date','status','evidence_uri','reviewer'}
VALID_STATUS={'Submitted','Missing','Rejected','Approved'}
def run(input_path,output_dir,as_of='2026-10-29'):
    date=datetime.strptime(as_of,'%Y-%m-%d').date()
    with open(input_path,newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    if not rows or not REQUIRED.issubset(rows[0]):
        raise ValueError('Input empty or columns missing')
    seen=set();results=[]
    for r in rows:
        if r['record_id'] in seen:raise ValueError('Duplicate record_id: '+r['record_id'])
        seen.add(r['record_id'])
        if r['status'] not in VALID_STATUS:raise ValueError('Unknown status '+r['status'])
        due=datetime.strptime(r['due_date'],'%Y-%m-%d').date()
        ev=datetime.strptime(r['evidence_date'],'%Y-%m-%d').date() if r['evidence_date'] else None
        flags=[]
        if r['status']!='Approved':flags.append('Not approved')
        if not r['evidence_uri']:flags.append('No evidence reference')
        if not r['reviewer']:flags.append('No reviewer')
        if due<date and r['status']!='Approved':flags.append('Overdue')
        if ev and ev>date:flags.append('Evidence dated in future')
        if ev and ev>due:flags.append('Evidence after due date')
        if r['status']=='Approved' and not ev:flags.append('Approval without evidence date')
        results.append({**r,'evaluation':'Needs review' if flags else 'Ready for sample review','flags':'; '.join(flags),'days_overdue':max(0,(date-due).days) if r['status']!='Approved' else 0})
    output=Path(output_dir);output.mkdir(parents=True,exist_ok=True)
    with open(output/'evidence_results.csv','w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(results[0]));writer.writeheader();writer.writerows(results)
    counts=Counter(r['evaluation'] for r in results)
    domain={d:{'records':sum(r['control_domain']==d for r in results),'flagged':sum(r['control_domain']==d and r['evaluation']=='Needs review' for r in results)} for d in sorted({r['control_domain'] for r in results})}
    summary={'as_of':as_of,'fictional_data':True,'total_records':len(results),'ready_for_sample_review':counts['Ready for sample review'],'needs_review':counts['Needs review'],'overdue_not_approved':sum('Overdue' in r['flags'] for r in results),'by_domain':domain,'caution':'Automated checks are not control effectiveness testing or compliance conclusions.'}
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    report=['# ControlTower — Fictional Continuous Controls Dashboard','',f'As of **{as_of}** | Sample records: **{len(results)}**',f"Flagged: **{summary['needs_review']}** | Ready for manual sample review: **{summary['ready_for_sample_review']}**",'','## Domain review','','| Domain | Records | Flagged |','|---|---:|---:|']
    report += [f"| {d} | {m['records']} | {m['flagged']} |" for d,m in domain.items()]
    report += ['','## Items needing review','','| Record | Control | Status | Flags |','|---|---|---|---|']
    report += [f"| {r['record_id']} | {r['control_id']} | {r['status']} | {r['flags']} |" for r in results if r['evaluation']=='Needs review']
    report += ['','**Limitations:** Constructed data only; no live control was tested.']
    (output/'dashboard.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    return summary
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',default='data/sample_evidence.csv');p.add_argument('--out',default='outputs');p.add_argument('--as-of',default='2026-10-29');a=p.parse_args();print(json.dumps(run(a.input,a.out,a.as_of),indent=2))
