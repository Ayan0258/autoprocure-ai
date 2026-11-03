import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def generate_training_catalog(n_samples=600):
    """Generates historical B2B product pricing data for training our ML pipeline."""
    np.random.seed(42)

    categories = ["Monitor", "Keyboard", "Webcam", "Headset", "Docking Station"]
    warranty_tiers = ["Standard_1Yr", "Pro_2Yr", "Enterprise_3Yr"]

    base_market_prices = {
        "Monitor": 240.0,
        "Keyboard": 95.0,
        "Webcam": 80.0,
        "Headset": 110.0,
        "Docking Station": 160.0,
    }

    rows = []
    for _ in range(n_samples):
        cat = np.random.choice(categories)
        warranty = np.random.choice(warranty_tiers)
        seller_rating = np.round(np.random.uniform(3.2, 5.0), 2)
        review_count = int(np.random.randint(15, 2500))
        spec_tier = int(np.random.choice([1, 2, 3]))  # 1=Entry, 2=Mid, 3=Pro

        # Calculate the true fair market value based on specs, rating, and warranty
        base = base_market_prices[cat]
        spec_multiplier = 1.0 + (spec_tier - 1) * 0.35
        rating_bonus = (seller_rating - 4.0) * 18.0
        warranty_bonus = (
            0
            if warranty == "Standard_1Yr"
            else (15 if warranty == "Pro_2Yr" else 35)
        )

        true_fair_price = np.round(
            max(
                25.0,
                base * spec_multiplier
                + rating_bonus
                + warranty_bonus
                + np.random.normal(0, 6),
            ),
            2,
        )

        rows.append({
            "category": cat,
            "warranty": warranty,
            "seller_rating": seller_rating,
            "review_count": review_count,
            "spec_tier": spec_tier,
            "true_fair_price": true_fair_price,
        })

    return pd.DataFrame(rows)


def train_and_save_pipeline():
    print("1. Generating B2B historical product dataset with Pandas...")
    df = generate_training_catalog()

    # Features (X) and Target (y)
    X = df[
        ["category", "warranty", "seller_rating", "review_count", "spec_tier"]
    ]
    y = df["true_fair_price"]

    # Split into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Define categorical and numerical columns
    categorical_cols = ["category", "warranty"]
    numerical_cols = ["seller_rating", "review_count", "spec_tier"]

    # Step A: Build ColumnTransformer for Scaling & Encoding
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_cols),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_cols,
            ),
        ]
    )

    # Step B: Bundle Preprocessor + Model into a single Scikit-Learn Pipeline
    model_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "regressor",
                RandomForestRegressor(n_estimators=120, random_state=42),
            ),
        ]
    )

    print("2. Training Scikit-Learn Pipeline...")
    model_pipeline.fit(X_train, y_train)

    # Step C: Evaluate Model on Unseen Test Data
    predictions = model_pipeline.predict(X_test)
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    print(
        f"3. Model Evaluation Complete -> R2 Score: {r2:.4f} | Mean Absolute Error: ${mae:.2f}"
    )

    # Save trained pipeline to disk
    joblib.dump(model_pipeline, "deal_scorer_pipeline.joblib")
    print("4. Saved trained pipeline to 'deal_scorer_pipeline.joblib'!")
    return model_pipeline


def evaluate_product_deal(product_dict, pipeline=None):
    """Uses our trained Scikit-Learn Pipeline to predict fair market price

    and compute a 0-100 Deal Quality Score.
    """
    if pipeline is None:
        pipeline = joblib.load("deal_scorer_pipeline.joblib")

    input_df = pd.DataFrame([{
        "category": product_dict["category"],
        "warranty": product_dict.get("warranty", "Pro_2Yr"),
        "seller_rating": product_dict["seller_rating"],
        "review_count": product_dict["review_count"],
        "spec_tier": product_dict.get("spec_tier", 2),
    }])

    predicted_fair_price = float(pipeline.predict(input_df)[0])
    listed_price = float(product_dict["listed_price"])

    # Calculate savings % vs fair market value
    savings_pct = (
        (predicted_fair_price - listed_price) / predicted_fair_price
    ) * 100.0

    # Convert savings & seller rating into a 0-100 Deal Score
    raw_score = 70.0 + (savings_pct * 1.4) + (
        (product_dict["seller_rating"] - 4.0) * 10.0
    )
    deal_score = int(np.clip(round(raw_score), 12, 99))

    if deal_score >= 80:
        verdict = "STRONG BUY (Undervalued)"
    elif deal_score >= 60:
        verdict = "FAIR DEAL (Market Price)"
    else:
        verdict = "OVERPRICED RISK"

    return {
        "predicted_fair_price": round(predicted_fair_price, 2),
        "deal_score": deal_score,
        "savings_usd": round(predicted_fair_price - listed_price, 2),
        "verdict": verdict,
    }


if __name__ == "__main__":
    trained_pipe = train_and_save_pipeline()

    # Quick sanity test on a sample monitor
    sample_item = {
        "name": "UltraSharp 27-inch 4K IPS Monitor",
        "category": "Monitor",
        "warranty": "Pro_2Yr",
        "seller_rating": 4.8,
        "review_count": 640,
        "spec_tier": 2,
        "listed_price": 279.00,
    }
    result = evaluate_product_deal(sample_item, trained_pipe)
    print("\n--- SAMPLE DEAL PREDICTION ---")
    print(f"Product: {sample_item['name']} | Listed: ${sample_item['listed_price']}")
    print(f"ML Predicted Fair Price: ${result['predicted_fair_price']}")
    print(f"Deal Score: {result['deal_score']}/100 -> {result['verdict']}")