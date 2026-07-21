import pandas as pd
import joblib

from sklearn.model_selection import (
    train_test_split,
    cross_val_score
)

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    HistGradientBoostingRegressor
)

from sklearn.linear_model import LinearRegression

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("data/engineered_data.csv")

# ==========================================
# FEATURE SELECTION
# ==========================================

FEATURES = [

    "Suction press",

    "Discharge press",

    "Voltage",

    "Current",

    "Flow Rate",

    "HMR_Hours",

    "Pressure_Difference",

    "Pressure_Ratio",

    "Electrical_Load",

    "Flow_Utilization",

    "Load_Index"

]

TARGET = "KWH Diff"

X = df[FEATURES]

y = df[TARGET]

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42

)

# ==========================================
# MODELS
# ==========================================

models = {

    "Random Forest":

        RandomForestRegressor(

            n_estimators=300,

            random_state=42

        ),

    "Extra Trees":

        ExtraTreesRegressor(

            n_estimators=300,

            random_state=42

        ),

    "Gradient Boosting":

        GradientBoostingRegressor(

            random_state=42

        ),

    "HistGradientBoosting":

        HistGradientBoostingRegressor(

            random_state=42

        ),

    "Linear Regression":

        LinearRegression()

}

# ==========================================
# TRAIN
# ==========================================

results = []

best_model = None

best_score = -999

print("=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

for name, model in models.items():

    model.fit(
        X_train,
        y_train
    )

    prediction = model.predict(
        X_test
    )

    r2 = r2_score(
        y_test,
        prediction
    )

    mae = mean_absolute_error(
        y_test,
        prediction
    )

    mse = mean_squared_error(
        y_test,
        prediction
    )

    rmse = mse ** 0.5

    cv = cross_val_score(
        model,
        X,
        y,
        cv=5,
        scoring="r2"
    ).mean()

    print(f"\n{name}")
    print("-" * 40)

    print(f"R2 Score : {r2:.4f}")
    print(f"MAE      : {mae:.4f}")
    print(f"RMSE     : {rmse:.4f}")
    print(f"CV Score : {cv:.4f}")

    results.append([
        name,
        r2,
        mae,
        rmse,
        cv
    ])

    if r2 > best_score:
        best_score = r2
        best_model = model

# ==========================================
# SAVE BEST MODEL
# ==========================================

joblib.dump(

    best_model,

    "models/compressor_model_v2.pkl"

)

print("\n" + "=" * 70)

print("BEST MODEL SAVED")

print("=" * 70)

print(f"Best R2 Score : {best_score:.4f}")

print("\nSaved As")

print("models/compressor_model_v2.pkl")

# ==========================================
# SAVE RESULTS
# ==========================================

results_df = pd.DataFrame(

    results,

    columns=[

        "Model",

        "R2",

        "MAE",

        "RMSE",

        "Cross Validation"

    ]

)

results_df.to_csv(

    "data/model_comparison.csv",

    index=False

)

print("\nModel comparison saved.")