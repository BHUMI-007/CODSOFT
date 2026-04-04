# Tic-Tac-Toe AI 🎮

An unbeatable Tic-Tac-Toe game with an AI backend powered by the **Minimax Algorithm**.  
Play against an AI that never loses — the best you can do is a draw!

🔗 **Live Demo:** [https://codsoft-sigma-murex.vercel.app/](https://codsoft-sigma-murex.vercel.app/)

---

## 🧠 How the AI Works

- Human plays as **X**, AI plays as **O**
- AI uses the **Minimax Algorithm** to evaluate every possible future game state
- AI is unbeatable — optimal play always results in a draw at best for the human

---

## 🛠️ Tech Stack

| Layer      | Technology        |
|------------|-------------------|
| Frontend   | HTML/CSS/JS (Vercel) |
| Backend    | Python + FastAPI (Render) |
| Algorithm  | Minimax (recursive, no pruning) |
| Deployment | Vercel + Render |

---

## 🏗️ Architecture

```
User (Browser)
     ↓
Frontend — Vercel
     ↓ POST /move
Backend API — Render (FastAPI)
     ↓
Minimax Algorithm
     ↓
Best move returned as JSON
```

---

## 📁 Project Structure

```
├── backend/
│   ├── main.py        # FastAPI app, /move endpoint
│   ├── game.py        # Board logic, winner check
│   └── minimax.py     # Minimax recursive AI
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js      # Calls backend API on each move
```

---

## 🚀 Run Locally

**Backend:**
```bash
cd backend
pip install fastapi uvicorn
uvicorn main:app --reload
```

**Frontend:**  
Open `frontend/index.html` in your browser  
or set `API_URL` in `script.js` to `http://localhost:8000`

---

## 📡 API

`POST /move`

**Request:**
```json
{ "board": ["X", "", "O", "", "X", "", "", "", ""] }
```

**Response:**
```json
{ "move": 8 }
```

## Project
Built as Task 2 for CodSoft Internship.
