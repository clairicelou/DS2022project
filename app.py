import os
import re
import json
from datetime import datetime
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Folders for uploads and logs
UPLOAD_FOLDER = os.path.join('static', 'uploads')
LOG_FILE = os.path.join('logs', 'data.json')

# Make sure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('logs', exist_ok=True)

@app.route("/")
def index():
    return render_template("upload.html")

# ---------- Upload Route ----------
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    species = request.form.get("species", "unknown").replace(" ", "_")
    location = request.form.get("location", "unspecified").replace(" ", "_")
    filename = re.sub(r'[^A-Za-z0-9._-]', '_', file.filename)
    blob_name = f"EcoTrack_{species}_{location}_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}_{filename}"

    file_path = os.path.join(UPLOAD_FOLDER, blob_name)
    file.save(file_path)  # <- make sure you save it!

    # Log metadata
    log_entry = {
        "filename": filename,
        "filepath": file_path,
        "species": species,
        "location": location,
        "timestamp": datetime.utcnow().isoformat()
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return jsonify({"ok": True, "message": "Upload successful!", "file": filename})

# ---------- Gallery Route ----------
@app.route("/gallery")
def gallery():
    query = request.args.get("q", "").lower().strip()

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    images = []
    for log in logs:
        filepath = log["filepath"]
        if not os.path.exists(filepath):
            continue  # skip if file missing

        if query:
            # filter by species or location
            if query in log.get("species", "").lower() or query in log.get("location", "").lower():
                images.append((filepath, log))
        else:
            images.append((filepath, log))

    return render_template("gallery.html", images=images, query=query)

# ---------- Health Check ----------
@app.route("/health")
def health():
    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(debug=True, port=5001)



