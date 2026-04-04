import { useState, useEffect } from "react";
import "./App.css";

const API = "https://tictactoe-backend-u5jh.onrender.com";

function App() {
  const [board, setBoard] = useState(Array(3).fill(Array(3).fill(" ")));
  const [status, setStatus] = useState("ongoing");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API}/state`)
      .then(r => r.json())
      .then(d => setBoard(d.board));
  }, []);

  const handleClick = async (row, col) => {
    if (loading || status !== "ongoing" || board[row][col] !== " ") return;
    setLoading(true);
    const res = await fetch(`${API}/move`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ row, col })
    });
    const data = await res.json();
    setBoard(data.board);
    setStatus(data.status || "ongoing");
    setLoading(false);
  };

  const handleReset = async () => {
    const res = await fetch(`${API}/reset`, { method: "POST" });
    const data = await res.json();
    setBoard(data.board);
    setStatus("ongoing");
  };

  const getStatusMessage = () => {
    if (status === "human_wins") return "🎉 You Won!";
    if (status === "ai_wins")   return "🤖 AI Wins!";
    if (status === "draw")      return "🤝 It's a Draw!";
    if (loading)                return "🤖 AI is thinking...";
    return "🎮 Your turn! (You are X)";
  };

  const getCellClass = (val) => {
    if (val === "X") return "cell x";
    if (val === "O") return "cell o";
    return "cell empty";
  };

  return (
    <div className="app">
      <h1 className="title">Tic-Tac-Toe <span>AI</span></h1>
      <p className="subtitle">You vs Minimax AI — Can you beat it?</p>

      <div className={`status-badge ${status}`}>
        {getStatusMessage()}
      </div>

      <div className="board">
        {board.map((row, i) =>
          row.map((cell, j) => (
            <div
              key={`${i}-${j}`}
              className={getCellClass(cell)}
              onClick={() => handleClick(i, j)}
            >
              <span>{cell !== " " ? cell : ""}</span>
            </div>
          ))
        )}
      </div>

      <button className="reset-btn" onClick={handleReset}>
        🔄 New Game
      </button>

      <div className="legend">
        <div className="legend-item"><span className="x-dot">X</span> You</div>
        <div className="legend-item"><span className="o-dot">O</span> AI</div>
      </div>
    </div>
  );
}

export default App;