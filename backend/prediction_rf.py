import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

# ... existing code ...
# Replace XGBClassifier with RandomForestClassifier
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=6,
    random_state=42,
    min_samples_split=5,
    min_samples_leaf=3,
    class_weight='balanced',
    n_jobs=-1
)

print("Training RandomForest model...")
model.fit(X_train_scaled, y_train)
# ... existing code ... 