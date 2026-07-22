fn main() {
    if let Err(message) = forge::cli::session::entry() {
        eprintln!("forge: {message}");
        std::process::exit(2);
    }
}
