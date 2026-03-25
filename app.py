# from flask import Flask, request, jsonify
# from modules.log_analyzer import analyze_log
# from modules.risk_engine import calculate_risk
# from modules.ai_insights import generate_insights
# from modules.masker import mask_data   #  correct place

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "AI Secure Data Intelligence Platform Running "

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     # Handle file upload OR JSON
#     if 'file' in request.files:
#         file = request.files['file']
#         content = file.read().decode('utf-8')
#     else:
#         data = request.json
#         content = data.get("content")

#     #  Apply masking INSIDE function
#     content = mask_data(content)

#     findings = analyze_log(content)
#     risk = calculate_risk(findings)
#     insights = generate_insights(findings)

#     return jsonify({
#         "summary": "Log analyzed successfully",
#         "findings": findings,
#         "risk_score": risk["score"],
#         "risk_level": risk["level"],
#         "insights": insights
#     })

# if __name__ == '__main__':
#     app.run(debug=True)
#     from flask import Flask, request, jsonify, send_from_directory

# app = Flask(__name__, static_folder='frontend')

# @app.route('/')
# def serve_frontend():
#     return send_from_directory('frontend', 'index.html')


from flask import Flask, request, jsonify, send_from_directory
from modules.log_analyzer import analyze_log
from modules.risk_engine import calculate_risk
from modules.ai_insights import generate_insights
from modules.masker import mask_data

app = Flask(__name__, static_folder='frontend')

# ✅ Serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

# ✅ API route
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Handle file upload OR JSON
        if 'file' in request.files:
            file = request.files['file']
            content = file.read().decode('utf-8')
        else:
            data = request.json
            content = data.get("content", "")

        # Mask sensitive data
        content = mask_data(content)

        findings = analyze_log(content)
        risk = calculate_risk(findings)
       # insights = generate_insights(findings)

        insights = generate_insights(findings, content)

        return jsonify({
    "summary": "Log contains sensitive credentials and system errors",
    "findings": findings,
    "risk_score": risk["score"],
    "risk_level": risk["level"],
    "insights": insights
})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)