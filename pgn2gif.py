import glob
import imageio
from PIL import Image
import numpy as np
import re

# Init. Variables #
# This image will be updated
GameBoard_img = Image.open('images/ChessBoard.png')

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
FILE2X = {'a': 0, 'b': 64, 'c': 128, 'd': 192, 'e': 256, 'f': 320, 'g': 384, 'h': 448}
RANK2Y = {'8': 0, '7': 64, '6': 128, '5': 192, '4': 256, '3': 320, '2': 384, '1': 448}

game_state = {'a8':'BR', 'b8': 'BN', 'c8': 'BB', 'd8': 'BQ', 'e8': 'BK', 'f8': 'BB', 'g8': 'BN', 'h8': 'BR',
              'a7':'BP', 'b7': 'BP', 'c7': 'BP', 'd7': 'BP', 'e7': 'BP', 'f7': 'BP', 'g7': 'BP', 'h7': 'BP',
              'a6':'', 'b6': '', 'c6': '', 'd6': '', 'e6': '', 'f6': '', 'g6': '', 'h6': '',
              'a5':'', 'b5': '', 'c5': '', 'd5': '', 'e5': '', 'f5': '', 'g5': '', 'h5': '',
              'a4':'', 'b4': '', 'c4': '', 'd4': '', 'e4': '', 'f4': '', 'g4': '', 'h4': '',
              'a3':'', 'b3': '', 'c3': '', 'd3': '', 'e3': '', 'f3': '', 'g3': '', 'h3': '',
              'a2':'WP', 'b2': 'WP', 'c2': 'WP', 'd2': 'WP', 'e2': 'WP', 'f2': 'WP', 'g2': 'WP', 'h2': 'WP',
              'a1':'WR', 'b1': 'WN', 'c1': 'WB', 'd1': 'WQ', 'e1': 'WK', 'f1': 'WB', 'g1': 'WN', 'h1': 'WR'}
# End Init. Variables #


def find_piece_vertically(destination, piece):
    if piece[1] == "P":





def get_moves(pgn_file):
    pgn_lines = open(pgn_file, "r")

    for line in pgn_lines:
        if line.startswith("1. "):
            move_line = re.sub("\d+\.\s", "", line)
            break

    return move_line.split()


def next_move(move, blacks_turn):
    piece = source = destination = None

    if move[0].islower():  # Pawn
        piece = 'BP' if blacks_turn else 'WP'

        if move[1].isdigit():  # Vertical Move
            destination = move[0:2]
            source = find_piece_vertically(destination, piece)

    update_position(piece, source, destination)


def coord2pixel(coord):
    return FILE2X[coord[0]], RANK2Y[coord[1]]


def update_position(piece, source, destination):
    GameBoard_img.paste(PIECES2IMAGES[piece], coord2pixel(destination), PIECES2IMAGES[piece])



def create_gif(pgn_file):
    moves = get_moves(pgn_file)

    images = [np.array(GameBoard_img)]

    for i, move in enumerate(moves):
        next_move(move, i % 2)
        images.append(np.array(GameBoard_img))
        if i == 1:
            break

    #
    # print(images)

    imageio.mimsave('result.gif', images, duration=1)


if __name__ == '__main__':

    for pgn_file in glob.glob('*.pgn'):
        create_gif(pgn_file)












