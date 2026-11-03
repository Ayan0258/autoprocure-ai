import os
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from ml_pipeline import evaluate_product_deal
from paypal_service import create_paypal_sandbox_order

app = FastAPI(
    title="AutoProcure AI API",
    description="Backend API powered by Scikit-Learn and PayPal Sandbox",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "deal_scorer_pipeline.joblib")

if os.path.exists(MODEL_PATH):
    ml_pipeline = joblib.load(MODEL_PATH)
    print(f"SUCCESS: Loaded ML model from {MODEL_PATH}")
else:
    ml_pipeline = None
    print(f"WARNING: ML model NOT found at {MODEL_PATH}")

class ItemEvaluateRequest(BaseModel):
    category: str
    warranty: str = "Pro_2Yr"
    seller_rating: float = 4.5
    review_count: int = 350
    spec_tier: int = 2
    listed_price: float = 250.0

class CheckoutRequest(BaseModel):
    items: list
    total_amount: float

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(html_path):
        try:
            with open(html_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"<h1>Error reading index.html: {str(e)}</h1>"
    
    # Fallback dashboard if index.html isn't found
    return """
    <html>
        <body style="background:#0f172a; color:#fff; font-family:sans-serif; text-align:center; padding-top:50px;">
            <h1>AutoProcure AI Backend Online 🚀</h1>
            <p>Scikit-Learn Model Loaded: """ + str(ml_pipeline is not None) + """</p>
            <p>Go to <a href="/docs" style="color:#38bdf8;">/docs</a> to test the API.</p>
        </body>
    </html>
    """

@app.get("/api/status")
def status_check():
    return {
        "status": "online", 
        "project": "AutoProcure AI", 
        "hackathon": "PayPal AI Hackathon", 
        "ml_model_loaded": ml_pipeline is not None
    }

@app.post("/api/evaluate-deal")
def evaluate_deal_endpoint(req: ItemEvaluateRequest):
    if not ml_pipeline:
        raise HTTPException(status_code=500, detail="ML Pipeline model not found.")
    
    product_dict = {
        "category": req.category,
        "warranty": req.warranty,
        "seller_rating": req.seller_rating,
        "review_count": req.review_count,
        "spec_tier": req.spec_tier,
        "listed_price": req.listed_price,
    }
    analysis = evaluate_product_deal(product_dict, ml_pipeline)
    return {"product": req.category, "listed_price": req.listed_price, **analysis}

@app.post("/api/create-paypal-checkout")
def create_checkout_endpoint(req: CheckoutRequest):
    result = create_paypal_sandbox_order(req.items, req.total_amount)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)