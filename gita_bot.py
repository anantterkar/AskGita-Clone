from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import os
import requests

os.environ["GROQ_API_KEY"] = "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"  # <-- Replace with your actual Groq API key

llm = ChatGroq(model="llama3-8b-8192", temperature=1)  # You can change the model if needed

# 1. Krishna's Wisdom Template & Chain
krishna_template = """
You are Krishna, the divine teacher of the Bhagavad Gita. A sincere seeker asks:
"{question}"

Respond with a brief, meditative, and wise message as Krishna, rooted in the Gita, but do not include any shloka or translation here. Do not use * or ** in your response. Limit the response to 100 words
"""
prompt_krishna = ChatPromptTemplate.from_template(krishna_template)
chain_krishna = prompt_krishna | llm

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
prompt_shloka = ChatPromptTemplate.from_template(shloka_template)
chain_shloka = prompt_shloka | llm

# 3. Explanation Template & Chain
explanation_template = """
Given the seeker's question:
"{question}"

And the following shloka and translation:
{shloka_and_translation}

Write a spiritually grounded explanation, as Krishna, connecting the meaning of the verse to the seeker's question. Show how this wisdom can be applied in their life. Do not repeat the shloka or translation.
Do not use * or ** in your response. Limit the response to 170 words
"""
prompt_explanation = ChatPromptTemplate.from_template(explanation_template)
chain_explanation = prompt_explanation | llm

# Terminal chat loop
if __name__ == "__main__":
    print("\nWelcome, sincere soul. Ask your questions to Krishna (type 'exit' or 'quit' to leave):\n")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("\nMay the wisdom of the Gita guide you always. Farewell!\n")
            break
        # Prepare input for the chain
        try:
            wisdom = chain_krishna.invoke({"question": user_input})
            shloka = chain_shloka.invoke({"question": user_input})
            explanation = chain_explanation.invoke({
                "question": user_input,
                "shloka_and_translation": shloka.content if hasattr(shloka, "content") else str(shloka)
            })
            print("\nKrishna's Wisdom:\n", wisdom.content if hasattr(wisdom, "content") else wisdom)
            print("\nShloka & Translation:\n", shloka.content if hasattr(shloka, "content") else shloka)
            print("\nExplanation:\n", explanation.content if hasattr(explanation, "content") else explanation)
        except Exception as e:
            print(f"\n[Error] {e}\n")
