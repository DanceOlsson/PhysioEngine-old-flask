# Import the Flask class and render_template function and others from the flask module
from flask import Flask, render_template, request, redirect, url_for
import qrcode  # For generating QR codes
import os      # For file path operations
import uuid    # For generating unique session IDs
import logging # For logging activity and catching issues
import socket  # For getting the local IP address
import json    # For getting the json data to backend. duh..

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from a .env file

from urllib.parse import urljoin

BASE_URL = os.environ.get('BASE_URL', 'https://safe-newly-salmon.ngrok-free.app')  # Default to localhost for local testing



# Create an instance of the Flask class for your web application
app = Flask(__name__)





# Configure logging
# level=logging.INFO: Sets the logging level to INFO, which means all messages at this level and above (WARNING, ERROR, CRITICAL) will be logged.
# Default Handler: By default, logs are printed to the console (stdout).
logging.basicConfig(level=logging.INFO)
# Fråga chatGPT om implementering av loggning!! Finns att hitta med ctrl+f i original OBSchatten i chatGPT


@app.before_request
def redirect_to_www():
    # Check if the host is the root domain without www
    if request.host == "physioengine.com":
        # Redirect to the www version
        return redirect(f"https://www.physioengine.com{request.path}", code=301)


# ------------------------- helper functions ----------------------

