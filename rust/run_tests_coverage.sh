# This short bash script runs the tests and opens a code coverage report in the default browser.
# see https://github.com/kennytm/cov#usage-for-local-testing-on-nightly-rust
cargo +nightly cov clean
cargo +nightly cov test --lib
cargo +nightly cov report --open
