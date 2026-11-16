#!/usr/bin/env python3
"""
Court402 demo buyer - walks the x402 handshake against app/seller.py.

Step 1 (no arguments):
    Requests the premium resource, receives HTTP 402, and prints the
    payment requirements - including the delivery terms and the evidence
    URL to lock into the Court402 escrow contract on GenLayer.

Step 2 (--agreement case-N):
    After you created the escrow agreement on-chain (GenLayer Studio:
    create_agreement with 0.1 GEN), re-requests the resource with the
    X-PAYMENT proof header and saves the delivered resource. The delivery
    snapshot is what the evidence URL serves - and what the Internet
    Court contract fetches if you file a dispute.

Usage:
    python3 app/seller.py 8402 &        # in another terminal
    python3 app/buyer.py
    python3 app/buyer.py --agreement case-1
"""

import argparse
import json
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8402"


def get(path: str, headers: dict | None = None) -> tuple[int, dict]:
    req = urllib.request.Request(BASE + path, headers=headers or {})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agreement", help="agreement id from the escrow contract, e.g. case-1")
    args = ap.parse_args()

    if not args.agreement:
        status, body = get("/premium/report")
        print(f"GET /premium/report -> HTTP {status}")
        print(json.dumps(body, indent=2))
        req = body["accepts"][0]
        print("\nNext step (on GenLayer, e.g. in Studio):")
        print("  create_agreement(seller, terms, evidenceUrl) with 0.1 GEN")
        print(f"  terms       = {req['terms']}")
        print(f"  evidenceUrl = {req['evidenceUrl']}")
        print("Then run:  python3 app/buyer.py --agreement <case-id>")
        return

    status, body = get("/premium/report", {"X-PAYMENT": f"agreement={args.agreement}"})
    print(f"GET /premium/report (X-PAYMENT: agreement={args.agreement}) -> HTTP {status}")
    print(json.dumps(body, indent=2))
    with open("delivered.json", "w") as f:
        json.dump(body, f, indent=2)
    print("\nDelivered resource saved to delivered.json.")
    print("Happy path: confirm_delivery(agreement) releases the escrow.")
    print("Dispute path: file_dispute(agreement, reason), then rule(agreement)")
    print("lets the Internet Court fetch the evidence URL and settle.")


if __name__ == "__main__":
    main()
