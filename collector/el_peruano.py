"""Conservative official-norms discovery; dynamic-page adapter is pending.

Do not interpret no server-rendered links as no norms. Records are never marked
legally verified without human review of the source and legal text.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import requests
from bs4 import BeautifulSoup
SOURCE="https://diariooficial.elperuano.pe/Normas"
HOSTS={"diariooficial.elperuano.pe","busquedas.elperuano.pe"}
KEYWORDS=("resolución","decreto","ordenanza","ley n","directiva")
def extract(html):
    seen={}
    for link in BeautifulSoup(html,"html.parser").select("a[href]"):
        url=urljoin(SOURCE,link["href"])
        if urlsplit(url).hostname not in HOSTS:continue
        title=" ".join(link.get_text(" ",strip=True).split())
        if len(title)<18 or not any(k in title.casefold() for k in KEYWORDS):continue
        seen[url]={"url":url,"title":title,"category":"norma","region":None,"source":"Diario Oficial El Peruano","review_status":"unreviewed","retrieval_status":"metadata_only","id":hashlib.sha256(url.encode()).hexdigest()[:20]}
    return list(seen.values())
def main():
    try:
        r=requests.get(SOURCE,timeout=25,headers={"User-Agent":"RadarSaludPeru/0.2 (metadata researcher)"})
        r.raise_for_status()
        items=extract(r.text)
        status="partial" if items else "failed"
        message="La vista HTML no garantiza cobertura completa; revisar la fuente dinámica."
    except requests.RequestException as e:
        items=[];status="failed";message=str(e)[:250]
    root=Path(__file__).resolve().parent.parent
    now=datetime.now(timezone.utc)
    path=root/"data"/now.strftime("%Y/%m/%d")/"el-peruano.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps({"checked_at":now.isoformat(),"source":SOURCE,"status":status,"coverage":"not_verified","message":message,"items":items},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(status,len(items))
    # The script does not fabricate a comprehensive daily legal bulletin.
    return 0 if status=="partial" else 2
if __name__=="__main__":raise SystemExit(main())
