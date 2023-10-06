# app.py (Flask Backend)

from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend_colors():
    input_text = request.form['text']
    # Perform color recommendation logic here based on input_text
    # Replace this with your actual recommendation code
    recommended_colors = ['#FF5733', '#34FF45', '#A232FF']

    return jsonify(colors=recommended_colors)

if __name__ == '__main__':
    app.run(debug=True)
