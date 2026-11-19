# Methods

## Board representation and evaluation

`posiciones.py` stores 20 FEN positions. `chess.Board.is_valid()` checks basic board consistency, not historical authenticity or agreement with the printed course diagrams. Position 3 has Black to move; the other positions have White to move.

Material evaluation is White's material minus Black's: pawn 1, knight 3, bishop 3, rook 5, queen 9. Kings have no material term. Terminal outcomes are checked before the depth cutoff: White win +10000, Black win -10000, draw 0.

## Plain Minimax

White maximizes and Black minimizes. The recursion tries legal moves, pushes each move, searches one ply deeper, and pops it in a finally block. At depth zero it uses material evaluation. Ties retain the first encountered move. Archived tactical runs use depth 3. There is no built-in time budget in this implementation.

## Alpha-beta

The recursion maintains alpha and beta bounds. A branch is cut when alpha reaches or exceeds beta. Legal moves are sorted by whether they give check, capture, and promote, in that priority order. Every call checks the deadline. Archived runs use depth 5 and a 60-second deadline, and all have completed outputs.

The program returns a score and an example principal line. Terminal mate values do not encode distance, so the search does not promise the shortest mate. A printed example line is not itself a certificate covering every possible defense.

## MCTS

The tree stores visits and accumulated rewards. UCT selection uses average reward plus `sqrt(2 * log(parent_visits) / child_visits)`. Expansion randomly chooses an untried move. Rollouts choose random legal moves for at most 80 plies.

Terminal rollout rewards from White's perspective are 1 for a White win, 0 for a Black win and 0.5 for a draw. A nonterminal cutoff gets `0.5 + 0.5 * tanh(material / 10)`. Backpropagation converts this to the previous mover's perspective at each node. The final selection is the root child with the most visits.

Each recorded tactical run uses 1,000 simulations and seed 42. The same seed is reset for each invocation. These are not repeated-seed experiments.

## Archived MCTS verification

For each position, the script reads the saved FEN and SAN move, requires a matching FEN, and checks move legality. It plays the selected move and invokes the same alpha-beta search for four additional plies, with a 60-second deadline. It compares the returned score with the attacking side's winning score. Missing, mismatched, invalid or timed-out records are inconclusive.

The archived summary reports 20 checked, 2 successes, 18 failures within the horizon, and zero unverified positions. Reusing alpha-beta means the verifier is not independent of the search code.

## Interpretation

A mate-preserving move is not necessarily a unique key. A failed bounded-mate check does not imply a lost game. Six plain-Minimax selections match the corresponding alpha-beta selections, but this agreement is not a complete independent accuracy measure. No causal claim about material bias or root visit counts is made without the relevant diagnostic data.
