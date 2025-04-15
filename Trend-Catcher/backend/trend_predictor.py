import numpy as np
from sklearn.linear_model import LinearRegression

def predict_trend_growth(view_counts):
    """
    Predict trend growth using linear regression.
    :param view_counts: list of daily views (e.g., [1000, 1200, 1500, ...])
    :return: projected view count on day 21
    """
    days = np.array(range(1, len(view_counts)+1)).reshape(-1, 1)
    views = np.array(view_counts).reshape(-1, 1)

    model = LinearRegression()
    model.fit(days, views)

    day_21 = np.array([[21]])
    prediction = model.predict(day_21)

    return int(prediction[0][0])
