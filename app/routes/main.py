from flask import Blueprint, render_template, request, redirect, url_for, current_app
import qrcode
import os
import uuid
import logging
import json
from urllib.parse import urljoin
from app.utils.koos_calculator import calculate_koos_scores  # Add this import
from app.questionnaires_config import QUESTIONNAIRES  # Add this import
from app.utils import calculate_koos_scores, calculate_hoos_scores

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html', show_navbar=True)

@bp.route('/generate_qr')
def generate_qr():
    evaluation_form = request.args.get('evaluation_form')
    if not evaluation_form:
        logging.warning("No evaluation form specified in the generate_qr request.")
        return "No evaluation form specified.", 400

    session_id = str(uuid.uuid4())
    base_url = current_app.config['BASE_URL']
    patient_form_url = f"{base_url}{url_for('main.patient_form', session_id=session_id, evaluation_form=evaluation_form)}"

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(patient_form_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    qr_directory = os.path.join('app', 'static', 'qr_codes')
    if not os.path.exists(qr_directory):
        os.makedirs(qr_directory)

    qr_filename = f"{session_id}.png"
    qr_path = os.path.join(qr_directory, qr_filename)
    img.save(qr_path)

    return redirect(url_for('main.wait_for_result', session_id=session_id, evaluation_form=evaluation_form))

@bp.route('/thank_you')
def thank_you():
    return render_template('thank_you.html', show_navbar=False)

@bp.route('/test_env')
def test_env():
    heroku = current_app.config.get('HEROKU')
    base_url = current_app.config['BASE_URL']
    return f'HEROKU environment variable is set to: {heroku}<br>BASE_URL is: {base_url}'

@bp.route('/patient_form/<session_id>/<evaluation_form>', methods=['GET', 'POST'])
def patient_form(session_id, evaluation_form):
    logging.debug(f"Accessing patient_form with session_id: {session_id}, evaluation_form: {evaluation_form}")
    if request.method == 'POST':
        return handle_form_submission(session_id)
    else:
        return render_questionnaire(session_id, evaluation_form)

@bp.route('/wait_for_result/<session_id>/<evaluation_form>')
def wait_for_result(session_id, evaluation_form):
    result_file = os.path.join('results', f'{session_id}.json')
    if os.path.exists(result_file):
        return process_results(result_file, session_id, evaluation_form)
    else:
        return render_template('wait_for_result.html', session_id=session_id, evaluation_form=evaluation_form)

def handle_form_submission(session_id):
    responses = {key.split('_')[1]: int(value) for key, value in request.form.items() if key.startswith('question_')}
    
    result_directory = os.path.join('results')
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    result_file = os.path.join(result_directory, f'{session_id}.json')

    try:
        with open(result_file, 'w') as file:
            json.dump(responses, file)
        logging.info(f"Saved responses to {result_file}")
    except Exception as e:
        logging.error(f"Error saving responses: {e}")
        return "An error occurred while saving your responses.", 500

    return redirect(url_for('main.thank_you'))

def render_questionnaire(session_id, evaluation_form):
    if evaluation_form not in ['koos', 'hoos']:
        logging.warning(f"Unknown evaluation form requested: {evaluation_form}")
        return "Form not found", 404

    try:
        data = load_questionnaire_data(evaluation_form, 'swedish')
        if not data['sections']:
            logging.error(f"No sections found for {evaluation_form}")
            return "An error occurred while loading the questionnaire.", 500
        
        return render_template(
            f'questionnaires/{evaluation_form}/{evaluation_form}_swe.html',
            session_id=session_id,
            instructions=data.get('instructions', 'Instruktioner saknas.'),
            sections=data.get('sections', [])
        )
    except Exception as e:
        logging.error(f"Error loading questionnaire data: {str(e)}")
        return "An error occurred while loading the questionnaire.", 500

def process_results(result_file, session_id, evaluation_form):
    with open(result_file, 'r') as file:
        responses = json.load(file)
    
    if evaluation_form == 'koos':
        result = calculate_koos_scores(responses)
    elif evaluation_form == 'hoos':
        result = calculate_hoos_scores(responses)
    else:
        return "Unknown questionnaire type", 400
    
    os.remove(result_file)
    logging.info(f"Removed result file: {result_file}")
    
    qr_path = os.path.join('app', 'static', 'qr_codes', f'{session_id}.png')
    if os.path.exists(qr_path):
        os.remove(qr_path)
        logging.info(f"Removed QR code image: {qr_path}")
    
    return render_template('display_result.html', result=result)

def load_questionnaire_data(questionnaire, language='swedish'):
    filename = f'{questionnaire}_{language}.json'
    filepath = os.path.join('data', filename)
    logging.info(f"Attempting to load questionnaire data from: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if isinstance(data, list):
            data = data[0]
        
        instructions = data.get('instructions', 'Instruktioner saknas.')
        sections = data.get('sections', [])
        
        for section in sections:
            section['questions'] = [
                q if isinstance(q, dict) and 'id' in q
                else {'type': 'instructions', 'text': q['text']}
                for q in section.get('questions', [])
            ]
        
        return {"instructions": instructions, "sections": sections}
    except FileNotFoundError:
        logging.error(f"{questionnaire.upper()} data file not found: {filepath}")
        return {"instructions": "Instructions not available.", "sections": []}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON for {questionnaire}: {e}")
        return {"instructions": "Instructions not available.", "sections": []}
    except Exception as e:
        logging.error(f"Unexpected error loading {questionnaire} data: {str(e)}")
        return {"instructions": "Instructions not available.", "sections": []}