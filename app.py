from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
from resume_processor import ResumeProcessor
from database import Database

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

processor = ResumeProcessor()
db = Database()

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'resume' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(url_for('index'))
        
        file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        if not job_description:
            flash('Please enter a job description', 'error')
            return redirect(url_for('index'))
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload PDF only.', 'error')
            return redirect(url_for('index'))
        
        filename = secure_filename(f"{uuid.uuid4().hex}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            result = processor.analyze_resume(filepath, job_description)
            result['original_filename'] = file.filename
            db.save_result(result)
            os.remove(filepath)
            return render_template('results.html', result=result)
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e
            
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/history')
def history():
    results = db.get_all_results()
    return render_template('history.html', results=results)

@app.route('/result/<int:result_id>')
def view_result(result_id):
    result = db.get_result_by_id(result_id)
    if result:
        return render_template('results.html', result=result)
    flash('Result not found', 'error')
    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)