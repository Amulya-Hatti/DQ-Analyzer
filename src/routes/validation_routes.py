# from fastapi import APIRouter, HTTPException, Depends, Path, Query, Body
# from typing import List, Dict, Any, Optional

# import pandas as pd
# from src.services.db_service import DatabaseService
# from src.services.sql_generator import SQLQueryGenerator

# validation_router = APIRouter()
# db_service = DatabaseService()
# sql_generator = SQLQueryGenerator()

# @validation_router.post("/store-rules/")
# async def store_validation_rules(
#     table_name: str = Query(..., description="Name of the table to store rules for"),
#     rules_data: Dict[str, Any] = Body(..., description="Generated rules data")
# ):
#     """Store generated validation rules in the database"""
#     try:
#         last_id = db_service.store_validation_rules(table_name, rules_data)
#         return {"message": "Rules stored successfully", "rules_count": len(rules_data.get("rules", []))}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @validation_router.get("/rules/")
# async def get_validation_rules(
#     table_name: Optional[str] = Query(None, description="Filter by table name"),
#     column_name: Optional[str] = Query(None, description="Filter by column name")
# ):
#     """Get stored validation rules with optional filtering"""
#     try:
#         rules = db_service.get_validation_rules(table_name, column_name)
#         return {"rules": rules}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @validation_router.post("/generate-sql/{rule_id}")
# async def generate_sql_for_rule(
#     rule_id: int = Path(..., description="ID of the rule to generate SQL for")
# ):
#     """Generate SQL validation query for a specific rule"""
#     try:
#         # Get the rule details
#         rules = db_service.get_validation_rules()
#         rule = next((r for r in rules if r["id"] == rule_id), None)
        
#         if not rule:
#             raise HTTPException(status_code=404, detail="Rule not found")
        
#         # Get table schema to help with SQL generation
#         table_name = rule["table_name"]
#         df = db_service.get_table_data(table_name)
#         schema_info = "\n".join([f"{col} ({df[col].dtype})" for col in df.columns])
        
#         # Generate SQL query
#         sql_query = sql_generator.generate_validation_query(
#             table_name=rule["table_name"],
#             column_name=rule["column_name"],
#             rule_text=rule["rule_text"],
#             table_schema=schema_info
#         )
        
#         # Update the rule with the generated SQL
#         db_service.update_rule_sql_query(rule_id, sql_query)
        
#         return {
#             "rule_id": rule_id,
#             "table_name": rule["table_name"],
#             "column_name": rule["column_name"],
#             "rule_text": rule["rule_text"],
#             "generated_sql": sql_query
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @validation_router.post("/run-validation/{rule_id}")
# async def run_validation_for_rule(
#     rule_id: int = Path(..., description="ID of the rule to run validation for")
# ):
#     """Run validation for a specific rule and store results"""
#     try:
#         # Get the rule details
#         rules = db_service.get_validation_rules()
#         rule = next((r for r in rules if r["id"] == rule_id), None)
        
#         if not rule:
#             raise HTTPException(status_code=404, detail="Rule not found")
        
#         if not rule["sql_query"]:
#             raise HTTPException(status_code=400, detail="SQL query not generated for this rule yet")
        
#         # Run the validation
#         validation_result = db_service.run_validation_query(rule_id, rule["sql_query"])
        
#         return {
#             "rule_id": rule_id,
#             "table_name": rule["table_name"],
#             "column_name": rule["column_name"],
#             "rule_text": rule["rule_text"],
#             "validation_result": validation_result
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @validation_router.get("/dashboard-data/")
# async def get_dashboard_data(
#     table_name: Optional[str] = Query(None, description="Filter by table name")
# ):
#     """Get aggregated data for the dashboard"""
#     try:
#         conn = db_service.get_connection()
        
