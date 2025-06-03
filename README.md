# 🕵️‍♂️ Ayaan - Real-time Fraud Detection Dashboard

Ayaan is a real-time fraud detection dashboard built using **Golang** for the backend and **React** for the frontend. It processes transactions, flags suspicious activity, and updates in real-time using polling. This project is designed for financial monitoring and visual transaction analysis.

## 🚀 Features

- 🧠 Rule-based fraud detection logic
- 📊 Interactive frontend to view transactions
- 🔍 Suspicious transaction filter
- 🔄 Real-time data updates via polling
- 🌐 Arabic name support
- 🟢 Backend deployed on [Render](https://render.com/)
- 🟣 Frontend deployed on [Netlify](https://www.netlify.com/)

---

## 🧱 Tech Stack

| Layer      | Tech       |
|------------|------------|
| Frontend   | React.js (Vite) |
| Backend    | Golang     |
| Styling    | Vanilla CSS |
| Hosting    | Netlify (frontend) + Render (backend) |

---

## 📂 Project Structure
Ayaan/
├── backend_go/
│ └── cmd/
│ └── main.go # Go backend logic
├── frontend_react/
│ ├── public/
│ ├── src/
│ │ ├── App.jsx
│ │ ├── main.jsx
│ │ └── index.css
│ └── vite.config.js
└── README.md


## 🛠️ Running Locally

### 1. Backend (Go)

```bash
cd backend_go/cmd
go run main.go

Server starts at: http://localhost:8080/transactions


2. Frontend (React)

cd frontend_react
npm install
npm run dev

🌍 Deployment
Backend (Render)
Go to Render

Create new Web Service

Connect GitHub and select the repo

Build Command: go build -o server ./backend_go/cmd/main.go

Start Command: ./server

Add backend_go/cmd/main.go as the entry point

Frontend (Netlify)
Go to Netlify

Link GitHub repo
Build Command: npm run build
Publish directory: frontend_react/dist


📬 API
GET /transactions
Returns a list of transactions:

json
Copy
Edit
[
  {
    "customer_name": "محمد فهد",
    "amount": 55000,
    "location": "Riyadh",
    "timestamp": "2025-06-01T13:00:00Z"
  }
]
