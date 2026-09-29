import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import lightgbm as lgb


df = pd.read_parquet('data/processed/features.parquet')

df['date'] = pd.to_datetime(df['date'])

split_date = '2019-11-01'

train = df[df['date'] < split_date].copy()

test = df[df['date'] >= split_date].copy()

feature_columns = ['hour', 'dayofweek', 'month', 'is_weekend', 'line', 'from', 'stop_sequence']
weather_features = ['temperature_2m', 'precipitation', 'snowfall', 'is_precip', 'is_snow', 'snow_depth', 'heavy_precip', 'windgusts_10m']


for col in ['line', 'from']:

    train[col] = train[col].astype('category')
    test[col] = test[col].astype('category')


X_train, y_train = train[feature_columns], train['delayed']

X_test, y_test = test[feature_columns], test['delayed']



baseline_prediction = [False] * len(y_test)

print("=== BASELINE ===")
print('Accuracy:', round(accuracy_score(y_test, baseline_prediction), 4))
print("(precision/recall/F1 are 0 - it never predicts a delay\n)")

def train_and_eval(name, feature_cols):
    model = lgb.LGBMClassifier(n_estimators=200, learning_rate=0.05)
    model.fit(train[feature_cols], y_train)
    pred = model.predict(test[feature_cols])
    print(f"\n=== {name} ===")
    print("Accuracy: ", round(accuracy_score(y_test, pred), 4))
    print("Precision:", round(precision_score(y_test, pred), 4))
    print("Recall:   ", round(recall_score(y_test, pred), 4))
    print("F1:       ", round(f1_score(y_test, pred), 4))
    print("Confusion:\n", confusion_matrix(y_test, pred))
    imp = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
    print("Top 10 features:\n", imp.head(10))
    return model

train_and_eval("NO WEATHER", feature_columns)
train_and_eval("WITH WEATHER", feature_columns + weather_features)
