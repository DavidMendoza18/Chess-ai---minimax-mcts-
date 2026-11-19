# Chess AI · From checking moves to forced mate

**David Mendoza · University of Illinois Chicago · Fall 2026**

I explored how Minimax, alpha-beta pruning, and Monte Carlo Tree Search (MCTS) choose moves on 20 course-provided chess positions. This repository brings together my Python programs, original experiment logs, and analysis of their decisions and execution times.

The main question: **when does a search find a move that preserves a short forced mate, rather than simply giving check or gaining material?**

[**Read the report**](reports/Chess_Search_Report.pdf) · [**All 20 results**](docs/results.md) · [**Download CSV**](data/summary.csv) · [**Evergreen case study**](docs/evergreen.md)

## Where to start

| What to explore | Location |
|---|---|
| Overview, methods, results and limitations | [Four-page report](reports/Chess_Search_Report.pdf) |
| Every recorded move and search time | [Comparison table](docs/results.md) |
| Annotated Evergreen position | [Case study](docs/evergreen.md) |
| Original outputs from the 20 positions | [Raw logs](resultados_20/) |
| Earlier 4-, 10- and 32-piece board tests | [Earlier runs](archive/early_runs/) |
| How the algorithms work | [Methods](docs/methods.md) |
| Sources and preparation checks | [Provenance](docs/provenance.md) |

## 1. How long did each search take?

The archive contains 60 completed search outputs: one run of each configuration on each of 20 positions.

| Method | Configuration | Completed logs | Median seconds | Range, seconds |
|---|---|---:|---:|---:|
| Minimax | 3 plies | 20/20 | 0.3011 | 0.0146–1.8415 |
| Minimax with alpha-beta | 5 plies; 60-second limit | 20/20 | 0.2562 | 0.0593–1.2808 |
| MCTS | 1,000 simulations; rollout cap 80 plies; seed 42 | 20/20 | 3.8040 | 3.0611–5.1820 |

![Archived execution times for all 20 positions](figures/runtime.png)

![Median times for the three configurations](figures/median_times.png)

Alpha-beta had a lower median recorded time than plain Minimax in these runs, despite its deeper horizon. However, the programs differ in depth and move ordering as well as pruning. This is **not an equal-budget comparison or a controlled measurement of pruning speedup**. These are single-run observations, not repeated-trial estimates.

### Earlier exploration: boards with different piece counts

| Pieces | Minimax depth 4: move / seconds | MCTS 1,000 simulations: move / seconds |
|---|---|---|
| 4 | Kf2 / 0.1280 | Kf2 / 3.1625 |
| 10 | Ke2 / 0.2049 | Ke2 / 4.3022 |
| 32 | Nh3 / 4.1861 | a4 / 5.6592 |

These [six earlier logs](archive/early_runs/) are kept separate from the tactical-position dataset. Their MCTS rollout limit was 80 plies; the seed and exact early code version were not recorded. Since the boards differ, these observations do not isolate the effect of piece count.

## 2. Which selections preserved a short forced mate?

The criterion here is a forced mate **within five total plies**, including the selected first move. One ply is one move by one player. With the attacker moving first, five plies allow three attacking moves and two defensive replies.

| Evidence | Recorded result |
|---|---|
| Alpha-beta, depth 5 | All 20 search logs report a forced mate |
| MCTS selections checked by the archived verifier | 2/20 preserve a forced mate within five plies |
| MCTS successes | Position 15: Rxa8; position 20: c8=Q+ |
| Inconclusive MCTS verifications | 0 |
| Plain Minimax first moves matching the alpha-beta selection | 6/20; move agreement, not a separate mate-success rate |

The [verification script](verificar_mcts.py) plays each recorded MCTS move and searches four more plies with the alpha-beta implementation. It checks the result against the attacking side's terminal winning score. It therefore shares both the search implementation and `python-chess` with the other programs; it is **not an independent engine check**.

A NO result means that the verifier did not find a forced mate within this horizon. It does not establish that the move loses the game. No claim is made that every solution is unique or that five plies is the shortest possible mate.

