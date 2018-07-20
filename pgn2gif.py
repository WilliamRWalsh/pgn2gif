import glob
import imageio
from PIL import Image
import numpy as np
import re

# Init. Variables #
WS_img = Image.open('images/WhiteSquare.png')
WK_img = Image.open('images/WhiteKing.png')
WQ_img = Image.open('images/WhiteQueen.png')
WR_img = Image.open('images/WhiteRook.png')
WB_img = Image.open('images/WhiteBishop.png')
WN_img = Image.open('images/WhiteKnight.png')
WP_img = Image.open('images/WhitePawn.png')

BS_img = Image.open('images/BlackSquare.png')
BK_img = Image.open('images/BlackKing.png')
BQ_img = Image.open('images/BlackQueen.png')
BR_img = Image.open('images/BlackRook.png')
BB_img = Image.open('images/BlackBishop.png')
BN_img = Image.open('images/BlackKnight.png')
BP_img = Image.open('images/BlackPawn.png')

PIECES2IMAGES = {'WK': WK_img, 'BK': BK_img, 'WQ': WQ_img, 'BQ': BQ_img, 'WR': WR_img, 'BR': BR_img,
                'WB': WB_img, 'BB': BB_img, 'WN': WN_img, 'BN': BN_img, 'WP': WP_img, 'BP': BP_img}

FILE2PIXEL = {'a': 0, 'b': 64, 'c': 128, 'd': 192, 'e': 256, 'f': 320, 'g': 384, 'h': 448}
RANK2PIXEL = {'8': 0, '7': 64, '6': 128, '5': 192, '4': 256, '3': 320, '2': 384, '1': 448}
# End Init. Variables #


def add_to_file(file, value):
    return chr(ord(file) + value)


def isSquareWhite(square):
    diff = FILE2PIXEL[square[0]] - RANK2PIXEL[square[1]]
    return True if abs(diff/64) % 2 == 0 else False


def find_bishop(destination, piece):
    # if isSquareWhite(destination)
    for square, p in game_state.items():
        if p == piece and isSquareWhite(destination) == isSquareWhite(square):
            return square


def find_knight(destination, piece, distinction):
    file = destination[0]
    rank = destination[1]

    try:
        source = add_to_file(file, 1) + str(int(rank)+2)
        if game_state[source] == piece and (distinction is None or distinction in source):
            return source
    except KeyError:
            pass
    try:
        source = add_to_file(file, -1) + str(int(rank)+2)
        if game_state[source] == piece and (distinction is None or distinction in source):
            return source
    except KeyError:
            pass
    try:
        source = add_to_file(file, 2) + str(int(rank)+1)
        if game_state[source] == piece and (distinction is None or distinction in source):
            return source
    except KeyError:
            pass
    try:
        source = add_to_file(file, 2) + str(int(rank)-1)
        if game_state[source] == piece and (distinction is None or distinction in source):
            return source
    except KeyError:
            pass
    try:
        source = add_to_file(file, -2) + str(int(rank)+1)
        if game_state[source] == piece and (distinction is None or distinction in source):
            return source
    except KeyError:
            pass
    try:
        source = add_to_file(file, -2) + str(int(rank)-1)
        if game_state[source] == piece and (distinction is None or distinction in source):
            return source
    except KeyError:
            pass
    try:
        source = add_to_file(file, 1) + str(int(rank)-2)
        if game_state[source] == piece and (distinction is None or distinction in source):
            return source
    except KeyError:
            pass
    try:
        source = add_to_file(file, -1) + str(int(rank)-2)
        if game_state[source] == piece and (distinction is None or distinction in source):
            return source
    except KeyError:
            pass


def get_moves(pgn):
    pgn_lines = open(pgn, "r")

    for line in pgn_lines:
        if line.startswith("1."):
            move_line = re.sub("\d+\.\s?", "", line)
            move_line = re.sub("\+|\#", "", move_line)
            break

    return move_line.split()


