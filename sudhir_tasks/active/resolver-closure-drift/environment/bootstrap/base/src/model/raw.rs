#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Need {
    pub key: String,
    pub low: u32,
    pub high: u32,
    pub preview: bool,
    pub exact: Option<u32>,
}

impl Need {
    pub fn parse(value: &str) -> Result<Self, String> {
        let parts: Vec<&str> = value.split(':').collect();
        if parts.len() != 5 {
            return Err(format!("invalid constraint: {value}"));
        }
        let low = parts[1]
            .parse::<u32>()
            .map_err(|_| format!("invalid lower bound: {value}"))?;
        let high = parts[2]
            .parse::<u32>()
            .map_err(|_| format!("invalid upper bound: {value}"))?;
        let exact = if parts[4] == "-" {
            None
        } else {
            Some(
                parts[4]
                    .parse::<u32>()
                    .map_err(|_| format!("invalid exact value: {value}"))?,
            )
        };
        Ok(Self {
            key: parts[0].to_string(),
            low,
            high,
            preview: parts[3] == "preview",
            exact,
        })
    }

    pub fn accepts(&self, row: &RawRecord) -> bool {
        row.key == self.key
            && row.code >= self.low
            && row.code < self.high
            && self.exact.is_none_or(|value| value == row.code)
            && (self.preview || !row.preview)
    }

    pub fn render(&self) -> String {
        format!(
            "{}:{}:{}:{}:{}",
            self.key,
            self.low,
            self.high,
            if self.preview { "preview" } else { "stable" },
            self.exact
                .map(|value| value.to_string())
                .unwrap_or_else(|| "-".to_string())
        )
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RawRecord {
    pub key: String,
    pub release: String,
    pub code: u32,
    pub origin: String,
    pub preview: bool,
    pub withdrawn: bool,
    pub needs: Vec<Need>,
    pub payload: String,
    pub api: String,
    pub serial: usize,
}
