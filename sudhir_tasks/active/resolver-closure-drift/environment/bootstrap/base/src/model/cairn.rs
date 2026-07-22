#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Cairn<T> {
    pub nodes: Vec<T>,
    pub edges: Vec<(String, String)>,
}

impl<T> Cairn<T> {
    pub fn new(nodes: Vec<T>, edges: Vec<(String, String)>) -> Self {
        Self { nodes, edges }
    }
}
