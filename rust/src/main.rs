use ::lib::*;

use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    assert!(args.len() == 2);
    let snake = args[1]
        .split(",")
        .map(|s| s.trim().parse().unwrap())
        .collect::<Vec<usize>>();
    let solution = solve_fast(&snake);
    println!(
        "{}",
        solution
            .iter()
            .map(|direction| format!("{}", direction))
            .collect::<Vec<_>>()
            .join(",")
    );
}
