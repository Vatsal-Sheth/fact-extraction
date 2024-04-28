#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, jsonify
import threading
import requests
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes and methods.

# Initialize OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
openai_client = OpenAI(api_key=api_key)
GPT4_MODEL = "gpt-4-turbo"

state = {
    "question": "",
    "facts": [],
    "status": "idle"  # Possible values: idle, processing, done
}

def fetch_and_process_documents(documents, question):
    state['question'] = question
    state['status'] = 'processing'
    all_facts = []

    for document_url in documents:
        document_text = fetch_document(document_url)
        if document_text:
            extracted_facts = extract_facts(document_text)
            all_facts.extend(extracted_facts)

    consolidated_facts = refine_facts_with_gpt(all_facts)[0].split("\n")
    state['facts'] = consolidated_facts
    state['status'] = 'done'

def fetch_document(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch document from {url}. Error: {e}")
        return None

def extract_facts(text):
    if not text:
        return []
    prompt = "Extract key decisions made by the team from the following text. Please provide a summary in bullet points. State facts not reasons. Start each bullet with 'The team decided to'. Answer the question:"+"".join(state['question'])+"\n".join(text)
    try:
        response = openai_client.chat.completions.create(
            model=GPT4_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return [choice.message.content for choice in response.choices]
    except Exception as e:
        print(f"Error extracting facts with GPT-4: {e}")
        return []

def refine_facts_with_gpt(facts):
    if not facts:
        return []
    prompt = "Here are multiple facts from various documents, the facts are older to newer from start to end. Consolidate these into a concise, accurate list of current decisions (the newer the fact, more accurate it is). Remove any outdated, contradictory, held off or postponed actions. State facts not reasons. Start each point with 'The team decided to'. Answer the following question:" +"".join(state['question'])+ "\n\n".join(facts)
    try:
        response = openai_client.chat.completions.create(
            model=GPT4_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return [choice.message.content for choice in response.choices]
    except Exception as e:
        print(f"Error refining facts with GPT-4: {e}")
        return []

@app.errorhandler(Exception)
def handle_exception(e):
    response = jsonify({"status": "error", "message": str(e)})
    response.status_code = 500
    return response

@app.route('/submit_question_and_documents', methods=['POST'])
def submit_question_and_documents():
    data = request.json
    try:
        threading.Thread(target=fetch_and_process_documents, args=(data['documents'], data['question'])).start()
        return jsonify({"status": "Processing started"}), 202
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/get_question_and_facts', methods=['GET'])
def get_question_and_facts():
    return jsonify({
        "question": state['question'],
        "facts": state['facts'],
        "status": state['status']
    }), 200

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
