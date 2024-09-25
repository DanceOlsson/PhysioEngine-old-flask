# Import the Flask class and render_template function and others from the flask module
from flask import Flask, render_template, request, redirect, url_for
import qrcode  # For generating QR codes
import os      # For file path operations
import uuid    # For generating unique session IDs
import logging # For logging activity and catching issues
import socket  # For getting the local IP address

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from a .env file

# Create an instance of the Flask class for your web application
app = Flask(__name__)





# Configure logging
# level=logging.INFO: Sets the logging level to INFO, which means all messages at this level and above (WARNING, ERROR, CRITICAL) will be logged.
# Default Handler: By default, logs are printed to the console (stdout).
logging.basicConfig(level=logging.INFO)
# Fråga chatGPT om implementering av loggning!! Finns att hitta med ctrl+f i original OBSchatten i chatGPT



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
        return "No evaluation form specified.", 400  # Return a 400 Bad Request if missing

    # Step 3: Generate a unique session ID using UUID4
    session_id = str(uuid.uuid4())
    
    # Step 4: Dynamically determine the base URL of the deployed app
    # Use the 'BASE_URL' environment variable if set (in terminal venv?); otherwise, use 'request.host_url'
    # 'request.host_url' captures the base URL from the hosting service instead(I think?) (includes protocol and domain)
    base_url = os.environ.get('BASE_URL', request.host_url.rstrip('/'))  # Removes trailing slash to prevent double slashes
    
    # Step 5: Construct the full URL for the patient form using the session ID and evaluation form
    # 'url_for' generates the URL for the 'patient_form' route with the given parameters
    qr_url = f'{base_url}{url_for("patient_form", session_id=session_id, evaluation_form=evaluation_form)}'
    
    # Log the generated QR code URL for debugging purposes
    logging.info(f"Generated QR code URL: {qr_url}")
    
    # Step 6: Generate the QR code image for the constructed URL
    img = qrcode.make(qr_url)
    
    # Step 7: Define the directory to store generated QR codes
    qr_directory = os.path.join('static', 'qr_codes')
    
    # Create the directory if it doesn't exist
    if not os.path.exists(qr_directory):
        os.makedirs(qr_directory)
    
    # Define the filename for the QR code image using the session ID
    qr_filename = f'{session_id}.png'
    qr_path = os.path.join(qr_directory, qr_filename)
    
    # Save the QR code image to the defined path
    img.save(qr_path)
    
    # Step 8: Redirect the user to the result waiting page with session details
    return redirect(url_for('wait_for_result', session_id=session_id, evaluation_form=evaluation_form))




#Route for physio "Result waiting page"
@app.route('/wait_for_result/<session_id>/<evaluation_form>')
def wait_for_result(session_id, evaluation_form):
    
    #logging to check the HTTP method used when the wait_for_result route is accessed 
    #(put in because of issue with GET and POST methods...)
    logging.info(f"wait_for_result accessed via {request.method}")
    
    # Check if the result is available
    result_file = os.path.join('results', f'{session_id}.txt')
    if os.path.exists(result_file):
        # Read the result from the file
        with open(result_file, 'r') as file:
            total_score = file.read()
        # Delete the result file after reading
        os.remove(result_file)
        # Render the result page
        return render_template('display_result.html', total_score=total_score)
    else:
        # Render the waiting page
        return render_template('wait_for_result.html', session_id=session_id, evaluation_form=evaluation_form)


# Route for the Patient Form, as seen after scanning QR-code
@app.route('/patient_form/<session_id>/<evaluation_form>', methods=['GET', 'POST'])
def patient_form(session_id, evaluation_form):
    if request.method == 'POST':
        # Process the submitted form data
        # Retrieve the answers from the form
        pain_intensity = int(request.form.get('pain_intensity', 0))
        
        # Calculate the score (this is a simplified example)(Add more here when we put the real questionaire in)
        total_score = pain_intensity  # Adjust this calculation based on additional fields
        
        # Save the result to a file named after the session_id
        result_directory = os.path.join('results')
        if not os.path.exists(result_directory):
            os.makedirs(result_directory)
        result_file = os.path.join(result_directory, f'{session_id}.txt')
        with open(result_file, 'w') as file:
            file.write(str(total_score))
        
        # Redirect to a thank-you page
        return redirect(url_for('thank_you'))
    else:
        # Render the appropriate form based on the evaluation_form parameter
        if evaluation_form == 'oswestry':
            # Render the Oswestry Disability Index form template
            return render_template('questionnaires/oswestry_form.html', session_id=session_id)
        else:
            # Return a 404 error if the form is not found
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





# Check if the executed file is the main program and run the app
if __name__ == '__main__':
    # Run the Flask app with debugging enabled, accessible externally & defined port
    PORT = 8000  # Define your port number here
    app.run(debug=True, host='0.0.0.0', port=PORT)





