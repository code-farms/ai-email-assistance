from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

async def summarize_email(content: str) -> str:
    prompt = f'''
        You are an assistant that writes crisp, professional email summaries.

        INSTRUCTIONS:
        • Write 3–6 bullet points that capture the key information and required actions.
        • Use plain language suitable for a non-technical reader.
        • Omit greetings, signatures, and trivial details.
        • Preserve any dates, numbers, or commitments exactly as written.
        • Do NOT add opinions or explanations beyond the summary.

        EXAMPLE:
        EMAIL:
        """
        Dear Manager,

        I will be on leave from 12th to 16th June due to a family emergency. I've informed the team and completed my pending tasks. Please approve my leave request.

        Best,
        Alice
        """

        SUMMARY:
        • Request for leave from 12th to 16th June  
        • Reason: Family emergency  
        • Pending tasks completed  
        • Team has been informed  
        • Awaiting leave approval  

        EMAIL TO SUMMARIZE:
        """
        {content}
        """

        SUMMARY:
    '''
    
    responses = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=350,
    )
    return responses.choices[0].message.content

