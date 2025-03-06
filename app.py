import os
import pdfplumber
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Configure Gemini AI
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n" if page.extract_text() else ""
    return text.strip()

# Score resume using Gemini AI
def score_resume(jd_text, resume_text):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    Compare the following resume with the given job description and provide a score out of 100.
    - Job Description: {jd_text}
    - Resume: {resume_text}
    Return only the score.
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response else "N/A"

# Upload Job Description
@app.route("/upload_jd", methods=["POST"])
def upload_jd():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    jd_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(jd_path)

    # Extract JD text and store it
    jd_text = extract_text_from_pdf(jd_path)
    return jsonify({"message": "JD uploaded successfully", "jd_text": jd_text})

# Upload Resumes and Score them
@app.route("/upload_resumes", methods=["POST"])
def upload_resumes():
    jd_text = request.form.get("jd_text")  # Get JD text from frontend
    if not jd_text:
        return jsonify({"error": "JD not uploaded"}), 400

    if "files[]" not in request.files:
        return jsonify({"error": "No resumes uploaded"}), 400

    files = request.files.getlist("files[]")
    results = []

    for file in files:
        filename = secure_filename(file.filename)
        resume_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(resume_path)

        resume_text = extract_text_from_pdf(resume_path)
        score = score_resume(jd_text, resume_text)

        results.append({"filename": filename, "score": score})

    return jsonify({"message": "Resumes scored", "results": results})

if __name__ == "__main__":
    app.run(debug=True)
