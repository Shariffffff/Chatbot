from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Make sure to import your specific functions and models
from chatbot import get_chatbot_response
from document_processor import process_uploaded_file
from database import db, Document
from documents import init_docsearch_and_chain

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
app.config['UPLOAD_FOLDER'] = '/Users/sharif/Documents/SpecialistResponses'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
load_dotenv()
CORS(app)

# Serve the React Frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    try:
        file.save(file_path)
        process_uploaded_file(file_path, filename)  # Process and index the file
        return jsonify({'message': 'File uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/documents')
def list_documents():
    documents = Document.query.all()
    documents_list = [{'id': doc.id, 'filename': doc.filename, 'upload_date': doc.upload_date.strftime('%Y-%m-%d %H:%M:%S')} for doc in documents]
    return jsonify(documents_list)

@app.route('/documents/delete/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    document_to_delete = Document.query.get_or_404(document_id)
    db.session.delete(document_to_delete)
    db.session.commit()
    return jsonify({'message': 'Document deleted successfully'}), 200

@app.route('/documents/<filename>')
def get_document(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = get_chatbot_response(user_input)
    return jsonify({'response': response})


if __name__ == '__main__':
    with app.app_context():
        init_docsearch_and_chain(app)  # Initialize document search and QA chain
    app.run(debug=True, port=5000)

