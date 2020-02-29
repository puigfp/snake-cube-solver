# std
import sys

# 3p
import numpy as np

# fmt: off
directions = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])

directions_names = {
    (1, 0, 0): "front",
    (-1, 0, 0): "back",
    (0, 1, 0): "right",
    (0, -1, 0): "left",
    (0, 0, 1): "up",
    (0, 0, -1): "down",
}

def snake_size(snake):
    length = np.sum(snake) + 1
    size = np.int(np.round(length **(1/3)))
    assert size ** 3 == length
    return size

def positions(snake, partial_solution):
    pos = [np.array([0, 0, 0])]
    for l, direction in zip(snake, partial_solution):
        for _ in range(l):
            pos.append(pos[-1] + direction)
    return np.array(pos)


def valid_partial_solution(snake, partial_solution, size):
    # the snake should fit in a size*size*size cube
    pos = positions(snake, partial_solution)  # (M, 3)
    min_ = np.min(pos, axis=0)  # (3,)
    max_ = np.max(pos, axis=0)  # (3,)

    if not np.all(max_ - min_ < size):
        return False

    # there should be no collision
    pos_unique = set(tuple(p) for p in pos)

    if not len(pos) == len(pos_unique):
        return False

    return True


def solve_naive(snake):
    size = snake_size(snake)
    partial_solution = []

    def rec():
        # partial solution is invalid: early exit
        if not valid_partial_solution(snake, np.array(partial_solution), size):
            return False

        # solution is complete: early exit
        if len(partial_solution) == len(snake):
            return True

        # try all possible next positions
        for direction in directions:
            if partial_solution and not partial_solution[-1] @ direction.T == 0:
                continue
            for coef in [1, -1]:
                partial_solution.append(coef * direction)
                if rec():
                    return True
                partial_solution.pop()

        return False

    rec()

    return np.array(partial_solution)

def solve_fast(snake):
    size = snake_size(snake)
    partial_solution = []
    positions = [(np.array([0, 0, 0]), (0, 0, 0), (0, 0, 0))]
    positions_set = {(0,0,0)}

    def try_extend_snake(direction):
        length = snake[len(partial_solution)]
        res = True
        pushed = 0

        for _ in range(length):
            pos, min_, max_ = positions[-1]
            next_pos = pos + direction
            next_min = np.min([min_, next_pos], axis=0)
            next_max = np.max([max_, next_pos], axis=0)
            if not np.all(next_max - next_min < size):
                res = False
                break
            if tuple(next_pos) in positions_set:
                res = False
                break
            positions.append((next_pos, next_min, next_max))
            positions_set.add(tuple(next_pos))
            pushed += 1

        if not res:
            for _ in range(pushed):
                pos, _, _ = positions.pop()
                positions_set.remove(tuple(pos))
            return False

        partial_solution.append(direction)
        return True


    def rec():
        if len(partial_solution) == len(snake):
            return True

        for direction in directions:
            if partial_solution and not partial_solution[-1] @ direction.T == 0:
                continue
            for coef in [1, -1]:
                if not try_extend_snake(coef * direction):
                    continue
                if rec():
                    return True
                for _ in range(snake[len(partial_solution) - 1]):
                    pos, _, _ = positions.pop()
                    positions_set.remove(tuple(pos))
                partial_solution.pop()

        return False

    rec()

    assert valid_partial_solution(snake, partial_solution, size)
    assert len(partial_solution) == len(snake)
    return np.array(partial_solution)

def show_solution(solution):
    return ",".join(directions_names[tuple(d)] for d in solution)


if __name__ == "__main__":
    assert len(sys.argv) == 2
    snake = [int(s.strip()) for s in sys.argv[1].split(",")]
    print(show_solution(solve_fast(snake)))
