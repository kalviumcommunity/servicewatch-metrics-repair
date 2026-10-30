import json,urllib.request,urllib.parse,sys
base="http://localhost:19093/api/v1/"
if sys.argv[1]=="target":
    with urllib.request.urlopen(base+"targets",timeout=3) as r:payload=json.load(r)
    targets=[t for t in payload["data"]["activeTargets"] if t["labels"].get("job")=="servicewatch"]
    assert len(targets)==1,"Wait for target discovery; do not edit monitor.py"
    t=targets[0];print(json.dumps({"job":t["labels"]["job"],"health":t["health"],"scrapeUrl":t["scrapeUrl"],"lastError":t["lastError"]}))
elif sys.argv[1]=="query":
    query=open("query.txt").read().strip()
    with urllib.request.urlopen(base+"query?"+urllib.parse.urlencode({"query":query}),timeout=3) as r:payload=json.load(r)
    print("QUERY="+query);print(json.dumps(payload))
