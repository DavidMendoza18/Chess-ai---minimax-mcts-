import argparse
import time
import chess

from posiciones import POSITIONS, load_position, evaluate, show_position


def minimax(board, depth):
    outcome = board.outcome()

    if outcome is not None:
        if outcome.winner == chess.WHITE:
            return 10000, None
        if outcome.winner == chess.BLACK:
            return -10000, None
        return 0, None

    if depth == 0:
        return evaluate(board), None

    white_turn = board.turn == chess.WHITE
    best_score = float("-inf") if white_turn else float("inf")
    best_move = None

    for move in list(board.legal_moves):
        board.push(move)

        try:
            score, _ = minimax(board, depth - 1)
        finally:
            board.pop()

        if best_move is None or (
            white_turn and score > best_score
        ) or (
            not white_turn and score < best_score
        ):
            best_score = score
            best_move = move

    return best_score, best_move


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--position",
        type=int,
        choices=sorted(POSITIONS),
        required=True,
    )

    parser.add_argument("--depth", type=int, default=3)
    args = parser.parse_args()

    if args.depth < 1:
        parser.error("--depth must be at least 1")

    name, board = load_position(args.position)
    show_position(args.position, name, board)

    print("Algorithm: Minimax", flush=True)
    print("Depth (plies):", args.depth, flush=True)
    print("Searching... Please wait.", flush=True)

    start = time.perf_counter()

    try:
        score, move = minimax(board, args.depth)
    except KeyboardInterrupt:
        elapsed = time.perf_counter() - start
        print(f"\nInterrupted after {elapsed:.4f} seconds.")
        print("No completed result.")
        return

    elapsed = time.perf_counter() - start

    print("Selected move:", board.san(move) if move else "None")
    print("Evaluation:", score)
    print(f"Time: {elapsed:.4f} seconds")


if __name__ == "__main__":
    main()