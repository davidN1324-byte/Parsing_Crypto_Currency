import subprocess
from flask import Flask, render_template
import os

app = Flask(__name__)

# Executing the necessary scripts.
subprocess.run(["python", "analysis.py"])
subprocess.run(["python", "graf.py"])

@app.route('/')
def home():
    graph_html = ""
    if os.path.exists("crypto_chart.html"):
        with open("crypto_chart.html", "r") as file:
            graph_html = file.read()

    # Reading the analysis text (analysis.txt)
    analysis_content = ""
    if os.path.exists("analysis.txt"):
        with open("analysis.txt", "r") as file:
            analysis_content = file.read()

    return render_template('index.html', graph_html=graph_html, analysis_content=analysis_content)

if __name__ == "__main__":
    app.run(debug=True)
