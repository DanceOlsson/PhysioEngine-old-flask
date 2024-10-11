## PhysioEngine API Documentation

This API allows physiotherapists to generate QR codes for patients to fill out evaluation forms on their mobile devices. The API then processes the results and provides them to the physiotherapist.

### Inputs

* **Evaluation Form:** The type of evaluation form to be used. Currently supported forms are 'koos' (Knee injury and Osteoarthritis Outcome Score) and 'hoos' (Hip dysfunction and Osteoarthritis Outcome Score).
* **Patient Responses:** The patient's responses to the questions on the evaluation form. These are submitted as a JSON object, where the keys are the question IDs and the values are the patient's answers.

### Outputs

* **QR Code:** A QR code image that, when scanned, takes the patient to the evaluation form on their mobile device.
* **Results:** The processed results of the evaluation form, including subscale scores, total score, and interpretation. This is returned as a JSON object.