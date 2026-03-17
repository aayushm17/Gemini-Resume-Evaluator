import flask
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from extractor import extract_text_from_file
from evaluator import process_resume_evaluation

app = flask.Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/evaluate-resume', methods=['POST'])
def evaluate_resume():
    if 'file' not in flask.request.files:
        return flask.jsonify({'error': 'No file provided'}), 400

    resume_file = flask.request.files['file']
    job_description = flask.request.form.get('job_description', '')

    if not job_description:
        return flask.jsonify({'error': 'Job description is required'}), 400

    filename = secure_filename(resume_file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    resume_file.save(filepath)

    try:
        resume_text = extract_text_from_file(filepath)
        print(f"DEBUG: Checking extracted text length: {len(resume_text)} characters")
        result = process_resume_evaluation(resume_text, job_description)
        print(f"DEBUG: Final JSON sent to Frontend: {result}")  # ADD THIS
        return flask.jsonify(result)
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True)
