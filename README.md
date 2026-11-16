# Court402 — Internet Court adjudication for x402 agent payments

**An Internet Court × x402 integration built on GenLayer.**
When AI agents buy digital goods from each other with the
[x402](https://www.x402.org/) payment standard, payment is instant — but
disputes are not. *Did the API actually return what was promised? Was the
file the right one?* A normal smart contract cannot judge that. An
Intelligent Contract can.

Court402 puts the payment in escrow on GenLayer and lets the
**Internet Court** — GenLayer's AI-jury dispute-resolution layer — rule
on delivery disputes by fetching the evidence and judging it against the
agreed terms.

Built for the GenLayer Portal Builders Working Group mission
**“Internet Court: Partner Demo Lab”** (deadline 2026-11-22).

![Internet Court](docs/logos/internet-court.png) ![GenLayer](docs/logos/genlayer.png) ![x402](docs/logos/x402.png)

## The demo flow

1. **402 handshake** — a buyer agent requests a premium resource from a
   seller agent. The seller answers `402 Payment Required` with payment
   requirements that point at the Court402 escrow contract instead of a
   direct wallet payment.
2. **Escrow** — the buyer calls `create_agreement` on
   `AgentEscrowCourt`, locking GEN together with the *natural-language
   delivery terms* and an *evidence URL* (where the delivery can be
   inspected).
3. **Delivery** — the seller delivers and calls `mark_delivered`.
4. **Happy path** — the buyer calls `confirm_delivery`; the escrow is
   released to the seller.
5. **Dispute path** — the buyer calls `file_dispute` with a reason.
   Anyone can then call `rule()`: the contract fetches the evidence
   page, an LLM jury of GenLayer validators judges delivery against the
   terms under the Equivalence Principle, and the escrow is
   automatically released to the seller or refunded to the buyer.

## Why GenLayer is essential here

The verdict is a *subjective judgment over web evidence* — exactly what
only an Intelligent Contract can settle on-chain:

- `gl.nondet.web.render` fetches the delivery evidence inside consensus.
- `gl.nondet.exec_prompt` reasons over terms + evidence as a judge.
- `gl.eq_principle.strict_eq` makes independent validators agree on the
  verdict (Optimistic Democracy — the same jury model the Internet
  Court uses at protocol level).
- Value moves only by verdict: `@gl.public.write.payable` escrows GEN,
  `emit_transfer` pays it out.

## Repository layout

| Path | What |
| --- | --- |
| `contracts/AgentEscrowCourt.py` | The Intelligent Contract (escrow + AI adjudication) |
| `app/` | x402 seller mock (`seller.py`) + buyer walkthrough (`buyer.py`), stdlib only |
| `docs/` | Demo landing page + delivery evidence pages (served via GitHub Pages) |
| `video/` | The ≤45 s demo video and its build script *(in progress)* |

## Try it in GenLayer Studio

1. Open [GenLayer Studio](https://studio.genlayer.com/) and import
   `contracts/AgentEscrowCourt.py`.
2. Deploy it (Bradbury testnet or the Studio simulator).
3. As the buyer, call `create_agreement(seller, terms, evidence_url)`
   **with value** (e.g. 0.1 GEN) — save the returned `case-N` id.
4. As the seller, call `mark_delivered(case-N)`.
5. Happy path: as the buyer, `confirm_delivery(case-N)`.
   Dispute path: as the buyer, `file_dispute(case-N, "reason")`, then
   anyone calls `rule(case-N)` and reads the verdict with
   `get_agreement(case-N)`.

## Status

- [x] Intelligent Contract (escrow, delivery, dispute, AI ruling, payout)
- [x] x402 seller/buyer demo app (402 handshake verified locally)
- [x] Demo landing page + evidence pages on GitHub Pages
- [ ] Deploy on Bradbury testnet + explorer link
- [ ] Demo video (≤45 s)

## License

MIT
