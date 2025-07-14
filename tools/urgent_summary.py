from langchain_core.tools import tool
# Import helper functions for CRM, email loading, tone detection, and reply analysis
from utils.crm import calculate_urgent_deals
from utils.email_loader import load_emails_from_duckdb, parse_timestamp
from utils.tone import classify_tone
from utils.replies import calculate_reply_info

# Register this function as a LangChain tool
@tool
def urgent_deal_summary() -> str:
    """
    Returns a summary of urgent deals with:
    - urgency score
    - median reply time
    - customer's tone
    - contact email
    - full chain of customer messages
    This output is formatted for display, not for structured data consumption.
    """
    # Step 1: Load urgent deals based on CSV data (idle_days > 7, urgency > 250)
    urgent_deals = calculate_urgent_deals("data/crm_events.csv")
    # Step 2: Extract deal IDs for filtering email data
    urgent_ids = {d['deal_id'] for d in urgent_deals}
    # Step 3: Load email threads from JSON via DuckDB
    email_data = load_emails_from_duckdb()
    # Step 4: Compute reply statistics, tone, and contact info
    reply_info = calculate_reply_info(email_data, urgent_ids)
    # Step 5: Format the result as a human-readable string
    output = []
    for item in urgent_deals:
        deal_id = item["deal_id"]
        # Skip if no reply info was found for this deal
        if deal_id not in reply_info:
            continue
        score = item["urgency"]
        # Only show urgency score if > 250, otherwise don't show the urgency field
        display_urgency = score if score > 250 else None
        
        info = reply_info[deal_id]
        median_reply = info.get("median_reply")
        bodies = info.get("body_chain", [])
        tone = info.get("tone", "unknown")
        contact = info.get("contact", "null")
        # Format each deal into a block of lines
        lines = [f"Deal {deal_id}:"]
        
        # Only add urgency line if score > 250
        if display_urgency is not None:
            lines.append(f"  Urgency: {display_urgency:.2f}")
            
        lines.extend([
            f"  Median reply: {median_reply} minutes",
            f"  Tone: {tone}",
            f"  Contact: {contact}",
            "  Bodies chain:"
        ])
        lines += [f"    {idx+1}. {body}" for idx, body in enumerate(bodies)]
        output.append("\n".join(lines))
    # Join all blocks into a final string
    return "\n\n".join(output)