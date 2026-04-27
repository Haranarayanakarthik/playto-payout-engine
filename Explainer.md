Overview

I built a payout engine that allows a merchant to withdraw funds safely. The system focuses on correctness under concurrency, idempotent APIs, and asynchronous processing, which are critical in financial systems.

Key Decisions
1) Ledger over stored balance

I used an append-only ledger (credit/debit entries) and compute balance via a DB aggregation.

Why:

Avoids race conditions from updating a single balance field
Provides a full audit trail
Ensures correctness even with concurrent requests
2) Concurrency control with DB locks

Before creating a payout, I lock rows using:

select_for_update()

Why:

Prevents two requests from spending the same balance
Guarantees only one transaction modifies funds at a time
Eliminates double-spend scenarios
3) Idempotent payout API

Each request includes an Idempotency-Key with a unique constraint per merchant.

Behavior:

Same key → returns the same payout
No duplicate records created

Why:

Safe retries during network failures
Required pattern in payment systems
4) Asynchronous processing (Celery + Redis)

Payout execution is offloaded to a worker:

process_payout.delay(payout.id)

Why:

Non-blocking API responses
Simulates real payment gateway latency
Scales independently of API
5) Payout lifecycle (state machine)
pending → processing → completed
                     → failed

Why:

Explicit states make transitions predictable
Easier to debug and extend (retries, audits)
6) Failure handling

On failure:

Status → failed
Funds are credited back via the ledger

Why:

Ensures no money is lost
Keeps system consistent
Frontend Integration
Built with React
Uses Axios to call APIs
Uses polling (every few seconds) to reflect async status changes

Tradeoff:

Polling is simple but not optimal → would replace with WebSockets in production
CORS Handling

Enabled CORS and explicitly allowed custom header:

Idempotency-Key
What I improved from a naive approach

Naive:

Store balance in a column
Update in application code

Problems:

Race conditions
Inconsistent state

Final:

DB aggregation + row locks + idempotency → correct under concurrency
Summary

This system ensures:

Correctness under concurrent requests
Safe retries via idempotency
Non-blocking execution using async workers
Clean, auditable financial records
