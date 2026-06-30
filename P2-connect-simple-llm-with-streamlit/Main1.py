
# project connect to google ai studio llm (gemini-2.5-flash) and create user details  
# It user data is created, it can answer bsed on data avaiable thru LLM


import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load the API key from the .env file
load_dotenv()

def main():
    # 1. Initialize the Google AI Studio LLM (Gemini 2.5 Flash)
    # It automatically detects the GOOGLE_API_KEY from your environment variables
    print("Connecting to Google AI Studio...")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7
    )
    
    print("=" * 60)
    print("Gemini Q&A Terminal (Type 'exit' or 'quit' to stop)")
    print("=" * 60)
    
    # 2. Start a simple loop to ask questions
    while True:
        user_query = input("\nYou: ").strip()
        
        if user_query.lower() in ['exit', 'quit', 'q', '']:
            print("Goodbye!")
            break
            
        print("Gemini: Thinking...", end="\r")
        
        try:
            # Format the prompt using standard message structures
            messages = [
                SystemMessage(content="You are a clear, direct, and concise AI assistant."),
                HumanMessage(content=user_query)
            ]
            
            # Send query to Gemini
            response = llm.invoke(messages)
            
            # Print the text answer cleanly on the screen
            print(f"Gemini: {response.content}")
            
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please make sure your GOOGLE_API_KEY in the .env file is valid.")

if __name__ == "__main__":
    main()