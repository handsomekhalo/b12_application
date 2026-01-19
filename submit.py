import json
import hmac
import hashlib
import datetime
import requests

# ===== CONFIG =====
SIGNING_SECRET = b"hello-there-from-b12"
URL = "https://b12.io/apply/submission"

NAME = "Titus Monaheng"
EMAIL = "titus.khalomonaheng@gmail.com"
RESUME_LINK = "http://www.linkedin.com/in/khalo-monaheng-b6a821b0"
REPOSITORY_LINK = "https://github.com/handsomekhalo/b12_application"
ACTION_RUN_LINK = "https://github.com/handsomekhalo/b12_application/actions/runs/REPLACE_ME"
# ==================

payload = {
    "action_run_link": ACTION_RUN_LINK,
    "email": EMAIL,
    "name": NAME,
    "repository_link": REPOSITORY_LINK,
    "resume_link": RESUME_LINK,
    # timestamp an ISO 8601 timestamp in UTC with milliseconds precision
    "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
}


#post body should contain no extra whitespace (compact separators), have keys sorted alphabetically, and be UTF-8-encoded
json_body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

# HMAC-SHA256 signature
signature = hmac.new(
    SIGNING_SECRET,
    json_body,
    hashlib.sha256
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}",
}

response = requests.post(URL, data=json_body, headers=headers)

print("Status:", response.status_code)
print("Response:", response.text)

if response.status_code == 200:
    data = response.json()
    print("RECEIPT:", data.get("receipt"))
