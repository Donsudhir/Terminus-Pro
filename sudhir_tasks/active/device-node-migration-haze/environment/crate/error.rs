use std::fmt;

#[derive(Debug)]
pub struct AppError {
    message: String,
}

pub type AppResult<T> = Result<T, AppError>;

impl AppError {
    pub fn msg(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
        }
    }
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.message)
    }
}

pub fn map_code(message: &str) -> i32 {
    if message.contains("reject") {
        2
    } else if message.contains("conf") || message.contains("input") {
        1
    } else {
        1
    }
}
