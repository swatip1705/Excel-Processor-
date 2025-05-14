from fastapi import FastAPI, HTTPException, Query
from typing import List
import pandas as pd
import os

app = FastAPI()

EXCEL_PATH = "./Data/capbudg.xls"

def load_excel_sheets(path: str) -> dict:
    """
    Reads the Excel file located at the specified path and returns a dictionary 
    where the keys are sheet names, and the values are DataFrames representing 
    the content of each sheet.

    Args:
        path (str): The path to the Excel file.

    Returns:
        dict: A dictionary containing the sheet names as keys and DataFrames as values.

    Raises:
        FileNotFoundError: If the provided path does not exist or is invalid.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Excel file not found at path: {path}")
    # Using xlrd engine for .xls files to load the Excel data
    excel_data = pd.read_excel(path, sheet_name=None, engine='xlrd')
    return excel_data

@app.get("/list_tables")
def list_tables():
    """
    Endpoint to list all the table names (sheet names) in the Excel file.

    Returns:
        dict: A dictionary with a key "tables" and a list of table names (sheet names).
    
    Raises:
        HTTPException: If there is an error loading the Excel file or processing the data.
    """
    try:
        sheets = load_excel_sheets(EXCEL_PATH)
        table_names = list(sheets.keys())
        return {"tables": table_names}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_table_details")
def get_table_details(table_name: str = Query(..., description="The name of the table (sheet) to fetch row details from.")):
    """
    Endpoint to get the details (row names) of a specified table (sheet).

    Args:
        table_name (str): The name of the table (sheet) to retrieve row details for.
    
    Returns:
        dict: A dictionary containing the table name and a list of row names.
    
    Raises:
        HTTPException: 
            - If the specified table does not exist in the Excel file.
            - If the table is empty.
            - If any other error occurs while processing the request.
    """
    try:
        table_name = table_name.strip()
        sheets = load_excel_sheets(EXCEL_PATH)
        if table_name not in sheets:
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found.")
        
        df = sheets[table_name]
        if df.empty:
            return {"table_name": table_name, "row_names": []}

        first_column_name = df.columns[0]
        row_names = df[first_column_name].dropna().astype(str).tolist()

        return {"table_name": table_name, "row_names": row_names}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/row_sum")
def row_sum(
    table_name: str = Query(..., description="The name of the table (sheet)"),
    row_name: str = Query(..., description="The name of the row to sum numeric values for")
):
    """
    Endpoint to calculate the sum of all numerical values in a specified row of a specified table.
    I am returning the numerical value at the end

    Args:
        table_name (str): The name of the table (sheet) containing the row.
        row_name (str): The name of the row for which to calculate the sum of numerical values.
    
    Returns:
        dict: A dictionary containing the table name, row name, and the sum of numerical values in the row.
    
    Raises:
        HTTPException:
            - If the specified table does not exist in the Excel file.
            - If the specified row does not exist in the table.
            - If the table is empty or if no numerical values exist in the specified row.
            - If any other error occurs during the calculation.
    """
    try:
        sheets = load_excel_sheets(EXCEL_PATH)
        if table_name not in sheets:
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found.")
        
        df = sheets[table_name]
        if df.empty:
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' is empty.")
        
        #locate the specified row by matching the value in the first column
        first_column_name = df.columns[0]
        row = df[df[first_column_name].astype(str) == row_name]

        if row.empty:
            raise HTTPException(status_code=404, detail=f"Row '{row_name}' not found in table '{table_name}'.")

        #exclude the first column (row names) and sum the numeric columns
        numeric_values = row.drop(columns=[first_column_name]).select_dtypes(include='number')
        row_sum_value = numeric_values.sum(axis=1).iloc[0] if not numeric_values.empty else 0

        return {
            "table_name": table_name,
            "row_name": row_name,
            "sum": row_sum_value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
