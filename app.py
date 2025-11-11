import os
import re
import json
from datetime import datetime
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# ---------- Config ----------
UPLOAD_FOLDER = os.path.join("static", "uploads")
LOG_FILE = os.path.join("logs", "data.json")

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# ---------- Routes ----------

# Browser home page
@app.route("/")
def index():
    return render_template("upload.html")

# API: Upload image
@app.route("/api/v1/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"ok": False, "error": "No file uploaded"}), 400

    species = request.form.get("species", "unknown").replace(" ", "_")
    location = request.form.get("location", "unspecified").replace(" ", "_")
    filename = re.sub(r"[^A-Za-z0-9._-]", "_", file.filename)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    blob_name = f"EcoTrack_{species}_{location}_{timestamp}_{filename}"

    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, blob_name)
    file.save(file_path)

    # Log metadata
    log_entry = {
        "filename": filename,
        "filepath": f"/static/uploads/{blob_name}",  # relative URL for browser access
        "species": species,
        "location": location,
        "timestamp": datetime.utcnow().isoformat(),
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(log_entry)
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return jsonify({"ok": True, "message": "Upload successful!", "file": filename, "url": log_entry["filepath"]})

# API: Gallery JSON
@app.route("/api/v1/gallery", methods=["GET"])
def api_gallery():
    if not os.path.exists(LOG_FILE):
        return jsonify({"ok": True, "gallery": []})

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    # Return only files that exist
    urls = [log["filepath"] for log in logs if os.path.exists("." + log["filepath"])]
    return jsonify({"ok": True, "gallery": urls})

# Browser gallery page
@app.route("/gallery")
def gallery():
    query = request.args.get("q", "").lower().strip()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    images = []
    for log in logs:
        if not os.path.exists("." + log["filepath"]):
            continue
        if query and query not in log.get("species", "").lower() and query not in log.get("location", "").lower():
            continue
        images.append(log)

    return render_template("gallery.html", images=images, query=query)

# Health check
@app.route("/health")
def health():
    return jsonify(ok=True)

# ---------- Main ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)






