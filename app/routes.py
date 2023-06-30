from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

BASE_URL = "http://127.0.0.1:5000/tasks"


@app.get('/')
def main():
    timestamp = datetime.now().strftime("%F %H:%M:%S")
    return render_template('home.html', ts=timestamp)


@app.get('/about')
def about_me():
    return render_template('about.html')


@app.get('/tasks')
def display_all_tasks():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        task_list = response.json().get('tasks')
        return render_template('list.html', tasks=task_list)
    return render_template('error.html', err=response.status_code), response.status_code


@app.get('/tasks/<int:task_id>')
def display_task(task_id):
    response = requests.get(f"{BASE_URL}/{task_id}")
    if response.status_code == 200:
        task_1 = response.json().get('task')
        return render_template('detail.html', task=task_1)
    return render_template('error.html', err=response.status_code), response.status_code


@app.get('/tasks/new')
def new_task_form():
    return render_template('new.html')


@app.post('/tasks')
def create_task():
    task_data = request.form
    task_json = {
        "summary": task_data.get('summary'),
        "description": task_data.get('description'),
    }
    response = requests.post(BASE_URL, json=task_json)
    if response.status_code == 201:
        return render_template('success.html', task=response.json().get('task'), message='New task created!')
    return render_template('error.html', err=response.status_code), response.status_code
