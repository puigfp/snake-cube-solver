# 3p
import pytest
import numpy as np

# local
from .solver import positions, ok, solve


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
def test_ok(snake, partial_solution, size, expected):
    assert ok(snake, partial_solution, size) == expected


@pytest.mark.parametrize(
    "snake,size",
    [
        ([1, 1, 1, 1, 1, 1, 1], 2),
        ([2, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2], 3),
    ],
)
@pytest.mark.parametrize(
    "clever_caching", [True, False],
)
def test_solve(snake, size, clever_caching):
    solution = solve(snake, size, clever_caching)
    # the solution should be a valid partial solution
    assert ok(snake, solution, size)
    # the solution shouldn't be partial, ie, all segments should have an orientation
    assert solution.shape[0] == len(snake)
    # the solution should fill the entirety of the size * size * size cube
    assert positions(snake, solution).shape[0] == size ** 3
