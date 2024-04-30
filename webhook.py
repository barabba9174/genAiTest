import requests
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)

# GitHub API credentials
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_OWNER = os.environ.get('GITHUB_OWNER')
GITHUB_REPO = os.environ.get('GITHUB_REPO')


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Get the request payload
    payload = request.get_json()

    # Check if the payload is from a GitHub push event to the main branch

    print(payload['ref'])

    if payload['ref'] == 'refs/heads/main':
        # Extract the relevant information from the payload
        repo_name = payload['repository']['name']
        branch_name = payload['ref'].split('/')[-1]
        commit_sha = payload['after']

        # Create a new branch based on the latest commit in the main branch
        create_new_branch(repo_name, branch_name, commit_sha)

        return jsonify({'message': 'Webhook received and new branch created successfully'})
    else:
        return jsonify({'message': 'Webhook received, but not a push event to the main branch'})

def create_new_branch(repo_name, new_branch_name, base_branch_sha):
    

    # API endpoint for creating a reference (branch)
    ref_endpoint = 'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/git/refs'

    # Create a new reference (branch) based on the base branch
    new_branch_data = {
        'ref': 'refs/heads/{new_branch_name}',
        'sha': base_branch_sha
    }
    create_branch_response = requests.post(ref_endpoint, json=new_branch_data, headers={'Authorization': f'token {GITHUB_TOKEN}'})

    if create_branch_response.status_code == 201:
        print(f'New branch {new_branch_name} created successfully')
    else:
        print(f'Error creating new branch: {create_branch_response.json()["message"]}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)