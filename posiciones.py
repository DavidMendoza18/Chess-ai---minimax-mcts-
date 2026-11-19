import chess


POSITIONS = {
    1: (
        "The Immortal Game",
        "r1b1k1nr/p2p1ppp/n2B4/1p1NPN1P/6P1/3P1Q2/P1P1K3/q5b1 w - - 0 1",
    ),
    2: (
        "The Evergreen Game",
        "1r4r1/pbpknp1p/1b3P2/8/8/B1PB1q2/P4PPP/3R2K1 w - - 0 1",
    ),
    3: (
        "The Game of the Century",
        "1Q6/5pk1/2p3p1/1p2N2p/1b5P/1b4n1/r5P1/2K5 b - - 0 1",
    ),
    4: (
        "Reti's Mate",
        "rnb1kb1r/pp3ppp/2p5/4q3/4n3/3Q4/PPPB1PPP/2KR1BNR w - - 0 1",
    ),
    5: (
        "Loyd's Charles XII Problem",
        "8/6R1/7p/5K1k/8/6p1/5bPP/4N3 w - - 0 1",
    ),
    6: (
        "Back-Rank Mate: Queen Sacrifices",
        "7k/3Q2pp/4r3/8/8/8/3r3P/6K1 w - - 0 1",
    ),
    7: (
        "Back-Rank Mate: Quiet Knight Move",
        "6rk/6pp/8/8/8/3Q3N/8/4R2K w - - 0 1",
    ),
    8: (
        "Queen Sacrifice and Knight Support",
        "2N3rk/5Qpp/8/8/8/8/5R2/2K5 w - - 0 1",
    ),
    9: (
        "Rook Sacrifice: Queen on the Long Diagonal",
        "1R4rk/3N2pp/7Q/8/8/8/8/6K1 w - - 0 1",
    ),
    10: (
        "Rook Sacrifice: Queen and Knight Mate",
        "4R3/6pk/3Q4/5N2/2p5/8/7p/1K6 w - - 0 1",
    ),
    11: (
        "Anastasia's Mate",
        "1rN3k1/5pp1/8/4Q3/1q1R4/8/5PP1/6K1 w - - 0 1",
    ),
    12: (
        "Arabian Mate",
        "6N1/Q4Rpk/8/8/8/6n1/8/K7 w - - 0 1",
    ),
    13: (
        "Arabian Mate: Rook Lift",
        "2n4k/3R4/3p4/8/4N3/8/8/3nK3 w - - 0 1",
    ),
    14: (
        "Smothered Mate",
        "6rk/6pp/7P/1N2Q3/6pb/8/8/6K1 w - - 0 1",
    ),
    15: (
        "Double-Check Mate",
        "r2B2k1/5ppp/8/5Q2/8/R7/5PPP/6K1 w - - 0 1",
    ),
    16: (
        "Promotion Mate",
        "7k/1P6/6p1/8/8/6K1/8/5R2 w - - 0 1",
    ),
    17: (
        "Double Promotion",
        "6k1/P2P4/5R2/6b1/8/8/6K1/8 w - - 0 1",
    ),
    18: (
        "Under-Promotion to a Rook",
        "3Nk3/2P3b1/8/8/8/8/8/K5R1 w - - 0 1",
    ),
    19: (
        "Under-Promotion to a Bishop",
        "8/n5kP/3P4/8/2Q5/5K2/8/8 w - - 0 1",
    ),
    20: (
        "Promotion, Sacrifice and Queen-and-Pawn Mate",
        "7k/b1Pn4/R6P/8/8/6K1/8/8 w - - 0 1",
    ),
}


def load_position(number):
    name, fen = POSITIONS[number]
    board = chess.Board(fen)

    if not board.is_valid():
        raise ValueError(
            f"Invalid position: {number}. Check the PDF diagram and FEN."
        )

    return name, board


def evaluate(board):
    values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
    }

    score = 0

    for piece_type, value in values.items():
        white = len(board.pieces(piece_type, chess.WHITE))
        black = len(board.pieces(piece_type, chess.BLACK))
        score += (white - black) * value

    return score


def show_position(number, name, board):
    print(f"Position: {number} - {name}", flush=True)
    print("FEN:", board.fen(), flush=True)
    print("Pieces:", len(board.piece_map()), flush=True)
    print("Turn:", "White" if board.turn else "Black", flush=True)
    print(board, flush=True)


if __name__ == "__main__":
    # Revisar la validez básica de las 20 posiciones.
    for number, (name, fen) in POSITIONS.items():
        board = chess.Board(fen)
        status = "OK" if board.is_valid() else "CHECK POSITION"

        print(
            f"{number:02d}. {name} | "
            f"Pieces: {len(board.piece_map())} | {status}"
        )