pub(crate) type AppResult<T> = Result<T, String>;

pub(crate) fn with_path(action: &str, path: &std::path::Path, error: impl std::fmt::Display) -> String {
    format!("{action} {}: {error}", path.display())
}
