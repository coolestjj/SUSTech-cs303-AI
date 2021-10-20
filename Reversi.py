import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


# don't change the class name
def get_total_number(chessboard, color):
    piece_number = np.sum(chessboard == color)
    return piece_number


class AI(object):

    weight = np.array([
        [10000, -250, 50, 50, 50, 50, -250, 10000],
        [-250, -1000, 5, 5, 5, 5, -1000, -250],
        [50, 5, 15, 1, 1, 15, 5, 50],
        [50, 5, 1, 1, 1, 1, 5, 50],
        [50, 5, 1, 1, 1, 1, 5, 50],
        [50, 5, 15, 1, 1, 15, 5, 50],
        [-250, -1000, 5, 5, 5, 5, -1000, -250],
        [10000, -250, 50, 50, 50, 50, -250, 10000]
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
        # action_list = self.get_all_actions(chessboard, self.color)

        # if 0 < len(action_list) < 3:
        #     self.max_depth = 8
        # elif 3 <= len(action_list) < 6:
        #     self.max_depth = 7
        # else:
        #     self.max_depth = 6

        action = self.alpha_beta(chessboard, self.color)
        action_list = self.get_all_actions(chessboard, self.color)
        self.candidate_list = action_list
        if action != () and action in action_list:
            self.candidate_list.remove(action)
            self.candidate_list.append(action)

    def get_all_actions(self, chessboard, color):
        action_list = []
        drow = [-1, -1, -1, 0, 0, 1, 1, 1]
        dcol = [-1, 0, 1, -1, 1, -1, 0, 1]

        if get_total_number(chessboard, color) <= get_total_number(chessboard, COLOR_NONE):
            idx = np.where(chessboard == color)
            idx = zip(idx[0], idx[1])
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
        else:
            idx = np.where(chessboard == COLOR_NONE)
            idx = zip(idx[0], idx[1])
            for empty_pos in idx:
                for j in range(8):
                    row = empty_pos[0] + drow[j]
                    col = empty_pos[1] + dcol[j]
                    First_step_out = False
                    while 0 <= row < self.chessboard_size and 0 <= col < self.chessboard_size:
                        if chessboard[row][col] == -1 * color:  # If there is an opponent nearby
                            row += drow[j]
                            col += dcol[j]
                            First_step_out = True
                        elif First_step_out is True and chessboard[row][col] == color:
                            if empty_pos not in action_list:
                                action_list.append(empty_pos)
                            break
                        else:
                            break
        return action_list

    def evaluate(self, chessboard):
        score = 0
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if chessboard[i][j] == self.color:
                    score += self.weight[i][j]
                elif chessboard[i][j] == -1 * self.color:
                    score -= self.weight[i][j]
        return score

    def alpha_beta(self, chessboard, color):

        def max_value(chessboard, alpha, beta, color):

            if self.depth > self.max_depth:
                return self.evaluate(chessboard)

            action_list = self.get_all_actions(chessboard, color)
            if len(action_list) == 0:
                if len(self.get_all_actions(chessboard, -1 * color)) == 0:
                    return self.evaluate(chessboard)
                return min_value(chessboard, alpha, beta, -1 * color)
            v = float('-inf')
            for a in action_list:
                new_chessboard = np.copy(chessboard)
                new_chessboard[a[0]][a[1]] = color
                self.depth += 1
                v = max(v, min_value(new_chessboard, alpha, beta, -1 * color))
                self.depth -= 1
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(chessboard, alpha, beta, color):

            if self.depth > self.max_depth:
                return self.evaluate(chessboard)

            action_list = self.get_all_actions(chessboard, color)
            if len(action_list) == 0:
                if len(self.get_all_actions(chessboard, -1 * color)) == 0:
                    return self.evaluate(chessboard)
                return max_value(chessboard, alpha, beta, -1 * color)
            v = float('inf')
            for a in action_list:
                new_chessboard = np.copy(chessboard)
                new_chessboard[a[0]][a[1]] = color
                self.depth += 1
                v = min(v, max_value(chessboard, alpha, beta, -1 * color))
                self.depth -= 1
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        best_score = float('-inf')
        beta = float('inf')
        action = ()
        action_list = self.get_all_actions(chessboard, color)
        for a in action_list:
            new_chessboard = np.copy(chessboard)
            new_chessboard[a[0]][a[1]] = color
            self.depth += 1
            v = min_value(new_chessboard, best_score, beta, color)
            self.depth -= 1
            if v > best_score:
                best_score = v
                action = a
        return action
