import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_linkedin_post(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # Fast, high-quality Groq model
            messages=[
                {"role": "system", "content": "You are a LinkedIn personal branding expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print("🔥 Groq API ERROR:", e)
        return f"❌ Error: {str(e)}"
