# Import pandas for CSV and DataFrame manipulation
import pandas as pd

# Import datetime for timestamp comparison
from datetime import datetime

# Type hints for clean return signatures
from typing import List, Dict, Union

# This function analyzes CRM data from a CSV file
# It identifies deals that are idle for >7 days and have high urgency
def calculate_urgent_deals(csv_path: str) -> List[Dict[str, Union[str, float]]]:
    # Load CRM data from a CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Ensure 'amount_eur' is treated as float by removing spaces and casting
    df['amount_eur'] = (
        df['amount_eur']
        .astype(str)
        .str.replace(' ', '', regex=False)
        .astype(float)
    )

    # Parse the 'last_activity' timestamp to datetime objects with timezone
    df['last_activity'] = pd.to_datetime(df['last_activity'], utc=True)

    # Get the current UTC datetime to compute inactivity duration
    now = datetime.now(tz=df['last_activity'].dt.tz)

    # Calculate number of days since the last activity (idle period)
    df['idle_days'] = (now - df['last_activity']).dt.days

    # Filter out deals that have been idle 7 days or fewer
    df = df[df['idle_days'] > 7]

    # Compute urgency score = idle_days × (amount_eur / 1000)
    df['urgency'] = df['idle_days'] * (df['amount_eur'] / 1000)

    # Keep only deals where urgency > 250
    urgent_df = df[df['urgency'] > 250]

    # Return a list of dictionaries containing deal_id and urgency
    return urgent_df[['deal_id', 'urgency']].to_dict(orient='records')
