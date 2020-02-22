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

invariant_transformations = np.array([
    # symmetries
    # x/y plane
    [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, -1],
    ],
    # x/z plane
    [
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1],
    ],
    # y/z plane
    [
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ],
    # rotations
    # around x axis
    [
        [1, 0, 0],
        [0, 0, 1],
        [0, -1, 0],
    ],
    # around y axis
    [
        [0, 0, 1],
        [0, 1, 0],
        [-1, 0, 0],
    ],
    # around z axis
    [
        [0, 1, 0],
        [-1, 0, 0],
        [0, 0, 1],
    ],
])
# fmt: on


def positions(snake, partial_solution):
    pos = [np.array([0, 0, 0])]
    for l, direction in zip(snake, partial_solution):
        for _ in range(l):
            pos.append(pos[-1] + direction)
    return np.array(pos)


def ok(snake, partial_solution, size):
    # successive directions should be orthogonal to one another
    for i in range(partial_solution.shape[0] - 1):
        if not partial_solution[i, :] @ partial_solution[i + 1, :].T == 0:
            return False

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


def hash_array(arr):
    return hash((arr.shape, tuple(arr.flatten())))


def solve(snake, size, clever_caching):
    partial_solution = []
    seen = set()
    calls = 0  # to keep track of the number of rec calls
    m = 0

    def rec():
        nonlocal calls
        calls += 1

        nonlocal m
        m = max(m, len(partial_solution))

        print(len(partial_solution), m, len(snake), len(seen), calls)

        # partial solution is invalid: early exit
        if not ok(snake, np.array(partial_solution), size):
            return False

        # solution is complete: early exit
        if len(partial_solution) == len(snake):
            return True

        # clever caching trick
        if clever_caching:
            partial_solution_arr = np.array(partial_solution).reshape(-1, 3)

            # we've already processed an equivalent position:
            # early exit (we know the current position won't work)
            if hash_array(partial_solution_arr) in seen:
                return False

            # we add all the equivalent positions to the seen set
            q = [partial_solution_arr]
            while q:
                s = q.pop()
                if hash_array(s) in seen:
                    continue
                seen.add(hash_array(s))
                for transformation in invariant_transformations:
                    q.append(partial_solution_arr @ transformation.T)

        # try all possible next positions
        for direction in directions:
            for coef in [1, -1]:
                partial_solution.append(coef * direction)
                if rec():
                    return True
                partial_solution.pop()

        return False

    rec()

    print(f"{calls} rec calls")

    return np.array(partial_solution)


def show_solution(solution):
    return ",".join(directions_names[tuple(d)] for d in solution)


# XXX: debug
if __name__ == "__main__":
    snake = [2, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2]
    size = 3
    print(sum(snake), size ** 3)
    print(show_solution(solve(snake, size, True)))

    # fmt: off
    snake = [
        2, 1, 2, 1, 1, 3, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1,
        1, 2, 3, 1, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1,
    ]
    size = 4
    # fmt: on
    print(sum(snake), size ** 3)
    # print(show_solution(solve(snake, size, True))
    print(show_solution(solve(snake, size, False)))
