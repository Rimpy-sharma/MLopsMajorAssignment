# app.py
from flask import Flask, request, render_template_string, redirect, url_for
import joblib
from PIL import Image  # type: ignore
import numpy as np
import io
import os

app = Flask(__name__)
MODEL_PATH = "savedmodel.pth"

# Lazy load model
model = None

def get_model():
    """Load model on first request to avoid startup issues"""
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found. Please run train.py first.")
        model = joblib.load(MODEL_PATH)
    return model

HTML = """
<!doctype html>
<title>Olivetti Face Predict</title>
<h1>Upload image (64x64 grayscale recommended)</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
{% if error %}
  <h2 style="color: red;">{{ error }}</h2>
{% endif %}
{% if pred is not none %}
  <h2>Predicted class: {{ pred }}</h2>
{% endif %}
"""

def preprocess_image(file_stream):
    img = Image.open(io.BytesIO(file_stream)).convert("L")  # grayscale
    img = img.resize((64, 64))
    arr = np.asarray(img, dtype=np.float32)
    # olivetti faces are scaled between 0 and 1 (float); dataset uses values ~0-1
    arr = arr / 255.0
    flat = arr.reshape(1, -1)
    return flat

@app.route("/", methods=["GET", "POST"])
def index():
    pred = None
    error = None
    if request.method == "POST":
        f = request.files.get("file")
        if f:
            try:
                data = f.read()
                X = preprocess_image(data)
                m = get_model()
                label = int(m.predict(X)[0])
                pred = label
            except Exception as e:
                error = f"Error: {str(e)}"
    return render_template_string(HTML, pred=pred, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)