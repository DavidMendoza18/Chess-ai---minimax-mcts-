import argparse
import math
import random
import time
import chess

from posiciones import POSITIONS, load_position, evaluate, show_position


class MCTS:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = []
        self.untried_moves = list(board.legal_moves)
        self.visits = 0
        self.total_reward = 0.0
        self.player = not board.turn

    def expand(self):
        move = random.choice(self.untried_moves)
        self.untried_moves.remove(move)

        next_board = self.board.copy()
        next_board.push(move)

        child = MCTS(next_board, parent=self, move=move)
        self.children.append(child)
        return child

    def best_child(self):
        def uct(child):
            average = child.total_reward / child.visits
            exploration = math.sqrt(
                2 * math.log(self.visits) / child.visits
            )
            return average + exploration

        return max(self.children, key=uct)

    def select(self):
        node = self

        while not node.board.is_game_over():
            if node.untried_moves:
                return node.expand()

            node = node.best_child()

        return node

    def simulate(self, max_moves):
        board = self.board.copy()

        for _ in range(max_moves):
            if board.is_game_over():
                break

            move = random.choice(list(board.legal_moves))
            board.push(move)

        outcome = board.outcome()

        if outcome is not None:
            if outcome.winner == chess.WHITE:
                return 1.0
            if outcome.winner == chess.BLACK:
                return 0.0
            return 0.5

        return 0.5 + 0.5 * math.tanh(evaluate(board) / 10)

    def backpropagate(self, white_reward):
        node = self

        while node is not None:
            node.visits += 1

            if node.player == chess.WHITE:
                node.total_reward += white_reward
            else:
                node.total_reward += 1 - white_reward

            node = node.parent

    def best_action(self, simulations, max_moves):
        if self.board.is_game_over():
            return None

        for _ in range(simulations):
            node = self.select()
            reward = node.simulate(max_moves)
            node.backpropagate(reward)

        best = max(self.children, key=lambda child: child.visits)
        return best.move


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--position",
        type=int,
        choices=sorted(POSITIONS),
        required=True,
    )

    parser.add_argument("--simulations", type=int, default=1000)
    parser.add_argument("--rollout", type=int, default=80)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.simulations < 1 or args.rollout < 1:
        parser.error("--simulations and --rollout must be at least 1")

    random.seed(args.seed)

    name, board = load_position(args.position)
    show_position(args.position, name, board)

    print("Algorithm: MCTS", flush=True)
    print("Simulations:", args.simulations, flush=True)
    print("Rollout limit (plies):", args.rollout, flush=True)
    print("Seed:", args.seed, flush=True)
    print("Searching... Please wait.", flush=True)

    start = time.perf_counter()

    try:
        root = MCTS(board)
        move = root.best_action(args.simulations, args.rollout)
    except KeyboardInterrupt:
        elapsed = time.perf_counter() - start
        print(f"\nInterrupted after {elapsed:.4f} seconds.")
        print("No completed result.")
        return

    elapsed = time.perf_counter() - start

    print("Selected move:", board.san(move) if move else "None")
    print(f"Time: {elapsed:.4f} seconds")


if __name__ == "__main__":
    main()