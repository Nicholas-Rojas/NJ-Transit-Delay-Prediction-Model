import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import lightgbm as lgb
import warnings; warnings.filterwarnings('ignore')


def load_split(df, split_date):

    df['date'] = pd.to_datetime(df['date'])

    train = df[df['date'] < split_date].copy()

    test = df[df['date'] >= split_date].copy()

    for col in ['line', 'from']:

        train[col] = train[col].astype('category')
        test[col] = test[col].astype('category')

    return train, test


def print_baseline(y_test):

    baseline_prediction = [False] * len(y_test)
    print("=== BASELINE ===")
    print('Accuracy:', round(accuracy_score(y_test, baseline_prediction), 4))
    print("(precision/recall/F1 are 0 - it never predicts a delay\n)")


def train_and_eval(name, features, test, train, y_train, y_test):

    model = lgb.LGBMClassifier(n_estimators=200, learning_rate=0.05, class_weight='balanced', verbose=-1)
    model.fit(train[features], y_train)
    pred = model.predict(test[features])
    print(f"\n=== {name} ===")
    print("Accuracy: ", round(accuracy_score(y_test, pred), 4))
    print("Precision:", round(precision_score(y_test, pred), 4))
    print("Recall:   ", round(recall_score(y_test, pred), 4))
    print("F1:       ", round(f1_score(y_test, pred), 4))
    print("Confusion:\n", confusion_matrix(y_test, pred))
    imp = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
    print("Top 10 features:\n", imp.head(10))
    return model


def main():

    feature_columns = ['hour', 'dayofweek', 'month', 'is_weekend', 'line', 'from', 'stop_sequence']

    weather_features = ['temperature_2m', 'precipitation', 'snowfall', 'is_precip', 
                        'is_snow', 'snow_depth', 'heavy_precip', 'windgusts_10m']
    

    df = pd.read_parquet('data/processed/features.parquet')

    split_date = '2019-11-01'

    train, test = load_split(df, split_date)

    X_train, y_train = train[feature_columns], train['delayed']

    X_test, y_test = test[feature_columns], test['delayed']

    print_baseline(y_test)

    train_and_eval("NO WEATHER", feature_columns, test, train, y_train, y_test)

    train_and_eval("WITH WEATHER", feature_columns + weather_features, test, train, y_train, y_test)

    train_and_eval("BASE + AMTRAK", feature_columns + ['amtrak_count'], test, train, y_train, y_test)

    train_and_eval("BASE + PREV_DELAY", feature_columns + ['prev_delay'], test, train, y_train, y_test)

    train_and_eval("BASE + PREV_DELAY + WEATHER", feature_columns + weather_features + ['prev_delay'], test, train, y_train, y_test)

    train_and_eval("BASE + PREV_DELAY + AMTRAK", feature_columns + ['amtrak_count'] + ['prev_delay'], test, train, y_train, y_test)

    train_and_eval("BASE + PREV_DELAY + WEATHER + AMTRAK", feature_columns + weather_features + ['prev_delay'] 
                   + ['amtrak_count'], test, train, y_train, y_test)



if __name__ == '__main__':

    main()