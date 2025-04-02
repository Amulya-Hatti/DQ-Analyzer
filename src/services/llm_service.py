import json
import openai
from fastapi import HTTPException
from src.config.settings import settings

class LLMService:
    def __init__(self):
        self.client = openai.AzureOpenAI(
            azure_endpoint=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
            api_version="2024-02-01"
        )
    
    def generate_data_quality_rules(self, metadata_script):  
        """
        Calls Azure OpenAI API to generate data quality validation rules from dataset metadata.
        Ensures the output is in JSON format by explicitly instructing the model.
        """
        try:
            response = self.client.chat.completions.create(  
                model=settings.azure_deployment_name,  
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in data quality rule generation. Always return a valid JSON object with no extra text."
                        },
                        {
                        "role": "user",
                        "content": f"Based on the following dataset metadata, generate data quality validation rules. "
                                    f"For each column, suggest all applicable rules instead of just one. "
                                    f"Each rule should have a reason explaining why it is important. "
                                    f"Ensure the response is a properly formatted JSON object without extra text.\n\n"
                                    f"Metadata:\n{metadata_script}\n\n"
                                    f"Example JSON format:\n"
                                    f'{{"rules": ['
                                    f'{{"column": "email", "rules": ['
                                    f'{{"rule": "Must be a valid email format", "reason": "Ensures correct email format for contact purposes"}}, '
                                    f'{{"rule": "Cannot be null", "reason": "Email is mandatory for communication"}}]}}, '
                                    f'{{"column": "age", "rules": ['
                                    f'{{"rule": "Must be an integer", "reason": "Age should be stored as a whole number"}}, '
                                    f'{{"rule": "Must be between 18 and 99", "reason": "Age must be within reasonable human limits"}}]}}, '
                                    f'{{"column": "phone_number", "rules": ['
                                    f'{{"rule": "Must be a valid phone number format", "reason": "Ensures proper phone format for communication"}}, '
                                    f'{{"rule": "Must be exactly 10 digits", "reason": "Standardizes phone number length"}}]}}'
                                    f']}}'
                        }

                ],
                temperature=0.7
            )

            rules_text = response.choices[0].message.content.strip()

            try:
                rules_json = json.loads(rules_text)
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Invalid JSON response from OpenAI.")

            return rules_json

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
