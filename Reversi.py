import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


# don't change the class name
def get_total_number(chessboard):
    piece_number = np.sum(chessboard != 0)
    return piece_number


class AI(object):
    weight = np.array([
        [70, -15, 20, 20, 20, 20, -15, 70],
        [-20, -30, 5, 5, 5, 5, -30, -15],
        [20, 5, 1, 1, 1, 1, 5, 20],
        [20, 5, 1, 1, 1, 1, 5, 20],
        [20, 5, 1, 1, 1, 1, 5, 20],
        [20, 5, 1, 1, 1, 1, 5, 20],
        [-20, -30, 5, 5, 5, 5, -30, -15],
        [70, -15, 20, 20, 20, 20, -15, 70]
    ])

    weight = weight * (-1)

    depth = 0
    max_depth = 3

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
        action, weight = self.alpha_beta(chessboard, self.color, -9999999, 9999999)
        action_list = self.get_all_actions(chessboard, self.color)
        self.candidate_list = action_list
        if action != () and action in action_list:
            self.candidate_list.remove(action)
            self.candidate_list.append(action)

    def get_all_actions(self, chessboard, color):
        action_list = []
        drow = [-1, -1, -1, 0, 0, 1, 1, 1]
        dcol = [-1, 0, 1, -1, 1, -1, 0, 1]

        if get_total_number(chessboard) <= 45:
            idx = np.where(chessboard == color)
            idx = list(zip(idx[0], idx[1]))
            for my_piece in idx:
                for i in range(8):
                    permission_to_go = False
                    row = my_piece[0] + drow[i]
                    col = my_piece[1] + dcol[i]
                    while 0 <= row < self.chessboard_size and 0 <= col < self.chessboard_size:  # If not out of border
                        if chessboard[row][col] == -1 * color:  # If there is an opponent nearby
                            row = row + drow[i]
                            col = col + dcol[i]
                            permission_to_go = True
                        elif chessboard[row][col] == 0 and permission_to_go is True:
                            if (row, col) not in action_list:
                                action_list.append((row, col))
                            break
                        else:
                            break
        elif get_total_number(chessboard) > 45:
            idx = np.where(chessboard == COLOR_NONE)
            idx = list(zip(idx[0], idx[1]))
            for i in idx:
                for j in range(8):
                    row = i[0] + drow[j]
                    col = i[1] + dcol[j]
                    permission_to_go = False
                    while 0 <= row < self.chessboard_size and 0 <= col < self.chessboard_size:
                        if chessboard[row][col] == color or chessboard[row][col] == 0:
                            break
                        row += drow[j]
                        col += dcol[j]
                        permission_to_go = True
                    if permission_to_go is True:
                        if 0 <= row < self.chessboard_size and 0 <= col < self.chessboard_size:
                            if chessboard[row][col] == color:
                                if i not in action_list:
                                    action_list.append(i)
                                break
        return action_list

    def evaluate(self, chessboard):
        count = 0
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if chessboard[i][j] == self.color:
                    count += self.weight[i][j]
                elif chessboard[i][j] == -1 * self.color:
                    count -= self.weight[i][j]
        return count

    def alpha_beta(self, chessboard, color, a, b):
        if self.depth > self.max_depth:
            return (), self.evaluate(chessboard)
        action_list2 = self.get_all_actions(chessboard, color)
        if len(action_list2) == 0:
            if len(self.get_all_actions(chessboard, -1 * color)) == 0:
                return (), self.evaluate(chessboard)
            return self.alpha_beta(chessboard, -1 * color, a, b)

        Max = -9999999
        Min = 9999999
        action = ()

        for p in action_list2:
            self.depth += 1
            p1, current = self.alpha_beta(chessboard, -1 * color, a, b)
            self.depth -= 1
            if color == self.color:
                if current > a:
                    if current > b:
                        return p, current
                    a = current
                if current > Max:
                    Max = current
                    action = p
            else:
                if current < b:
                    if current < a:
                        return p, current
                    b = current
                if current < Min:
                    Min = current
                    action = p

        if color == self.color:
            return action, Max
        else:
            return action, Min

        # Make sure that the position of your decision in chess board is empty.
        # If not, the system will return error.
        # Add your decision into candidate_list, Records the chess board
        # You need add all the positions which is valid
        # candidate_list example: [(3,3),(4,4)]
        # You need append your decision at the end of the candidate_list,
        # we will choice the last element of the candidate_list as the position you choose
        # If there is no valid position, you must return an empty list.
