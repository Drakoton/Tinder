from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

def get_random_users(n=10):
    response = requests.get(f'https://randomuser.me/api/?results={n}')
    users = response.json().get('results', [])
    formatted_users = [
        {
            "id": str(uuid.uuid4()),
            "name": f"{user['name']['first']} {user['name']['last']}",
            "age": user['dob']['age'],
            "city": user['location']['city'],
            "picture": user['picture']['large']
        }
        for user in users
    ]
    return formatted_users

@app.route('/api/profiles', methods=['GET'])
def profiles():
    num_profiles = request.args.get('num', default=10, type=int)
    profiles = get_random_users(num_profiles)
    return jsonify(profiles)

if __name__ == '__main__':
    app.run(debug=True)