def load_koos_data(language='swedish'):
    """
    Loads the KOOS questionnaire data based on the specified language.
    
    Args:
        language (str): The language of the questionnaire (e.g., 'swedish').
    
    Returns:
        dict: The KOOS data containing instructions and a flat list of questions.
    """
    filename = f'koos_{language}.json'
    filepath = os.path.join('data', filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            sections = json.load(file)
            questions = []
            for section in sections:
                section_title = section.get('title', 'Utan Titel')  # Default to 'Utan Titel' if title is missing
                for question in section.get('questions', []):
                    # Optionally, include section title within each question
                    question_copy = question.copy()
                    question_copy['section'] = section_title
                    questions.append(question_copy)
            instructions = "Fyll i frågeformuläret nedan."  # You can customize this or include it in JSON
            return {"instructions": instructions, "questions": questions}
    except FileNotFoundError:
        logging.error(f"KOOS data file not found: {filepath}")
        return {"instructions": "Instructions not available.", "questions": []}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        return {"instructions": "Instructions not available.", "questions": []}



def calculate_koos_scores(responses):
    """
    Calculates and normalizes KOOS scores for each subscale.

    Args:
        responses (dict): A dictionary with question IDs as keys and responses as integer values.

    Returns:
        dict: A dictionary with subscale names as keys and normalized scores as values.
    """
    subscales = {
        'Pain': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9'],
        'Symptoms': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7'],
        'ADL': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17'],
        'Sport/Rec': ['SP1', 'SP2', 'SP3', 'SP4', 'SP5'],
        'QOL': ['Q1', 'Q2', 'Q3', 'Q4']
    }

    subscale_scores = {}

    for subscale, questions in subscales.items():
        subscale_responses = [responses.get(q_id, 0) for q_id in questions]
        total_score = sum(subscale_responses)
        num_questions = len(questions)
        max_possible_score = num_questions * 4  # Assuming maximum value per question is 4
        min_possible_score = num_questions * 0  # Assuming minimum value per question is 0

        # Normalize the score to a 0-100 scale
        if max_possible_score - min_possible_score == 0:
            normalized_score = 0
        else:
            normalized_score = ((max_possible_score - total_score) / (max_possible_score - min_possible_score)) * 100
            normalized_score = round(normalized_score, 2)

        subscale_scores[subscale] = normalized_score

    return subscale_scores










# ----------------- Routes ------------------

# Define the route for the home page using the route() decorator
@app.route('/')
def home():
    return render_template('index.html')  # This will render the index.html template



# ----------------- Physios ----------------------------------




# Route to handle the physio list of questionnaires. Click link to generate qr-code
@app.route('/physio')
def physio():
    # Render the 'physio.html' template for the physiotherapist interface
    return render_template('physio.html')



# Route to Handle QR Code Generation
@app.route('/generate_qr')
def generate_qr():
    """
    Generates a QR code for the selected evaluation form and redirects to the result waiting page.
    
    Steps:
    1. Retrieve the 'evaluation_form' parameter from the query string.
    2. Validate that the 'evaluation_form' parameter is provided.
    3. Generate a unique session ID for the evaluation.
    4. Dynamically determine the base URL of the deployed app.
    5. Construct the full URL for the patient form using the session ID and evaluation form.
    6. Generate a QR code image for the constructed URL.
    7. Save the QR code image to the 'static/qr_codes' directory.
    8. Redirect the user to the result waiting page.
    """
    
    # Step 1: Retrieve the 'evaluation_form' parameter from the query string
    evaluation_form = request.args.get('evaluation_form')
        
    # Step 2: Validate that the 'evaluation_form' parameter is provided
    if not evaluation_form:
        logging.warning("No evaluation form specified in the generate_qr request.")
        return "No evaluation form specified.", 400  # Return a 400 Bad Request if missing

    # Step 3: Generate a unique session ID using UUID4
    session_id = str(uuid.uuid4())
    logging.info(f"Generated session ID: {session_id}")
    
    # Step 4: Dynamically determine the base URL of the deployed app
    # Use the 'BASE_URL' environment variable if set; otherwise, use 'request.host_url'
    base_url = os.environ.get('BASE_URL', request.host_url.rstrip('/'))  # Removes trailing slash to prevent double slashes
    logging.info(f"Base URL: {base_url}")
    
    # Step 5: Construct the full URL for the patient form using the session ID and evaluation form
    # 'url_for' generates the URL for the 'patient_form' route with the given parameters
    patient_form_url = f"{base_url}{url_for('patient_form', session_id=session_id, evaluation_form=evaluation_form)}"
    logging.info(f"Patient form URL: {patient_form_url}")
    
    # Step 6: Generate the QR code image for the constructed URL
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(patient_form_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    logging.info("QR code generated successfully.")
    
    # Step 7: Define the directory to store generated QR codes
    qr_directory = os.path.join('static', 'qr_codes')
    
    # Create the directory if it doesn't exist
    if not os.path.exists(qr_directory):
        os.makedirs(qr_directory)
        logging.info(f"Created QR codes directory at {qr_directory}")
    
    # Define the filename for the QR code image using the session ID
    qr_filename = f"{session_id}.png"
    qr_path = os.path.join(qr_directory, qr_filename)
    
    # Save the QR code image to the defined path
    img.save(qr_path)
    logging.info(f"Saved QR code image to {qr_path}")
    
    # Step 8: Redirect the user to the result waiting page with session details
    return redirect(url_for('wait_for_result', session_id=session_id, evaluation_form=evaluation_form))



#Route for physio "Result waiting page"
@app.route('/wait_for_result/<session_id>/<evaluation_form>')
def wait_for_result(session_id, evaluation_form):
    """
    Checks for the existence of a response file and displays the results.
    
    Args:
        session_id (str): Unique identifier for the session.
        evaluation_form (str): Type of evaluation form (e.g., 'koos').
    
    Returns:
        Rendered HTML template with results or a waiting page.
    """
    result_file = os.path.join('results', f'{session_id}.json')
    if os.path.exists(result_file):
        with open(result_file, 'r') as file:
            responses = json.load(file)
        
        subscale_scores = calculate_koos_scores(responses)
        
        # Optionally, remove the result file after processing to prevent reprocessing
        os.remove(result_file)
        logging.info(f"Removed result file: {result_file}")
        
        # Optionally, remove the QR code image associated with this session
        qr_path = os.path.join('static', 'qr_codes', f'{session_id}.png')
        if os.path.exists(qr_path):
            os.remove(qr_path)
            logging.info(f"Removed QR code image: {qr_path}")
        
        # Redirect to display_result.html with the scores
        return render_template('display_result.html', subscale_scores=subscale_scores)
    else:
        # Render the waiting page with QR code and auto-refresh
        return render_template('wait_for_result.html', session_id=session_id, evaluation_form=evaluation_form)




@app.route('/patient_form/<session_id>/<evaluation_form>', methods=['GET', 'POST'])
def patient_form(session_id, evaluation_form):
    """
    Handles the rendering and processing of the KOOS questionnaire form.

    Args:
        session_id (str): Unique identifier for the session.
        evaluation_form (str): Type of evaluation form (e.g., 'koos').

    Returns:
        Rendered HTML template or redirect to another route.
    """
    if request.method == 'POST':
        # ========================
        # Processing Form Submission
        # ========================

        # Initialize an empty dictionary to store responses
        responses = {}

        # Iterate over all form data submitted by the patient
        for key, value in request.form.items():
            if key.startswith('question_'):
                # Extract the question ID from the form field name
                question_id = key.split('_')[1]  # e.g., 'S1' from 'question_S1'
                try:
                    # Convert the response value to an integer
                    responses[question_id] = int(value)
                except ValueError:
                    # Handle cases where conversion fails
                    logging.warning(f"Invalid value for {question_id}: {value}")
                    responses[question_id] = 0  # Default to 0 or handle as needed

        # ========================
        # Saving Responses for Scoring
        # ========================

        # Define the directory where results will be saved
        result_directory = os.path.join('results')

        # Create the directory if it doesn't exist
        if not os.path.exists(result_directory):
            os.makedirs(result_directory)
            logging.info(f"Created directory: {result_directory}")

        # Define the path for the result file using session_id
        result_file = os.path.join(result_directory, f'{session_id}.json')

        try:
            # Open the result file in write mode and save the responses as JSON
            with open(result_file, 'w') as file:
                json.dump(responses, file)
            logging.info(f"Saved responses to {result_file}")
        except Exception as e:
            # Log any errors that occur during file writing
            logging.error(f"Error saving responses: {e}")
            return "An error occurred while saving your responses.", 500

        # ========================
        # Redirecting to Thank-You Page
        # ========================

        return redirect(url_for('thank_you'))
    
    else:
        # ========================
        # Rendering the KOOS Questionnaire Form
        # ========================

        if evaluation_form == 'koos':
            # Load the KOOS data for Swedish
            koos_data = load_koos_data('swedish')
            instructions = koos_data.get('instructions', 'Instruktioner saknas.')
            questions = koos_data.get('questions', [])

            # Log the number of questions loaded
            logging.info(f"Loaded {len(questions)} KOOS questions for Swedish.")

            # Render the KOOS questionnaire template with instructions and questions
            return render_template(
                'questionnaires/koos/koos_swe.html',
                session_id=session_id,
                instructions=instructions,
                questions=questions
            )
        else:
            # If the evaluation_form type is not recognized, return a 404 error
            logging.warning(f"Unknown evaluation form requested: {evaluation_form}")
            return "Form not found", 404







# ----------------- General Users ---------------------




# Route for General User Flow
@app.route('/user/questionnaires')
def user_questionnaires():
    # List of available questionnaires with descriptions
    questionnaires = [
        {
            'name': 'Oswestry Disability Index',
            'slug': 'oswestry',
            'description': 'Assessing disability in patients with low back pain.'
        },
        # Add more questionnaires as needed
    ]
    # Render the general user questionnaire list template
    return render_template('users/user_questionnaires.html', questionnaires=questionnaires)




# Route for "thank you" page
@app.route('/thank_you')
def thank_you():
    # Render a simple thank-you template
    return render_template('thank_you.html')





#------------------- NOW RUN THIS SHIT BIIIIITCHH--------------------

# Check if the executed file is the main program and run the app
if __name__ == '__main__':
    # Run the Flask app with debugging enabled, accessible externally & defined port
    PORT = 8000  # Define your port number here
    app.run(debug=True, host='0.0.0.0', port=PORT)





