# Type hints for structured typing and datetime operations
from typing import Dict, List, Union
from datetime import datetime
from statistics import median

# Import helper functions: tone detection and timestamp parser
from .tone import classify_tone
from .email_loader import parse_timestamp

# This function analyzes email threads for each deal to extract:
# - Median reply delay (in minutes)
# - Tone of the customer emails
# - Customer's contact email
# - Body of customer replies (thread)
def calculate_reply_info(email_data: List[dict], valid_deals: set) -> Dict[str, Dict[str, Union[float, List[str], str]]]:
    results = {}

    # Iterate through all email conversations
    for conv in email_data:
        deal_id = conv["deal_id"]

        # Skip non-urgent deals based on filtered valid_deals set
        if deal_id not in valid_deals:
            continue

        thread = conv["thread"]
        last_sent_by_ae = None  # Track last AE (account executive) timestamp
        gaps = []               # Stores reply delays in minutes
        bodies = []             # Stores customer message content

        # Loop through each message in the thread
        for msg in thread:
            sender = msg.get("from")
            ts = parse_timestamp(msg.get("ts", ""))

            # If AE sent the message, store the timestamp
            if sender == "ae@nudge.ai":
                last_sent_by_ae = ts
            else:
                # If it's a customer reply and there's a preceding AE message
                if last_sent_by_ae:
                    delta = (ts - last_sent_by_ae).total_seconds() / 60
                    if delta >= 0:
                        gaps.append(delta)  # Store reply delay
                body = msg.get("body", "").strip()
                if body:
                    bodies.append(body)  # Save the customer message
                last_sent_by_ae = None  # Reset after customer response

        # If the thread has at least one message body, process results
        if bodies:
            # Compute median reply delay, or None if empty
            median_reply = round(median(gaps), 2) if gaps else None

            # Estimate tone using the heuristic function
            tone = classify_tone(bodies)

            # Try to extract the customer's email address
            contact = next((msg.get("from") for msg in thread if msg.get("from") != "ae@nudge.ai"), None)

            # Store results for this deal_id
            results[deal_id] = {
                "median_reply": median_reply,
                "body_chain": bodies,
                "tone": tone,
                "contact": contact
            }

    # Return all processed deal insights
    return results
