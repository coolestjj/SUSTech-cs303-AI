import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your
        # decision .
        self.candidate_list = []

    # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list, must do this step
        self.candidate_list.clear()
        # ==================================================================
        # Write your algorithm here
        # Here is the simplest sample:Random decision
        idx = np.where(chessboard == self.color)
        idx = list(zip(idx[0], idx[1]))
        # ==============Find new pos========================================
        drow = [-1, -1, -1, 0, 0, 1, 1, 1]
        dcol = [-1, 0, 1, -1, 1, -1, 0, 1]
        for my_piece in idx:
            for i in range(8):
                permission_to_go = False
                row = my_piece[0] + drow[i]
                col = my_piece[1] + dcol[i]
                while 0 <= row < self.chessboard_size and 0 <= col < self.chessboard_size:  # If not out of border
                    if chessboard[row][col] == -1 * self.color:  # If there is an opponent nearby
                        row = row + drow[i]
                        col = col + dcol[i]
                        permission_to_go = True
                    elif chessboard[row][col] == 0 and permission_to_go is True:
                        self.candidate_list.append((row, col))
                        break
                    else:
                        break



        # Make sure that the position of your decision in chess board is empty.
        # If not, the system will return error.
        # Add your decision into candidate_list, Records the chess board
        # You need add all the positions which is valid
        # candidate_list example: [(3,3),(4,4)]
        # You need append your decision at the end of the candiidate_list,
        # we will choice the last element of the candidate_list as the position you choose
        # If there is no valid position, you must return an empty list.
