# 📊 FastAPI Excel Processor Assignment

## 🚀 Overview

This FastAPI project processes an Excel file (`capbudg.xls`) and exposes RESTful endpoints to:

* List table names (sheets)
* Retrieve row names from a sheet
* Calculate the sum of numerical values in a row

The APIs are tested using Postman with `GET` requests.

---

## 📅 Excel Sheet Location

The Excel file used is located at:

```
/Data/capbudg.xls
```

Ensure this path is correct when running the app.

---

## 🔗 API Endpoints

### Base URL

```
http://localhost:9090
```

---

### 1. 📄 GET `/list_tables`

Returns the names of all tables (sheet names) in the Excel file.

#### ✅ Example Response:

```json
{
  "tables": ["CapBudgWS"]
}
```

---

### 2. 📄 GET `/get_table_details`

Returns the first-column values (row names) for a given table (sheet).

#### 🔧 Query Parameters:

* `table_name`: Name of the sheet (e.g., `CapBudgWS`)

#### ✅ Example Request:

```
http://localhost:9090/get_table_details?table_name=CapBudgWS
```

#### ✅ Example Response:

```json
{
  "table_name": "CapBudgWS",
  "row_names": [
    "INITIAL INVESTMENT",
    "Initial Investment=",
    "Opportunity cost (if any)=",
    ...
  ]
}
```

---

### 3. 📄 GET `/row_sum`

Returns the sum of all numeric values in a specified row in the given sheet.

#### 🔧 Query Parameters:

* `table_name`: Name of the sheet
* `row_name`: Label of the row from the first column

#### ✅ Example Request:

```
http://localhost:9090/row_sum?table_name=CapBudgWS&row_name=EBIT
```

#### ✅ Example Response:

```json
{
  "table_name": "CapBudgWS",
  "row_name": "EBIT",
  "sum": 152551.44
}
```

---

## 🧰 How I Implemented It

### Step-by-Step:

1. **Read Excel File**: Used `pandas.read_excel()` to load all sheets into a dictionary.
2. **Created FastAPI app** with three endpoints:

   * `/list_tables`: Lists keys of the Excel dictionary (sheet names)
   * `/get_table_details`: Returns first-column values of the selected sheet
   * `/row_sum`: Extracts values from a row and sums only numeric ones
3. **Error Handling**:

   * Returns 404 if table or row is not found
   * Handles empty DataFrames and malformed names
4. **Testing**:

   * I tested each GET endpoint using Postman with the appropriate query parameters

---

## 🕹️ Testing Instructions (Postman)

You can test the APIs using Postman:

1. Open Postman
2. Create a collection called `Excel Processor API`
3. Add the following requests:

   * `GET http://localhost:9090/list_tables`
   * `GET http://localhost:9090/get_table_details?table_name=CapBudgWS`
   * `GET http://localhost:9090/row_sum?table_name=CapBudgWS&row_name=EBIT`
4. Click **Send** to view the responses.

> ✅ No Postman environment or token is needed since all are simple GET requests.

---

## 💭 Potential Improvements

* Support uploading Excel files dynamically
* Allow processing `.xlsx` and CSV formats
* Return table metadata like number of rows/columns
* Add frontend interface for end users

---

## ⚠️ Edge Cases Not Handled

* Empty/missing Excel files
* Sheet or row names with trailing whitespaces or line breaks
* Rows with mixed data types (e.g., strings and numbers)

---

## 🔧 How to Run the App

```bash
uvicorn main:app --reload --port 9090
```

Visit the interactive API docs at:

```
http://localhost:9090/docs
```

---

## 💾 Postman Collection

You can export the Postman collection using:

* Click the collection in the sidebar
* Click the three dots → Export
* Choose **Collection v2.1** format
* Submit the JSON file

---

Feel free to reach out if you want the `.json` Postman file exported from my side.
