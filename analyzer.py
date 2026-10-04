import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()

class PMAnalysis(BaseModel):
    category: str = Field(description="Category of update: e.g., Feature Release, Pricing Change, Positioning Shift, Infrastructure, or General Announcement")
    impact_level: str = Field(description="Strategic impact level: High, Medium, or Low")
    summary: str = Field(description="Concise 2 to 3 sentence product management summary of what changed and why it matters")
    key_takeaways: list[str] = Field(description="List of 2 to 3 bullet points highlighting core product changes")

def analyze_diff_content(diff_text: str, url: str) -> PMAnalysis:
    """
    Sends page diff text to Gemini Flash model and returns a structured PM analysis.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an expert Product Manager analyzing competitive intelligence updates.

    Target Website URL: {url}
    Raw Text Additions Detected:
    ----------------------------------------
    {diff_text}
    ----------------------------------------

    Analyze the text additions above and summarize the product update. If the additions are minor or formatting changes, note that accordingly.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": PMAnalysis,
        },
    )

    # Parse structured json response into Pydantic model
    analysis = PMAnalysis.model_validate_json(response.text)
    return analysis

if __name__ == "__main__":
    # Test with sample product release diff text
    sample_url = "https://github.com/readme"
    sample_diff = """
    + Added support for automatic AI pull request generation.
    + Integrated real-time security scanning directly into standard CI/CD pipelines.
    + Updated enterprise pricing tier to $21/user/month.
    """

    try:
        result = analyze_diff_content(sample_diff, sample_url)
        print("\n--- PM Analysis Output ---")
        print(f"Category: {result.category}")
        print(f"Impact Level: {result.impact_level}")
        print(f"Summary: {result.summary}")
        print("Key Takeaways:")
        for takeaway in result.key_takeaways:
            print(f" - {takeaway}")
        print("--------------------------")
    except Exception as e:
        print(f"Analysis failed: {e}")