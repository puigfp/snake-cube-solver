use ::lib::*;

fn main() {
    let cases = vec![
        vec![1, 1, 1, 1, 1, 1, 1],
        vec![2, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2],
        vec![
            2, 1, 2, 1, 1, 3, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2,
            1, 1, 1, 1, 1, 2, 3, 1, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            3, 1,
        ],
    ];
    for snake in cases.iter() {
        for f in &[solve_2] {
            let solution = f(snake);
            println!(
                "{}",
                solution
                    .iter()
                    .map(|direction| format!("{}", direction))
                    .collect::<Vec<_>>()
                    .join(",")
            );
        }
    }
}
