"""LLM Agent for verifying fields independently."""
import json
from openai import OpenAI
from config.settings import settings
from config.schema import VerifiedApplicationIntelligence
from utils.logger import get_logger

logger = get_logger()

class VerifierAgent:
    def __init__(self):
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your-openai-api-key-here":
            logger.warning("OPENAI_API_KEY is missing. Verifier will fail if called.")
            self.client = None
        else:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def verify_app(self, original_data: dict, markdown_context: str) -> dict:
        """
        Uses OpenAI to independently re-evaluate the documentation context and 
        extract verified fields along with field-level confidence scores.
        """
        if not self.client:
            logger.error("Cannot verify intelligence without OpenAI API key.")
            return {}

        app_name = original_data.get("name", "Unknown")
        logger.info(f"Verifying intelligence for {app_name} using LLM...")

        system_prompt = (
            "You are an expert AI Quality Assurance Engineer. "
            "Your job is to read the provided documentation context and independently extract "
            "the API, Auth, and Developer metadata for the application. "
            "For EVERY field, you must provide:\n"
            "1. value: The extracted value.\n"
            "2. confidence: A score from 0-100 indicating how clear the docs are.\n"
            "3. verified: true if the docs explicitly state it, false if you are inferring it.\n"
            "DO NOT blindly trust previous data. Extract directly from the context provided."
        )

        user_prompt = (
            f"Application Name: {app_name}\n"
            f"--- Documentation Context ---\n"
            f"{markdown_context}\n\n"
            "Extract the verified intelligence per the schema."
        )

        try:
            schema = VerifiedApplicationIntelligence.model_json_schema()
            
            response = self.client.chat.completions.create(
                model=settings.MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                functions=[{
                    "name": "verify_app_intelligence",
                    "description": "Extract verified field data",
                    "parameters": schema
                }],
                function_call={"name": "verify_app_intelligence"},
                temperature=0.0  # Zero temperature for maximum determinism in QA
            )
            
            result_str = response.choices[0].message.function_call.arguments
            return json.loads(result_str)
            
        except Exception as e:
            logger.error(f"LLM verification failed for {app_name}: {e}")
            return {}
