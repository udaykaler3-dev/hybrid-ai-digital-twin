"""
==========================================================
AI DIGITAL TWIN V3
Production Model Training Pipeline
==========================================================
Author : Uday Kaler
Project : AI Digital Twin for CNG Booster Compressor
==========================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================

import os
import warnings
import joblib
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ==========================================================
# SKLEARN
# ==========================================================

from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV,
    KFold,
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

# ==========================================================
# PATHS
# ==========================================================

DATASET = "data/training_dataset_v3.csv"

MODEL_FOLDER = "models"

REPORT_FOLDER = "training_reports"

os.makedirs(MODEL_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# ==========================================================
# LOAD DATASET
# ==========================================================

print("=" * 70)
print("AI DIGITAL TWIN V3")
print("Loading Training Dataset")
print("=" * 70)

df = pd.read_csv(DATASET)

print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")

# ==========================================================
# FEATURE SELECTION
# ==========================================================

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

TARGET = "Power_kW"

# ==========================================================
# DATASET
# ==========================================================

X = df[FEATURES]

y = df[TARGET]

print("\nTraining Features")

for feature in FEATURES:
    print("✓", feature)

print(f"\nTarget Variable : {TARGET}")

# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    shuffle=True

)

print("\nDataset Split")

print(f"Training Samples : {len(X_train)}")

print(f"Testing Samples  : {len(X_test)}")

# ==========================================================
# CROSS VALIDATION
# ==========================================================

cv = KFold(

    n_splits=5,

    shuffle=True,

    random_state=42

)

print("\nCross Validation")

print("5-Fold Cross Validation Enabled")

# ==========================================================
# MODEL DEFINITIONS
# ==========================================================

MODELS = {

    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        random_state=42
    ),

    "Extra Trees": ExtraTreesRegressor(
        random_state=42
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        random_state=42
    ),

    "HistGradientBoosting": HistGradientBoostingRegressor(
        random_state=42
    )

}

print("\nModels Loaded")

for model in MODELS.keys():
    print("✓", model)

print("\nSetup Completed Successfully.")
print("=" * 70)
# ==========================================================
# HYPERPARAMETER SEARCH SPACE
# ==========================================================

RF_PARAMS = {
    "n_estimators": [100, 200, 300, 500],
    "max_depth": [5, 10, 15, 20, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4]
}

ET_PARAMS = {
    "n_estimators": [100, 200, 300, 500],
    "max_depth": [5, 10, 15, 20, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4]
}

GB_PARAMS = {
    "n_estimators": [100, 200, 300],
    "learning_rate": [0.01, 0.05, 0.1],
    "max_depth": [2, 3, 4]
}

# ==========================================================
# RESULTS
# ==========================================================

results = []

best_model = None
best_name = ""
best_r2 = float("-inf")
print("\n")
print("=" * 70)
print("MODEL TRAINING")
print("=" * 70)

# ==========================================================
# LINEAR REGRESSION
# ==========================================================

print("\nTraining Linear Regression...")

lr = MODELS["Linear Regression"]

lr.fit(X_train, y_train)

pred = lr.predict(X_test)

r2 = r2_score(y_test, pred)
mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
cv_score = cross_val_score(
    lr,
    X,
    y,
    cv=cv,
    scoring="r2"
).mean()

results.append([
    "Linear Regression",
    r2,
    mae,
    rmse,
    cv_score
])

# Linear Regression is evaluated only.
# It is NOT eligible as the production model.

print("Linear Regression evaluated but excluded from production selection.")

print(f"R² : {r2:.4f}")
print(f"MAE : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")

# ==========================================================
# RANDOM FOREST
# ==========================================================

print("\nOptimizing Random Forest...")

rf_search = RandomizedSearchCV(
    estimator=RandomForestRegressor(random_state=42),
    param_distributions=RF_PARAMS,
    n_iter=20,
    cv=cv,
    scoring="r2",
    random_state=42,
    n_jobs=-1
)

rf_search.fit(X_train, y_train)

rf = rf_search.best_estimator_

pred = rf.predict(X_test)

r2 = r2_score(y_test, pred)
mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
cv_score = cross_val_score(
    rf,
    X,
    y,
    cv=cv,
    scoring="r2"
).mean()

results.append([
    "Random Forest",
    r2,
    mae,
    rmse,
    cv_score
])

print(f"Best Parameters : {rf_search.best_params_}")
print(f"R² : {r2:.4f}")

if r2 > best_r2:
    best_r2 = r2
    best_model = rf
    best_name = "Random Forest"

# ==========================================================
# EXTRA TREES
# ==========================================================

print("\nOptimizing Extra Trees...")

et_search = RandomizedSearchCV(
    estimator=ExtraTreesRegressor(random_state=42),
    param_distributions=ET_PARAMS,
    n_iter=20,
    cv=cv,
    scoring="r2",
    random_state=42,
    n_jobs=-1
)

et_search.fit(X_train, y_train)

et = et_search.best_estimator_

pred = et.predict(X_test)

r2 = r2_score(y_test, pred)
mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
cv_score = cross_val_score(
    et,
    X,
    y,
    cv=cv,
    scoring="r2"
).mean()

results.append([
    "Extra Trees",
    r2,
    mae,
    rmse,
    cv_score
])

print(f"Best Parameters : {et_search.best_params_}")
print(f"R² : {r2:.4f}")

if r2 > best_r2:
    best_r2 = r2
    best_model = et
    best_name = "Extra Trees"
    # ==========================================================
# GRADIENT BOOSTING
# ==========================================================

print("\nOptimizing Gradient Boosting...")

gb_search = RandomizedSearchCV(
    estimator=GradientBoostingRegressor(random_state=42),
    param_distributions=GB_PARAMS,
    n_iter=15,
    cv=cv,
    scoring="r2",
    random_state=42,
    n_jobs=-1
)

gb_search.fit(X_train, y_train)

gb = gb_search.best_estimator_

pred = gb.predict(X_test)

r2 = r2_score(y_test, pred)
mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
cv_score = cross_val_score(
    gb,
    X,
    y,
    cv=cv,
    scoring="r2"
).mean()

results.append([
    "Gradient Boosting",
    r2,
    mae,
    rmse,
    cv_score
])

print(f"Best Parameters : {gb_search.best_params_}")
print(f"R² : {r2:.4f}")

if r2 > best_r2:
    best_r2 = r2
    best_model = gb
    best_name = "Gradient Boosting"

# ==========================================================
# HIST GRADIENT BOOSTING
# ==========================================================

print("\nTraining HistGradientBoosting...")

hgb = HistGradientBoostingRegressor(
    random_state=42
)

hgb.fit(X_train, y_train)

pred = hgb.predict(X_test)

r2 = r2_score(y_test, pred)
mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
cv_score = cross_val_score(
    hgb,
    X,
    y,
    cv=cv,
    scoring="r2"
).mean()

results.append([
    "HistGradientBoosting",
    r2,
    mae,
    rmse,
    cv_score
])

print(f"R² : {r2:.4f}")

if r2 > best_r2:
    best_r2 = r2
    best_model = hgb
    best_name = "HistGradientBoosting"

# ==========================================================
# MODEL COMPARISON
# ==========================================================

results_df = pd.DataFrame(
    results,
    columns=[
        "Model",
        "R2",
        "MAE",
        "RMSE",
        "CrossValidation"
    ]
)

results_df = results_df.sort_values(
    by="R2",
    ascending=False
)

print("\n")
print("=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

print(results_df)

results_df.to_csv(
    "training_reports/model_metrics.csv",
    index=False
)

# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================

print("\n")
print("=" * 70)
print("FEATURE IMPORTANCE")
print("=" * 70)

if hasattr(best_model, "feature_importances_"):

    importance = pd.DataFrame({

        "Feature": FEATURES,

        "Importance": best_model.feature_importances_

    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )

    print(importance)

    importance.to_csv(
        "training_reports/feature_importance.csv",
        index=False
    )

else:

    print("Feature importance not available for this model.")

# ==========================================================
# SAVE MODEL
# ==========================================================

model_path = os.path.join(
    MODEL_FOLDER,
    "compressor_model_v3.pkl"
)

joblib.dump(
    best_model,
    model_path
)

print("\n")
print("=" * 70)
print("BEST MODEL")
print("=" * 70)

print(f"Model : {best_name}")
print(f"R²    : {best_r2:.4f}")

print("\nSaved Model")

print(model_path)

print("\nMetrics Saved")

print("training_reports/model_metrics.csv")

print("\nTraining Completed Successfully.")