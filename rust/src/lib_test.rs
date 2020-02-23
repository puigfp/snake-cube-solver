use super::*;

#[test]
fn test_snake_size() {
    let cases = [
        (vec![1, 1, 1, 1, 1, 1, 1], 2),
        (vec![2, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2], 3),
    ];
    for (snake, expected_size) in cases.iter() {
        assert_eq!(*expected_size, snake_size(snake));
    }
}

#[test]
#[should_panic]
fn test_snake_size_panic() {
    let snake = vec![1, 1, 1, 1, 1, 1, 1, 1];
    snake_size(&snake);
}

#[test]
fn test_orthogonal() {
    use Orientation::*;
    let cases = [((Up, Up), false), ((Right, Up), true)];
    for ((o1, o2), expected) in cases.iter() {
        assert_eq!(*expected, orthogonal(o1, o2));
    }
}
