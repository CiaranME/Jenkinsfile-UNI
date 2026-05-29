from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return f"goodbye! I'm currently running in {os.environ.get('ENV', 'development')}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
