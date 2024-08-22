from functools import lru_cache

import pandas as pd


@lru_cache(maxsize=2)
def load_csv(file_path: str) -> pd.DataFrame:
    """Load and cache a CSV file."""
    return pd.read_csv(file_path, sep="\t")
