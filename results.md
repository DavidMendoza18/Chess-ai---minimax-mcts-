# Results across 20 positions

Source: the original logs in [`resultados_20`](../resultados_20/). One recorded run per algorithm per position. Alpha-beta reported a forced mate in all 20 runs. The final column comes from the archived MCTS verification log.

| # | Position | Minimax d3 | Seconds | Alpha-beta d5 | Seconds | MCTS | Seconds | MCTS mate ≤5 plies |
|---|---|---|---:|---|---:|---|---:|---|
| 1 | The Immortal Game | Nf4 | 1.0802 | Nxg7+ | 0.2574 | Qf2 | 4.9363 | NO |
| 2 | The Evergreen Game | Be2+ | 0.8258 | Bf5+ | 0.1627 | Ba6+ | 4.2119 | NO |
| 3 | The Game of the Century | Bc3 | 0.6602 | Ne2+ | 0.1285 | Rxg2 | 4.3588 | NO |
| 4 | Reti's Mate | Qe3 | 1.8415 | Qd8+ | 0.1693 | Qa6 | 5.1820 | NO |
| 5 | Loyd's Charles XII Problem | Nf3 | 0.1247 | Rxg3 | 0.3399 | hxg3 | 3.7008 | NO |
| 6 | Back-Rank Mate: Queen Sacrifices | Qc8+ | 0.2997 | Qc8+ | 0.0606 | Qxd2 | 3.4672 | NO |
| 7 | Back-Rank Mate: Quiet Knight Move | Ng5 | 0.4091 | Ng5 | 1.0778 | Re7 | 3.7561 | NO |
| 8 | Queen Sacrifice and Knight Support | Qf8 | 0.3024 | Qxg8+ | 0.2162 | Ne7 | 4.0115 | NO |
| 9 | Rook Sacrifice: Queen on the Long Diagonal | Qd6 | 0.2976 | Rxg8+ | 0.3616 | Qh2 | 3.7961 | NO |
| 10 | Rook Sacrifice: Queen and Knight Mate | Qxh2+ | 0.3757 | Rh8+ | 0.3077 | Kb2 | 3.8672 | NO |
| 11 | Anastasia's Mate | Qe8+ | 1.2892 | Rd8+ | 0.2305 | Qe2 | 4.6764 | NO |
| 12 | Arabian Mate | Ne7 | 0.2784 | Rxg7+ | 1.2808 | Rb7 | 4.2195 | NO |
| 13 | Arabian Mate: Rook Lift | Kxd1 | 0.1122 | Nf6 | 0.2550 | Nxd6 | 3.8119 | NO |
| 14 | Smothered Mate | hxg7+ | 0.3717 | Nd6 | 0.2404 | Na3 | 3.8222 | NO |
| 15 | Double-Check Mate | Rxa8 | 0.8039 | Rxa8 | 0.7272 | Rxa8 | 3.0611 | YES |
| 16 | Promotion Mate | Kg4 | 0.0366 | Rf7 | 0.5852 | Rh1+ | 3.0614 | NO |
| 17 | Double Promotion | d8=Q+ | 0.2206 | d8=Q+ | 0.5517 | Ra6 | 3.6060 | NO |
| 18 | Under-Promotion to a Rook | Rxg7 | 0.0146 | Rxg7 | 0.0593 | Kb1 | 3.4939 | NO |
| 19 | Under-Promotion to a Bishop | Qg8+ | 0.2347 | Qg8+ | 1.1341 | Qe2 | 3.1981 | NO |
| 20 | Promotion, Sacrifice and Queen-and-Pawn Mate | Rxa7 | 0.1890 | c8=Q+ | 0.1696 | c8=Q+ | 3.5993 | YES |

A NO means no forced mate within the five-ply horizon under the verifier, not necessarily a losing move. No unique-key or shortest-mate claim is made.

[Download the full CSV](../data/summary.csv)
