# Q3: Restore Live Monitoring Signals

**Course:** DevOps Foundation · **Module:** 5, Monitoring, Cost & Production Readiness  
**Submission:** one PDF file upload · **Difficulty:** medium · **Marks:** 20  
**Target duration:** 33 minutes, including screenshots and PDF assembly after preparation. Budget 40 minutes maximum; pilot timing not yet measured.  
**Lesson alignment:** 5.1 metrics; 5.7 anomaly baseline; 5.9 alert design; monitoring subset of 5.10.

## Problem statement

ServiceWatch API responds, but its metrics do not reach Prometheus and its supplied query selects a nonexistent metric. Restore live visibility, then interpret a small supplied incident dataset and propose a useful alert.

**Starter repository:** https://github.com/kalviumcommunity/servicewatch-metrics-repair  
**Allowed edits:** prometheus.yml: target port only; query.txt: metric name only; alert-review.md: two answer lines. Preserve app, traffic generator, monitor helper, ports and supplied signals.

## Preparation (before assessment timer)

Use Python 3.10+ on host, Git, Docker Engine/Desktop and Compose v2 (supports --no-log-prefix). Linux/macOS or prepared WSL. No pip packages, jq, paid tools, registry credentials or cloud account required. Docker Desktop subject to its license; free Linux Docker Engine sufficient.

Clone supplied repo (fork optional), enter directory and reserve host port 18093 plus 19093. Download/build before timer:

```sh
docker pull python:3.12-slim
docker pull prom/prometheus:v3.5.0
docker compose config --quiet
docker compose build
mkdir -p evidence
docker compose up -d
```

Wait up to 15 seconds for listeners/probes/scrapes before diagnosing. Initial task faults are intentional, not setup failures. If Docker/tool/download or port setup fails, resolve before starting timer. Commands run from repo root. Host evidence/ is ignored. Use a fresh exercise stack with no unrelated traffic. Do not edit helpers to force checks to pass.

## Task 1: Repair metrics collection (6 marks, ~10 minutes)

Show API /metrics response while Prometheus reports servicewatch target down. Diagnose mismatch from scrape URL/error and provided internal API port 8080. Correct scrape target port only. Recreate Prometheus and show target up after at least one scrape. Do not change app ports or metrics path.

```sh
python3 http_get.py http://localhost:18093/metrics
python3 monitor.py target
# After target repair:
docker compose up -d --force-recreate prometheus
# Wait up to 15 seconds for discovery/scraping, then:
python3 monitor.py target
```

**Evidence:** capture actual commands/results requested above and add a short cause/fix/result caption. Extra screenshots are allowed when output cannot fit readably. At least one labelled screenshot per task; one screenshot need not contain all checks.

## Task 2: Repair and verify metric query (7 marks, ~12 minutes)

Execute supplied query to show empty result despite target up. Compare exposed metric names; correct query.txt. Wait for a scrape and record counter value, run traffic.py ONCE (five requests), wait for next scrape and query again. Show same uninterrupted API counter increases by exactly five; do not rebuild/recreate API between samples. Empty/stale result means wait and retry, not fabricate values.

```sh
python3 monitor.py query
# After query.txt repair; wait at least 3 seconds before each sample:
python3 monitor.py query
python3 traffic.py
# Wait at least 3 seconds for scrape:
python3 monitor.py query
```

**Evidence:** capture actual commands/results requested above and add a short cause/fix/result caption. Extra screenshots are allowed when output cannot fit readably. At least one labelled screenshot per task; one screenshot need not contain all checks.

## Task 3: Interpret signals and propose alert (7 marks, ~11 minutes)

signals.csv contains SUPPLIED SIMULATED equal one-minute windows, not live data. Complete alert-review.md: (1) calculate baseline and all three incident error percentages (failed/requests*100), identify sustained anomaly using values; (2) propose error-percentage threshold, duration, severity and one owning on-call role, explaining why a one-off failure should not page. A justified policy is accepted; no exact threshold answer required. No alert implementation or wait-to-fire required.

```sh
python3 -c "from pathlib import Path; print(Path('signals.csv').read_text())"
# Fill two short answer lines in alert-review.md. Include them in PDF.
```

**Evidence:** capture actual commands/results requested above and add a short cause/fix/result caption. Extra screenshots are allowed when output cannot fit readably. At least one labelled screenshot per task; one screenshot need not contain all checks.

## Submission: one PDF only

Three labelled task sections with readable genuine terminal screenshots, requested written findings, and complete diff of permitted files once. No PR, video, ZIP or separate code upload. Retain evidence locally; only PDF is uploaded. Tool choice for PDF assembly is unrestricted; export/print labelled screenshots and text to PDF. Do not expose secrets or personal data. No separate marks for filename, URLs, fork ownership, branch labels or submission commit IDs. An instructor standalone reference is valid under identical technical criteria.

The scored work is exactly the three tasks above. No hidden rubric requirements, duplicate deductions or automatic whole-submission zero for an unrelated missing item. Technical request IDs and release values requested within tasks ARE evidence, not submission metadata. Score missing technical evidence only against its corresponding subcriterion.

## Evaluation rubric

| Task | Explicit task criteria | Marks |
|---|---|---|
| Task 1 | Working metrics versus failed target diagnosis (2); correct internal scrape target port (2); observed target up (2). | 6 |
| Task 2 | Empty-result/metric-name diagnosis (2); corrected query (2); two actual samples and measured +5 after supplied traffic (3). | 7 |
| Task 3 | Four accurate percentages and anomaly conclusion (3); threshold/duration appropriate to supplied sustained incident (2); severity and one owner (1); transient-noise rationale (1). | 7 |

**Total: 6 + 7 + 7 = 20.** Written alternatives accepted when technically correct and supported by requested evidence. No cloud execution required or credited.

## Cleanup (after evidence capture)

```sh
docker compose down
```

Remove only exercise resources, never unrelated containers or images. Source code, supplied fixtures and helper scripts outside allowed edits must remain unchanged.
