# train.py
from sklearn.datasets import fetch_olivetti_faces
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib
import numpy as np

def main():
    X, y = fetch_olivetti_faces(return_X_y=True, shuffle=True, random_state=42)
    # X shape: (400, 64*64) where each sample is flattened
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.7, random_state=42, stratify=y
    )

    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)

    # Save model
    joblib.dump(clf, "savedmodel.pth")
    # (Optionally) save test indices for reproducible testing (not required)
    np.save("test_X.npy", X_test)
    np.save("test_y.npy", y_test)
    print("Training complete. savedmodel.pth written.")

if __name__ == "__main__":
    main()
