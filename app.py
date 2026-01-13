# app.py
from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
import os

# Folder for uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Enhanced HTML template
HTML = """
<!doctype html>
<html>
<head>
<title>📁 File Upload & Browser</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
    body {
        font-family: 'Inter', Arial, sans-serif;
        background: #f5f7fa;
        color: #333;
        margin: 0;
        padding: 0;
    }
    .container {
        max-width: 800px;
        margin: 40px auto;
        padding: 20px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    h1 {
        text-align: center;
        color: #1e40af;
        margin-bottom: 20px;
    }
    form {
        display: flex;
        justify-content: center;
        margin-bottom: 30px;
        gap: 10px;
    }
    input[type="file"] {
        padding: 6px;
    }
    input[type="submit"] {
        background-color: #1e40af;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        transition: background-color 0.3s;
    }
    input[type="submit"]:hover {
        background-color: #3b82f6;
    }
    .files {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 12px;
    }
    .file-card {
        background: #f1f5f9;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        word-break: break-word;
        transition: transform 0.2s;
    }
    .file-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .file-card a {
        text-decoration: none;
        color: #1e40af;
        font-weight: 500;
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        font-size: 0.9em;
        color: #555;
    }
</style>
</head>
<body>
<div class="container">
    <h1>📁 Upload & Browse Files</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <input type="submit" value="Upload">
    </form>
    <div class="files">
    {% for filename in files %}
        <div class="file-card">
            <a href="{{ url_for('uploaded_file', filename=filename) }}" target="_blank">{{ filename }}</a>
        </div>
    {% endfor %}
    </div>
    <div class="footer">
        Powered by Flask & Python
    </div>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        f = request.files['file']
        if f:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            return redirect(url_for('upload_file'))
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string(HTML, files=files)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
