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

# Elegant Glassmorphism Interface with Enhanced Theme & Smooth Micro-interactions
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Predictive Analytics Dashboard</title>
    <style>
        :root {
            --bg-gradient: radial-gradient(circle at 50% 50%, #1e1b4b 0%, #0f172a 100%);
            --card-bg: rgba(30, 41, 59, 0.4);
            --card-border: rgba(255, 255, 255, 0.08);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.3);
            --btn-gradient: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }

        body {
            background: var(--bg-gradient);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 40px 20px;
        }

        .container {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--card-border);
            padding: 48px;
            border-radius: 28px;
            width: 100%;
            max-width: 720px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            animation: slideUpFade 0.7s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .header-section {
            text-align: center;
            margin-bottom: 40px;
        }

        h2 {
            font-size: 2.25rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            background: linear-gradient(to right, #ffffff, #cbd5e1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 0.95rem;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 28px;
        }

        @media (max-width: 640px) {
            .grid {
                grid-template-columns: 1fr;
            }
            .container {
                padding: 32px 24px;
            }
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        label {
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-secondary);
            transition: color 0.2s ease;
        }

        .input-group:focus-within label {
            color: var(--accent);
        }

        input, select {
            padding: 14px 18px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            color: #fff;
            font-size: 1rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            outline: none;
            width: 100%;
        }

        input:focus, select:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 4px var(--accent-glow);
            background: rgba(15, 23, 42, 0.8);
        }

        select {
            appearance: none;
            background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'></polyline></svg>");
            background-repeat: no-repeat;
            background-position: right 16px center;
            background-size: 16px;
            padding-right: 40px;
        }

        select option {
            background: #0f172a;
            color: #fff;
        }

        .btn-container {
            grid-column: span 2;
            text-align: center;
            margin-top: 12px;
        }

        @media (max-width: 640px) {
            .btn-container {
                grid-column: span 1;
            }
        }

        button {
            width: 100%;
            max-width: 320px;
            padding: 16px 32px;
            border: none;
            border-radius: 14px;
            background: var(--btn-gradient);
            color: #fff;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 20px rgba(2, 132, 199, 0.4);
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 28px rgba(2, 132, 199, 0.6);
            filter: brightness(1.05);
        }

        button:active {
            transform: translateY(0);
        }

        #result {
            margin-top: 32px;
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            font-size: 1.15rem;
            font-weight: 600;
            display: none;
            opacity: 0;
            transform: translateY(10px);
            transition: all 0.4s ease;
        }

        .show-result {
            display: block !important;
            opacity: 1 !important;
            transform: translateY(0) !important;
        }

        .success {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.25);
            color: #34d399;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.05);
        }
        
        .danger {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.25);
            color: #f87171;
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.05);
        }

        @keyframes slideUpFade {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header-section">
        <h2>Predictive Dashboard</h2>
        <div class="subtitle">Input system variables below to evaluate model metrics</div>
    </div>
    
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
                <label for="ExperienceInCurrentDomain">Domain Experience (Years)</label>
                <input type="number" id="ExperienceInCurrentDomain" name="ExperienceInCurrentDomain" min="0" value="2" required>
            </div>

            <div class="btn-container">
                <button type="submit">Execute Prediction</button>
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
        resultDiv.classList.remove('show-result');

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            
            if (result.error) {
                resultDiv.innerText = `System Error: ${result.error}`;
                resultDiv.classList.add('danger', 'show-result');
            } else {
                resultDiv.innerText = `Prediction Output Matrix: ${result.prediction}`;
                resultDiv.classList.add('success', 'show-result');
            }
        } catch (error) {
            resultDiv.innerText = "Network failure: Unable to connect to inference server.";
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

if __name__ == '__main__':
    app.run(debug=True)
