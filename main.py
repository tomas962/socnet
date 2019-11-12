from flask import Flask, escape, request, jsonify, Response

app = Flask(__name__)

def exists(resource, id):
    for r in resource:
        if r["id"] == id:
            return True
    return False

def new_id(resoure):
    max = 0
    for r in resoure:
        if r["id"] > max:
            max = r["id"]
    return max + 1

users = [
    {"id":0,"username":"Bob", "age":22, "group":"admin"},
    {"id":1,"username":"Jeff", "age":18, "group":"regular"},
    {"id":2,"username":"Jerry", "age":25, "group":"regular"}
]

posts = [
    {"id":0, "user_id":1, "text":"Hello everyone!", "date":"2019-09-23T18:25:43.511Z"},
    {"id":1, "user_id":1, "text":"I'm an admin :)", "date":"2019-09-24T18:28:43.511Z"},
    {"id":2, "user_id":0, "text":"I'm an admin :)", "date":"2019-09-24T18:28:43.511Z"}
]

comments = [
    {"id":0, "user_id":1, "post_id":1, "text":"Who?", "date":"2019-09-24T18:35:35.000Z"},
    {"id":1, "user_id":2, "post_id":1, "text":"So?", "date":"2019-09-25T08:55:44.000Z"},
    {"id":2, "user_id":2, "post_id":2, "text":"So?", "date":"2019-09-25T08:55:44.000Z"}
]

