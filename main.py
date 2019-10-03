from flask import Flask, escape, request, jsonify, Response
import models

app = Flask(__name__)

users = [
    {"id":0,"username":"Bob", "age":22, "group":"admin"},
    {"id":1,"username":"Jeff", "age":18, "group":"regular"},
    {"id":2,"username":"Jerry", "age":25, "group":"regular"}
]

posts = [
    {"id":0, "user_id":1, "text":"Hello everyone!", "date":"2019-09-23T18:25:43.511Z"},
    {"id":1, "user_id":1, "text":"I'm an admin :)", "date":"2019-09-24T18:28:43.511Z"}
]

comments = [
    {"id":0, "user_id":1, "post_id":1, "text":"Who?", "date":"2019-09-24T18:35:35.000Z"},
    {"id":1, "user_id":2, "post_id":1, "text":"So?", "date":"2019-09-25T08:55:44.000Z"}
]

@app.after_request
def set_content_type(response):
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/')
def hello():
    return {"routes": ["users", "comments", "posts"]}


####### USERS ############
@app.route('/users/', methods=['GET'])
def users_list():
    global users
    global posts
    global comments
    for user in users:
        user["posts"] = []
        for post in posts:
            post["comments"] = []
            for comment in comments:
                if comment["post_id"] == post["id"]:
                    post["comments"].append(comment)
            if post["user_id"] == user["id"]:
                user["posts"].append(post)
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            user["posts"] = []
            for post in posts:
                post["comments"] = []
                for comment in comments:
                    if comment["post_id"] == post["id"]:
                        post["comments"].append(comment)
                if post["user_id"] == user["id"]:
                    user["posts"].append(post)
            return user
    return Response(status=404, content_type="application/json")

@app.route('/users/', methods=['POST'])
def post_user():
    global users
    user = request.get_json()
    users.append(user)
    return Response(status=200, content_type="application/json")

@app.route('/users/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    global users
    new_user = request.get_json()
    if user_id != new_user["id"]:
        return Response(status=400, content_type="application/json")
    for i in range(len(users)):
        if users[i]["id"] == user_id:
            users[i] = new_user
            return Response(status=200, content_type="application/json")
    # if not found create new
    users.append(new_user)
    return Response(status=201, content_type="application/json")

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    for i in range(len(users)):
        if users[i]["id"] == user_id:
            return users.pop(i)
            
    return Response(status=404, content_type="application/json")

####### POSTS ############
@app.route('/posts/', methods=['GET'])
def posts_list():
    return jsonify(posts)

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    for post in posts:
        if post["id"] == post_id:
            return post
    return Response(status=404, content_type="application/json")

@app.route('/posts/', methods=['POST'])
def post_post():
    post = request.get_json()
    posts.append(post)
    return Response(status=200, content_type="application/json")

@app.route('/posts/<int:post_id>', methods=['PUT'])
def put_post(post_id):
    global posts
    new_post = request.get_json()
    if post_id != new_post["id"]:
        return Response(status=400, content_type="application/json")
    for i in range(len(posts)):
        if posts[i]["id"] == post_id:
            posts[i] = new_post
            return Response(status=200, content_type="application/json")
    # if not found create new
    posts.append(new_post)
    return Response(status=201, content_type="application/json")

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global posts
    for i in range(len(posts)):
        if posts[i]["id"] == post_id:
            return posts.pop(i)
            
    return Response(status=404, content_type="application/json")

####### COMMENTS ############
@app.route('/comments/', methods=['GET'])
def comments_list():
    return jsonify(comments)

@app.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    for comment in comments:
        if comment["id"] == comment_id:
            return comment
    return Response(status=404, content_type="application/json")

@app.route('/comments/', methods=['POST'])
def post_comment():
    comment = request.get_json()
    comments.append(comment)
    return Response(status=200, content_type="application/json")

@app.route('/comments/<int:comment_id>', methods=['PUT'])
def put_comment(comment_id):
    global comments
    new_comment = request.get_json()
    if comment_id != new_comment["id"]:
        return Response(status=400, content_type="application/json")
    for i in range(len(comments)):
        if comments[i]["id"] == comment_id:
            comments[i] = new_comment
            return Response(status=200, content_type="application/json")
    # if not found create new
    comments.append(new_comment)
    return Response(status=201, content_type="application/json")

@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    global comments
    for i in range(len(comments)):
        if comments[i]["id"] == comment_id:
            return comments.pop(i)
            
    return Response(status=404, content_type="application/json")
