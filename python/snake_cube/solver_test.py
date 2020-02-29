# 3p
import numpy as np
import pytest

# local
from .solver import (
    positions,
    snake_size,
    solve_fast,
    solve_naive,
    valid_partial_solution,
)


@pytest.mark.parametrize(
    "snake,partial_solution,expected",
    [
        # empty input
        ([], np.zeros((0, 3)), np.array([[0, 0, 0]])),
        # empty partial solution
        ([1, 1, 1, 1, 1, 1, 1], np.zeros((0, 3)), np.array([[0, 0, 0]])),
        # empty snake cube
        ([], np.array([[1, 0, 0], [0, 1, 0]]), np.array([[0, 0, 0]])),
        (
            [1, 1, 1, 1, 1, 1, 1],
            np.array([[1, 0, 0], [0, 1, 0]]),
            np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0]]),
        ),
        (
            [1, 1, 1, 1, 1, 1, 1],
            np.array([[1, 0, 0], [0, 1, 0], [-1, 0, 0], [0, -1, 0]]),
            np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 0]]),
        ),
        (
            [1, 3, 1],
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]]),
            np.array(
                [[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 2, 0], [1, 3, 0], [1, 3, -1]]
            ),
        ),
    ],
)
def test_positions(snake, partial_solution, expected):
    assert np.all(positions(snake, partial_solution) == expected)


@pytest.mark.parametrize(
    "snake,partial_solution,size,expected",
    [
        ([1, 1, 1, 1, 1, 1, 1], np.zeros((0, 3), dtype=np.int64), 2, True),
        (
            [1, 1, 1, 1, 1, 1, 1],
            np.array([[1, 0, 0], [0, 1, 0]], dtype=np.int64),
            2,
            True,
        ),
        # successive directions aren't orthogonal to one another
        (
            [1, 1, 1, 1, 1, 1, 1],
            np.array([[1, 0, 0], [-1, 0, 0]], dtype=np.int64),
            2,
            False,
        ),
        # collision
        (
            [1, 1, 1, 1, 1, 1, 1],
            np.array([[1, 0, 0], [0, 1, 0], [-1, 0, 0], [0, -1, 0]], dtype=np.int64),
            2,
            False,
        ),
        # the snake goes out of the 2x2 cube
        (
            [1, 1, 1, 1, 1, 1, 1],
            np.array([[1, 0, 0], [0, 1, 0], [1, 0, 0]], dtype=np.int64),
            2,
            False,
        ),
    ],
)
def test_valid_partial_solution(snake, partial_solution, size, expected):
    assert valid_partial_solution(snake, partial_solution, size) == expected


@pytest.mark.parametrize(
    "snake",
    [[1, 1, 1, 1, 1, 1, 1], [2, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2]],
)
@pytest.mark.parametrize(
    "solve", [solve_naive, solve_fast],
)
def test_solve(snake, solve):
    size = snake_size(snake)
    solution = solve(snake)
    # the solution should be a valid partial solution
    assert valid_partial_solution(snake, solution, size)
    # the solution shouldn't be partial, ie, all segments should have an orientation
    assert solution.shape[0] == len(snake)
    # the solution should fill the entirety of the size * size * size cube
    assert positions(snake, solution).shape[0] == size ** 3
