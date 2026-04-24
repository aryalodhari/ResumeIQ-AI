from flask import Flask, request, render_template, redirect, session
from db import Base, engine, SessionLocal
import models
import PyPDF2
import docx
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "App is running"

if __name__ == "__main__":
    app.run(debug=True)

