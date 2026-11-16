"""Daily, source-transparent RSS discovery. Never implies complete regional coverage.

The Google News RSS search feed is a discovery mechanism, not a verified
epidemiological data source. Official portals and norms are handled separately.
"""
import argparse
import hashlib
import json
import re
import time
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import requests

LIMA = ZoneInfo("America/Lima")
REGIONS = ["Amazonas","Áncash","Apurímac","Arequipa","Ayacucho","Cajamarca","Callao","Cusco","Huancavelica","Huánuco","Ica","Junín","La Libertad","Lambayeque","Lima","Loreto","Madre de Dios","Moquegua","Pasco","Piura","Puno","San Martín","Tacna","Tumbes","Ucayali"]
ROOT = Path(__file__).resolve().parent.parent
MAX_PER_FEED = 8
USER_AGENT = "RadarSaludPeru/0.2 (+https://github.com/josephruiz/radar-salud-peru; public metadata research)"
def queries():
    yield ("Nacional", '(salud OR hospital OR dengue OR epidemiologia) Peru when:1d')
    yield ("Riesgos", '("fenomeno del nino" OR inundaciones OR lluvias) (salud OR dengue OR epidemiologia) Peru when:2d')
    for region in REGIONS:
        yield (region, f'("{region}" salud OR "{region}" dengue OR "{region}" hospital) when:2d')
def rss_url(query):
    return "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q":query,"hl":"es-419","gl":"PE","ceid":"PE:es-419"})
def published(value):
    if not value:
        return None
    try:
        t = parsedate_to_datetime(value)
        if t.tzinfo is None: t=t.replace(tzinfo=timezone.utc)
        return t.astimezone(LIMA)
    except (TypeError, ValueError, IndexError): return None
def strip_tags(value):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", value or "")).strip()
def region_in_title(title):
    normalized = title.casefold()
    # Explicit title-level evidence only; the query's region alone is not proof.
    for region in sorted(REGIONS, key=len, reverse=True):
        if re.search(r"(?<!\w)"+re.escape(region.casefold())+r"(?!\w)", normalized):
            return region
    return None
def parse_rss(xml_bytes, requested_date):
    root=ET.fromstring(xml_bytes)
    out=[]
    for item in root.findall(".//channel/item")[:MAX_PER_FEED]:
        title=(item.findtext("title") or "").strip()
        link=(item.findtext("link") or "").strip()
        pub=published(item.findtext("pubDate"))
        if not title or not link.startswith("https://") or not pub or pub.date().isoformat()!=requested_date:continue
        source=item.find("source")
        source_name=(source.text or "").strip() if source is not None else "Agregador de noticias"
        key=hashlib.sha256(link.encode("utf-8")).hexdigest()[:20]
        out.append({"id":key,"title":title,"url":link,"published_at":pub.isoformat(),"region":region_in_title(title),"category":"noticia","source":source_name,"origin":"Google News RSS; fuente original sin verificar","review_status":"unreviewed","summary":""})
    return out
def run(target_date, fetch=requests.get, delay=0.35):
    items={}; errors=[]; succeeded=0
    for label, query in queries():
        try:
            response=fetch(rss_url(query),timeout=22,headers={"User-Agent":USER_AGENT})
            response.raise_for_status()
            new=parse_rss(response.content, target_date)
            succeeded+=1
            for row in new:items[row["url"]]=row
        except (requests.RequestException, ET.ParseError, ValueError) as exc:
            errors.append({"feed":label,"message":str(exc)[:250]})
        if delay: time.sleep(delay)
    status = "success" if not errors else ("partial" if succeeded else "failed")
    return {"date":target_date,"checked_at":datetime.now(timezone.utc).isoformat(),"status":status,"coverage":"unverified_rss_discovery","sources_checked":succeeded,"sources_total":len(REGIONS)+2,"errors":errors,"items":sorted(items.values(),key=lambda x:x["published_at"],reverse=True)}
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--date",default=datetime.now(LIMA).date().isoformat())
    parser.add_argument("--output-root",default=str(ROOT/"data"))
    args=parser.parse_args()
    try:target=datetime.strptime(args.date,"%Y-%m-%d").date()
    except ValueError:parser.error("Use YYYY-MM-DD")
    if target>datetime.now(LIMA).date():parser.error("La fecha no puede estar en el futuro")
    data=run(target.isoformat())
    base=Path(args.output_root)
    dest=base/target.strftime("%Y/%m/%d")/"edition.json"
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    index=base/"index.json"
    try:payload=json.loads(index.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError):payload={"days":[]}
    days={x["date"]:x for x in payload.get("days",[]) if isinstance(x,dict) and "date" in x}
    days[target.isoformat()]={"date":target.isoformat(),"count":len(data["items"]),"status":data["status"]}
    payload={"updated_at":data["checked_at"],"days":sorted(days.values(),key=lambda r:r["date"],reverse=True)}
    index.parent.mkdir(parents=True,exist_ok=True)
    index.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    # Small rolling searchable index until PostgreSQL full-text search is enabled.
    search_file=base/"search-index.json"
    try:
        old=json.loads(search_file.read_text(encoding="utf-8"))
        existing={x["url"]:x for x in old.get("items",[]) if isinstance(x,dict) and x.get("url")}
    except (OSError,json.JSONDecodeError,TypeError):existing={}
    for row in data["items"]:existing[row["url"]]=row
    ordered=sorted(existing.values(),key=lambda x:x.get("published_at",""),reverse=True)[:8000]
    search_file.write_text(json.dumps({"updated_at":data["checked_at"],"limited_to":8000,"items":ordered},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    print(json.dumps({"status":data["status"],"records":len(data["items"]),"errors":len(data["errors"]),"date":args.date}))
    # Never claim completeness; task fails if all sources fail.
    return 2 if data["status"]=="failed" else 0
if __name__=="__main__":
    raise SystemExit(main())
