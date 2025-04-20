from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)

# Update Database Configuration for production
DATABASE_URL = os.environ.get('DATABASE_URL', 'mysql+pymysql://Username:Password@localhost/YOUR_DATABASE_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Database Model
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mean_radius = db.Column(db.Float)
    mean_texture = db.Column(db.Float)
    mean_perimeter = db.Column(db.Float)
    mean_area = db.Column(db.Float)
    mean_smoothness = db.Column(db.Float)
    mean_compactness = db.Column(db.Float)
    mean_concavity = db.Column(db.Float)
    mean_concave_points = db.Column(db.Float)
    mean_symmetry = db.Column(db.Float)
    mean_fractal_dimension = db.Column(db.Float)
    radius_error = db.Column(db.Float)
    texture_error = db.Column(db.Float)
    perimeter_error = db.Column(db.Float)
    area_error = db.Column(db.Float)
    smoothness_error = db.Column(db.Float)
    compactness_error = db.Column(db.Float)
    concavity_error = db.Column(db.Float)
    concave_points_error = db.Column(db.Float)
    symmetry_error = db.Column(db.Float)
    fractal_dimension_error = db.Column(db.Float)
    worst_radius = db.Column(db.Float)
    worst_texture = db.Column(db.Float)
    worst_perimeter = db.Column(db.Float)
    worst_area = db.Column(db.Float)
    worst_smoothness = db.Column(db.Float)
    worst_compactness = db.Column(db.Float)
    worst_concavity = db.Column(db.Float)
    worst_concave_points = db.Column(db.Float)
    worst_symmetry = db.Column(db.Float)
    worst_fractal_dimension = db.Column(db.Float)
    result = db.Column(db.String(50))  # Increased length to accommodate longer result text

# Create Database Tables
with app.app_context():
    db.create_all()

# Load the Trained XGBoost Model
model = joblib.load("model/breast_cancer_model.pkl")

# Home Route
@app.route('/')
def home():
    return render_template("index.html")

# Prediction Route (Supports Both JSON and Form Data)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        print("Request received:", request.data)  # Debugging line
        if request.is_json:  # If request is JSON (Postman)
            data = request.get_json()
            print("JSON Data:", data)  # Debugging line
        else:  # If request is from an HTML form
            data = {key: float(request.form[key]) for key in request.form}
            print("Form Data:", data)  # Debugging line

        # Extract features in the correct order
        features = [
            data["mean_radius"], data["mean_texture"], data["mean_perimeter"], data["mean_area"], data["mean_smoothness"],
            data["mean_compactness"], data["mean_concavity"], data["mean_concave_points"], data["mean_symmetry"], data["mean_fractal_dimension"],
            data["radius_error"], data["texture_error"], data["perimeter_error"], data["area_error"], data["smoothness_error"],
            data["compactness_error"], data["concavity_error"], data["concave_points_error"], data["symmetry_error"], data["fractal_dimension_error"],
            data["worst_radius"], data["worst_texture"], data["worst_perimeter"], data["worst_area"], data["worst_smoothness"],
            data["worst_compactness"], data["worst_concavity"], data["worst_concave_points"], data["worst_symmetry"], data["worst_fractal_dimension"]
        ]

        # Make Prediction
        prediction = model.predict([features])[0]
        result_text = "No Cancer Detected (Benign)" if prediction else "Cancer Detected"

        # Save the prediction to the database
        new_prediction = Prediction(**data, result=result_text)
        db.session.add(new_prediction)
        db.session.commit()

        # If JSON request, return JSON response
        if request.is_json:
            return jsonify({"requestNumber": new_prediction.id, "Message": "No Cancer Detected (Benign)" if prediction else "Cancer Detected"})

        # If form submission, render a result page
        return render_template("result.html", result="No Cancer Detected (Benign)" if prediction else "Cancer Detected")

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Retrieve All Past Predictions
@app.route('/getPredictions', methods=['GET'])
def get_predictions():
    all_predictions = Prediction.query.all()
    result = [
        {
            "id": p.id,
            "mean_radius": p.mean_radius,
            "mean_texture": p.mean_texture,
            "result": p.result
        }
        for p in all_predictions
    ]
    return jsonify(result)

# API Prediction Route for React Frontend
@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json()

        # Extract features in the correct order
        features = [
            data["mean_radius"], data["mean_texture"], data["mean_perimeter"], data["mean_area"], data["mean_smoothness"],
            data["mean_compactness"], data["mean_concavity"], data["mean_concave_points"], data["mean_symmetry"], data["mean_fractal_dimension"],
            data["radius_error"], data["texture_error"], data["perimeter_error"], data["area_error"], data["smoothness_error"],
            data["compactness_error"], data["concavity_error"], data["concave_points_error"], data["symmetry_error"], data["fractal_dimension_error"],
            data["worst_radius"], data["worst_texture"], data["worst_perimeter"], data["worst_area"], data["worst_smoothness"],
            data["worst_compactness"], data["worst_concavity"], data["worst_concave_points"], data["worst_symmetry"], data["worst_fractal_dimension"]
        ]

        # Make Prediction with shorter result text
        prediction = model.predict([features])[0]
        result_text = "No Cancer Detected" if prediction else "Cancer Detected"

        # Save to database
        new_prediction = Prediction(**data, result=result_text)
        db.session.add(new_prediction)
        db.session.commit()

        # Return detailed text in response but save shorter text in DB
        return jsonify({
            "requestNumber": new_prediction.id,
            "result": "No Cancer Detected" if prediction else "Cancer Detected"
        })
    except Exception as e:
        print(f"Error: {str(e)}")  # Add logging for debugging
        db.session.rollback()  # Rollback on error
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask application
