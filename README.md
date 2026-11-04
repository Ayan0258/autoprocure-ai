# AutoProcure AI 🚀

[![Watch the Demo](https://img.shields.io/badge/YouTube-Watch%20Demo%20Video-red?style=for-the-badge&logo=youtube)](https://youtu.be/K9y3PxVxKTY)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML%20Pipeline-F7931E?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)

**AutoProcure AI** is an autonomous B2B hardware procurement platform powered by a **Scikit-Learn** machine learning pipeline and a **PayPal Sandbox** checkout integration. It evaluates hardware deals in real time—predicting fair market value, calculating a 0–100 Deal Score, and executing automated test orders.

🎥 **Live Demo Video:** https://youtu.be/K9y3PxVxKTY

---

## ✨ Key Features
* **Real-Time ML Deal Scoring:** Evaluates B2B hardware listings (`Monitor`, `Keyboard`, `Webcam`, `Headset`, `Docking Station`) based on warranty tier, listed price, seller rating, and review volume.
* **Instant Valuation & Risk Verdict:** Outputs predicted fair value, estimated savings, a 0–100 Deal Score, and a clear recommendation (`STRONG BUY` vs. `OVERPRICED RISK`).
* **Zero-Config PayPal Sandbox Integration:** Supports live PayPal Sandbox API checkout and automatically falls back to a built-in **Simulation Mode** if no API keys are provided, so anyone can test the full workflow out of the box.

---

## 🚀 How to Run Locally (For Developers & Reviewers)

Follow these steps to run the project on your own machine:

### 1. Clone the Repository
```bash
git clone [https://github.com/Ayan0258/autoprocure-ai.git](https://github.com/Ayan0258/autoprocure-ai.git)
cd autoprocure-ai
