from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'super-secret-key'

@app.route('/')
def home():
    return render_template('index.html')