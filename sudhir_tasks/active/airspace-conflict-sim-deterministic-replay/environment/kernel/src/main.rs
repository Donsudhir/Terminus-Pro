mod io;
mod ranker;
mod resolve;
mod types;

fn main() {
    let req = match io::read_request() {
        Ok(r) => r,
        Err(e) => {
            eprintln!("{e}");
            std::process::exit(1);
        }
    };

    let accepted = resolve::resolve(req.candidates, req.capacity);
    let out = match io::encode_response(accepted) {
        Ok(v) => v,
        Err(e) => {
            eprintln!("{e}");
            std::process::exit(1);
        }
    };
    println!("{out}");
}
