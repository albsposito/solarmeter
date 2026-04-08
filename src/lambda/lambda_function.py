import json
import os
import time
from decimal import Decimal
import urllib.request

INFLUX_URL = os.environ["INFLUX_URL"]
INFLUX_TOKEN = os.environ["INFLUX_TOKEN"]
ORG = os.environ["INFLUX_ORG"]
BUCKET = os.environ["INFLUX_BUCKET"]

def is_number(v):
    return isinstance(v, (int, float, Decimal))

def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))

    # Timestamp (IoT rule provides ts in ms as string)
    if "ts" in event:
        ts_ns = int(event["ts"]) * 1_000_000
    else:
        ts_ns = int(time.time() * 1_000_000_000)

    inverter_id = event.get("thingId", "unknown")

    lines = []
    for k, v in event.items():
        if k in ("ts", "thingId", "ingested_at"):
            continue
        if is_number(v):
            lines.append(
                f"solar_metrics,inverter_id={inverter_id} {k}={float(v)} {ts_ns}"
            )

    if not lines:
        print("NO NUMERIC FIELDS FOUND")
        return {"status": "no numeric fields"}

    payload = "\n".join(lines)
    print("LINE PROTOCOL:\n", payload)

    url = f"{INFLUX_URL}/api/v2/write?org={ORG}&bucket={BUCKET}&precision=ns"

    req = urllib.request.Request(
        url,
        data=payload.encode("utf-8"),
        headers={
            "Authorization": f"Token {INFLUX_TOKEN}",
            "Content-Type": "text/plain; charset=utf-8"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            body = resp.read().decode()
    except Exception as e:
        print("WRITE FAILED:", str(e))
        raise

    print("INFLUX STATUS:", status)
    print("INFLUX RESPONSE:", body)

    return {"status": "ok", "points": len(lines)}

