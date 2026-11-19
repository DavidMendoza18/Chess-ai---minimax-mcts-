import time
from pathlib import Path

import chess

from posiciones import POSITIONS, load_position
from minimax_ab import minimax_ab


def main():
    correct = 0
    checked = 0
    inconclusive = 0

    for number in sorted(POSITIONS):
        name, board = load_position(number)

        path = Path("resultados_20") / f"mcts_posicion_{number}.txt"

        print(f"\nPosition: {number} - {name}", flush=True)

        if not path.exists():
            print("Result: missing MCTS result file.", flush=True)
            inconclusive += 1
            continue

        text = path.read_text(encoding="utf-8")

        recorded_fen = next(
            (
                line.removeprefix("FEN:").strip()
                for line in text.splitlines()
                if line.startswith("FEN:")
            ),
            None,
        )

        if recorded_fen != board.fen():
            print("Result: FEN does not match.", flush=True)
            inconclusive += 1
            continue

        selected = next(
            (
                line.removeprefix("Selected move:").strip()
                for line in text.splitlines()
                if line.startswith("Selected move:")
            ),
            None,
        )

        if selected is None:
            print("Result: no recorded move.", flush=True)
            inconclusive += 1
            continue

        try:
            move = board.parse_san(selected)
        except ValueError:
            print("Result: invalid recorded move.", flush=True)
            inconclusive += 1
            continue

        print("MCTS move:", selected, flush=True)

        attacker = board.turn
        board.push(move)

        start = time.perf_counter()

        try:
            score, _ = minimax_ab(
                board,
                4,
                float("-inf"),
                float("inf"),
                start + 60,
            )
        except TimeoutError:
            print("Result: inconclusive (time limit).", flush=True)
            inconclusive += 1
            continue

        target = 10000 if attacker == chess.WHITE else -10000
        success = score == target

        checked += 1
        correct += int(success)

        print(
            "Forces mate within 3 moves:",
            "YES" if success else "NO",
            flush=True,
        )
        print(
            f"Verification time: {time.perf_counter() - start:.4f} seconds",
            flush=True,
        )

    print("\nSUMMARY", flush=True)
    print("Positions checked:", checked, flush=True)
    print("MCTS moves that force mate within 3:", correct, flush=True)
    print("MCTS moves that do not:", checked - correct, flush=True)
    print("Unverified positions:", inconclusive, flush=True)


if __name__ == "__main__":
    main()