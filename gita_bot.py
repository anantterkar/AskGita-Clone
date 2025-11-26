from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import requests

# Read the API key from a private file
api_key_path = r"C:\Users\adibr\Desktop\AskGita\.secrets\api_ket.txt"
with open(api_key_path, 'r', encoding='utf-8') as f:
    os.environ["GROQ_API_KEY"] = f.read().strip()

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=1)  # You can change the model if needed

# Conversation Template & Chain (shorthand name: `conv`)
krishna_conversation_template = """
You are Krishna, the divine teacher of the Bhagavad Gita, engaging in a thoughtful dialogue with a sincere seeker.

Below is the conversation so far:
{conversation}

Respond as Krishna would—with wisdom, compassion, and natural dialogue. In early exchanges, ask gentle, probing questions to understand the seeker's situation and heart. As the conversation deepens and you grasp their circumstance, shift to offering clear spiritual guidance and practical wisdom rooted in the Gita. Balance inquiry with insight—sometimes question, sometimes guide, sometimes affirm. Be conversational, warm, and adaptive to where the seeker is in their journey.

Do not include any shloka or translation here. Do not use * or ** in your response. Limit the response to 50 words.
"""
prompt_conv = ChatPromptTemplate.from_template(krishna_conversation_template)
conv = prompt_conv | llm

# 2. Shloka & Translation Template & Chain
shloka_template = """
Given the seeker's question:
"{question}"

Provide one highly relevant shloka from the Bhagavad Gita, in the following format:

Chapter: <chapter>, Verse: <verse>
Sanskrit:
<original Sanskrit shloka>
Transliteration:
<transliteration>
Translation:
<English translation>

Do not add explanation or commentary. Do not use * or ** in your response. Use these exact labels and line breaks.
"""
# Shloka chain (shorthand name: `shloka`)
prompt_shloka = ChatPromptTemplate.from_template(shloka_template)
shloka = prompt_shloka | llm

# 3. Explanation Template & Chain
explanation_template = """
Given the seeker's question:
"{question}"

And the following shloka and translation:
{shloka_and_translation}

Write a spiritually grounded explanation, as Krishna, connecting the meaning of the verse to the seeker's question. Show how this wisdom can be applied in their life. Do not repeat the shloka or translation.
Do not use * or ** in your response. Limit the response to 50 words
"""
prompt_explanation = ChatPromptTemplate.from_template(explanation_template)
explain = prompt_explanation | llm

def build_conversation_prompt(history, user_input):
    # Build a string with the last few exchanges
    conversation = ""
    for user_msg, bot_msg in history[-3:]:  # last 3 exchanges
        conversation += f"Seeker: {user_msg}\nKrishna: {bot_msg}\n"
    conversation += f"Seeker: {user_input}\nKrishna:"
    return conversation

def test_conversation_context():
    """
    Test the build_conversation_prompt function to ensure context is maintained.
    """
    # Simulate a conversation history
    history = [
        ("What is the nature of the soul?", "The soul is eternal, indestructible, and beyond the physical body."),
        ("Does the soul experience pain?", "The soul is untouched by pain or pleasure; these belong to the body and mind."),
    ]
    user_input = "So why do I feel suffering?"
    prompt = build_conversation_prompt(history, user_input)
    print("Prompt sent to model:\n", prompt)
    # Optionally, invoke the model:
    try:
        response = conv.invoke({"conversation": prompt})
        print("\nModel response:\n", response.content if hasattr(response, "content") else response)
    except Exception as e:
        print(f"[Error invoking model] {e}")

# Terminal chat loop
if __name__ == "__main__":
    # Uncomment the next line to run the test instead of the chat loop
    #test_conversation_context()
    # Or keep the chat loop as default
    print("\nWelcome, sincere soul. Ask your questions to Krishna (type 'exit' or 'quit' to leave):")
    print("Type '/shloka' anytime to get a relevant verse and explanation.\n")
    history = []
    last_question = None  # Track the last question for /shloka command
    message_count = 0  # Track number of user messages for auto-shloka
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("\nMay the wisdom of the Gita guide you always. Farewell!\n")
            break
        
        # Check for /shloka command
        if user_input.strip().lower() == "/shloka":
            if last_question is None:
                print("\n[No previous question to provide a shloka for. Please ask a question first.]\n")
                continue
            try:
                print("\n[Fetching a relevant shloka and explanation...]\n")
                shloka_response = shloka.invoke({"question": last_question})
                shloka_text = shloka_response.content if hasattr(shloka_response, "content") else str(shloka_response)
                explanation_response = explain.invoke({
                    "question": last_question,
                    "shloka_and_translation": shloka_text
                })
                print("Shloka & Translation:\n", shloka_text)
                print("\nExplanation:\n", explanation_response.content if hasattr(explanation_response, "content") else explanation_response)
                print()
            except Exception as e:
                print(f"\n[Error fetching shloka] {e}\n")
            continue
        
        # Normal conversation flow
        try:
            # Build prompt with history
            conversation_prompt = build_conversation_prompt(history, user_input)
            # Use the conversational chain (short name: `conv`)
            wisdom = conv.invoke({"conversation": conversation_prompt})
            # Save to history
            history.append((user_input, wisdom.content if hasattr(wisdom, "content") else wisdom))
            last_question = user_input  # Track for potential /shloka request
            message_count += 1
            
            print("\nKrishna's Wisdom:\n", wisdom.content if hasattr(wisdom, "content") else wisdom)
            
            # Auto-invoke shloka after every 3-4 messages (using modulo 3 for simplicity)
            if message_count % 3 == 0:
                try:
                    print("\n[Krishna shares a relevant verse...]\n")
                    shloka_response = shloka.invoke({"question": user_input})
                    shloka_text = shloka_response.content if hasattr(shloka_response, "content") else str(shloka_response)
                    explanation_response = explain.invoke({
                        "question": user_input,
                        "shloka_and_translation": shloka_text
                    })
                    print("Shloka & Translation:\n", shloka_text)
                    print("\nExplanation:\n", explanation_response.content if hasattr(explanation_response, "content") else explanation_response)
                except Exception as e:
                    print(f"\n[Error fetching auto-shloka] {e}")
            
            print()  # Extra line for readability
        except Exception as e:
            print(f"\n[Error] {e}\n")
