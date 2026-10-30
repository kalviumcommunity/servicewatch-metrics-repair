import urllib.request
for _ in range(5):
    with urllib.request.urlopen("http://localhost:18093/demo",timeout=3) as r:assert r.status==200
print("Generated 5 successful demo requests")
