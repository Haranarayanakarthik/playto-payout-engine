# Playto Payout Engine

A full-stack payout system built using **Django + PostgreSQL + Celery + Redis + React**.

This project simulates a real-world fintech payout engine with:
- Ledger-based accounting
- Idempotent APIs
- Concurrency-safe transactions
- Asynchronous payout processing
- Live frontend dashboard

---

## 🚀 Tech Stack

### Backend
- Django (REST Framework)
- PostgreSQL
- Celery
- Redis

### Frontend
- React (Vite)
- Axios

---

## ⚙️ Features

- ✅ Create payouts via API/UI
- ✅ Real-time balance tracking
- ✅ Ledger-based accounting (credit/debit)
- ✅ Idempotency using unique keys
- ✅ Concurrency-safe using DB locks
- ✅ Async payout processing (Celery)
- ✅ Automatic status updates (polling)

---

## 🏗️ Project Structure
playto-payout-engine/
├── backend/
│ ├── config/
│ ├── payouts/
│ ├── manage.py
│ └── requirements.txt
│
├── frontend/
│ ├── src/
│ └── package.json
│
├── README.md
├── EXPLAINER.md


---

## 🧑‍💻 Local Setup

### 1. Clone repo

git clone <your-repo-url>
cd playto-payout-engine


---

### 2. Backend setup


cd backend
pip install -r requirements.txt


---

### 3. Start PostgreSQL

Make sure PostgreSQL is running and DB is created:


DB Name: playto
User: postgres
Password: your_password


---

### 4. Run migrations


python manage.py migrate


---

### 5. Seed initial data


python manage.py shell


```python
from payouts.models import Merchant, LedgerEntry

m = Merchant.objects.create(name="Test Merchant")
LedgerEntry.objects.create(merchant=m, amount_paise=10000, entry_type="credit")
```
6. Start backend
python manage.py runserver
7. Start Redis
redis-server
8. Start Celery worker
cd backend
celery -A config worker -l info -P solo
9. Frontend setup
cd frontend
npm install
npm run dev
10. Open app
http://localhost:5173
📡 API Endpoints
GET /api/v1/dashboard

Returns:

Balance
List of payouts
POST /api/v1/payouts

Headers:

Idempotency-Key: unique_key

Body:

{
  "amount_paise": 5000
}
🧪 Testing Scenarios
Idempotency
Same key → same payout returned
Concurrency
Multiple requests → only valid ones succeed
Insufficient balance
Returns error safely
