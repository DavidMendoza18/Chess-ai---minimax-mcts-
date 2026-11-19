# The Evergreen Game: three checking moves

**Position 2 · White to move · 21 pieces**

```text
1r4r1/pbpknp1p/1b3P2/8/8/B1PB1q2/P4PPP/3R2K1 w - - 0 1
```

![Three recorded first moves](../figures/evergreen_comparison.png)

Left to right: Minimax **Be2+**, alpha-beta **Bf5+**, MCTS **Ba6+**.

| Configuration | Move | Archived seconds | Evidence |
|---|---|---:|---|
| Minimax, depth 3 | Be2+ | 0.8258 | Evaluation -6 |
| Alpha-beta, depth 5 | Bf5+ | 0.1627 | Evaluation 10000; reported forced mate |
| MCTS, 1,000 simulations, seed 42 | Ba6+ | 4.2119 | Archived verifier: no forced mate within five total plies |

These times come from `resultados_20/`, not from later individual reruns.

## A recorded continuation

**1. Bf5+ Ke8 2. Bd7+ Kf8 3. Bxe7#**

The bishop starts on d3 and moves to f5. The subsequent recorded continuation ends in checkmate after White's third move. It spans five plies. Portfolio preparation replayed this line legally to checkmate, but replaying one line alone does not prove the result against every defense; the force claim is the alpha-beta search's reported result.

## What I learned

Checking the king is not the same as preserving a forced mate. The five-ply search can reach the end of this continuation; the three-ply search cannot. MCTS uses sampled rollouts and selects the most visited root child, so its choice is not an exhaustive tactical proof.

The stored outputs show different decisions, but contain no root visit counts or rollout trace. A precise explanation for MCTS's preference for Ba6+ would require additional instrumentation and a new experiment.

## Source records

- [Minimax](../resultados_20/minimax_posicion_2.txt)
- [Alpha-beta](../resultados_20/minimax_ab_posicion_2_depth5.txt)
- [MCTS](../resultados_20/mcts_posicion_2.txt)
- [MCTS verification](../resultados_20/verificacion_mcts.txt)
