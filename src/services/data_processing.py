import pandas as pd
import re
import numpy as np
from scipy.stats import zscore
from typing import List, Dict, Any

def detect_common_pattern(series: pd.Series) -> str:
    """Detect common regex patterns in categorical columns"""
    sample_values = series.dropna().astype(str).unique()[:100]
    if len(sample_values) == 0:
        return "No pattern detected"
    
    patterns = {
        "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "phone": r"^\+?\d{1,3}?[-. ]?\(?\d{1,4}?\)?[-. ]?\d{1,4}[-. ]?\d{1,9}$"
    }
    
    for pattern_name, pattern in patterns.items():
        if all(re.match(pattern, val) for val in sample_values):
            return f"{pattern_name.capitalize()} Pattern"
    
    return "Mixed/Unknown Pattern"

def detect_outliers(series: pd.Series) -> int:
    """Detects outliers using the 3-sigma rule (z-score > 3)"""
    if pd.api.types.is_numeric_dtype(series):
        z_scores = np.abs(zscore(series.dropna()))
        return int((z_scores > 3).sum())
    return 0

def generate_metadata(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Generate comprehensive dataset metadata"""
    metadata = []
    
    for col in df.columns:
        col_data = df[col].dropna()
        unique_values = col_data.nunique()
        null_percentage = round(df[col].isnull().mean() * 100, 2)
        
        column_metadata = {
            "column_name": col,
            "data_type": str(df[col].dtype),
            "null_percentage": null_percentage,
            "unique_values": unique_values,
            "min_value": col_data.min() if pd.api.types.is_numeric_dtype(col_data) else None,
            "max_value": col_data.max() if pd.api.types.is_numeric_dtype(col_data) else None,
            "mean_value": round(col_data.mean(), 2) if pd.api.types.is_numeric_dtype(col_data) else None,
            "std_dev": round(col_data.std(), 2) if pd.api.types.is_numeric_dtype(col_data) else None,
            "outliers_detected": detect_outliers(col_data),
            "min_length": col_data.astype(str).str.len().min() if df[col].dtype == 'object' else None,
            "max_length": col_data.astype(str).str.len().max() if df[col].dtype == 'object' else None,
            "common_pattern": detect_common_pattern(col_data) if df[col].dtype == 'object' else None,
            "most_common_value": col_data.value_counts().idxmax() if not col_data.empty else None,
        }
        metadata.append(column_metadata)
    
    return metadata

def format_metadata_script(metadata: List[Dict[str, Any]]) -> str:
    """Format metadata into a structured report"""
    script = ["### Dataset Metadata Report ###\n"]
    
    for col in metadata:
        script.append(f"Column: {col['column_name']}")
        script.append(f"- Data Type: {col['data_type']}")
        script.append(f"- Null Percentage: {col['null_percentage']}%")
        script.append(f"- Unique Values: {col['unique_values']}")
        
        if col["min_value"] is not None:
            script.append(f"- Min Value: {col['min_value']}")
        if col["max_value"] is not None:
            script.append(f"- Max Value: {col['max_value']}")
        if col["mean_value"] is not None:
            script.append(f"- Mean Value: {col['mean_value']}")
        if col["std_dev"] is not None:
            script.append(f"- Standard Deviation: {col['std_dev']}")
        if col["outliers_detected"]:
            script.append(f"- Outliers Detected: {col['outliers_detected']}")
        if col["min_length"] and col["max_length"]:
            script.append(f"- Min/Max Length: {col['min_length']} - {col['max_length']} characters")
        if col["common_pattern"]:
            script.append(f"- Common Pattern: {col['common_pattern']}")
        if col["most_common_value"]:
            script.append(f"- Most Common Value: {col['most_common_value']}")
        script.append("")
    
    script.append("### End of Metadata Report ###")
    return "\n".join(script)



