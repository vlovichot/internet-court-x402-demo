#!/usr/bin/env python3
"""
Court402 demo seller - a minimal x402-style paid API.

The seller agent offers a premium market report. Instead of asking for a
direct wallet payment, its 402 response points the buyer at the Court402
escrow contract on GenLayer: the buyer locks GEN in the contract with
delivery terms + an evidence URL, then re-requests the resource with an
X-PAYMENT proof header carrying the agreement id.

Run:  python3 app/seller.py [port]        (default 8402)
Then: python3 app/buyer.py                (walks the handshake)

No third-party dependencies - Python standard library only.
"""

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

# Fill in after deploying contracts/AgentEscrowCourt.py (Bradbury testnet).
ESCROW_CONTRACT = "0x0000000000000000000000000000000000000000"

TERMS = (
    "The premium report must contain: the BTC price, the ETH price, and a "
    "one-line market sentiment, all dated 2026-11-16."
)

EVIDENCE_URL = (
    "https://vlovichot.github.io/internet-court-x402-demo"
    "/evidence/good-delivery.html"
)

RESOURCE = {
    "report": "Court402 premium market snapshot",
    "date": "2026-11-16",
    "BTC": "$97,240",
    "ETH": "$3,412",
    "sentiment": "Cautiously bullish - ETF inflows positive for a 6th day.",
}


def payment_requirements() -> dict:
    return {
        "x402Version": 1,
        "error": "Payment required",
        "accepts": [
            {
                "scheme": "escrow",
                "network": "genlayer-bradbury",
                "asset": "GEN",
                "amount": "0.1",
                "payTo": "Court402 escrow contract",
                "escrowContract": ESCROW_CONTRACT,
                "terms": TERMS,
                "evidenceUrl": EVIDENCE_URL,
                "instructions": (
                    "Call create_agreement(seller, terms, evidenceUrl) on "
                    "the escrow contract with 0.1 GEN, then retry this "
                    "request with header 'X-PAYMENT: agreement=<case-id>'."
                ),
            }
        ],
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 (stdlib naming)
        if self.path == "/":
            self._send(
                200,
                json.dumps(
                    {"service": "Court402 premium data seller", "endpoints": ["/premium/report"]}
                ).encode(),
                "application/json",
            )
            return

        if self.path == "/premium/report":
            proof = self.headers.get("X-PAYMENT", "")
            if proof.startswith("agreement=") and len(proof) > len("agreement="):
                # Payment escrowed on GenLayer: deliver the resource.
                self._send(200, json.dumps(RESOURCE, indent=2).encode(), "application/json")
            else:
                # x402 handshake: tell the buyer how to pay - via escrow.
                self._send(
                    402,
                    json.dumps(payment_requirements(), indent=2).encode(),
                    "application/json",
                )
            return

        self._send(404, b'{"error": "not found"}', "application/json")

    def log_message(self, *args) -> None:  # keep the demo output clean
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8402
    print(f"Court402 seller listening on http://127.0.0.1:{port}")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
