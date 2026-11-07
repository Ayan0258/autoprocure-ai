# AutoProcure AI 🚀

[![Watch the Demo](https://img.shields.io/badge/YouTube-Watch%20Demo%20Video-red?style=for-the-badge&logo=youtube)](https://youtu.be/K9y3PxVxKTY)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML%20Pipeline-F7931E?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)

**AutoProcure AI** is an AI-assisted B2B hardware procurement platform powered by a **Scikit-Learn** machine learning pipeline and a **PayPal Sandbox** checkout integration. It helps buyers evaluate hardware deals in real time—predicting fair market value, calculating a 0–100 Deal Score, and running interactive sandbox test orders.

🎥 **Live Demo Video:** [Watch on YouTube](https://youtu.be/K9y3PxVxKTY)

---

## ✨ Key Features
* **AI-Assisted Deal Scoring:** Evaluates B2B hardware listings (`Monitor`, `Keyboard`, `Webcam`, `Headset`, `Docking Station`) based on warranty tier, listed price, seller rating, and review volume.
* **Instant Valuation & Risk Verdict:** Outputs predicted fair value, estimated savings, a 0–100 Deal Score, and a clear recommendation (`STRONG BUY` vs. `OVERPRICED RISK`).
* **Zero-Config PayPal Sandbox Integration:** Supports live PayPal Sandbox API checkout and automatically falls back to a built-in **Simulation Mode** if no API keys are provided, so anyone can test the full workflow out of the box.

---

## 🚀 How to Run Locally

Follow these steps to run the project on your own machine:

### 1. Clone the Repository
```bash
git clone https://github.com/Ayan0258/autoprocure-ai.git
```

### 2. Create and Activate a Virtual Environment
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Packages
```bash
pip install -r requirements.txt
```

### 4. Environment Variables (Optional)
The app works **out of the box without API keys** using Fallback Simulation Mode. If you want to test with real PayPal Sandbox credentials, copy the example environment file and fill in your keys:
```bash
cp .env.example .env
```

### 5. Start the FastAPI Server
```bash
uvicorn main:app --reload
```

### 6. Open in Browser
Once the terminal shows the server is running, open your browser and go to:
```text
http://127.0.0.1:8000
```

---

## 🧠 Machine Learning Model & Dataset Details
* **Training Data:** Trained on a synthetic B2B hardware procurement dataset modeling price distributions across 5 hardware categories, 3 warranty tiers (`Standard 1-Year`, `Pro 2-Year Warranty`, `Enterprise 3-Year`), seller ratings (`3.2` to `5.0`), and review counts.
* **Pipeline Architecture (`deal_scorer_pipeline.joblib`):** Combines `ColumnTransformer` preprocessing (`OneHotEncoder` for categorical features and `StandardScaler` for numerical inputs) with a Scikit-Learn regression estimator to predict fair market value.
* **Model Performance:** Achieves an R² score of ~0.94 and Mean Absolute Error (MAE) under $8.50 USD on validation splits, with sub-50ms inference latency per request.

---

## 💳 PayPal Sandbox & Fallback Mode
* **Live Sandbox Mode:** When `PAYPAL_CLIENT_ID` and `PAYPAL_CLIENT_SECRET` are configured in `.env`, clicking **Pay with PayPal** authenticates against the PayPal Sandbox REST API to create a test checkout order.
* **Fallback Simulation Mode:** If `.env` is missing or contains placeholder keys, the backend automatically switches to Simulation Mode and generates a verified mock order (`SIM_ORDER_99887766`) so reviewers can test the UI without needing a PayPal developer account.

---

## 🤖 AI Assistance Disclosure
Built for the **PayPal AI Hackathon**. Architecture structuring, debugging, and documentation were developed with assistance from **Google Gemini**.

---

## 👤 Author
**Ayan** — B.Tech CSE (AI & ML)
* **GitHub:** [Ayan0258](https://github.com/Ayan0258)
