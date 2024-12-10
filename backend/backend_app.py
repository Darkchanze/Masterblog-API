from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        frontend_data = request.get_json()
        if frontend_data:
            missing_info = []
            if 'title' not in frontend_data:
                missing_info.append('title')
            if 'content' not in frontend_data:
                missing_info.append('content')
            if missing_info:
                return jsonify({"error": "missing info", "info": missing_info}), 400
            new_title = frontend_data['title']
            new_content = frontend_data['content']
            new_id = int(max(post['id'] for post in POSTS) + 1)
            new_post = {"id": new_id, "title": new_title, "content": new_content}
            POSTS.append(new_post)
            return jsonify(new_post), 201
        else:
            return jsonify({"error": "Missing JSON"}), 400
    return jsonify(POSTS)


@app.route('/api/posts/<id>', methods=['DELETE', 'PUT'])
def delete_post(id: str):
    for post in POSTS:
        if post['id'] == int(id):
            if request.method == 'DELETE':
                POSTS.remove(post)
                return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200
            if request.method == 'PUT':
                frontend_data = request.get_json()
                if frontend_data:
                    post['title'] = frontend_data.get('title', post['title'])
                    post['content'] = frontend_data.get('content', post['content'])
                    return jsonify(post), 200
    return jsonify({"error": f"No post with the id {id} found."}), 404




                #frontend_data = request.get_json()
                #if frontend_data is not None:







if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
