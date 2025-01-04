from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import PyPDF2
import requests
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to convert PDF to text
def pdf_to_text(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to send a call to the LLM model
def send_call_to_llm(data):
    url = "https://a640-35-240-158-176.ngrok-free.app/"
    headers = {"content-type": "application/json"}
    try:
        response = requests.post(url, data=json.dumps({"data": data}), headers=headers)

        # Process response
        if response.status_code == 200:
           # return response.json().get('answer', "No answer provided by the model")
           return response.text  
        else:
            return f"Error: {response.status_code}, {response.text}"
    except requests.RequestException as e:
        return f"Request failed: {str(e)}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model_choice = request.form.get('model_choice')
        user_question = request.form.get('user_question')
        file = request.files.get('file')

        # Initialize the data dictionary
        data = {
            'question': user_question,
            'model_used': model_choice,
            'resume_text': None
        }

        # If 'resume_based' model is selected, process the uploaded file
        if model_choice == 'resume_based' and file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            if filename.lower().endswith('.pdf'):
                data['resume_text'] = pdf_to_text(file_path)
            elif filename.lower().endswith('.txt'):
                with open(file_path, 'r') as f:
                    data['resume_text'] = f.read()

        # Call the LLM model and return the answer
        answer = send_call_to_llm(data)
        print(answer)
        return jsonify({"answer": answer})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

