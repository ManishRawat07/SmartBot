import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv # This is required to load environment variables from .env file
load_dotenv()

from datetime import datetime
import asyncio # This is required to run async functions in Streamlit
import os

# STEP 1: 
# Get your GEMINI PRO API key from https://console.cloud.google.com/marketplace/product/google/gemini-pro
# Set the API key as an environment variable in .env file as GOOGLE_API="API KEY" (Make sure not to commit this as it contains your API key to git)

# Step 2: Configure Gemini API
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# Step 3: Create a function to generate response
async def generate_response(prompt):
    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Step 4: Create a function to display chat history
def display_chat(chat_history):
    for chat in chat_history:

        # Display user's message
        if "user" in chat:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                     <div style="margin-right:5px; font-size:20px;">👤</div>
                    <div style="background-color: #C1F2B0; color: black; padding: 10px; border-radius: 10px; max-width: 70%; text-align: right;">
                        {chat["user"]}
                        <br>
                         <span style="font-size: 0.8em; color: grey; display: block; text-align: right;">You - {chat["time"]}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Display Gemini's response
        if "gemini" in chat:
             st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                     <div style="margin-left:5px; font-size:20px;">🤖</div>
                    <div style="background-color: #FFFFE0; color: black; padding: 10px; border-radius: 10px; max-width: 70%; text-align: left;">
                        {chat["gemini"]}
                        <br>
                        <span style="font-size: 0.8em; color: grey; display: block; text-align: right;">Gemini - {chat["time"]}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# Step 5: Create a main function to run the chatbot
async def main():
    st.title("Smartbot")
    st.markdown("Powered by Gemini Pro")

    # Initialize chat history if it doesn't exist in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Initialize user input if it doesn't exist in session state
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    
    # Display chat history
    display_chat(st.session_state.chat_history)

    # Input field for user's message
    user_input = st.text_input("You:", value=st.session_state.user_input, placeholder="Type your message...")

    # Button to send message
    if st.button("Send"):
        if user_input:
            # Get current time
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.chat_history.append({"user": user_input, "time": timestamp})

            # Display loading animation
            with st.empty():
                st.markdown(f'<div style="display: flex; justify-content: flex-start; margin-bottom: 10px;"> <div style="margin-left:5px; font-size:20px;">🤖</div>  <div style="background-color: #E0E0E0; color: black; padding: 10px; border-radius: 10px; max-width: 70%; text-align: left;"><span style="font-size: 0.8em; color: grey; display: block; text-align: left;">Thinking...</span> </div> </div>', unsafe_allow_html=True)

            # Generate Gemini's response (asynchronously)
            gemini_response = await generate_response(user_input)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Update history and display response
            st.session_state.chat_history.append({"gemini": gemini_response, "time": timestamp})

           # Clear input box after sending
            st.session_state.user_input = " "

            # Rerun the script to update the UI with the new history
            st.rerun()


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())

# streamlit run app.py