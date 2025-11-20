# test.py
import joblib
import numpy as np
from sklearn.metrics import accuracy_score

def main():
    # load model
    model = joblib.load("savedmodel.pth")

    # load test arrays saved by train.py (if present)
    try:
        X_test = np.load("test_X.npy")
        y_test = np.load("test_y.npy")
    except Exception as e:
        # fallback: re-create the split (consistent with train.py)
        from sklearn.datasets import fetch_olivetti_faces
        from sklearn.model_selection import train_test_split
        X, y = fetch_olivetti_faces(return_X_y=True, shuffle=True, random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, train_size=0.7, random_state=42, stratify=y
        )

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Test accuracy: {acc:.4f}")

if __name__ == "__main__":
    main()