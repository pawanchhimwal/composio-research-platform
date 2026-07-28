"""Autonomous Research Agent powered by OpenAI Structured Outputs."""
import json
from openai import OpenAI
from config.settings import settings
from config.schema import ApplicationIntelligence
from utils.logger import get_logger

logger = get_logger()

class ResearchAgent:
    def __init__(self):
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your-openai-api-key-here":
            logger.warning("OPENAI_API_KEY is missing. Agent will fail if called.")
            self.client = None
        else:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def extract_intelligence(self, app_id: int, app_name: str, app_category: str, app_website: str, markdown_context: str) -> dict:
        """
        Uses OpenAI structured outputs to extract required metadata.
        We return a dict instead of the Pydantic model directly to allow the Orchestrator
        to validate it and manage the DB.
        """
        if not self.client:
            logger.error("Cannot extract intelligence without OpenAI API key.")
            return {}

        logger.info(f"Extracting intelligence for {app_name} using LLM...")

        system_prompt = (
            "You are an expert AI Automation Engineer researching developer APIs. "
            "Your job is to read the provided documentation and accurately extract structured metadata "
            "about the application. "
            "CRITICAL RULES:\n"
            "1. NEVER guess or hallucinate. If information is not in the text, return 'Unknown' or None.\n"
            "2. Ensure you provide Evidence mapping for EVERY important field you extract (auth, api_type, etc). "
            "The evidence URL MUST be an exact URL found in the text, and the reason must explain why it proves the claim.\n"
            "3. Provide a Confidence score (0-100) reflecting how explicit the documentation was."
        )

        user_prompt = (
            f"Application Name: {app_name}\n"
            f"Category: {app_category}\n"
            f"Website: {app_website}\n\n"
            f"--- Documentation Context ---\n"
            f"{markdown_context}\n\n"
            "Extract the intelligence."
        )

        try:
            # Note: For production with openai>=1.14.0, we would use the beta.chat.completions.parse 
            # or Instructor. But using simple json_schema format works too.
            # Here we use the Pydantic schema to define the required JSON schema.
            schema = ApplicationIntelligence.model_json_schema()
            
            response = self.client.chat.completions.create(
                model=settings.MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                # For forcing JSON matching the Pydantic schema:
                functions=[{
                    "name": "extract_app_intelligence",
                    "description": "Extract structured data",
                    "parameters": schema
                }],
                function_call={"name": "extract_app_intelligence"},
                temperature=0.1
            )
            
            result_str = response.choices[0].message.function_call.arguments
            return json.loads(result_str)
            
        except Exception as e:
            logger.error(f"LLM extraction failed for {app_name}: {e}")
            return {}
