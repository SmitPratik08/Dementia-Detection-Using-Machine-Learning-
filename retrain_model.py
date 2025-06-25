import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv('oasis_longitudinal.csv')

# Drop nulls
df.dropna(inplace=True)

# Convert gender to numeric
df['M/F'] = LabelEncoder().fit_transform(df['M/F'])  # M = 1, F = 0

# Encode target
def encode_target(cdr):
    if cdr == 0.0:
        return 0  # No Dementia
    elif cdr == 0.5:
        return 1  # Mild Dementia
    elif cdr == 1.0:
        return 2  # Moderate Dementia
    else:
        return 3  # Severe Dementia

df['Target'] = df['CDR'].apply(encode_target)

# Features and target
X = df[['Age', 'M/F', 'EDUC', 'SES', 'MMSE', 'CDR', 'eTIV', 'nWBV', 'ASF']]
y = df['Target']

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'model.pkl')
print("✅ Model saved as model.pkl using current sklearn version.")
