# waf.py
from flask import Flask, request, Response
import requests
import re

app = Flask(__name__)

BACKEND_URL = "http://127.0.0.1:5001"
SQLI_PATTERNS = [
    r"(\bUNION\b.*\bSELECT\b)",
    r"(\bSELECT\b.*\bFROM\b)",
    r"(\bOR\b.*=.*)",
    r"(--|#|;)",
]
XSS_PATTERNS = [
    r"<script.*?>.*?</script>",
    r"on\w+\s*=",
    r"javascript:",
]
def is_malicious(data):
    for pattern in SQLI_PATTERNS:
        if re.search(pattern, data, re.IGNORECASE):
            return "SQL Injection Detected"

    for pattern in XSS_PATTERNS:
        if re.search(pattern, data, re.IGNORECASE):
            return "XSS Detected"

    return None
@app.route('/', defaults={'path': ''}, methods=["GET", "POST"])
@app.route('/<path:path>', methods=["GET", "POST"])
def proxy(path):
    data = request.query_string.decode() + str(request.form)

    threat = is_malicious(data)

    if threat:
        return Response(f"Blocked: {threat}", status=403)

    # Forward request
    resp = requests.request(
        method=request.method,
        url=f"{BACKEND_URL}/{path}",
        params=request.args,
        data=request.form
    )

    return Response(resp.content, resp.status_code)
def log_attack(data, threat):
    with open("logs.txt", "a") as f:
        f.write(f"{threat}: {data}\n")
        if threat:
    log_attack(data, threat)
    return Response(f"Blocked: {threat}", status=403)
blocked_ips = set()

if request.remote_addr in blocked_ips:
    return "IP Blocked", 403
blocked_ips.add(request.remote_addr)
