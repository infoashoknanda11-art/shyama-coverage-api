from flask import Flask, request, jsonify
import cv2, numpy as np

app = Flask(__name__)

@app.get("/")            # <-- add this
def index():
    return {"ok": True, "msg": "Shyama Coverage API"}

@app.get("/health")      # already present
def health():
    return {"ok": True}
def calc_coverage(image_bytes):
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None: return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    sheet_px = int(cv2.countNonZero(th))
    total_px = int(th.size)
    coverage = (sheet_px/total_px)*100
    return round(coverage,2)

@app.post("/coverage")
def coverage():
    if "image" not in request.files:
        return {"error":"no_file"},400
    f = request.files["image"]
    res = calc_coverage(f.read())
    if res is None:
        return {"error":"bad_image"},400
    return {"coverage":res,"open":round(100-res,2)}
