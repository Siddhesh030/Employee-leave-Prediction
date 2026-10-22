import os
import pickle
import numpy as np
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Resolve path relative to current file for robust Vercel serverless execution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "lr_model.pkl")

model = None
if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
    except Exception as err:
        print(f"Error loading model: {err}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RetainIQ | Enterprise Attrition Intelligence</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#eef2ff',
                            100: '#e0e7ff',
                            500: '#6366f1',
                            600: '#4f46e5',
                            700: '#4338ca',
                            900: '#1e1b4b',
                        }
                    },
                    fontFamily: {
                        sans: ['Plus Jakarta Sans', 'Inter', 'system-ui', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- FontAwesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    
    <style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(226, 232, 240, 0.8);
        }
        .dark .glass-card {
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .mesh-bg {
            background-image: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
                              radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.1) 0px, transparent 50%);
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 5px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: rgba(148, 163, 184, 0.3);
            border-radius: 8px;
        }
    </style>
</head>
<body class="bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 min-h-screen mesh-bg custom-scrollbar antialiased transition-colors duration-300">

    <!-- Top Executive Navigation Bar -->
    <nav class="sticky top-0 z-50 glass-card border-b border-slate-200/80 dark:border-slate-800/80 px-6 py-3.5 shadow-sm">
        <div class="max-w-7xl mx-auto flex items-center justify-between">
            <div class="flex items-center gap-3.5">
                <div class="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-600 flex items-center justify-center text-white shadow-md shadow-indigo-500/20">
                    <i class="fa-solid fa-chart-line text-lg"></i>
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <span class="text-lg font-black tracking-tight text-slate-900 dark:text-white">Retain<span class="text-indigo-500">IQ</span></span>
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-indigo-500/10 text-indigo-500 border border-indigo-500/20">Enterprise ML</span>
                    </div>
                    <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium">Workforce Departure Risk & Retention Engine</p>
                </div>
            </div>

            <div class="flex items-center gap-3">
                <div class="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs font-semibold">
                    <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    Model Engine Active
                </div>

                <button id="themeToggle" title="Toggle Theme" class="p-2.5 rounded-xl bg-slate-200/70 dark:bg-slate-800/70 hover:bg-slate-300/70 dark:hover:bg-slate-700 transition text-slate-700 dark:text-amber-400 border border-slate-300/40 dark:border-slate-700/60 shadow-sm">
                    <i id="themeIcon" class="fa-solid fa-moon text-sm"></i>
                </button>
            </div>
        </div>
    </nav>

    <!-- Main Workspace -->
    <main class="max-w-7xl mx-auto px-6 py-8">
        
        <!-- Header Banner -->
        <div class="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-slate-200 dark:border-slate-800/80 pb-6">
            <div>
                <h1 class="text-2xl md:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">Employee Retention Analytics</h1>
                <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Simulate workforce attributes to assess probability of resignation versus retention in real-time.</p>
            </div>
            <div class="flex items-center gap-2">
                <span class="text-xs text-slate-400 font-medium">Algorithm: <strong class="text-slate-700 dark:text-slate-200">Logistic Regression (L-BFGS)</strong></span>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            
            <!-- Parameters Input Form -->
            <section class="lg:col-span-5 flex flex-col">
                <div class="glass-card rounded-2xl p-6 shadow-xl border border-slate-200/80 dark:border-slate-800/80">
                    <div class="flex items-center justify-between pb-4 mb-5 border-b border-slate-200 dark:border-slate-800/80">
                        <div class="flex items-center gap-2.5">
                            <span class="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-500 flex items-center justify-center text-sm font-semibold">
                                <i class="fa-solid fa-sliders"></i>
                            </span>
                            <h2 class="text-base font-bold text-slate-900 dark:text-slate-100">Profile Parameters</h2>
                        </div>
                        <button type="button" id="resetBtn" class="text-xs text-slate-400 hover:text-indigo-500 transition font-medium">Reset</button>
                    </div>

                    <form id="predictionForm" class="space-y-4">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5">Education Degree</label>
                                <select id="Education" name="Education" class="w-full bg-slate-50 dark:bg-slate-900/90 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-2 text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none transition">
                                    <option value="0">Bachelors (B.Tech/BS)</option>
                                    <option value="1">Masters (M.Tech/MS)</option>
                                    <option value="2">PHD</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5">Joining Year</label>
                                <input type="number" id="JoiningYear" name="JoiningYear" value="2018" min="2012" max="2026" class="w-full bg-slate-50 dark:bg-slate-900/90 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-2 text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none transition">
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5">Base Office Location</label>
                                <select id="City" name="City" class="w-full bg-slate-50 dark:bg-slate-900/90 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-2 text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none transition">
                                    <option value="0">Bangalore</option>
                                    <option value="1">Pune</option>
                                    <option value="2">New Delhi</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5">Compensation Tier</label>
                                <select id="PaymentTier" name="PaymentTier" class="w-full bg-slate-50 dark:bg-slate-900/90 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-2 text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none transition">
                                    <option value="1">Tier 1 (Executive / High)</option>
                                    <option value="2">Tier 2 (Mid-Level)</option>
                                    <option value="3" selected>Tier 3 (Entry / Standard)</option>
                                </select>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5">Employee Age</label>
                                <input type="number" id="Age" name="Age" value="28" min="18" max="65" class="w-full bg-slate-50 dark:bg-slate-900/90 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-2 text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none transition">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5">Gender</label>
                                <select id="Gender" name="Gender" class="w-full bg-slate-50 dark:bg-slate-900/90 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-2 text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none transition">
                                    <option value="0">Male</option>
                                    <option value="1">Female</option>
                                </select>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5">Ever Benchmarked/Benched</label>
                                <select id="EverBenched" name="EverBenched" class="w-full bg-slate-50 dark:bg-slate-900/90 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-2 text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none transition">
                                    <option value="0">No (Continuous Billing)</option>
                                    <option value="1">Yes (Benched Previously)</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5">Domain Experience (Yrs)</label>
                                <input type="number" id="ExperienceInCurrentDomain" name="ExperienceInCurrentDomain" value="3" min="0" max="30" class="w-full bg-slate-50 dark:bg-slate-900/90 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-2 text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none transition">
                            </div>
                        </div>

                        <button type="submit" id="submitBtn" class="w-full mt-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-4 rounded-xl shadow-lg shadow-indigo-500/25 transition duration-200 flex items-center justify-center gap-2 group cursor-pointer active:scale-[0.99]">
                            <i class="fa-solid fa-microchip text-sm group-hover:rotate-12 transition"></i>
                            <span>Evaluate Retention Likelihood</span>
                        </button>
                    </form>
                </div>
            </section>

            <!-- Diagnostic Readout & Dashboard -->
            <section class="lg:col-span-7 flex flex-col gap-6">
                
                <!-- Primary Verdict Card -->
                <div id="verdictContainer" class="glass-card rounded-2xl p-6 shadow-xl border border-slate-200/80 dark:border-slate-800/80 transition-all duration-300">
                    <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-200 dark:border-slate-800/80">
                        <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Risk Assessment Analysis</span>
                        <span id="riskBadge" class="px-2.5 py-1 rounded-full text-[11px] font-bold bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                            Awaiting Evaluation
                        </span>
                    </div>

                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-6">
                        <div class="flex items-center gap-4">
                            <div id="statusIconBox" class="w-16 h-16 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-400 flex items-center justify-center text-2xl shrink-0 transition-colors">
                                <i id="statusIcon" class="fa-solid fa-user-clock"></i>
                            </div>
                            <div>
                                <h3 id="verdictTitle" class="text-xl md:text-2xl font-black text-slate-800 dark:text-white">Ready to Predict</h3>
                                <p id="verdictDesc" class="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-sm">Adjust employee attributes on the left and trigger evaluation to display flight-risk probabilities.</p>
                            </div>
                        </div>

                        <div class="flex sm:flex-col items-center sm:items-end justify-between border-t sm:border-t-0 sm:border-l border-slate-200 dark:border-slate-800 pt-3 sm:pt-0 sm:pl-6 shrink-0">
                            <span class="text-[11px] uppercase tracking-wider font-semibold text-slate-400">Model Confidence</span>
                            <span id="confidenceMetric" class="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">--%</span>
                        </div>
                    </div>
                </div>

                <!-- Visualization Hub -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="glass-card rounded-2xl p-5 shadow-xl border border-slate-200/80 dark:border-slate-800/80 flex flex-col justify-between">
                        <h4 class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-3 flex items-center gap-2">
                            <i class="fa-solid fa-chart-pie text-indigo-500"></i> Probability Breakdown
                        </h4>
                        <div class="relative h-44 w-full flex items-center justify-center">
                            <canvas id="probChart"></canvas>
                        </div>
                    </div>

                    <div class="glass-card rounded-2xl p-5 shadow-xl border border-slate-200/80 dark:border-slate-800/80 flex flex-col justify-between">
                        <h4 class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-3 flex items-center gap-2">
                            <i class="fa-solid fa-chart-column text-purple-500"></i> Encoded Features Overview
                        </h4>
                        <div class="relative h-44 w-full flex items-center justify-center">
                            <canvas id="featChart"></canvas>
                        </div>
                    </div>
                </div>

                <!-- Strategic HR Insights Card -->
                <div class="glass-card rounded-2xl p-5 shadow-xl border border-slate-200/80 dark:border-slate-800/80">
                    <h4 class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2 flex items-center gap-2">
                        <i class="fa-solid fa-lightbulb text-amber-500"></i> Recommended Retention Strategy
                    </h4>
                    <p id="actionableAdvice" class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                        Input employee parameters to generate personalized talent management and retention actions.
                    </p>
                </div>

            </section>
        </div>
    </main>

    <script>
        // Theme Toggle Controller
        const themeToggleBtn = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        
        themeToggleBtn.addEventListener('click', () => {
            const isDark = document.documentElement.classList.toggle('dark');
            themeIcon.className = isDark ? 'fa-solid fa-moon text-sm' : 'fa-solid fa-sun text-sm text-amber-500';
            updateChartTheme(isDark);
        });

        // Initialize Chart.js
        let probChart, featChart;

        function initCharts() {
            const ctxProb = document.getElementById('probChart').getContext('2d');
            probChart = new Chart(ctxProb, {
                type: 'doughnut',
                data: {
                    labels: ['Retention Likelihood', 'Attrition Risk'],
                    datasets: [{
                        data: [50, 50],
                        backgroundColor: ['#10b981', '#f43f5e'],
                        borderWidth: 0,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 }, color: '#94a3b8' } }
                    },
                    cutout: '72%'
                }
            });

            const ctxFeat = document.getElementById('featChart').getContext('2d');
            featChart = new Chart(ctxFeat, {
                type: 'bar',
                data: {
                    labels: ['Edu', 'Year', 'City', 'Tier', 'Age', 'Gend', 'Bench', 'Exp'],
                    datasets: [{
                        label: 'Value',
                        data: [0, 2018, 0, 3, 28, 0, 0, 3],
                        backgroundColor: '#6366f1',
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { display: false } },
                        y: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: 'rgba(148,163,184,0.1)' } }
                    },
                    plugins: { legend: { display: false } }
                }
            });
        }

        function updateChartTheme(isDark) {
            const color = isDark ? '#94a3b8' : '#64748b';
            if (probChart) {
                probChart.options.plugins.legend.labels.color = color;
                probChart.update();
            }
            if (featChart) {
                featChart.options.scales.x.ticks.color = color;
                featChart.options.scales.y.ticks.color = color;
                featChart.update();
            }
        }

        // Form Submit
        const form = document.getElementById('predictionForm');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const submitBtn = document.getElementById('submitBtn');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin text-sm"></i> Calculating...';

            const formData = new FormData(form);
            const payload = {};
            formData.forEach((val, key) => payload[key] = parseFloat(val));

            try {
                const res = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();

                if (data.success) {
                    const verdictTitle = document.getElementById('verdictTitle');
                    const verdictDesc = document.getElementById('verdictDesc');
                    const statusIconBox = document.getElementById('statusIconBox');
                    const statusIcon = document.getElementById('statusIcon');
                    const riskBadge = document.getElementById('riskBadge');
                    const confidenceMetric = document.getElementById('confidenceMetric');
                    const advice = document.getElementById('actionableAdvice');

                    const stayProb = (data.probabilities[0] * 100).toFixed(1);
                    const leaveProb = (data.probabilities[1] * 100).toFixed(1);

                    if (data.prediction === 0) {
                        verdictTitle.innerText = "Employee Retained";
                        verdictTitle.className = "text-xl md:text-2xl font-black text-emerald-600 dark:text-emerald-400";
                        verdictDesc.innerText = "High stability profile. The employee shows consistent alignment with existing tenure metrics.";
                        
                        statusIconBox.className = "w-16 h-16 rounded-2xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center text-2xl shrink-0";
                        statusIcon.className = "fa-solid fa-user-check";

                        riskBadge.innerText = "Low Attrition Risk";
                        riskBadge.className = "px-2.5 py-1 rounded-full text-[11px] font-bold bg-emerald-500/10 text-emerald-500 border border-emerald-500/20";

                        confidenceMetric.innerText = `${stayProb}%`;
                        advice.innerHTML = "<strong>Recommended Action:</strong> Standard appraisal cycle applies. Maintain recurring 1-on-1 check-ins and recognize recent contributions to preserve high engagement.";
                    } else {
                        verdictTitle.innerText = "High Flight Risk";
                        verdictTitle.className = "text-xl md:text-2xl font-black text-rose-600 dark:text-rose-400";
                        verdictDesc.innerText = "Heightened probability of resignation. Critical retention interventions are strongly advised.";
                        
                        statusIconBox.className = "w-16 h-16 rounded-2xl bg-rose-500/10 text-rose-500 flex items-center justify-center text-2xl shrink-0";
                        statusIcon.className = "fa-solid fa-user-xmark";

                        riskBadge.innerText = "High Attrition Risk";
                        riskBadge.className = "px-2.5 py-1 rounded-full text-[11px] font-bold bg-rose-500/10 text-rose-500 border border-rose-500/20";

                        confidenceMetric.innerText = `${leaveProb}%`;
                        advice.innerHTML = "<strong>Recommended Action:</strong> Immediate compensation & tier benchmarking recommended. Schedule career-pathing discussion, review billing/bench history, and evaluate domain workload.";
                    }

                    probChart.data.datasets[0].data = [stayProb, leaveProb];
                    probChart.update();

                    featChart.data.datasets[0].data = Object.values(payload);
                    featChart.update();
                } else {
                    alert('Error: ' + data.error);
                }
            } catch (err) {
                console.error(err);
                alert('Connection failure to prediction server.');
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fa-solid fa-microchip text-sm group-hover:rotate-12 transition"></i> <span>Evaluate Retention Likelihood</span>';
            }
        });

        document.getElementById('resetBtn').addEventListener('click', () => {
            form.reset();
        });

        window.addEventListener('DOMContentLoaded', initCharts);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({
            'success': False, 
            'error': 'Logistic Regression model (lr_model.pkl) was not found or could not be loaded.'
        }), 500

    try:
        data = request.get_json(force=True)
        feature_order = [
            'Education', 'JoiningYear', 'City', 'PaymentTier',
            'Age', 'Gender', 'EverBenched', 'ExperienceInCurrentDomain'
        ]
        
        features = [float(data.get(feat, 0)) for feat in feature_order]
        features_array = np.array([features])

        prediction = int(model.predict(features_array)[0])
        probabilities = model.predict_proba(features_array)[0].tolist()

        return jsonify({
            'success': True,
            'prediction': prediction,
            'probabilities': probabilities
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Vercel needs the WSGI application object directly exposed
app_handler = app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
