from src.services.llm_service import LLMService
from src.config.settings import settings

class SQLQueryGenerator:
    def __init__(self):
        self.llm_service = LLMService()
    
    def generate_validation_query(self, table_name, column_name, rule_text, table_schema=None):
        """
        Generate an SQL query to validate a data quality rule
        
        Args:
            table_name: Name of the table to validate
            column_name: Name of the column to validate 
            rule_text: The text description of the rule
            table_schema: Optional schema information to help with query generation
            
        Returns:
            SQL query string to identify records failing the validation
        """
        # Construct the prompt for the LLM
        prompt = f"""
        Generate an SQL query to identify records that violate the following data quality rule:
        
        Table: {table_name}
        Column: {column_name}
        Rule: {rule_text}
        
        """
        
        # Add schema information if available
        if table_schema:
            prompt += f"\nTable Schema:\n{table_schema}\n"
        
        prompt += """
        The SQL query should:
        1. Return only the records that FAIL the validation rule
        2. Include all columns from the original table in the result
        3. Be optimized for SQLite syntax
        4. Only return the SQL query as plain text. Do NOT include a semicolon at the end or any markdown (no ```sql).
        """
        
        # Call the LLM service - use the Azure deployment name from settings
        try:
            response = self.llm_service.client.chat.completions.create(
                model=settings.azure_deployment_name,  # Use the deployment name from settings
                messages=[
                    {"role": "system", "content": "You are an expert in SQL query generation. Always return only the SQL query without any explanations or comments."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
           
            sql_query = response.choices[0].message.content.strip()
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            # sql_query = sql_query.rstrip(';') 

            
            return sql_query
        
        except Exception as e:
            raise Exception(f"Error generating SQL validation query: {str(e)}")