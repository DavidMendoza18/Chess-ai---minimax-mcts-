# Provenance and scope

## Original material

The five Python source files and the `resultados_20/` directory were taken from David Mendoza's uploaded `chess_results_David.zip`. Their bytes are preserved in this portfolio. That archive contains 60 search logs and one MCTS verification log. Six earlier uploaded logs are retained under `archive/early_runs/`; its README records the original-to-archived filename mapping.

The course supplied the chess positions. `posiciones.py` is the operational FEN source used for this analysis; portfolio preparation did not independently compare all boards with the source PDF. Position names, including under-promotion labels, are preserved as supplied and do not prove that an under-promotion is necessary.

No classmate's data, code, images, reports, timing statistics or experimental claims are included. This is a personal portfolio, not the official group poster.

## New portfolio preparation

On November 19, 2026, the archived results were organized into a README, CSV, charts, annotated boards and a consolidated PDF with AI assistance. The new build script checks all recorded FENs against `posiciones.py`, parses all 60 selected moves as legal, matches the MCTS verification records, and replays all 20 alpha-beta example lines to checkmate. The derived validation record is `data/validation.json`.

These are preparation-time consistency checks, not new historical timing runs. Source hashes are in `data/source_hashes.json`. No forced-mate uniqueness audit, independent-engine comparison, new multi-seed study, or equal-time experiment was performed.

The report source is the Python script `scripts/build_portfolio.py`; the new consolidated PDF is generated with ReportLab, not LaTeX. No claim is made that this new report was submitted during the course.

## Tools and assistance

David ran the experiments in Python using WSL Ubuntu. AI assistance was used for code development, explanations, troubleshooting, and preparation of the portfolio documentation and graphics. `python-chess` provides board representation and legal move generation. Matplotlib creates plots, `python-chess` creates SVG board drawings, CairoSVG renders them, and ReportLab produces the PDF.

The requirement pins describe packages used in portfolio preparation. They are not a recovered original experiment lockfile. The original logs do not identify the CPU, operating-system version, Python version or package versions.

## Limits of the findings

- One recorded run per method and tactical position; MCTS seed 42 only.
- Different depths and computational budgets; no controlled pruning-speedup result.
- Material-only evaluation at cutoff and random MCTS rollouts.
- The verifier shares alpha-beta code and chess legality with the search programs.
- One mating line does not demonstrate every defense; the logs' force claims come from the search implementation.
- No proof of unique keys, minimum mate distance, or general playing strength.
- Earlier three-board runs are separate and do not isolate the effect of piece count.
- An unsuccessful short-mate check does not establish that a move loses the game.
