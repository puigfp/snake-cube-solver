use std::collections::HashSet;
use std::fmt;

#[cfg(test)]
mod lib_test;

#[derive(Clone, PartialEq)]
pub enum Orientation {
    Up,
    Front,
    Right,
}

// Direction = Orientation + coef (+1 or -1)
#[derive(Clone)]
pub struct Direction(Orientation, isize);

impl Direction {
    fn to_string(&self) -> &str {
        use Orientation::*;
        match *self {
            Direction(Up, d) if d == 1 => "up",
            Direction(Up, d) if d == -1 => "down",
            Direction(Front, d) if d == 1 => "front",
            Direction(Front, d) if d == -1 => "back",
            Direction(Right, d) if d == 1 => "right",
            Direction(Right, d) if d == -1 => "left",
            Direction(_, d) => panic!("d should be +1 or -1, not {}", d),
        }
    }
}

impl fmt::Display for Direction {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.to_string())
    }
}

fn orthogonal(o1: &Orientation, o2: &Orientation) -> bool {
    o1 != o2
}

fn delta_orientation(o: &Orientation) -> [isize; 3] {
    use Orientation::*;
    match o {
        Front => [1, 0, 0],
        Right => [0, 1, 0],
        Up => [0, 0, 1],
    }
}

fn add(a: [isize; 3], b: [isize; 3]) -> [isize; 3] {
    [a[0] + b[0], a[1] + b[1], a[2] + b[2]]
}

fn scale(s: isize, a: [isize; 3]) -> [isize; 3] {
    [s * a[0], s * a[1], s * a[2]]
}

fn snake_size(snake: &Vec<usize>) -> usize {
    let length = snake.iter().sum::<usize>() + 1;
    let size = (length as f64).powf(1. / 3.).round() as usize;
    if size.pow(3) != length {
        println!("{} {}", (length as f64).powf(1. / 3.), length);
        panic!("{} isn't a valid snake length", length);
    }
    size
}

fn valid_partial_solution(
    snake: &Vec<usize>,
    size: usize,
    partial_solution: &Vec<Direction>,
) -> bool {
    // we assume that successive directions of the solution are orthogonal
    // to one another

    // compute positions array: there should be no collisions
    let mut position = vec![[0, 0, 0]];
    for (length, Direction(o, d)) in snake.iter().zip(partial_solution.iter()) {
        for _ in 0..*length {
            let next = add(
                position[position.len() - 1],
                scale(*d, delta_orientation(&o)),
            );
            if position.contains(&next) {
                return false;
            }
            position.push(next);
        }
    }

    // snake should fit in a size*size*size cube
    let min = (0..3).map(|i| position.iter().map(|p| p[i]).min().unwrap());
    let max = (0..3).map(|i| position.iter().map(|p| p[i]).max().unwrap());

    if min
        .zip(max)
        .map(|(a, b)| b - a < size as isize)
        .collect::<Vec<_>>()
        .contains(&false)
    {
        return false;
    }

    true
}

pub fn solve_naive(snake: &Vec<usize>) -> Vec<Direction> {
    let mut partial_solution: Vec<Direction> = vec![];
    let size = snake_size(snake);
    solve_naive_rec(snake, size, &mut partial_solution);
    partial_solution
}

fn solve_naive_rec(
    snake: &Vec<usize>,
    size: usize,
    partial_solution: &mut Vec<Direction>,
) -> bool {
    if !valid_partial_solution(snake, size, partial_solution) {
        return false;
    }

    if partial_solution.len() == snake.len() {
        return true;
    }

    use Orientation::*;

    for o in &[Front, Right, Up] {
        if partial_solution.len() >= 1
            && !orthogonal(&partial_solution[partial_solution.len() - 1].0, o)
        {
            continue;
        }
        for d in &[1, -1] {
            partial_solution.push(Direction(o.clone(), *d));
            if solve_naive_rec(snake, size, partial_solution) {
                return true;
            }
            partial_solution.pop();
        }
    }

    false
}

pub fn solve_fast(snake: &Vec<usize>) -> Vec<Direction> {
    let mut partial_solution: Vec<Direction> = vec![];
    let mut snake_positions = vec![([0, 0, 0], [0, 0, 0], [0, 0, 0])];
    let mut snake_positions_set = HashSet::new();
    snake_positions_set.insert([0, 0, 0]);
    let size = snake_size(snake);
    solve_fast_rec(
        snake,
        size,
        &mut partial_solution,
        &mut snake_positions,
        &mut snake_positions_set,
    );
    assert!(valid_partial_solution(snake, size, &partial_solution));
    assert!(partial_solution.len() == snake.len());
    partial_solution
}

pub fn solve_fast_rec(
    snake: &Vec<usize>,
    size: usize,
    partial_solution: &mut Vec<Direction>,
    snake_positions: &mut Vec<([isize; 3], [isize; 3], [isize; 3])>,
    snake_positions_set: &mut HashSet<[isize; 3]>,
) -> bool {
    if partial_solution.len() == snake.len() {
        return true;
    }

    use Orientation::*;
    for o in &[Front, Right, Up] {
        if partial_solution.len() >= 1
            && !orthogonal(&partial_solution[partial_solution.len() - 1].0, o)
        {
            continue;
        }
        for d in &[1, -1] {
            if !try_extend_snake(
                snake,
                size,
                partial_solution,
                snake_positions,
                snake_positions_set,
                Direction(o.clone(), *d),
            ) {
                continue;
            }

            if solve_fast_rec(
                snake,
                size,
                partial_solution,
                snake_positions,
                snake_positions_set,
            ) {
                return true;
            }

            for _ in 0..snake[partial_solution.len() - 1] {
                let (pos, _, _) = snake_positions.pop().unwrap();
                snake_positions_set.remove(&pos);
            }
            partial_solution.pop();
        }
    }

    false
}

fn try_extend_snake(
    snake: &Vec<usize>,
    size: usize,
    partial_solution: &mut Vec<Direction>,
    snake_positions: &mut Vec<([isize; 3], [isize; 3], [isize; 3])>,
    snake_positions_set: &mut HashSet<[isize; 3]>,
    direction: Direction,
) -> bool {
    let length = snake[partial_solution.len()];
    let Direction(o, d) = direction.clone();

    let mut res = true;
    let mut pushed = 0;

    'append: for _ in 0..length {
        let (pos, min, max) = snake_positions[snake_positions.len() - 1];
        let next_pos = add(pos, scale(d, delta_orientation(&o)));

        // compute next rolling min/max values
        let mut next_min = [0, 0, 0];
        let mut next_max = [0, 0, 0];
        for i in 0..3 {
            next_min[i] = min[i].min(next_pos[i]);
            next_max[i] = max[i].max(next_pos[i]);
            // early exit: we're using too much space
            if !(next_max[i] - next_min[i] < size as isize) {
                res = false;
                break 'append;
            }
        }
        // early exit: collision
        if snake_positions_set.contains(&next_pos) {
            res = false;
            break 'append;
        }
        // ok
        snake_positions.push((next_pos, next_min, next_max));
        snake_positions_set.insert(next_pos);
        pushed += 1;
    }

    // there was an early exit, remove the positions we inserted
    if !res {
        for _ in 0..pushed {
            let (pos, _, _) = snake_positions.pop().unwrap();
            snake_positions_set.remove(&pos);
        }
        return false;
    }

    partial_solution.push(direction);
    true
}