[Read the full table](docs/results.md) · [Original verification output](resultados_20/verificacion_mcts.txt)

## 3. Case study: The Evergreen Game

Position 2 was my favorite position to investigate. White is to move.

![Evergreen: Minimax, alpha-beta, and MCTS recorded moves](figures/evergreen_comparison.png)

**Left:** Minimax, Be2+. **Center:** alpha-beta, Bf5+. **Right:** MCTS, Ba6+.

| Method | Selected move | Archived search time |
|---|---|---:|
| Minimax, depth 3 | Be2+ | 0.8258 s |
| Alpha-beta, depth 5 | Bf5+ | 0.1627 s |
| MCTS, 1,000 simulations | Ba6+ | 4.2119 s |

One recorded mating continuation is:

**1. Bf5+ Ke8 2. Bd7+ Kf8 3. Bxe7#**

The alpha-beta search reported a forced mate. The archived verifier reports that Ba6+ does not preserve mate within five plies. All three selected moves give check, but that alone does not guarantee a short forced mate.

Depth-three search cannot see the final position of the five-ply continuation above. MCTS samples random continuations rather than exhaustively checking every defense. These are relevant algorithmic differences, but the saved logs do not contain the root visit counts or rollout traces needed to explain precisely why MCTS preferred Ba6+.

[Read the case study and FEN](docs/evergreen.md)

## Run the programs

Download this repository with **Code → Download ZIP**, extract it, and open a terminal in the extracted project folder. Use **Python 3.9 or newer** (the verifier uses `str.removeprefix`).

Create an environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on Linux / WSL / macOS:

```bash
source .venv/bin/activate
```

Install the chess dependency:

```bash
python -m pip install -r requirements.txt
```

Run from the repository root:

```bash
python posiciones.py
python minimax.py --position 2 --depth 3
python minimax_ab.py --position 2 --depth 5 --seconds 60
python mcts.py --position 2 --simulations 1000 --rollout 80 --seed 42
python verificar_mcts.py
```

Change the position number to any integer from 1 to 20. The verifier expects `resultados_20/` in the working directory. If alpha-beta reaches its deadline, it reports an inconclusive result rather than a completed depth-five answer.

### Rebuild the portfolio figures and report

The following optional command parses the existing logs; it does **not** rerun the timed searches. Use Python 3.10+ and a system Cairo installation for this report-building environment. A PDF and figures are already included, so this step is not required to read the project.

```bash
python -m pip install -r requirements-report.txt
python scripts/build_portfolio.py
```

It regenerates the CSV, statistics, graphics, PDF, hashes and validation record. It also checks FEN consistency and legal selected moves for 60 logs and replays all 20 alpha-beta example lines to checkmate. Those checks were added during portfolio preparation and do not replace exhaustive defensive verification.

The dependency pins describe the portfolio-preparation environment, not the unrecorded original experiment environment. Execution times vary by machine and run.

## Repository map

| Path | Contents |
|---|---|
| `posiciones.py` | 20 FENs, board validation and material evaluation |
| `minimax.py` | Plain recursive Minimax |
| `minimax_ab.py` | Alpha-beta search, move ordering and deadline |
| `mcts.py` | UCT selection, rollout simulation and backpropagation |
| `verificar_mcts.py` | Bounded-mate verification of archived MCTS selections |
| `resultados_20/` | Original 60 search logs and MCTS verification output |
| `archive/early_runs/` | Six original board-size experiment logs |
| `data/` | Derived CSV, statistics, source hashes and validation record |
| `figures/` | Charts and annotated boards; SVG versions where available |
| `docs/` | Detailed results, methods, case study and provenance |
| `reports/` | Consolidated PDF report |
| `scripts/` | Script to rebuild the derived portfolio artifacts |

## Scope and acknowledgments

This is a personal record of my chess AI work at UIC. The positions were provided through the course. I used Python and `python-chess`, with AI assistance during code development, troubleshooting and documentation. I ran the original experiments using WSL Ubuntu.

The portfolio documents my work; it does not claim inclusion in the final group poster. The original logs are preserved, and the tables and charts are derived from those records. [Full provenance and limitations](docs/provenance.md).
