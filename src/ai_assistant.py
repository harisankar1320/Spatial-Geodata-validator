from google import genai

client = genai.Client(api_key="AQ.Ab8RN6JK4kDNb7StsWx0UvdYQw7dAFcfNMV5aRkq3ngoJVv2EA")

def ask_assistant(question, data_summary):
    prompt = f"""
    You are a GIS data assistant. 
    Only answer based on the data provided below. 
    Do not guess or make up information.
    
    Data summary:
    {data_summary}
    
    User question: {question}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text