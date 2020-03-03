# snake cube solver

Solvers for puzzles of the snake cube family ([video](https://www.youtube.com/watch?v=iTzVPgFjE9c)).

This repository host two implementations, one in Python and the other in Rust.

I wrote the Python code first, but it turned out to be too slow to solve the 4\*4\*4 snake cube you can find in the input examples below. The Rust implementation can solve it in just a few seconds.

## input examples

A snake is represented as a comma-separated list of integers. Each integer represents the number of steps to take before the next "turn".

For instance, the string `1,2,3,1` represents the following snake:

```
##
 #
 ####
    #
```

Notice that the length of a snake is equal to the sum of the numbers in its string, plus one.

Here, the snake is of length `8 = (1 + 2 + 3 + 1) + 1`.

Here are some examples of solvable snakes:

- 2\*2\*2 cube:

  `1,1,1,1,1,1,1` (only solvable 2\*2\*2 snake cube)

- 3\*3\*3 cube:

  `2,1,1,2,1,2,1,1,2,2,1,1,1,2,2,2,2`

- 4\*4\*4 cube:

  `2,1,2,1,1,3,1,2,1,2,1,2,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,2,3,1,1,1,3,1,2,1,1,1,1,1,1,1,1,1,3,1`

## usage

### python

The dependencies are managed using [poetry](https://python-poetry.org/).

```
poetry install  # install dependencies
poetry run snake_cube/solver.py "<snake cube>"
```

The solver outputs a sequence of orientations that describe one of the solutions (because of symmetries, there is a lot of solutions):

Example:

```
$ poetry run snake_cube/solver.py "1,1,1,1,1,1,1"
front,right,back,up,front,left,back
```

### rust

```
cargo run --release "<snake cube>"
```

## tests

I did write some tests, but the coverage isn't perfect.

Here's how to run the tests with coverage.

### python

```
poetry run pytest -vv -s --cov snake_cube --cov-report html
```

### rust

```
# you need the nightly Rust toolchain
rustup install nightly

# actually run the tests
./run_tests_coverage.sh
```
