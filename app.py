from flask import Flask, request, jsonify

app = Flask(__name__)


# Simulated IAM Role Tokens
AUTHORIZED_TOKENS = {
    "Bearer admin-secret-123": "IAM-Admin",
    "Bearer viewer-secret-456": "Cloud-Viewer"
}

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cloud & IAM DevSecOps Portal</title>
        <style>
            body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; text-align: center; padding: 50px; }
            .card { background: #1e293b; padding: 30px; border-radius: 12px; max-width: 560px; margin: 0 auto; box-shadow: 0 4px 15px rgba(0,0,0,0.4); }
            .badge { background: #22c55e; color: #052e16; padding: 6px 14px; border-radius: 999px; font-weight: bold; font-size: 14px; }
            h1 { margin-top: 20px; font-size: 26px; }
            p { color: #cbd5e1; line-height: 1.6; }
            code { background: #0f172a; padding: 4px 8px; border-radius: 6px; color: #38bdf8; }
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">CI/CD Pipeline: Active & Verified</span>
            <h1>Cloud & IAM Service Portal</h1>
            <p>This web application is automatically built, tested, security-scanned, and deployed via <strong>GitHub Actions</strong> and <strong>Docker</strong>.</p>
            <p>Health Endpoint: <code>/health</code> | IAM Protected API: <code>/api/secure-data</code></p>
        </div>
    </body>
    </html>
    """, 200

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "webapp-cicd-demo"}), 200

@app.route("/api/secure-data")
def secure_data():
    token = request.headers.get("Authorization")
    if token not in AUTHORIZED_TOKENS:
        return jsonify({"error": "Unauthorized: Valid IAM Bearer token required"}), 401
    return jsonify({
        "status": "access_granted",
        "role": AUTHORIZED_TOKENS[token],
        "data": "Confidential Cloud Infrastructure Metrics"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
