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
    # weight = np.array([[500, -25, 10, 5, 5, 10, -25, 500],
    #                    [-25, -45, 1, 1, 1, 1, -45, -25],
    #                    [10, 1, 3, 2, 2, 3, 1, 10],
    #                    [5, 1, 2, 1, 1, 2, 1, 5],
    #                    [5, 1, 2, 1, 1, 2, 1, 5],
    #                    [10, 1, 3, 2, 2, 3, 1, 10],
    #                    [-25, -45, 1, 1, 1, 1, -45, -25],
    #                    [500, -25, 10, 5, 5, 10, -25, 500]])
    # weight = -1 * weight

    weight = np.array([
        [-10000, 500, -50, -50, -50, -50, 500, -10000],
        [500, 900, -5, 10, 10, -5, 900, 500],
        [-50, -5, -300, -1, -1, -300, -5, -50],
        [-50, 10, -1, 0, 0, -1, 10, -50],
        [-50, 10, -1, 0, 0, -1, 10, -50],
        [-50, -5, -300, -1, -1, -300, -5, -50],
        [500, 900, -5, 10, 10, -5, 900, 500],
        [-10000, 500, -50, -50, -50, -50, 500, -10000]
    ])

    depth = 0
    max_depth = 4

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
        action_list = self.get_all_actions(chessboard, self.color)

        self.candidate_list = action_list

        if 0 < len(action_list) < 6:
            self.max_depth = 5
        else:
            self.max_depth = 4

        if get_total_number(chessboard, COLOR_NONE) <= 8:
            self.max_depth = 8

        # self.candidate_list = action_list
        # action_list = self.get_all_actions(chessboard, self.color)
        action = self.alpha_beta(chessboard, self.color)
        # action_list = self.get_all_actions(chessboard, self.color)
        # self.candidate_list = action_list
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

    def evaluate_weight(self, chessboard):
        score = 0
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if chessboard[i][j] == self.color:
                    score += self.weight[i][j]
                elif chessboard[i][j] == -1 * self.color:
                    score -= self.weight[i][j]
        return score

    def stable(self, chessboard):
        number = 0
        a = [0, 7, 0, 7]
        b = [0, 0, 7, 7]
        drow = [-1, -1, -1, 0, 0, 1, 1, 1]
        dcol = [-1, 0, 1, -1, 1, -1, 0, 1]
        for i in range(4):
            if chessboard[a[i]][b[i]] == self.color:
                number += 1
                for j in range(8):
                    row = a[i] + drow[j]
                    col = b[i] + dcol[j]
                    while 0 <= row < self.chessboard_size and 0 <= col < self.chessboard_size:
                        if chessboard[row][col] == self.color:
                            number += 1
                            row += drow[j]
                            col += dcol[j]
                        else:
                            break

        return number

    def frontier(self, chessboard):
        number = 0
        drow = [-1, -1, -1, 0, 0, 1, 1, 1]
        dcol = [-1, 0, 1, -1, 1, -1, 0, 1]
        for i in range(1, 7):
            for j in range(1, 7):
                if chessboard[i][j] == self.color:
                    for k in range(8):
                        row = i + drow[k]
                        col = j + dcol[k]
                        if chessboard[row][col] == COLOR_NONE:
                            number += 1
                            break

        return number

    def evaluate(self, chessboard):
        score = self.evaluate_weight(chessboard) - 500 * self.stable(chessboard) + 50 * len(
            self.get_all_actions(chessboard, self.color)) + 10 * self.frontier(chessboard)
        return score

    # def evaluate(self, chessboard):
    #     score = self.evaluate_weight(chessboard) - 10 * self.stable(chessboard) - 10 * len(
    #         self.get_all_actions(chessboard, self.color)) + 10 * self.frontier(chessboard)
    #     return score

    # def evaluate(self, chessboard):
    #     score = 0
    #     for i in range(self.chessboard_size):
    #         for j in range(self.chessboard_size):
    #             if chessboard[i][j] == self.color:
    #                 score += self.weight[i][j]
    #             elif chessboard[i][j] == -1 * self.color:
    #                 score -= self.weight[i][j]
    #     return score

    def change_board(self, chessboard, color, position):
        new_chessboard = np.copy(chessboard)
        Suspect = []
        drow = [-1, -1, -1, 0, 0, 1, 1, 1]
        dcol = [-1, 0, 1, -1, 1, -1, 0, 1]
        new_chessboard[position[0]][position[1]] = color
        for i in range(8):
            Suspect.clear()
            row = position[0] + drow[i]
            col = position[1] + dcol[i]
            Permission_to_go = False
            while 0 <= row < self.chessboard_size and 0 <= col < self.chessboard_size:
                if new_chessboard[row][col] == -1 * color:
                    Permission_to_go = True
                    Suspect.append((row, col))
                    row += drow[i]
                    col += dcol[i]
                elif new_chessboard[row][col] == color and Permission_to_go is True:
                    for pos in Suspect:
                        new_chessboard[pos[0]][pos[1]] = color
                    break
                else:
                    break
        return new_chessboard

    def alpha_beta(self, chessboard, color):

        def max_value(chessboard, alpha, beta, color):

            if self.depth >= self.max_depth:
                return self.evaluate(chessboard)

            action_list = self.get_all_actions(chessboard, color)
            if len(action_list) == 0:  # If I don't have moves
                if len(self.get_all_actions(chessboard, -1 * color)) == 0:  # If you don't have moves
                    return self.evaluate(chessboard)
                return min_value(chessboard, alpha, beta, color)
            v = float('-inf')
            for a in action_list:
                new_chessboard = self.change_board(chessboard, color, a)  # I move
                self.depth += 1
                v = max(v, min_value(new_chessboard, alpha, beta, color))  # Your turn
                self.depth -= 1
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(chessboard, alpha, beta, color):

            if self.depth >= self.max_depth:
                return self.evaluate(chessboard)

            action_list = self.get_all_actions(chessboard, -1 * color)
            if len(action_list) == 0:  # If you don't have moves
                if len(self.get_all_actions(chessboard, color)) == 0:  # If I don't have moves
                    return self.evaluate(chessboard)
                return max_value(chessboard, alpha, beta, color)
            v = float('inf')
            for a in action_list:
                new_chessboard = self.change_board(chessboard, -1 * color, a)  # You move
                self.depth += 1
                v = min(v, max_value(new_chessboard, alpha, beta, color))  # My turn
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
            new_chessboard = self.change_board(chessboard, color, a)  # I move
            self.depth += 1
            v = min_value(new_chessboard, best_score, beta, color)  # Your turn
            self.depth -= 1
            if v > best_score:
                best_score = v
                action = a
        return action
