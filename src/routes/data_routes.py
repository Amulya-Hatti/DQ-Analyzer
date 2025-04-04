# from fastapi import APIRouter, HTTPException, Depends, Query
# from typing import List
# from src.services.data_processing import generate_metadata, format_metadata_script
# from src.services.llm_service import LLMService
# from src.services.db_service import DatabaseService
# from src.config.firebase.firebase_auth import verify_firebase_token

# router = APIRouter()
# llm_service = LLMService()
# db_service = DatabaseService()

# @router.get("/tables/")
# async def get_database_tables():
#     """Get list of all tables in the SQLite database"""
#     try:
#         tables = db_service.get_tables()
#         return {"tables": tables}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/analyze-table/")
# async def analyze_table(table_name: str = Query(..., description="Name of the table to analyze")):
#     """Analyze a specific table and generate data quality rules"""
#     try:
#         # Get table data as DataFrame
#         df = db_service.get_table_data(table_name)
        
#         # Generate metadata and format it
#         metadata = generate_metadata(df)
#         metadata_script = format_metadata_script(metadata)
        
#         # Generate rules using LLM
#         rules = llm_service.generate_data_quality_rules(metadata_script)
        
#         # Create business summary
#         business_summary = {
#             "dataset_name": table_name,
#             "total_columns": df.shape[1],
#             "total_rows": df.shape[0],
#             "complete_records_percentage": round((df.dropna().shape[0] / df.shape[0]) * 100, 2),
#             "duplicate_records_percentage": round(df.duplicated().mean() * 100, 2),
#             "rule_coverage_percentage": round((len(rules.get("rules", [])) / df.shape[1]) * 100, 2)
#         }
        
#         return {"business_summary": business_summary, "generated_rules": rules}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from src.services.data_processing import generate_metadata, format_metadata_script
from src.services.llm_service import LLMService
from src.services.db_service import DatabaseService
from src.services.sql_generator import SQLQueryGenerator
from src.config.firebase.firebase_auth import verify_firebase_token

router = APIRouter()
llm_service = LLMService()
db_service = DatabaseService()
sql_generator = SQLQueryGenerator()

@router.get("/tables/")
async def get_database_tables():
    """Get list of all tables in the SQLite database"""
    try:
        tables = db_service.get_tables()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/analyze-table/")
async def analyze_table(table_name: str = Query(..., description="Name of the table to analyze")):
    """Analyze a specific table and generate data quality rules"""
    try:
        # Get table data as DataFrame
        df = db_service.get_table_data(table_name)
        
        # Generate metadata and format it
        metadata = generate_metadata(df)
        metadata_script = format_metadata_script(metadata)
        
        # Generate rules using LLM
        rules = llm_service.generate_data_quality_rules(metadata_script)
        
        # Create business summary
        business_summary = {
            "dataset_name": table_name,
            "total_columns": df.shape[1],
            "total_rows": df.shape[0],
            "complete_records_percentage": round((df.dropna().shape[0] / df.shape[0]) * 100, 2),
            "duplicate_records_percentage": round(df.duplicated().mean() * 100, 2),
            "rule_coverage_percentage": round((len(rules.get("rules", [])) / df.shape[1]) * 100, 2)
        }
        
        # Store rules and generate SQL in separate step - not automatically
        # to avoid overwhelming initial analysis
        
        return {"business_summary": business_summary, "generated_rules": rules}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
