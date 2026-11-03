# AutoProcure AI 


Welcome to **AutoProcure AI**! This is my project for the PayPal AI Hackathon on Devpost. 

I built this because modern B2B procurement is usually bogged down by messy pricing, unverified vendor metrics, and clunky checkout steps. AutoProcure AI solves this by combining smart machine learning deal scoring with seamless payment workflows in one clean dashboard.

---

## What it does
- **Scikit-Learn Deal Scoring:** It looks at product categories, warranty tiers, seller ratings, and review counts to predict fair market value, calculate a 0-100 deal score, and instantly tell you whether it's a solid buy.
- **PayPal Sandbox Checkout:** Automatically triggers test orders and secure simulation workflows to finish the procurement loop without needing live keys or personal accounts.
- **FastAPI & Tailwind UI:** Powered by a fast asynchronous backend and a sleek, modern enterprise-style dashboard.

---

## Tech Stack
- **Backend & ML:** Python, Scikit-Learn, Pandas, FastAPI, Uvicorn, Joblib, Python-Dotenv
- **Frontend:** HTML5, Tailwind CSS, JavaScript (Fetch API)
- **Payments:** PayPal Sandbox API (supports live sandbox tokens or fallback simulation mode)

---

## How to Run It Locally

Want to test it out on your machine? Just follow these steps:

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/Ayan0258/autoprocure-ai.git](https://github.com/Ayan0258/autoprocure-ai.git)
   cd autoprocure-ai
