# app/services/llm_service.py
import os
from dotenv import load_dotenv
from openai import OpenAI  # We will use the OpenAI client for OpenRouter

# Load environment variables from .env file
load_dotenv()

# Configure the OpenRouter API client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generate_article_content(topic: str, difficulty: str, audience: str):
    """
    Generates a structured educational article on a given topic using an LLM via OpenRouter.
    """
    
    # Define the system prompt for the LLM
    system_prompt = (
        "You are an expert educational writer. Your task is to create a structured, "
        "high-quality, and easy-to-understand educational article. The article should "
        "be in Markdown format and follow a specific structure."
    )

    # Construct the user prompt
    user_prompt = (
        f"Generate a structured educational article on the topic of '{topic}'. "
        "The article should be approximately 800-1500 words long. "
        f"The content should be at a '{difficulty}' level, tailored for a '{audience}' audience. "
        "The article must follow this exact structure:\n\n"
        "## Title\n\n"
        "### Introduction\n\n"
        "### Main Sections\n"
        "- Create 3 to 5 main sections with clear headings (use '##' for main sections, '###' for subsections).\n"
        "- Each section must contain bullet points (`*`) or numbered lists (`1.`).\n"
        "- Include at least one practical example per section to illustrate concepts.\n\n"
        "### Summary / Key Takeaways\n"
        "- List 3 to 5 key points in bullet points (`*`).\n\n"
        "### Suggested Further Reading\n"
        "- List 3 to 5 relevant sources (e.g., books, academic papers, reputable websites)."
    )

    try:
        # Use the configured OpenRouter client
        completion = client.chat.completions.create(
            # Use the specified DeepSeek model
            model="deepseek/deepseek-r1-0528:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        # The generated content is in the message object
        article_content = completion.choices[0].message.content
        return {"article": article_content}
        
    except Exception as e:
        print(f"An error occurred with the OpenRouter API: {e}")
        return {"error": "Failed to generate article content. Please check your API key or try again later."}