#         # Query to get rule statistics
#         query = """
#         SELECT 
#             r.table_name,
#             COUNT(DISTINCT r.column_name) as columns_with_rules,
#             COUNT(r.id) as total_rules,
#             SUM(CASE WHEN r.sql_query IS NOT NULL THEN 1 ELSE 0 END) as rules_with_sql,
#             AVG(CASE WHEN vr.pass_count + vr.fail_count > 0 
#                 THEN (vr.pass_count * 100.0 / (vr.pass_count + vr.fail_count)) 
#                 ELSE NULL END) as avg_compliance_rate
#         FROM 
#             data_validation_rules r
#         LEFT JOIN (
#             SELECT 
#                 rule_id, 
#                 MAX(validation_date) as latest_date
#             FROM 
#                 data_validation_results
#             GROUP BY 
#                 rule_id
#         ) latest ON r.id = latest.rule_id
#         LEFT JOIN 
#             data_validation_results vr ON latest.rule_id = vr.rule_id AND latest.latest_date = vr.validation_date
#         """
        
#         if table_name:
#             query += f" WHERE r.table_name = '{table_name}'"
            
#         query += " GROUP BY r.table_name"
        
#         df = pd.read_sql_query(query, conn)
        
#         # Query to get recent validation results
#         recent_results_query = """
#         SELECT 
#             r.id as rule_id,
#             r.table_name,
#             r.column_name,
#             r.rule_text,
#             vr.validation_date,
#             vr.pass_count,
#             vr.fail_count,
#             (vr.pass_count * 100.0 / (vr.pass_count + vr.fail_count)) as compliance_rate
#         FROM 
#             data_validation_results vr
#         JOIN 
#             data_validation_rules r ON vr.rule_id = r.id
#         ORDER BY 
#             vr.validation_date DESC
#         LIMIT 10
#         """
        
#         recent_results_df = pd.read_sql_query(recent_results_query, conn)
        
#         return {
#             "table_summaries": df.to_dict('records'),
#             "recent_validations": recent_results_df.to_dict('records')
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


from fastapi import APIRouter, HTTPException, Depends, Query, Body, Path
from typing import List, Dict, Any, Optional
from src.services.db_service import DatabaseService
from src.services.sql_generator import SQLQueryGenerator
import pandas as pd
import numpy as np

validation_router = APIRouter()
db_service = DatabaseService()
sql_generator = SQLQueryGenerator()


def convert_numpy_types(obj):
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(i) for i in obj]
    else:
        return obj



