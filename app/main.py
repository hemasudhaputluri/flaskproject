from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)

port = int(os.environ.get('PORT', 10000))  # Adjusted the default port

# Load the pre-trained model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
    
@app.route('/')
def index():
    # Load CSV data
    data = pd.read_csv('data.csv')
    # Convert to HTML table
    data_html = data.to_html(classes='table table-striped', index=False)
    return render_template('index.html', data=data_html)

@app.route('/graph')
def graph():
    # Load CSV data
    data = pd.read_csv('graph.csv')
    
    # Create a plotly figure
    fig = px.bar(data, x='Country', y='Score', title='Sample Data Visualization')
    graph_html = fig.to_html(full_html=False)
    
    return render_template('graph.html', graph=graph_html)

@app.route('/about')
def about():
    # Render the about.html template
    return render_template('about.html')

@app.route('/projects')
def projects():
    # Render the projects.html template
    return render_template('projects.html')

@app.route('/placement', methods=['GET', 'POST'])
def placement():
    if request.method == 'POST':
        # Get form data
        if_ = request.form['if']
        cgpa = request.form['cgpa']

        # Convert form data to float and create a feature array
        features = np.array([[float(if_), float(cgpa)]])

        # Predict using the model
        prediction = model.predict(features)

        # Convert prediction to a human-readable form
        result = 'Placed' if prediction[0] == 1 else 'Not Placed'

        # Render the result
        return render_template('result.html', result=result)
    
    # Render the input form
    return render_template('form.html')
if __name__ == '__main__':
    app.run()