def check_squares(destination, piece, directions, inc):
    file = destination[0]
    rank = destination[1]
    for index, direction in enumerate(directions):
        if direction == 0:
            continue

        if index == 0:  # up
            try:
                p = game_state[add_to_file(file, 0) + str(int(rank) + inc)]
            except KeyError:
                directions[index] = 0
                continue
            if p == piece:
                return add_to_file(file, 0) + str(int(rank)+inc)
            elif p != "":
                directions[index] = 0
        elif index == 1:  # up-right
            try:
                p = game_state[add_to_file(file, inc) + str(int(rank) + inc)]
            except KeyError:
                directions[index] = 0
                continue
            if p == piece:
                return add_to_file(file, inc) + str(int(rank) + inc)
            elif p != "":
                directions[index] = 0
        elif index == 2:  # right
            try:
                p = game_state[add_to_file(file, inc) + str(int(rank) + 0)]
            except KeyError:
                directions[index] = 0
                continue
            if p == piece:
                return add_to_file(file, inc) + str(int(rank) + 0)
            elif p != "":
                directions[index] = 0
        elif index == 3:  # down-right
            try:
                p = game_state[add_to_file(file, inc) + str(int(rank) + -inc)]
            except KeyError:
                directions[index] = 0
                continue
            if p == piece:
                return add_to_file(file, inc) + str(int(rank) + -inc)
            elif p != "":
                directions[index] = 0
        elif index == 4:  # down
            try:
                p = game_state[add_to_file(file, 0) + str(int(rank) + -inc)]
            except KeyError:
                directions[index] = 0
                continue
            if p == piece:
                return add_to_file(file, 0) + str(int(rank) + -inc)
            elif p != "":
                directions[index] = 0
        elif index == 5:  # down-left
            try:
                p = game_state[add_to_file(file, -inc) + str(int(rank) + -inc)]
            except KeyError:
                directions[index] = 0
                continue
            if p == piece:
                return add_to_file(file, -inc) + str(int(rank) + -inc)
            elif p != "":
                directions[index] = 0
        elif index == 6:  # left
            try:
                p = game_state[add_to_file(file, -inc) + str(int(rank) + 0)]
            except KeyError:
                directions[index] = 0
                continue
            if p == piece:
                return add_to_file(file, -inc) + str(int(rank) + 0)
            elif p != "":
                directions[index] = 0
        elif index == 7:  # left-up
            try:
                p = game_state[add_to_file(file, -inc) + str(int(rank) + inc)]
            except KeyError:
                directions[index] = 0
                continue
            if p == piece:
                return add_to_file(file, -inc) + str(int(rank) + inc)
            elif p != "":
                directions[index] = 0
    return None


def find_rook(destination, piece):
    # Clockwise (up first)
    directions = [1, 0, 1, 0, 1, 0, 1, 0]
    source = None
    inc = 1
    while source is None:
        source = check_squares(destination, piece, directions, inc)
        inc += 1
    return source


def find_king(destination, piece):
    # Clockwise (up first)
    directions = [1, 1, 1, 1, 1, 1, 1, 1]
    inc = 1
    source = check_squares(destination, piece, directions, inc)
    return source


def find_queen(destination, piece, distinction):
    # Clockwise (up first)
    directions = [1, 1, 1, 1, 1, 1, 1, 1]
    source = None
    inc = 1
    while source is None:
        source = check_squares(destination, piece, directions, inc)
        if distinction is not None and distinction not in source:
            source = None
        inc += 1
    return source


def find_pawn(destination, piece, isCapture):
    if isCapture:
        if piece[0] == 'B':
            # Clockwise (up first)
            directions = [0, 1, 0, 0, 0, 0, 0, 1]
        else:
            # Clockwise (up first)
            directions = [0, 0, 0, 1, 0, 1, 0, 0]

        # Checking en passant
        if game_state[destination] == '':
            file = destination[0]
            rank = destination[1]

            # Finding captured pawn
            if piece[0] == 'B':
                captured_pawn = file + str(int(rank) + 1)
            else:
                captured_pawn = file + str(int(rank) - 1)

            # Updating game board (img) and game state
            if isSquareWhite(captured_pawn):
                GameBoard_img.paste(WS_img, coord2pixel(captured_pawn))
            else:
                GameBoard_img.paste(BS_img, coord2pixel(captured_pawn))

            game_state[captured_pawn] = ''
    else:
        if piece[0] == 'B':
            # Clockwise (up first)
            directions = [1, 0, 0, 0, 0, 0, 0, 0]
        else:
            # Clockwise (up first)
            directions = [0, 0, 0, 0, 1, 0, 0, 0]

    source, inc = None, 1
    while source is None:
        source = check_squares(destination, piece, directions, inc)
        inc += 1

    return source


