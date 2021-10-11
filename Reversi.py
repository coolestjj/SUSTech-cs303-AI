import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


# don't change the class name
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
        action_list = AI.get_all_actions(self, chessboard)
        start = time.time()
        action, weight = self.alpha_beta(chessboard, self.color, -9999999, 9999999, start)
        self.candidate_list = action_list
        self.candidate_list.remove(action)
        self.candidate_list.append(action)

    def get_all_actions(self, chessboard):
        idx = np.where(chessboard == self.color)
        idx = list(zip(idx[0], idx[1]))
        action_list = []
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
                        action_list.append((row, col))
                        break
                    else:
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

    def alpha_beta(self, chessboard, color, a, b, start):
        if self.depth > self.max_depth:
            return None, self.evaluate(chessboard)
        action_list = AI.get_all_actions(self, chessboard)
        if len(action_list) == 0:
            run_time = time.time() - start
            if run_time >= 2:
                return None, self.evaluate(chessboard)
            return self.alpha_beta(chessboard, -1 * color, a, b, start)

        max = -9999999
        min = 9999999
        action = ()

        for p in action_list:
            self.depth += 1
            p1, current = self.alpha_beta(chessboard, -1 * color, a, b, start)
            self.depth -= 1
            if color == self.color:
                if current > a:
                    if current > b:
                        return p, current
                    a = current
                if current > max:
                    max = current
                    action = p
            else:
                if current < b:
                    if current < a:
                        return p, current
                    b = current
                if current < min:
                    min = current
                    action = p

        if color == self.color:
            return action, max
        else:
            return action, min

        # Make sure that the position of your decision in chess board is empty.
        # If not, the system will return error.
        # Add your decision into candidate_list, Records the chess board
        # You need add all the positions which is valid
        # candidate_list example: [(3,3),(4,4)]
        # You need append your decision at the end of the candiidate_list,
        # we will choice the last element of the candidate_list as the position you choose
        # If there is no valid position, you must return an empty list.
