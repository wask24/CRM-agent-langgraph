import os
import json
from agent import Nudge_Agent

if __name__ == "__main__":
    # Define the input question to prompt the agent
    question = "Which deals require urgent follow-up?"

    # Invoke the pre-configured agent with the input question
    response = Nudge_Agent.invoke({"input": question})

    # Verify the response is a dictionary and contains a list of messages
    if isinstance(response, dict) and "messages" in response:
        # Extract the last message from the agent's message history
        final_message = response["messages"][-1]

        # Check if the final message has a 'content' attribute (the text output)
        if hasattr(final_message, "content"):
            print("✅ Summary of Urgent Deals:\n")
            try:
                # Attempt to parse the content as JSON
                parsed = json.loads(final_message.content)
                # Pretty-print the parsed JSON to the console
                print(json.dumps(parsed, indent=2))

                # Ensure the output directory 'out' exists, create if missing
                os.makedirs("out", exist_ok=True)
                # Write the parsed JSON data to 'out/nudges.json' file
                with open("out/nudges.json", "w", encoding="utf-8") as f:
                    json.dump(parsed, f, indent=2)
                
                print("\n💾 Result saved to out/nudges.json")
            except json.JSONDecodeError:
                # If content is not valid JSON, just print the raw content
                print(final_message.content)
        else:
            # Warn if the final message lacks readable content
            print("⚠️ No readable output in final message.")
    else:
        # Handle unexpected or malformed responses
        print("⚠️ Unexpected response format:")
        print(response)
