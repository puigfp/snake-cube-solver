use std::fmt;

#[cfg(test)]
mod lib_test;

#[derive(Clone, PartialEq)]
pub enum Orientation {
    Up,
    Front,
    Right,
}

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
            _ => panic!("a direction shouldn't be 0"),
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

pub fn solve(
    snake: &Vec<usize>,
    size: isize,
) -> (Vec<[isize; 3]>, Vec<Direction>) {
    let mut position: Vec<[isize; 3]> = vec![[0, 0, 0]];
    let mut partial_solution: Vec<Direction> = vec![];
    solve_rec(snake, size, &mut partial_solution, &mut position);
    (position, partial_solution)
}

fn update_position(
    position: &mut Vec<[isize; 3]>,
    direction: &Direction,
    n: usize,
    size: isize,
) -> bool {
    let Direction(o, d) = direction;

    assert_eq!(position.len() >= 1, true);
    let mut current = position[position.len() - 1];
    let mut ok = true;

    for _ in 0..n {
        let next = add(current, scale(*d, delta_orientation(&o)));
        ok = ok && !position.contains(&next);
        position.push(next);
        current = next;
    }

    let mut min = [0, 0, 0];
    let mut max = [0, 0, 0];

    for p in position.iter() {
        for i in 0..3 {
            if p[i] < min[i] {
                min[i] = p[i];
            }
            if p[i] > max[i] {
                max[i] = p[i];
            }
        }
    }

    for i in 0..3 {
        ok = ok && (max[i] - min[i]) < size;
    }

    if !ok {
        for _ in 0..n {
            position.pop();
        }
    }

    ok
}

fn solve_rec(
    snake: &Vec<usize>,
    size: isize,
    partial_solution: &mut Vec<Direction>,
    position: &mut Vec<[isize; 3]>,
) -> bool {
    use Orientation::*;

    if partial_solution.len() == snake.len() {
        return true;
    }

    let i = partial_solution.len();

    for o in &[Front, Right, Up] {
        if partial_solution.len() >= 1
            && !orthogonal(&partial_solution[partial_solution.len() - 1].0, o)
        {
            continue;
        }
        for d in &[1, -1] {
            let direction = Direction(o.clone(), *d);
            if update_position(position, &direction, snake[i], size) {
                partial_solution.push(direction);
                if solve_rec(snake, size, partial_solution, position) {
                    return true;
                }
                partial_solution.pop();
                for _ in 0..snake[i] {
                    position.pop();
                }
            }
        }
    }

    false
}
