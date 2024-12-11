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
    """Handle GET and POST requests for posts.
    - GET: Get all posts. It is optional to sort them by sending query strings.
           Posts will be sorted by title or content when giving query string sort.
           Posts will be sorted by in ascending or descending when giving query string direction.
    - POST: Add a new post with title and content.
    """
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
    if request.method == 'GET':
        direction = request.args.get('direction')
        sort = request.args.get('sort')
        if sort or direction:
            if sort is None:
                sort = 'title'
            elif sort != "title" and sort != "content":
                return jsonify({"error": f"False input", "info": "sort has to be 'title' or 'content' if given."}), 400
            if direction is None:
                direction = True
            elif direction == 'asc':
                direction = False
            elif direction == 'desc':
                direction = True
            else:
                return jsonify({"error": f"False input", "info":  "direction has to be 'asc' or 'desc' if given."}), 400
            sorted_posts = sorted(POSTS, key=lambda post: post[sort], reverse=direction)
            return jsonify(sorted_posts), 200
        return jsonify(POSTS), 200


@app.route('/api/posts/<id>', methods=['DELETE', 'PUT'])
def delete_post(id: str):
    """Handle DELETE and PUT requests for a specific post by ID.

    - DELETE: Remove a post by its ID.
    - PUT: Update a post's title or content by its ID.
    """
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


@app.route('/api/posts/search', methods=['GET'])
def search_for_post():
    """Search for posts by title or content keywords."""
    search_title = request.args.get('title')
    search_content = request.args.get('content')
    filtered_posts = []
    if search_title:
        filtered_titles = [post for post in POSTS if search_title in post['title']]
    else:
        filtered_titles = []
    if search_content:
        filtered_contents = [post for post in POSTS if search_content in post['content']]
    else:
        filtered_contents = []
    for post in filtered_titles:
        if post not in filtered_posts:
            filtered_posts.append(post)
    for post in filtered_contents:
        if post not in filtered_posts:
            filtered_posts.append(post)
    return jsonify(filtered_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)



#todo 2. Upload Read page Conclusion and Next Steps
#todo 3. Upload to Codio