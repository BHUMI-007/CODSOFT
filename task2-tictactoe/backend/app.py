from flask import Flask, request, jsonify
from flask_cors import CORS
from game import create_board, check_winner, is_draw, make_move
from minimax import best_move

app = Flask(__name__)
CORS(app)  # React se connection allow karna

board = create_board()

@app.route("/state", methods=["GET"])
def get_state():
    return jsonify({"board": board})

@app.route("/move", methods=["POST"])
def human_move():
    global board
    data = request.get_json()
    row, col = data["row"], data["col"]

    if not make_move(board, row, col, "X"):
        return jsonify({"error": "Invalid move"}), 400

    if check_winner(board, "X"):
        return jsonify({"board": board, "status": "human_wins"})
    if is_draw(board):
        return jsonify({"board": board, "status": "draw"})

    # AI turn
    move = best_move(board)
    if move:
        make_move(board, move[0], move[1], "O")

    if check_winner(board, "O"):
        return jsonify({"board": board, "status": "ai_wins"})
    if is_draw(board):
        return jsonify({"board": board, "status": "draw"})

    return jsonify({"board": board, "status": "ongoing"})

@app.route("/reset", methods=["POST"])
def reset():
    global board
    board = create_board()
    return jsonify({"board": board, "status": "ongoing"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
