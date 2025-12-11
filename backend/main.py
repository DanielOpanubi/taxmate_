from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from storage import upload_file_to_minio
from tax_engine import calculate_tax

app = FastAPI(title="TaxCalc API")

class TaxRequest(BaseModel):
    income: float
    deductions: float
    period: str | None = None

@app.post("/upload_invoice")
async def upload_invoice(file: UploadFile = File(...), business_id: str = Form(...)):
    if not business_id.strip():
        raise HTTPException(status_code=400, detail="Business ID is required")
    if file.content_type not in ("application/pdf", "image/png", "image/jpeg"):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    object_key = f"{business_id}/{file.filename}"
    object_url = upload_file_to_minio(object_key, await file.read())  # your existing MinIO function
    return {"url": object_url, "filename": file.filename, "business_id": business_id}

@app.post("/calculate_tax")
def calc_tax(req: TaxRequest):
    res = calculate_tax(req.income, req.deductions)
    res.update({"period": req.period})
    return res