@app.after_request
def set_content_type(response):
    response.headers["Content-Type"] = "application/json"
    print(str(response.status_code // 100))
    if response.status_code // 100 == 4 or response.status_code // 100 == 5:
        response.set_data("")
    return response

@app.route('/')
def hello():
    return {"routes": ["users", "comments", "posts"]}


####### USERS ############
@app.route('/users/', methods=['GET'])
def users_list():
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return Response(status=404 )

@app.route('/users/', methods=['POST'])
def post_user():
    global users
    user = request.get_json()
    user["id"] = new_id(users)
    users.append(user)
    response = Response(status=201 )
    response.headers["Location"] = "/users/" + str(user["id"])
    return response

@app.route('/users/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    new_user = request.get_json()
    new_user["id"] = user_id
    for i in range(len(users)):
        if users[i]["id"] == user_id:
            users[i] = new_user
            return Response(status=204 )
    # if not found create new
    new_user["id"] = new_id(users)
    users.append(new_user)
    response = Response(status=201 )
    response.headers["Location"] = "/users/" + str(new_user["id"])
    return response

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    for i in range(len(users)):
        if users[i]["id"] == user_id:
            return users.pop(i)
            
    return Response(status=404 )

####### POSTS ############
@app.route('/posts/', methods=['GET'])
@app.route('/users/<int:user_id>/posts/', methods=['GET'])
def posts_list(user_id = None):
    if user_id is None:
        return jsonify(posts)
    else:
        if exists(users, user_id):
            user_posts = []
            for post in posts:
                if post["user_id"] == user_id:
                    user_posts.append(post)
            return jsonify(user_posts)
        else:
            return Response(status=404)
            

@app.route('/posts/<int:post_id>', methods=['GET'])
@app.route('/users/<int:user_id>/posts/<int:post_id>', methods=['GET'])
def get_post(post_id, user_id = None):
    if user_id is None:
        for post in posts:
            if post["id"] == post_id:
                return post
        return Response(status=404 )
    else:
        if exists(users, user_id):
            for post in posts:
                if post["id"] == post_id and post["user_id"] == user_id:
                    return post
            # if not found
            return Response(status=404)

@app.route('/posts/', methods=['POST'])
@app.route('/users/<int:user_id>/posts/', methods=['POST'])
def post_post(user_id = None):
    if user_id is None:
        post = request.get_json()
        post["id"] = new_id(posts)
        posts.append(post)
        response =  Response(status=201 )
        response.headers['location'] = "/posts/" + str(post["id"])
        return response
    elif exists(users, user_id):
        post = request.get_json()
        post["id"] = new_id(posts)
        post["user_id"] = user_id
        posts.append(post)
        response =  Response(status=201 )
        response.headers['location'] = "/users/" + str(user_id) + "/posts/" + str(post["id"])
        return response
    #if doesn't exist
    return Response(status = 404)
        

@app.route('/posts/<int:post_id>', methods=['PUT'])
@app.route('/users/<int:user_id>/posts/<int:post_id>', methods=['PUT'])
def put_post(post_id, user_id = None):
    if user_id is None: 
        new_post = request.get_json()
        new_post["id"] = post_id
        for i in range(len(posts)):
            if posts[i]["id"] == post_id:
                posts[i] = new_post
                return Response(status=204 )
        # if not found create new
        new_post["id"] = new_id(posts)
        posts.append(new_post)
        response = Response(status=201 )
        response.headers["Location"] = "/posts/" + str(new_post["id"])
        return response
    elif exists(users, user_id):
        new_post = request.get_json()
        new_post["id"] = post_id
        new_post["user_id"] = user_id
        for i in range(len(posts)):
            if posts[i]["id"] == post_id:
                if posts[i]["user_id"] == user_id:
                    posts[i] = new_post
                    return Response(status=204 )
                else: #user isn't owner of the post
                    return Response(status=400)
        # if not found create new
        new_post["id"] = new_id(posts)
        posts.append(new_post)
        response = Response(status=201 )
        response.headers["Location"] = "/users/" + str(user_id) + "/posts/" + str(new_post["id"])
        return response

    # if user not found return 404
    return Response(status = 404)

@app.route('/posts/<int:post_id>', methods=['DELETE'])
@app.route('/users/<int:user_id>/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id, user_id = None):
    if user_id is None:
        for i in range(len(posts)):
            if posts[i]["id"] == post_id:
                return posts.pop(i)
        return Response(status=404 )
    elif exists(users, user_id):
        for i in range(len(posts)):
            if posts[i]["id"] == post_id and posts[i]["user_id"] == user_id:
                return posts.pop(i)
        return Response(status=404 )
    # if user doesnt exist
    return Response(status=404 )

####### COMMENTS ############
@app.route('/comments/', methods=['GET'])
@app.route('/users/<int:user_id>/comments/', methods=['GET'])
@app.route('/posts/<int:post_id>/comments/', methods=['GET'])
@app.route('/users/<int:user_id>/posts/<int:post_id>/comments/', methods=['GET'])
@app.route('/posts/<int:post_id>/users/<int:user_id>/comments/', methods=['GET'])
def comments_list(user_id = None, post_id = None):
    if user_id is None and post_id is None:
        return jsonify(comments)
    elif post_id is None:
        if exists(users, user_id):
            user_comments = []
            for comment in comments:
                if comment["user_id"] == user_id:
                    user_comments.append(comment)
            return jsonify(user_comments)
        else:
            return Response(status=404)
    elif user_id is None:
        if exists(posts, post_id):
            post_comments = []
            for comment in comments:
                if comment["post_id"] == post_id:
                    post_comments.append(comment)
            return jsonify(post_comments)
        else:
            return Response(status=404)
    else: #user and post
        if exists(users, user_id) and exists(posts, post_id):
            user_post_comments = []
            for comment in comments:
                if comment["post_id"] == post_id and comment["user_id"] == user_id:
                    user_post_comments.append(comment)
            return jsonify(user_post_comments)
        else:
            return Response(status=404)

@app.route('/comments/<int:comment_id>', methods=['GET'])
@app.route('/users/<int:user_id>/comments/<int:comment_id>', methods=['GET'])
@app.route('/posts/<int:post_id>/comments/<int:comment_id>', methods=['GET'])
@app.route('/users/<int:user_id>/posts/<int:post_id>/comments/<int:comment_id>', methods=['GET'])
@app.route('/posts/<int:post_id>/users/<int:user_id>/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id, post_id = None, user_id = None):
    if user_id is None and post_id is None:
        for comment in comments:
            if comment["id"] == comment_id:
                return comment
        return Response(status=404)
    elif post_id is None:
        if exists(users, user_id):
            for comment in comments:
                if comment["user_id"] == user_id and comment["id"] == comment_id:
                    return comment
            return Response(status=404)
        else:
            return Response(status=404)
    elif user_id is None:
        if exists(posts, post_id):
            for comment in comments:
                if comment["post_id"] == post_id and comment["id"] == comment_id:
                    return comment
            return Response(status=404)
        else:
            return Response(status=404)
    else: #user and post
        if exists(users, user_id) and exists(posts, post_id):
            for comment in comments:
                if comment["post_id"] == post_id and comment["user_id"] == user_id and comment["id"] == comment_id:
                    return comment
            return Response(status=404)
        else:
            return Response(status=404)

@app.route('/comments/', methods=['POST'])
@app.route('/users/<int:user_id>/comments/', methods=['POST'])
@app.route('/posts/<int:post_id>/comments/', methods=['POST'])
@app.route('/users/<int:user_id>/posts/<int:post_id>/comments/', methods=['POST'])
@app.route('/posts/<int:post_id>/users/<int:user_id>/comments/', methods=['POST'])
def post_comment(user_id = None, post_id = None):
    comment = request.get_json()
    comment["id"] = new_id(comments)
    if user_id is None and post_id is None:
        comments.append(comment)
        response = Response(status=201)
        response.headers["Location"] = "/comments/" + str(comment["id"])
        return response
    elif user_id is None:
        if exists(posts, post_id):
            comment["post_id"] = post_id
            comments.append(comment)
            response = Response(status=201)
            response.headers["Location"] = "/posts/" + str(post_id) + "/comments/" + str(comment["id"])
            return response    
        return Response(status=404)
    elif post_id is None:
        if exists(users, user_id):
            comment["user_id"] = user_id
            comments.append(comment)
            response = Response(status=201)
            response.headers["Location"] = "/users/" + str(user_id) + "/comments/" + str(comment["id"])
            return response
        return Response(status=404)
    else: # both id's
        if exists(users, user_id) and exists(posts, post_id):
            comment["user_id"] = user_id
            comment["post_id"] = post_id
            comments.append(comment)
            response = Response(status=201)
            response.headers["Location"] = "/users/" + str(user_id) + "/posts/" + str(post_id) + "/comments/" + str(comment["id"])
            return response
        return Response(status=404)
    return Response(status=404 )

@app.route('/comments/<int:comment_id>', methods=['PUT'])
@app.route('/users/<int:user_id>/comments/<int:comment_id>', methods=['PUT'])
@app.route('/posts/<int:post_id>/comments/<int:comment_id>', methods=['PUT'])
@app.route('/users/<int:user_id>/posts/<int:post_id>/comments/<int:comment_id>', methods=['PUT'])
@app.route('/posts/<int:post_id>/users/<int:user_id>/comments/<int:comment_id>', methods=['PUT'])
def put_comment(comment_id, user_id = None, post_id = None):
    new_comment = request.get_json()
    new_comment["id"] = comment_id
    if user_id is None and post_id is None:
        for i in range(len(comments)):
            if comments[i]["id"] == comment_id:
                comments[i] = new_comment
                return Response(status=204)
        #not found, create new
        new_comment["id"] = new_id(comments)
        comments.append(new_comment)
        response = Response(status=201)
        response.headers["Location"] = "/comments/" + str(new_comment["id"])
        return response
    elif post_id is None:
        if exists(users, user_id):
            for i in range(len(comments)):
                if comments[i]["id"] == comment_id and comments[i]["user_id"] == user_id:
                    new_comment["user_id"] = user_id
                    comments[i] = new_comment
                    return Response(status=204 )
            #not found, create new
            new_comment["id"] = new_id(comments)
            new_comment["user_id"] = user_id
            comments.append(new_comment)
            response = Response(status=201)
            response.headers["Location"] = "/users/" + str(user_id) + "/comments/" + str(new_comment["id"])
            return response
        return Response(status=404)
    elif user_id is None:
        if exists(posts, post_id):
            for i in range(len(comments)):
                if comments[i]["id"] == comment_id and comments[i]["post_id"] == post_id:
                    new_comment["post_id"] = post_id
                    comments[i] = new_comment
                    return Response(status=204 )
            #not found, create new
            new_comment["id"] = new_id(comments)
            new_comment["post_id"] = post_id
            comments.append(new_comment)
            response = Response(status=201)
            response.headers["Location"] = "/posts/" + str(post_id) + "/comments/" + str(new_comment["id"])
            return response
        return Response(status=404)        
    else: #both id's
        if exists(users, user_id) and exists(posts, post_id):
            for i in range(len(comments)):
                if comments[i]["id"] == comment_id and comments[i]["post_id"] == post_id and comments[i]["user_id"] == user_id:
                    new_comment["post_id"] = post_id
                    new_comment["user_id"] = user_id
                    comments[i] = new_comment
                    return Response(status=204 )
            #not found, create new
            new_comment["id"] = new_id(comments)
            new_comment["user_id"] = user_id
            new_comment["post_id"] = post_id
            comments.append(new_comment)
            response = Response(status=201)
            response.headers["Location"] = "/posts/" + str(post_id) + "/users/" + str(user_id) + "/comments/" + str(new_comment["id"])
            return response
        return Response(status=404)        
    return Response(status=404 )

@app.route('/comments/<int:comment_id>', methods=['DELETE'])
@app.route('/users/<int:user_id>/comments/<int:comment_id>', methods=['DELETE'])
@app.route('/posts/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
@app.route('/users/<int:user_id>/posts/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
@app.route('/posts/<int:post_id>/users/<int:user_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id, post_id = None, user_id = None):
    if user_id is None and post_id is None:
        for i in range(len(comments)):
            if comments[i]["id"] == comment_id:
                return comments.pop(i)
        return Response(status=404)
    elif post_id is None:
        if exists(users, user_id):
            for i in range(len(comments)):
                if comments[i]["id"] == comment_id and comments[i]["user_id"] == user_id:
                    return comments.pop(i)
            return Response(status=404)
        return Response(status=404)
    elif user_id is None:
        if exists(posts, post_id):
            for i in range(len(comments)):
                if comments[i]["id"] == comment_id and comments[i]["post_id"] == post_id:
                    return comments.pop(i)
            return Response(status=404)
        return Response(status=404)
    else: #both
        if exists(users, user_id) and exists(posts, post_id):
            for i in range(len(comments)):
                if comments[i]["id"] == comment_id and comments[i]["post_id"] == post_id and comments[i]["user_id"] == user_id:
                    return comments.pop(i)
            return Response(status=404)
        return Response(status=404)
    return Response(status=404 )
