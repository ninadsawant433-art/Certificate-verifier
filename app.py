# app.py
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
from gridfs import GridFS
from main import verify_certificate
import os
import hashlib

app = Flask(__name__)
app.secret_key = "super_secret_key_for_cert_verifier"

# ================== MONGODB CONFIG ==================
app.config["MONGO_URI"] = "mongodb://localhost:27017/cert_verifier_db"
mongo = PyMongo(app)

db = mongo.db
fs = GridFS(db, collection="certificates")

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ================== MAIN ROUTE ==================
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    is_success = False

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return render_template('index.html')

        file = request.files['file']

        if file.filename == '':
            flash('No file selected')
            return render_template('index.html')

        if not allowed_file(file.filename):
            flash('Invalid file type. Allowed: PDF, PNG, JPG, JPEG')
            return render_template('index.html')

        filename = secure_filename(file.filename)

        # Save to GridFS
        file_id = fs.put(
            file,
            filename=filename,
            content_type=file.content_type
        )

        # Read back from GridFS to temporary file
        grid_out = fs.get(file_id)
        temp_path = f"temp_{filename}"

        try:
            # Write temp file
            with open(temp_path, 'wb') as f:
                f.write(grid_out.read())

            # Optional: compute hash
            with open(temp_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()

            # ----------------------------------------------------
            # VERIFY CERTIFICATE
            # ----------------------------------------------------
            report = verify_certificate(temp_path)

            # ----------------------------------------------------
            # 🟢 VERY FORGIVING SUCCESS DETECTION (AS REQUESTED)
            # ----------------------------------------------------
            clean_report = report.lower()                     # make lowercase
            clean_report = clean_report.replace('<[^>]+>', ' ')  # remove HTML tags
            clean_report = ' '.join(clean_report.split())     # collapse whitespace

            # Success if "valid" + any good percentage
            is_success = (
                "valid" in clean_report and
                any(num in clean_report for num in ["100%", "90%", "80%", "70%"])
            )

            print("REPORT:", report)
            print("CLEANED:", clean_report)
            print("is_success:", is_success)

            result = report

            # ----------------------------------------------------
            # UPDATE DB
            # ----------------------------------------------------
            db['certificates.files'].update_one(
                {"_id": file_id},
                {"$set": {"verified": is_success}}
            )

        except Exception as e:
            flash(f"Verification error: {str(e)}")

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # ------------------------------------------------------------
    # PASS TO TEMPLATE
    # ------------------------------------------------------------
    return render_template(
        'index.html',
        result=result,
        is_success=is_success
    )


# ================== RUN ==================
if __name__ == '__main__':
    app.run(debug=True)