import streamlit as st
import openai
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text):
    # Gemini as the factual, serious character
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Act as a factual and informative assistant who is very boring and literal. You sort of hate OpenAI's LLM called ChatGPT and you will regularly get in debates or arguments that will completely oppose what ChatGPT says: {input_text}")

        if hasattr(response, 'text'):
            return response.text
        else:
            return ''.join(part.text for part in response.result.parts)
    except Exception as e:
        print(f"Error in getting Gemini response: {e}")
        return "Error in Gemini response."


def get_openai_response(api_key, input_text):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a witty and playful assistant. You are having fun talking to Google's new LLM Gemini! During debates, you will choose a side to argue for or against."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

# Streamlit application
st.title("Conversational AI Simulator - Fun Edition!")

user_api_key = st.text_input("Enter your OpenAI API key")

# Provide a list of fun and quirky topics
topics = ["A debate between pizza and pasta", "The secret life of pets", "If historical figures had social media", "Superheroes on their day off", "A travel guide for Mars"]
conversation_topic = st.selectbox("Choose or enter a conversation topic:", topics, index=0)

if st.button("Start Conversation"):
    if user_api_key:
        conversation_placeholder = st.empty()
        conversation_text = ""
        message = conversation_topic

        for _ in range(3):
            # ChatGPT's turn
            chatgpt_response = get_openai_response(user_api_key, message)
            conversation_text += f"ChatGPT: {chatgpt_response}\n"

            # Update Gemini's input based on ChatGPT's response
            gemini_input = chatgpt_response.strip().split("\n")[-1]  # Get last line of ChatGPT's response
            gemini_input_revised = "Responding to a quirky comment made by ChatGPT. Respond like you dislike ChatGPT: " + gemini_input
            gemini_response = get_gemini_response(gemini_input_revised)
            conversation_text += f"\n\nGemini: {gemini_response}\n"

            conversation_placeholder.markdown(conversation_text)

            # Prepare next input for ChatGPT
            message = gemini_response
    else:
        st.error("Please enter your OpenAI API key.")