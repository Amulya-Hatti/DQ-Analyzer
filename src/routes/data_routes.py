from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import pandas as pd
import io
from src.services.data_processing import generate_metadata, format_metadata_script
from src.services.llm_service import LLMService
#from src.config.firebase.firebase_auth import verify_firebase_token  

router = APIRouter()
llm_service = LLMService()

@router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    """Upload and process CSV - Requires authentication"""
    try:
        
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents), low_memory=False)

       
        metadata = generate_metadata(df)
        metadata_script = format_metadata_script(metadata)

        
        rules = llm_service.generate_data_quality_rules(metadata_script)

        
        business_summary = {
            "dataset_name": file.filename,
            "total_columns": df.shape[1],
            "total_rows": df.shape[0],
            "complete_records_percentage": round((df.dropna().shape[0] / df.shape[0]) * 100, 2),
            "duplicate_records_percentage": round(df.duplicated().mean() * 100, 2),
            "rule_coverage_percentage": round((len(rules.get("rules", [])) / df.shape[1]) * 100, 2)
        }

        return {"business_summary": business_summary, "generated_rules": rules}

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Empty CSV file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
