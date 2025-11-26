# app.py
from flask import Flask, request, render_template_string, redirect, url_for
import joblib
from PIL import Image  # type: ignore
import numpy as np
import io

app = Flask(__name__)
MODEL_PATH = "savedmodel.pth"

model = joblib.load(MODEL_PATH)

HTML = """
<!doctype html>
<title>Olivetti Face Predict</title>
<h1>Upload image (64x64 grayscale recommended)</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
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
    if request.method == "POST":
        f = request.files.get("file")
        if f:
            data = f.read()
            X = preprocess_image(data)
            label = int(model.predict(X)[0])
            pred = label
    return render_template_string(HTML, pred=pred)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)