def next_move(move, blacks_turn):

    piece = source = destination = None

    if move[0].islower():  # Pawn
        piece = 'BP' if blacks_turn else 'WP'
        isCapture = True if move[1] == 'x' else False
        promote = move[-1] if move[-1].isupper() else ''

        if isCapture:
            destination = move[2:4]
        else:
            destination = move[0:2]

        source = find_pawn(destination, piece, isCapture)
        if promote != '':
            piece = piece[0] + promote

    elif move[0] == 'N':
        piece = 'BN' if blacks_turn else 'WN'
        destination = move[-2:]
        if (len(move) == 4 and move[1] != 'x') or len(move) == 5:
            distinction = move[1]
        else:
            distinction = None
        source = find_knight(destination, piece, distinction)
    elif move[0] == 'B':
        piece = 'BB' if blacks_turn else 'WB'
        destination = move[-2:]
        source = find_bishop(destination, piece)
    elif move == 'O-O':
        if blacks_turn:
            update_position('BK', 'e8', 'g8')
            update_position('BR', 'h8', 'f8')
        else:
            update_position('WK', 'e1', 'g1')
            update_position('WR', 'h1', 'f1')
        return
    elif move == 'O-O-O':
        if blacks_turn:
            update_position('BK', 'e8', 'c8')
            update_position('BR', 'a8', 'd8')
        else:
            update_position('WK', 'e1', 'c1')
            update_position('WR', 'a1', 'd1')
        return
    elif move[0] == 'Q':
        piece = 'BQ' if blacks_turn else 'WQ'
        destination = move[-2:]
        if (len(move) == 4 and move[1] != 'x') or len(move) == 5:
            distinction = move[1]
        else:
            distinction = None

        source = find_queen(destination, piece, distinction)
    elif move[0] == 'R':
        piece = 'BR' if blacks_turn else 'WR'
        destination = move[-2:]
        if (len(move) == 4 and move[1] != 'x') or len(move) == 5:
            if move[1].isdigit():
                source = move[-2] + move[1]
            else:
                source = move[1] + move[-1]
        else:
            source = find_rook(destination, piece)

    elif move[0] == 'K':
        piece = 'BK' if blacks_turn else 'WK'
        destination = move[-2:]
        source = find_king(destination, piece)

    update_position(piece, source, destination)


def coord2pixel(coord):
    return FILE2PIXEL[coord[0]], RANK2PIXEL[coord[1]]


def update_position(piece, source, destination):
    game_state[source] = ""
    game_state[destination] = piece

    if isSquareWhite(destination):
        GameBoard_img.paste(WS_img, coord2pixel(destination))
    else:
        GameBoard_img.paste(BS_img, coord2pixel(destination))

    GameBoard_img.paste(PIECES2IMAGES[piece], coord2pixel(destination), PIECES2IMAGES[piece])

    if isSquareWhite(source):
        GameBoard_img.paste(WS_img, coord2pixel(source))
    else:
        GameBoard_img.paste(BS_img, coord2pixel(source))


def create_gif(pgn):
    print("Creating gif for: " + pgn)

    global GameBoard_img
    GameBoard_img = Image.open('images/ChessBoard.png')

    global game_state
    game_state = {'a8': 'BR', 'b8': 'BN', 'c8': 'BB', 'd8': 'BQ', 'e8': 'BK', 'f8': 'BB', 'g8': 'BN', 'h8': 'BR',
                  'a7': 'BP', 'b7': 'BP', 'c7': 'BP', 'd7': 'BP', 'e7': 'BP', 'f7': 'BP', 'g7': 'BP', 'h7': 'BP',
                  'a6': '', 'b6': '', 'c6': '', 'd6': '', 'e6': '', 'f6': '', 'g6': '', 'h6': '',
                  'a5': '', 'b5': '', 'c5': '', 'd5': '', 'e5': '', 'f5': '', 'g5': '', 'h5': '',
                  'a4': '', 'b4': '', 'c4': '', 'd4': '', 'e4': '', 'f4': '', 'g4': '', 'h4': '',
                  'a3': '', 'b3': '', 'c3': '', 'd3': '', 'e3': '', 'f3': '', 'g3': '', 'h3': '',
                  'a2': 'WP', 'b2': 'WP', 'c2': 'WP', 'd2': 'WP', 'e2': 'WP', 'f2': 'WP', 'g2': 'WP', 'h2': 'WP',
                  'a1': 'WR', 'b1': 'WN', 'c1': 'WB', 'd1': 'WQ', 'e1': 'WK', 'f1': 'WB', 'g1': 'WN', 'h1': 'WR'}

    moves = get_moves(pgn)

    images = [np.array(GameBoard_img)]

    for i, move in enumerate(moves):
        next_move(move, i % 2)
        images.append(np.array(GameBoard_img))

    imageio.mimsave(pgn[:-3] + 'gif', images, duration=0.8)


if __name__ == '__main__':

    for pgn_file in glob.glob('*.pgn'):
        create_gif(pgn_file)
