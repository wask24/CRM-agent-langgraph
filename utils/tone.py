# Import the regex module for pattern matching (emojis)
import re

# Import type hinting for list of strings
from typing import List

# This function classifies the tone of a conversation thread (list of email bodies)
def classify_tone(bodies: List[str]) -> str:
    # Combine all customer email bodies into one text string
    all_text = " ".join(bodies)

    # Count how many exclamation marks are used
    exclam_count = all_text.count("!")

    # Count total number of characters (used to calculate rate of exclamation)
    char_count = len(all_text)

    # Define a basic emoji detection pattern using a Unicode emoji range
    emoji_pattern = re.compile(r"[😃-🙏🙂😉😊😎🥹😍🤔😭🤣🥰🤩🙃😡🥺😅😆😉🤗👍👎❤️💔🔥✨🎉]")

    # Count the number of emojis found in the text
    emoji_count = len(emoji_pattern.findall(all_text))

    # Apply tone classification heuristics:
    # Rule 1: if the message contains at least 2 emojis → it's casual
    if emoji_count >= 2:
        return "casual"

    # Rule 2: if more than 2% of the text are exclamation marks → casual
    if char_count > 0 and (exclam_count / char_count) > 0.02:
        return "casual"

    # Default rule: if neither applies → it's formal
    return "formal"
