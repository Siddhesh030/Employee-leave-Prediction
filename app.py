import os
import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# robust paths resolver for Vercel's environment
def load_model():
    # Potential locations for the model file in Vercel environment
    possible_paths = [
        os.path.join(os.getcwd(), "lrmodel.pkl"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lrmodel.pkl"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "lrmodel.pkl"),
        "/var/task/lrmodel.pkl"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    return pickle.load(f), None
            except Exception as e:
                return None, f"Failed to parse model file: {str(e)}"
    
    # If not found, return the path checked for debugging
    return None, f"Model file not found. Checked paths: {', '.join(possible_paths)}"

model, model_error = load_model()

# Elegant Glassmorphism Interface with Animations
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Predictive Analytics Dashboard</title>
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            --card-bg: rgba(255, 255, 255, 0.06);
            --card-border: rgba(255, 255, 255, 0.08);
            --text-color: #f1f5f9;
            --accent-color: #00f2fe;
            --accent-gradient: linear-gradient(45deg, #00c6ff, #0072ff);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }

        body {
            background: var(--bg-gradient);
            color: var(--text-color);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 24px;
        }

        .container {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            padding: 40px;
            border-radius: 24px;
            width: 100%;
            max-width: 680px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
            animation: fadeInScale 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }

        h2 {
            text-align: center;
            margin-bottom: 32px;
            font-size: 1.8rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            background: linear-gradient(45deg, #e0f2fe, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 24px;
        }

        @media (max-width: 580px) {
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
            font-weight: 500;
            margin-bottom: 8px;
            color: #94a3b8;
        }

        input, select {
            padding: 12px 16px;
            background: rgba(15, 32, 39, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 10px;
            color: #fff;
            font-size: 0.95rem;
            transition: all 0.25s ease;
            outline: none;
        }

        input:focus, select:focus {
            border-color: #38bdf8;
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25);
            background: rgba(15, 32, 39, 0.7);
        }

        select option {
            background: #1e293b;
            color: #fff;
        }

        .btn-container {
            grid-column: span 2;
            text-align: center;
            margin-top: 16px;
        }

        @media (max-width: 580px) {
            .btn-container {
                grid-column: span 1;
            }
        }

        button {
            width: 100%;
            max-width: 280px;
            padding: 14px 28px;
            border: none;
            border-radius: 50px;
            background: var(--accent-gradient);
            color: #fff;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(0, 114, 255, 0.3);
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 24px rgba(0, 114, 255, 0.5);
        }

        button:active {
            transform: translateY(0);
        }

        #result {
            margin-top: 24px;
            padding: 16px;
            border-radius: 12px;
            text-align: center;
            font-size: 1.1rem;
            font-weight: 600;
            display: none;
            opacity: 0;
        }

        .show-result {
            display: block !important;
            animation: fadeIn 0.4s forwards;
        }

        .success {
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: #34d399;
        }
        
        .danger {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.4);
            color: #f87171;
        }

        @keyframes fadeInScale {
            from {
                opacity: 0;
                transform: scale(0.96) translateY(10px);
            }
            to {
                opacity: 1;
                transform: scale(1) translateY(0);
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
        return jsonify({"error": model_error or "Model file not found on server context."}), 500
    
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
