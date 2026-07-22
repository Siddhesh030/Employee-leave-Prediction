import os
import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Dynamically locate the pickle model file relative to the api/ directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "lrm model.pkl")

# Load the model globally
if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
    except Exception as e:
        model = None
else:
    model = None

# Stunning modern UI with animations embedded directly inside app.py
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Model Prediction Dashboard</title>
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            --card-bg: rgba(255, 255, 255, 0.07);
            --card-border: rgba(255, 255, 255, 0.1);
            --text-color: #f8f9fa;
            --accent-color: #00f2fe;
            --accent-gradient: linear-gradient(45deg, #4facfe, #00f2fe);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background: var(--bg-gradient);
            color: var(--text-color);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            overflow-x: hidden;
        }

        .container {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--card-border);
            padding: 40px;
            border-radius: 20px;
            width: 100%;
            max-width: 700px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            animation: fadeInUp 0.8s ease-out;
        }

        h2 {
            text-align: center;
            margin-bottom: 30px;
            font-weight: 600;
            letter-spacing: 1px;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            justify-content: center;
        }

        @media (max-width: 600px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }

        .input-group {
            display: flex;
            flex-direction: column;
        }

        label {
            font-size: 0.85rem;
            margin-bottom: 8px;
            color: #cbd5e1;
        }

        input, select {
            padding: 12px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            color: white;
            font-size: 1rem;
            transition: all 0.3s ease;
            outline: none;
        }

        input:focus, select:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
            background: rgba(255, 255, 255, 0.1);
        }

        select option {
            background: #203a43;
            color: white;
        }

        .btn-container {
            grid-column: span 2;
            text-align: center;
            margin-top: 20px;
        }

        @media (max-width: 600px) {
            .btn-container {
                grid-column: span 1;
            }
        }

        button {
            width: 100%;
            max-width: 300px;
            padding: 14px;
            border: none;
            border-radius: 30px;
            background: var(--accent-gradient);
            color: #0f2027;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
        }

        button:active {
            transform: translateY(1px);
        }

        #result {
            margin-top: 30px;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: 600;
            display: none;
            opacity: 0;
            transition: opacity 0.5s ease;
        }

        .show-result {
            display: block !important;
            animation: fadeIn 0.5s forwards;
        }

        .success {
            background: rgba(46, 213, 115, 0.2);
            border: 1px solid #2ed573;
            color: #2ed573;
        }
        
        .danger {
            background: rgba(235, 77, 75, 0.2);
            border: 1px solid #eb4d4b;
            color: #eb4d4b;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeIn {
            to { opacity: 1; }
        }
    </style>
</head>
<body>

<div class="container">
    <h2>Predictive Model Dashboard</h2>
    <form id="predictionForm">
        <div class="grid">
            <div class="input-group">
                <label for="Education">Education</label>
                <select id="Education" name="Education" required>
                    <option value="0">Bachelors</option>
                    <option value="1">Masters</option>
                    <option value="2">PHD</option>
                </select>
            </div>
            
            <div class="input-group">
                <label for="JoiningYear">Joining Year</label>
                <input type="number" id="JoiningYear" name="JoiningYear" value="2026" required>
            </div>

            <div class="input-group">
                <label for="City">City</label>
                <select id="City" name="City" required>
                    <option value="0">Bangalore</option>
                    <option value="1">Pune</option>
                    <option value="2">New Delhi</option>
                </select>
            </div>

            <div class="input-group">
                <label for="PaymentTier">Payment Tier (1-3)</label>
                <input type="number" id="PaymentTier" name="PaymentTier" min="1" max="3" value="3" required>
            </div>

            <div class="input-group">
                <label for="Age">Age</label>
                <input type="number" id="Age" name="Age" min="18" max="100" value="25" required>
            </div>

            <div class="input-group">
                <label for="Gender">Gender</label>
                <select id="Gender" name="Gender" required>
                    <option value="0">Female</option>
                    <option value="1">Male</option>
                </select>
            </div>

            <div class="input-group">
                <label for="EverBenched">Ever Benched</label>
                <select id="EverBenched" name="EverBenched" required>
                    <option value="0">No</option>
                    <option value="1">Yes</option>
                </select>
            </div>

            <div class="input-group">
                <label for="ExperienceInCurrentDomain">Experience in Domain (Years)</label>
                <input type="number" id="ExperienceInCurrentDomain" name="ExperienceInCurrentDomain" min="0" value="2" required>
            </div>

            <div class="btn-container">
                <button type="submit">Run Prediction</button>
            </div>
        </div>
    </form>

    <div id="result"></div>
</div>

<script>
    document.getElementById('predictionForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());
        
        const resultDiv = document.getElementById('result');
        resultDiv.className = ''; 
        resultDiv.style.display = 'none';

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            
            if (result.error) {
                resultDiv.innerText = `Error: ${result.error}`;
                resultDiv.classList.add('danger', 'show-result');
            } else {
                resultDiv.innerText = `Prediction Output: ${result.prediction}`;
                resultDiv.classList.add('success', 'show-result');
            }
        } catch (error) {
            resultDiv.innerText = "Error connecting to server.";
            resultDiv.classList.add('danger', 'show-result');
        }
    });
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": f"Model file not found. Looking at: {MODEL_PATH}"}), 500
    
    try:
        data = request.json
        features = [
            float(data['Education']),
            float(data['JoiningYear']),
            float(data['City']),
            float(data['PaymentTier']),
            float(data['Age']),
            float(data['Gender']),
            float(data['EverBenched']),
            float(data['ExperienceInCurrentDomain'])
        ]
        
        prediction = model.predict([features])[0]
        return jsonify({"prediction": int(prediction)})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Required mapping for Vercel serverless environment
app.debug = True
