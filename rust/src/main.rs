use ::lib::*;

fn main() {
    let cases = vec![
        (vec![1, 1, 1, 1, 1, 1, 1], 2),
        (vec![2, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2], 3),
        (
            vec![
                2, 1, 2, 1, 1, 3, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2,
                2, 1, 1, 1, 1, 1, 2, 3, 1, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 3, 1,
            ],
            4,
        ),
    ];
    for (snake, size) in cases.iter() {
        let (position, solution) = solve(snake, *size);
        println!("{:?}", position);
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
