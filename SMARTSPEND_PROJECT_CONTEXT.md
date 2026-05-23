Project Name:
SmartSpend AI

Backend:
- FastAPI Async
- aiosqlite
- JWT Authentication
- Twilio WhatsApp Integration
- Groq AI Integration
- Async APIs
- Billing cycle based monthly spend computation
- Soft delete transaction handling
- Duplicate transaction prevention
- Forgot password via WhatsApp reset link

Frontend:
- Node.js + Express
- EJS Templates
- Session based login

Backend APIs:
POST /auth/signup
POST /auth/login
POST /auth/forgot-password
POST /auth/reset-password

POST /limit/create

POST /transaction/add
DELETE /transaction/delete/{id}

GET /history/transactions

Architecture:

Frontend(NodeJS)
    ↓
FastAPI Async Backend
    ↓
JWT Auth
    ↓
SQLite(aiosqlite)
    ↓
Groq AI
    ↓
Twilio WhatsApp

Folder Structure:

app/
 ├ auth/
 ├ api/
 ├ db/
 ├ whatsapp/
 ├ ai/
 └ utils/

smartspend-web/
 ├ routes/
 ├ views/
 └ public/

Important Decisions:

- Monthly billing cycle isolation
- New month computation independent
- Password never exposed
- Async APIs production safe
- Background WhatsApp tasks
- Forgot password token expiry 5 mins