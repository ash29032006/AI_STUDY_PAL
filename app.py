import os
import csv
from io import StringIO
from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS

import ai_engine

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    """Serve the single-page frontend (index.html)."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/study-plan', methods=['POST'])
def create_study_plan():
    """Generates a weekly study plan based on subjects and hours."""
    data = request.json
    subjects = data.get('subjects', [])
    if not subjects:
        subjects = [{"subject": "General", "hours": 7}]
        
    result = ai_engine.generate_study_plan(subjects)
    return jsonify(result)

@app.route('/api/quiz', methods=['POST'])
def get_quiz():
    """Returns a list of dynamically generated MCQ questions based on a PDF file."""
    import PyPDF2
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
        
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    except Exception as e:
        return jsonify({"error": f"Failed to read PDF: {str(e)}"}), 400
        
    # Limit to roughly 15000 chars to avoid hitting Llama max tokens
    text = text[:15000]
    
    result = ai_engine.generate_quiz(text)
    return jsonify(result)

@app.route('/api/summarize', methods=['POST'])
def get_summary():
    """Returns a summarized version of the pasted text."""
    data = request.json
    text = data.get('text', '')
    result = ai_engine.summarize_text(text)
    return jsonify(result)

@app.route('/api/tips', methods=['POST'])
def get_tips():
    """Returns bullet-point tips and keywords based on a topic."""
    data = request.json
    topic = data.get('topic', '')
    result = ai_engine.generate_tips(topic)
    return jsonify(result)

@app.route('/api/feedback', methods=['POST'])
def get_feedback():
    """Returns a motivational message."""
    data = request.json
    subject = data.get('subject', 'your studies')
    result = ai_engine.generate_feedback(subject)
    return jsonify(result)

@app.route('/api/download', methods=['GET'])
def download_schedule():
    """Generates and returns the study plan as a CSV file."""
    data_str = request.args.get('data', 'General:7')
    subjects = []
    
    for item in data_str.split(','):
        if ':' in item:
            subj, hrs_str = item.split(':', 1)
            try:
                subjects.append({"subject": subj, "hours": int(hrs_str)})
            except ValueError:
                pass
                
    if not subjects:
        subjects = [{"subject": "General", "hours": 7}]
        
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Day', 'Subject', 'Hours', 'Activity'])
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Simple fallback generation
    for subj_info in subjects:
        subj = subj_info['subject']
        hrs = subj_info['hours']
        daily_hours = round(hrs / 7, 1)
        for day in days:
            activity = f"Study {subj} notes" if day not in ["Saturday", "Sunday"] else f"Review {subj} material"
            cw.writerow([day, subj, daily_hours, activity])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=study_schedule.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == '__main__':
    app.run(debug=True, port=5000)
