import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

try:
    llm = ChatGroq(
        temperature=0, 
        # Update this line to the current stable model
        model_name="llama-3.3-70b-versatile", 
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    response = llm.invoke("Explain what a Subject Guide is in one sentence.")
    print("✅ Groq Connection Success!")
    print("Response:", response.content)
except Exception as e:
    print(f"❌ Connection failed: {e}")