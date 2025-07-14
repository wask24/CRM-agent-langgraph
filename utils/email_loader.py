# Import the DuckDB in-process SQL OLAP database engine
import duckdb

# Import standard typing utilities
from typing import List, Dict, Union
from datetime import datetime

# Load and transform nested email data from a JSON file using DuckDB
def load_emails_from_duckdb(db_path: str = ":memory:") -> List[dict]:
    # Connect to a DuckDB instance (in-memory by default)
    con = duckdb.connect(database=db_path)

    # Query to explode nested email threads (one row per message per deal)
    query = "SELECT deal_id, UNNEST(thread) AS message FROM read_json_auto('data/emails.json')"
    df = con.execute(query).fetchdf()

    # Group messages by deal_id to rebuild full conversation threads
    grouped: Dict[str, List[dict]] = {}
    for _, row in df.iterrows():
        deal_id = row["deal_id"]
        msg = row["message"]
        grouped.setdefault(deal_id, []).append(msg)

    # Return a list of dictionaries with deal_id and their associated thread
    return [{"deal_id": did, "thread": msgs} for did, msgs in grouped.items()]

# Parse a timestamp string (ISO 8601) into a Python datetime object
# Handles optional 'Z' (Zulu/UTC) time suffix
def parse_timestamp(ts: Union[str, datetime]) -> datetime:
    # Return directly if already a datetime object
    if isinstance(ts, datetime):
        return ts

    # Convert ISO timestamp string to datetime (handling 'Z' as UTC)
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))
