import argparse
import time
import chess

from posiciones import POSITIONS, load_position, evaluate, show_position


def minimax_ab(board, depth, alpha, beta, deadline):
    if time.perf_counter() >= deadline:
        raise TimeoutError

    outcome = board.outcome()

    if outcome is not None:
        if outcome.winner == chess.WHITE:
            return 10000, []
        if outcome.winner == chess.BLACK:
            return -10000, []
        return 0, []

    if depth == 0:
        return evaluate(board), []

    white_turn = board.turn == chess.WHITE
    best_score = float("-inf") if white_turn else float("inf")
    best_line = []

    # Revisar primero jaques y capturas para ayudar a la poda.
    moves = sorted(
        board.legal_moves,
        key=lambda move: (
            board.gives_check(move),
            board.is_capture(move),
            bool(move.promotion),
        ),
        reverse=True,
    )

    for move in moves:
        board.push(move)

        try:
            score, line = minimax_ab(
                board, depth - 1, alpha, beta, deadline
            )
        finally:
            board.pop()

        if not best_line or (
            white_turn and score > best_score
        ) or (
            not white_turn and score < best_score
        ):
            best_score = score
            best_line = [move] + line

        if white_turn:
            alpha = max(alpha, best_score)
        else:
            beta = min(beta, best_score)

        if alpha >= beta:
            break

    return best_score, best_line


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--position",
        type=int,
        choices=sorted(POSITIONS),
        required=True,
    )
    parser.add_argument("--depth", type=int, default=5)
    parser.add_argument("--seconds", type=float, default=60)
    args = parser.parse_args()

    if args.depth < 1 or args.seconds <= 0:
        parser.error("Depth and time limit must be positive.")

    name, board = load_position(args.position)
    show_position(args.position, name, board)

    print("Algorithm: Minimax with alpha-beta", flush=True)
    print("Depth (plies):", args.depth, flush=True)
    print("Time limit:", args.seconds, "seconds", flush=True)
    print("Searching...", flush=True)

    start = time.perf_counter()
    deadline = start + args.seconds

    try:
        score, line = minimax_ab(
            board,
            args.depth,
            float("-inf"),
            float("inf"),
            deadline,
        )
    except (TimeoutError, KeyboardInterrupt):
        elapsed = time.perf_counter() - start
        print("Search stopped before completion.")
        print("Result: inconclusive.")
        print(f"Time: {elapsed:.4f} seconds")
        return

    elapsed = time.perf_counter() - start

    print("Selected move:", board.san(line[0]) if line else "None")
    print("Evaluation:", score)

    winning_score = 10000 if board.turn == chess.WHITE else -10000
    print(
        "Forced mate within search depth:",
        "YES" if score == winning_score else "NOT FOUND",
    )

    replay = board.copy()
    moves_text = []

    for move in line:
        moves_text.append(replay.san(move))
        replay.push(move)

    print("Example line:", " ".join(moves_text))
    print(f"Time: {elapsed:.4f} seconds")


if __name__ == "__main__":
    main()