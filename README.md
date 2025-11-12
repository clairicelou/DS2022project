# Case–Study Final Project Write–Up: Wildlife Image Logger


## 1. Executive Summary
Flask web app for collecting and displaying wildlife photos. Users upload images, which are logged with metadata and shown in a public gallery.

Problem: Wildlife researchers and environmental scientists often have trouble keeping track of wildlife and animal sighting over time efficiently.

Solution: The Wildlife Image Logger is a web app built with Flask that lets users upload wildlife photos from their phones or computers, tag them by species and location, and view them in a searchable gallery. The images are stored either in the cloud (using Azure Blob Storage) or on the local computer for demos, and they show up automatically in a public gallery. This makes it easy to check uploads, share data with field teams, and keep track of wildlife sightings over time, without needing complicated tools or manual logs.


## 2. System Overview
- **Course Concepts**: 
  - Flask API: Created a simple web app with upload and gallery pages for managing images
  - Flask Routing & File Uploads: Implemented endpoints for image handling and metadata logging
  - Structured Logging (JSON): Stored upload metadata (species, location, timestamp) in a local JSON file
  - Docker Containerization: Packaged the entire app in a reproducible environment for easy deployment
- **Architecture Diagram**: 
  - ![Architecture Diagram](assets/architecture.png)
- **Data/Models/Services**: 
  - Uploads: Stored under `/static/uploads/`
  - Logs: Stored in `/logs/data.json`
  - File naming: Automatically includes species, location, and timestamp (for organization)
  - Formats: Accepts common image types (.png, .jpg, .jpeg)


## 3. How to Run (Docker) 
#### a. Build the image
docker build -t ecotrack:latest .
#### b. Run the container
docker run --rm -p 5001:5000 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/static/uploads:/app/static/uploads \
  ecotrack:latest

(Mounts local folders so uploaded files and logs are saved persistently.)
#### c. Then open your web browser and go to:
http://localhost:5001
#### d. Health check
curl http://localhost:5001/health


## 4. Design Decisions
**Why this concept?**

I decided to make a Wildlife Image Logger because I wanted to practice Flask routing, file uploads, and Docker deployment, which were topics that we learned in class. It’s a straightforward and simple idea, but it feels realistic to build because it demonstrates how user images can move through a full web app. 

**Alternatives considered:**

I could have made a command-line app to upload files, but using Flask shows more clearly how a web app handles users and files.

**Tradeoffs:**

Using Docker makes setup a little more complicated, but it lets the app run anywhere. I chose JSON logs to save upload data instead of a database because it’s simpler and easier to work with, even though that means the app wouldn’t handle a huge number of users as easily.

**Security/Privacy:** 

Input validation ensures only image files are uploaded. No sensitive user data (PII) is collected. Secrets management was not required for this project.

**Ops:** 

Uploaded data is logged in /logs/data.json so I can track uploads. The app isn’t built for heavy traffic, but it works smoothly in a single Docker container.

## 5. Results & Evaluation
**Gallery Example**
![Gallery Example](assets/app_gallery.png)

**Sample Output (from Upload)**
{
  "ok": true,
  "message": "Upload successful!",
  "file": "EcoTrack_Flamingos_South_America_20251110T202005_flamingos.jpeg"
}

**Performance Notes**
- App starts instantly in Docker.
- Memory footprint <50MB.
- Uploads and gallery rendering are fast.

**Validation Testing**
- Verified /upload, /gallery, and /health endpoints using curl.
- Confirmed that uploaded images appear in /static/uploads/ and show correctly in the gallery.

### Tested endpoints with curl commands:
#### Upload a test image
curl -X POST -F "file=@assets/test-image.png" http://localhost:5001/api/v1/upload

Sample Output (from Upload):

{
  "file": "test-image.png",
  "message": "Upload successful!",
  "ok": true,
  "url": "/static/uploads/EcoTrack_unknown_unspecified_20251111T012352_test-image.png"
}

#### Fetch gallery
curl http://localhost:5001/api/v1/gallery

Sample Output (from Gallery):

{
  "gallery": [
    "/static/uploads/EcoTrack_unknown_unspecified_20251111T012352_test-image.png"
  ],
  "ok": true
}


## 6. What’s Next
- Show a preview of the image on the upload page so users can see it before they submit.
- Add more search/filter options on the gallery page (like by date or species).
- Add login so only certain people can upload images.
- Add simple logs or a dashboard to monitor uploads and activity.


## 7. Links (Required)
GitHub Repo: https://github.com/clairicelou/DS2022project 

Public Cloud App (optional): <INSERT-CLOUD-URL>

