
import json
import re


# Load FAQ dataset
with open("sample_faq.json", "r") as file:
    data = json.load(file)

greetings = data["greetings"]
faqs = data["faqs"]


# Display welcome message
def welcome():
    print("\n" + "=" * 45)
    print("       DATHEON CUSTOMER SUPPORT BOT")
    print("=" * 45)
    print("Bot: Hello! Welcome to Datheon Support.")
    print("Bot: How can I help you today?")
    print("Bot: Type 'bye', 'exit', or 'quit' to leave.\n")


# Identify greeting
def check_greeting(user_input):
    for greeting in greetings:
        pattern = r"\b" + re.escape(greeting) + r"\b"

        if re.search(pattern, user_input):
            return "Hello! How can I assist you today?"

    return None


# Identify FAQ intent
def check_faq(user_input):
    user_input = user_input.lower()

    # Business hours
    if re.search(r"\b(hours|timing|open|closed|working hours)\b", user_input):
        return faqs[0]["answer"]

    # Project submission
    if re.search(r"\b(submit|submission|project|github|repository)\b", user_input):
        return faqs[1]["answer"]

    # Certificate
    if re.search(r"\b(certificate|certification|certificates)\b", user_input):
        return faqs[2]["answer"]

    return None


# Handle multiple intents
def chatbot_response(user_input):
    user_input = user_input.lower().strip()

    if not user_input:
        return "Please enter something so I can help you."

    # Greeting response
    greeting_response = check_greeting(user_input)

    # FAQ response
    faq_response = check_faq(user_input)

    responses = []

    if greeting_response:
        responses.append(greeting_response)

    if faq_response:
        responses.append(faq_response)

    if responses:
        return "\n".join(responses)

    return (
        "Sorry, I couldn't understand your question. "
        "Please ask about business hours, project submission, "
        "or certificates."
    )


def main():
    welcome()

    while True:
        user_input = input("You: ").lower().strip()

        # Exit commands
        if re.fullmatch(r"(bye|exit|quit)", user_input):
            print("Bot: Thank you for contacting Datheon Support. Goodbye!")
            break

        response = chatbot_response(user_input)

        print("Bot:", response)
        print()


if __name__ == "__main__":
    main()