@validation_router.post("/store-rules/")
async def store_validation_rules(
    table_name: str = Query(..., description="Name of the table to store rules for"),
    rules_data: Dict[str, Any] = Body(..., description="Generated rules data")
):
    """Store generated validation rules in the database"""
    try:
        last_id = db_service.store_validation_rules(table_name, rules_data)
        return {"message": "Rules stored successfully", "rules_count": len(rules_data.get("rules", []))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    



@validation_router.get("/rules/")
async def get_validation_rules(
    table_name: Optional[str] = Query(None, description="Filter by table name"),
    column_name: Optional[str] = Query(None, description="Filter by column name")
):
    """Get stored validation rules with optional filtering"""
    try:
        rules = db_service.get_validation_rules(table_name, column_name)
        return {"rules": rules}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@validation_router.post("/generate-sql/{rule_id}")
async def generate_sql_for_rule(
    rule_id: int = Path(..., description="ID of the rule to generate SQL for")
):
    """Generate SQL validation query for a specific rule"""
    try:
        # Get the rule details
        rules = db_service.get_validation_rules()
        rule = next((r for r in rules if r["id"] == rule_id), None)
        
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        
        # Get table schema to help with SQL generation
        table_name = rule["table_name"]
        df = db_service.get_table_data(table_name)
        schema_info = "\n".join([f"{col} ({df[col].dtype})" for col in df.columns])
        
        # Generate SQL query
        sql_query = sql_generator.generate_validation_query(
            table_name=rule["table_name"],
            column_name=rule["column_name"],
            rule_text=rule["rule_text"],
            table_schema=schema_info
        )
        
        # Update the rule with the generated SQL
        db_service.update_rule_sql_query(rule_id, sql_query)
        
        return {
            "rule_id": rule_id,
            "table_name": rule["table_name"],
            "column_name": rule["column_name"],
            "rule_text": rule["rule_text"],
            "generated_sql": sql_query
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@validation_router.post("/run-validation/{rule_id}")
async def run_validation_for_rule(
    rule_id: int = Path(..., description="ID of the rule to run validation for")
):
    """Run validation for a specific rule and store results"""
    try:
        # Get the rule details
        rules = db_service.get_validation_rules()
        rule = next((r for r in rules if r["id"] == rule_id), None)
        
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        
        if not rule["sql_query"]:
            raise HTTPException(status_code=400, detail="SQL query not generated for this rule yet")
        
        # Run the validation
        validation_result = db_service.run_validation_query(rule_id, rule["sql_query"])

        response = {
            "rule_id": rule_id,
            "table_name": rule["table_name"],
            "column_name": rule["column_name"],
            "rule_text": rule["rule_text"],
            "validation_result": validation_result
        }

        return convert_numpy_types(response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @validation_router.post("/run-validation/{rule_id}")
# async def run_validation_for_rule(
#     rule_id: int = Path(..., description="ID of the rule to run validation for")
# ):
#     """Run validation for a specific rule and store results"""
#     try:
#         # Get the rule details
#         rules = db_service.get_validation_rules()
#         rule = next((r for r in rules if r["id"] == rule_id), None)
        
#         if not rule:
#             raise HTTPException(status_code=404, detail="Rule not found")
        
#         if not rule["sql_query"]:
#             raise HTTPException(status_code=400, detail="SQL query not generated for this rule yet")
        
#         # Run the validation
#         validation_result = db_service.run_validation_query(rule_id, rule["sql_query"])
        
#         return {
#             "rule_id": int(rule_id),
#             "table_name": str(rule["table_name"]),
#             "column_name": str(rule["column_name"]),
#             "rule_text": str(rule["rule_text"]),
#             "validation_result": int(validation_result) if isinstance(validation_result, (np.integer, float)) else validation_result
#         }

#         # return {
#         #     "rule_id": rule_id,
#         #     "table_name": rule["table_name"],
#         #     "column_name": rule["column_name"],
#         #     "rule_text": rule["rule_text"],
#         #     "validation_result": validation_result
#         # }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@validation_router.get("/dashboard-data/")
async def get_dashboard_data(
    table_name: Optional[str] = Query(None, description="Filter by table name")
):
    """Get aggregated data for the dashboard"""
    try:
        conn = db_service.get_connection()
        
        # Query to get rule statistics
        query = """
        SELECT 
            r.table_name,
            COUNT(DISTINCT r.column_name) as columns_with_rules,
            COUNT(r.id) as total_rules,
            SUM(CASE WHEN r.sql_query IS NOT NULL THEN 1 ELSE 0 END) as rules_with_sql,
            AVG(CASE WHEN vr.pass_count + vr.fail_count > 0 
                THEN (vr.pass_count * 100.0 / (vr.pass_count + vr.fail_count)) 
                ELSE NULL END) as avg_compliance_rate
        FROM 
            data_validation_rules r
        LEFT JOIN (
            SELECT 
                rule_id, 
                MAX(validation_date) as latest_date
            FROM 
                data_validation_results
            GROUP BY 
                rule_id
        ) latest ON r.id = latest.rule_id
        LEFT JOIN 
            data_validation_results vr ON latest.rule_id = vr.rule_id AND latest.latest_date = vr.validation_date
        """
        
        if table_name:
            query += f" WHERE r.table_name = '{table_name}'"
            
        query += " GROUP BY r.table_name"
        
        df = pd.read_sql_query(query, conn)
        
        # Query to get recent validation results
        recent_results_query = """
        SELECT 
            r.id as rule_id,
            r.table_name,
            r.column_name,
            r.rule_text,
            vr.validation_date,
            vr.pass_count,
            vr.fail_count,
            (vr.pass_count * 100.0 / (vr.pass_count + vr.fail_count)) as compliance_rate
        FROM 
            data_validation_results vr
        JOIN 
            data_validation_rules r ON vr.rule_id = r.id
        ORDER BY 
            vr.validation_date DESC
        LIMIT 10
        """
        
        recent_results_df = pd.read_sql_query(recent_results_query, conn)
        
        return {
            "table_summaries": df.to_dict('records'),
            "recent_validations": recent_results_df.to_dict('records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))