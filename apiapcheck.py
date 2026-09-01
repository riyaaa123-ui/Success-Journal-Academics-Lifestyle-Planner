'''from flask import Flask, render_template, request, jsonify
import google.generativeai as ai

# Configure the API key for Google Generative AI
API_KEY = 'AIzaSyCaXlaXnIXZPOwSIbi6d7dWneZDF4-CvGo'
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel("gemini-1.5-flash-latest")
chat = model.start_chat()

app = Flask(__name__)

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('apiindex.html')  # Ensure index.html is in the templates folder

# Route to handle POST request from the frontend (sending user message)
@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['message']
    if user_message.lower() == 'bye':
        return jsonify({'response': 'Goodbye!'})
    response = chat.send_message(user_message)
    return jsonify({'response': response.text})

if __name__ == '_main_':
    app.run(debug=True)'''
'''from flask import Flask, render_template, request, jsonify
import google.generativeai as ai

# Configure the API key for Google Generative AI
API_KEY = 'AIzaSyCaXlaXnIXZPOwSIbi6d7dWneZDF4-CvGo'  # Replace with your actual API key
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel("gemini-1.5-flash-latest")
chat = model.start_chat()

app = Flask(__name__)

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('apiindex.html')  # Ensure apiindex.html is in the templates folder

# Route to handle POST request from the frontend (sending user message)
@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form.get('message', '')  # Default to empty string if 'message' key is missing
    if user_message.lower() == 'bye':
        return jsonify({'response': 'Goodbye!'})
    
    try:
        response = chat.send_message(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)'''

'''from flask import Flask, render_template, request, jsonify
import google.generativeai as ai

# Configure the API key for Google Generative AI
API_KEY = 'AIzaSyCaXlaXnIXZPOwSIbi6d7dWneZDF4-CvGo'  # Replace with your actual API key
try:
    ai.configure(api_key=API_KEY)
    model = ai.GenerativeModel("gemini-1.5-flash-latest")
    chat = model.start_chat()
except Exception as e:
    print(f"Error initializing Google Generative AI: {str(e)}")

app = Flask(__name__)

# Route to render the HTML page
@app.route('/')
def index():
    try:
        return render_template('apiindex.html')  # Ensure apiindex.html is in the templates folder
    except Exception as e:
        return f"Error loading template: {str(e)}", 500

# Route to handle POST request from the frontend (sending user message)
@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form.get('message', '')  # Default to empty string if 'message' key is missing
    if not user_message:
        return jsonify({'response': 'No message provided!'})
    
    if user_message.lower() == 'bye':
        return jsonify({'response': 'Goodbye!'})

    try:
        response = chat.send_message(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f"Error generating response: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)'''

# correctly working file below
'''from flask import Flask, render_template, request, jsonify
import google.generativeai as ai

# Configure the API key for Google Generative AI
API_KEY = 'AIzaSyCaXlaXnIXZPOwSIbi6d7dWneZDF4-CvGo'  # Replace with your actual API key
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel("gemini-1.5-flash-latest")
chat = model.start_chat()

app = Flask(__name__)

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('apiindex.html')  # Ensure apiindex.html is in the templates folder

# Route to handle POST request from the frontend (sending user message)
@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form.get('message', '')  # Default to empty string if 'message' key is missing
    if not user_message:
        return jsonify({'response': 'No message provided!'})
    
    if user_message.lower() == 'bye':
        return jsonify({'response': 'Goodbye!'})

    try:
        response = chat.send_message(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f"Error generating response: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)'''

'''#perfectly working one :-
from flask import Flask, render_template, request, jsonify
import google.generativeai as ai

# Configure the API key for Google Generative AI
API_KEY = 'AIzaSyCaXlaXnIXZPOwSIbi6d7dWneZDF4-CvGo'  # Replace with your actual API key
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel("gemini-1.5-flash-latest")
chat = model.start_chat()

app = Flask(__name__)

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('apiindex.html')  # Ensure apiindex.html is in the templates folder

# Route to handle POST request from the frontend (sending user message)
@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form.get('message', '')  # Default to empty string if 'message' key is missing
    if not user_message:
        return jsonify({'response': 'No message provided!'})
    
    if user_message.lower() == 'bye':
        return jsonify({'response': 'Goodbye!'})

    try:
        response = chat.send_message(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f"Error generating response: {str(e)}"})

# This ensures that the app runs only when this file is executed, not when imported
if __name__ == '__main__':
    app.run(debug=True)'''