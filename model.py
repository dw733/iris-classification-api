"""Train the classifier on the same split each time."""

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ("sepal_length_cm", "sepal_width_cm", "petal_length_cm", "petal_width_cm")


def fit_classifier():
    iris = load_iris()
    train_x, test_x, train_y, test_y = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
    )
    classifier = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    classifier.fit(train_x, train_y)
    return classifier, iris.target_names, test_x, test_y


if __name__ == "__main__":
    model, _, test_x, test_y = fit_classifier()
    correct = int((model.predict(test_x) == test_y).sum())
    print(f"Held-out accuracy: {correct}/{len(test_y)} ({correct / len(test_y):.1%})")
