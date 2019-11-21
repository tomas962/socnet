from flask import Flask, escape, request, jsonify, Response
from database import db_session
from models import User, Post, Comment
from datetime import datetime, timedelta
import sqlalchemy
import time
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)
app.debug = True

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'adrh51561234@!#(&$%$#@Hfgnr(#@g256sh12g9svd2))'
jwt = JWTManager(app)


@app.route('/auth', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    expires = timedelta(minutes=30)
    user = User.query.filter(User.username == username).one_or_none()
    if user.password == password:
        access_token = create_access_token(identity={"user_id":user.user_id, "group":user.group},
         expires_delta=expires)
        return jsonify(access_token=access_token), 200


    return jsonify({"error": "Bad username or password"}), 401

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.after_request
def set_content_type(response):
    print(str(response.status_code // 100))
    data = response.get_data(True)
    if response.status_code // 100 == 4 or response.status_code // 100 == 5:
        if "\"error\"" not in response.get_data(True):
            response.set_data("")
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/')
def hello():
    print("hello")    
    return {"routes": ["users", "comments", "posts"]}


####### USERS ############
@app.route('/users/', methods=['GET'])
def users_list():
    users = db_session.query(User).all()
    serialized_users = []
    for usr in users:
        serialized_users.append(usr.serialize())
    return jsonify(serialized_users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter(User.user_id == user_id).one_or_none()
    if user is not None:
        return user.serialize()
    else:
        return Response(status=404 )

@app.route('/users/', methods=['POST'])
def post_user():
    userjson = request.get_json()
    user = User.fromjson(userjson)
    db_session.add(user)
    try:
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return Response(status=409)
        
    response = Response(status=201)
    response.headers["Location"] = "/users/" + str(user.user_id)
    return response

@app.route('/users/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    userjson = request.get_json()
    userjson["user_id"] = user_id
    new_user = User.fromjson(userjson)

    # try to update
    user_to_update = User.query.filter(User.user_id == user_id).one_or_none()
    if user_to_update is not None:
        user_to_update.update_from_json(userjson)
        try:
            db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return Response(status=409)
        return Response(status=204 )
        
    # if not found create new
    db_session.add(new_user)
    try:
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return Response(status=409)
    response = Response(status=201 )
    response.headers["Location"] = "/users/" + str(new_user.user_id)
    return response

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_row = User.query.filter(User.user_id == user_id)
    user = user_row.one_or_none()
    if user is not None:
        user_row.delete()
        db_session.commit()
        return user.serialize()
    else:
        return Response(status=404 )
            

####### POSTS ############
@app.route('/users/<int:user_id>/posts/', methods=['GET'])
def user_posts_list(user_id = None):
    user = User.query.filter(User.user_id == user_id).one_or_none()
    if user is None:
        return Response(status=404)

    posts_rows = Post.query.filter(Post.user_id == user_id).all()
    posts = []
    for post in posts_rows:
        posts.append(post.serialize())
    return jsonify(posts)

@app.route('/posts/', methods=['GET'])
def posts_list():
    posts_rows = Post.query.all()
    posts = []
    for post in posts_rows:
        posts.append(post.serialize())
    return jsonify(posts)

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.filter(Post.post_id == post_id).one_or_none()
    if post is None:
        return Response(status=404)
    else:
        return post.serialize()

@app.route('/users/<int:user_id>/posts/<int:post_id>', methods=['GET'])
def get_user_post(post_id, user_id):
    post = Post.query.filter(Post.post_id == post_id).filter(Post.user_id == user_id).one_or_none()
    if post is None:
        return Response(status=404)
    else:
        return post.serialize()

@app.route('/posts/', methods=['POST'])
def post_post():
    postjson = request.get_json()
    if "user_id" not in postjson:
        response = Response("{\"error\":\"user_id not found in request body\"}", status=400)
        return response
    elif User.query.filter(User.user_id == postjson["user_id"]).first() is None:
        return Response(status=404)
    newpost = Post.fromjson(postjson)
    db_session.add(newpost)
    db_session.commit()
    response =  Response(status=201 )
    response.headers['location'] = "/posts/" + str(newpost.post_id)
    return response

@app.route('/users/<int:user_id>/posts/', methods=['POST'])
def post_user_post(user_id):
    if User.query.filter(User.user_id == user_id).first() is None:
        return Response('{"error":"user not found"}', status=404)

    postjson = request.get_json()
    postjson["user_id"] = user_id
    newpost = Post.fromjson(postjson)
    db_session.add(newpost)
    db_session.commit()
    response =  Response(status=201 )
    response.headers['location'] = "/users/" + str(user_id) + "/posts/" + str(newpost.post_id)
    return response

@app.route('/posts/<int:post_id>', methods=['PUT'])
def put_post(post_id):
    postjson = request.get_json()
    postjson["post_id"] = post_id


    post_to_update = Post.query.filter(Post.post_id == post_id).first()
    if post_to_update is None:
        #create new
        if "user_id" not in postjson:
            return Response('{"error":"user_id key not found"}', status=400)
        newpost = Post.fromjson(postjson)
        user = User.query.filter(User.user_id == newpost.user_id).first()
        if user is None:
            return Response('{"error":"user with user_id not found"}', status=404)

        db_session.add(newpost)
        db_session.commit()
        response = Response(status=201 )
        response.headers["Location"] = "/posts/" + str(newpost.post_id)
        return response
    else:
        # update existing
        post_to_update.update_from_json(postjson)
        db_session.commit()
        return Response(status=204 )


@app.route('/users/<int:user_id>/posts/<int:post_id>', methods=['PUT'])
def put_user_post(post_id, user_id):
    if User.query.filter(User.user_id == user_id).first() is None:
        return Response('{"error":"user with user_id not found"}', status = 404)

    post_to_update = Post.query.filter(Post.post_id == post_id).filter(Post.user_id == user_id).first()
    postjson = request.get_json()
    postjson["post_id"] = post_id
    postjson["user_id"] = user_id
    
    if post_to_update is not None:
        post_to_update.update_from_json(postjson)
        db_session.commit()
        return Response(status=204 )
    else:
        #create new
        newpost = Post.fromjson(postjson)


        db_session.add(newpost)
        db_session.commit()
        response = Response(status=201 )
        response.headers["Location"] = "/users/" + str(newpost.user_id) + "/posts/" + str(newpost.post_id)
        return response


@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id, user_id = None):
    post_row = Post.query.filter(Post.post_id == post_id)
    post = post_row.first()
    if post is None:
        return Response('{"error":"post not found"}',status=404 )
    
    post_row.delete()
    db_session.commit()
    return post.serialize()

@app.route('/users/<int:user_id>/posts/<int:post_id>', methods=['DELETE'])
def delete_users_post(post_id, user_id = None):
    if User.query.filter(User.user_id == user_id).first() is None:
        return Response('{"error":"user not found"}',status=404 )
    
    post_row = Post.query.filter(Post.post_id == post_id).filter(Post.user_id == user_id)
    post = post_row.first()
    if post is None:
        return Response('{"error":"post not found"}',status=404 )
    
    post_row.delete()
    db_session.commit()
    return post.serialize()

####### COMMENTS ############
@app.route('/comments/', methods=['GET'])
def comments_list():
    comment_rows = Comment.query.all()
    comments = []
    for c in comment_rows:
        comments.append(c.serialize())
    return jsonify(comments)

@app.route('/users/<int:user_id>/comments/', methods=['GET'])
def user_comments_list(user_id = None, post_id = None):
    user = User.query.filter(User.user_id == user_id).first()
    if user is None:
        return Response('{"error":"user not found"}',status=404 )
    
    return jsonify([c.serialize() for c in user.comments])


@app.route('/posts/<int:post_id>/comments/', methods=['GET'])
def post_comments_list(post_id):
    post = Post.query.filter(Post.post_id == post_id).first()
    if post is None:
        return Response('{"error":"post not found"}',status=404 )

    return jsonify([c.serialize() for c in post.comments])


@app.route('/users/<int:user_id>/posts/<int:post_id>/comments/', methods=['GET'])
@app.route('/posts/<int:post_id>/users/<int:user_id>/comments/', methods=['GET'])
def user_post_comments_list(user_id = None, post_id = None):
    user = User.query.filter(User.user_id == user_id).first()
    if user is None:
        return Response('{"error":"user not found"}',status=404 )
    
    post = Post.query.filter(Post.post_id == post_id).first()
    if post is None:
        return Response('{"error":"post not found"}',status=404 )

    comment_rows = Comment.query.filter(Comment.user_id == user_id).filter(Comment.post_id == post_id).all()

    return jsonify([c.serialize() for c in comment_rows])

@app.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = Comment.query.filter(Comment.comment_id == comment_id).first()
    if comment is None:
        return Response('{"error":"comment not found"}',status=404 )
    return comment.serialize()

@app.route('/users/<int:user_id>/comments/<int:comment_id>', methods=['GET'])
def get_user_comment(comment_id, user_id):
    user = User.query.filter(User.user_id == user_id).first()
    if user is None:
        return Response('{"error":"user not found"}',status=404 )

    comment = Comment.query.filter(Comment.user_id == user_id).filter(Comment.comment_id == comment_id).first()
    if comment is None:
        return Response('{"error":"comment not found"}',status=404 )

    return comment.serialize()

@app.route('/posts/<int:post_id>/comments/<int:comment_id>', methods=['GET'])
def get_post_comment(comment_id, post_id):
    post = Post.query.filter(Post.post_id == post_id).first()
    if post is None:
        return Response('{"error":"post not found"}',status=404 )

    comment = Comment.query.filter(Comment.post_id == post_id).filter(Comment.comment_id == comment_id).first()
    if comment is None:
        return Response('{"error":"comment not found"}',status=404 )
    
    return comment.serialize()

@app.route('/users/<int:user_id>/posts/<int:post_id>/comments/<int:comment_id>', methods=['GET'])
@app.route('/posts/<int:post_id>/users/<int:user_id>/comments/<int:comment_id>', methods=['GET'])
def get_user_post_comment(comment_id, post_id = None, user_id = None):
    user = User.query.filter(User.user_id == user_id).first()
    if user is None:
        return Response('{"error":"user not found"}',status=404 )

    post = Post.query.filter(Post.post_id == post_id).first()
    if post is None:
        return Response('{"error":"post not found"}',status=404 )

    comment = Comment.query.filter(Comment.user_id == user_id).filter(Comment.post_id == post_id).filter(Comment.comment_id == comment_id).first()
    if comment is None:
        return Response('{"error":"comment not found"}',status=404 )

    return comment.serialize()

@app.route('/comments/', methods=['POST'])
def post_comment():
    commentjson = request.get_json()
    if "user_id" not in commentjson:
        return Response('{"error":"user_id required"}',status=400 )
    if "post_id" not in commentjson:
        return Response('{"error":"post_id required"}',status=400 ) 

    newcomment = Comment.fromjson(commentjson)
    user = User.query.filter(User.user_id == newcomment.user_id).first()
    if user is None:
        return Response('{"error":"user not found"}',status=404 )
    post = Post.query.filter(Post.post_id == newcomment.post_id).first()
    if post is None:
        return Response('{"error":"post not found"}',status=404 )

    db_session.add(newcomment)
    db_session.commit()
    response = Response(status=201)
    response.headers["Location"] = "/comments/" + str(newcomment.comment_id)
    return response
    

@app.route('/users/<int:user_id>/comments/', methods=['POST'])
def post_user_comment(user_id):
    commentjson = request.get_json()
    commentjson["user_id"] = user_id

    if "post_id" not in commentjson:
        return Response('{"error":"post_id required"}',status=400 ) 

    user = User.query.filter(User.user_id == user_id).first()
    if user is None:
        return Response('{"error":"user not found"}',status=404 )

    newcomment = Comment.fromjson(commentjson)
    post = Post.query.filter(Post.post_id == newcomment.post_id).first()
    if post is None:
        return Response('{"error":"post not found"}',status=404 )

    db_session.add(newcomment)
    db_session.commit()
    response = Response(status=201)
    response.headers["Location"] = "/users/" + str(newcomment.user_id) + "/comments/" + str(newcomment.comment_id)
    return response


@app.route('/posts/<int:post_id>/comments/', methods=['POST'])
def post_post_comment(post_id):
    commentjson = request.get_json()
    commentjson["post_id"] = post_id

    if "user_id" not in commentjson:
        return Response('{"error":"user_id required"}',status=400 ) 

    user = User.query.filter(User.user_id == commentjson["user_id"]).first()
    if user is None:
        return Response('{"error":"user not found"}',status=404 )

    post = Post.query.filter(Post.post_id == post_id).first()
    if post is None:
        return Response('{"error":"post not found"}',status=404 )

    newcomment = Comment.fromjson(commentjson)
    db_session.add(newcomment)
    db_session.commit()
    response = Response(status=201)
    response.headers["Location"] = "/posts/" + str(newcomment.post_id) + "/comments/" + str(newcomment.comment_id)
    return response 
    


@app.route('/users/<int:user_id>/posts/<int:post_id>/comments/', methods=['POST'])
@app.route('/posts/<int:post_id>/users/<int:user_id>/comments/', methods=['POST'])
def post_user_post_comment(user_id, post_id):
    post = Post.query.filter(Post.post_id == post_id).first()
    if post is None:
        return Response('{"error":"post not found"}',status=404 )
        
    user = User.query.filter(User.user_id == user_id).first()
    if user is None:
        return Response('{"error":"user not found"}',status=404 )


    commentjson = request.get_json()
    commentjson["user_id"] = user_id
    commentjson["post_id"] = post_id

    newcomment = Comment.fromjson(commentjson)

    db_session.add(newcomment)
    db_session.commit()
    response = Response(status=201)
    response.headers["Location"] = "/users/" + str(newcomment.user_id) + "/posts/" + str(newcomment.post_id) + "/comments/" + str(newcomment.comment_id)
    return response
    

@app.route('/comments/<int:comment_id>', methods=['PUT'])
def put_comment(comment_id):
    commentjson = request.get_json()
    commentjson["comment_id"] = comment_id

    comment_to_update = Comment.query.filter(Comment.comment_id == comment_id).first()
    if comment_to_update is None:
        #create new
        if "user_id" not in commentjson:
            return Response('{"error":"user_id required"}',status=400 )
        if "post_id" not in commentjson:
            return Response('{"error":"post_id required"}',status=400 ) 
        post = Post.query.filter(Post.post_id == commentjson["post_id"]).first()
        if post is None:
            return Response('{"error":"post not found"}',status=404 )
        user = User.query.filter(User.user_id == commentjson["user_id"]).first()
        if user is None:
            return Response('{"error":"user not found"}',status=404 )
        newcomment = Comment.fromjson(commentjson)
        db_session.add(newcomment)
        db_session.commit()
        response = Response(status=201)
        response.headers["Location"] = "/comments/" + str(newcomment.comment_id)
        return response
    else:
        #update existing
        comment_to_update.update_from_json(commentjson)
        db_session.commit()
        return Response(status=204)


@app.route('/users/<int:user_id>/comments/<int:comment_id>', methods=['PUT'])
def put_users_comment(comment_id, user_id):
    commentjson = request.get_json()
    commentjson["user_id"] = user_id

    user = User.query.filter(User.user_id == commentjson["user_id"]).first()
    if user is None:
        return Response('{"error":"user not found"}',status=404 )
    
    comment_to_update = Comment.query.filter(Comment.user_id == user_id).filter(Comment.comment_id == comment_id).first()
    if comment_to_update is None:
        # create new 
        if "post_id" not in commentjson:
            return Response('{"error":"post_id required"}',status=400 ) 
        post = Post.query.filter(Post.post_id == comments["post_id"]).first()
        if post is None:
            return Response('{"error":"post not found"}',status=404 )


        newcomment = Comment.fromjson(commentjson)
        db_session.add(newcomment)
        db_session.commit()
        response.headers["Location"] = "/users/" + str(newcomment.user_id) + "/comments/" + str(newcomment.comment_id)
        return response
    else:
        # update existing
        comment_to_update.update_from_json(commentjson)
        db_session.commit()
        return Response(status=204 )



@app.route('/posts/<int:post_id>/comments/<int:comment_id>', methods=['PUT'])
def put_post_comment(comment_id, post_id):
    commentjson = request.get_json()
    commentjson["post_id"] = post_id

    post = Post.query.filter(Post.post_id == post_id).first()
    if post is None:
        return Response('{"error":"post not found"}',status=404 )

    comment_to_update = Comment.query.filter(Comment.post_id == post_id).filter(Comment.comment_id == comment_id).first()
    if comment_to_update is None:
        #create new
        if "user_id" not in commentjson:
            return Response('{"error":"user_id required"}',status=400 ) 

        user = User.query.filter(User.user_id == commentjson["user_id"]).first()
        if user is None:
            return Response('{"error":"user not found"}',status=404 )

        newcomment = Comment.fromjson(commentjson)
        db_session.add(newcomment)
        db_session.commit()
        response = Response(status=201)
        response.headers["Location"] = "/posts/" + str(newcomment.post_id) + "/comments/" + str(newcomment.comment_id)
        return response
    else:
        #update
        comment_to_update.update_from_json(commentjson)
        db_session.commit()
        return Response(status=204 )


@app.route('/users/<int:user_id>/posts/<int:post_id>/comments/<int:comment_id>', methods=['PUT'])
@app.route('/posts/<int:post_id>/users/<int:user_id>/comments/<int:comment_id>', methods=['PUT'])
def put_user_post_comment(comment_id, user_id, post_id):
    commentjson = request.get_json()
    commentjson["user_id"] = user_id
    commentjson["post_id"] = post_id

    user = User.query.filter(User.user_id == user_id).first()
    if user is None:
        return Response('{"error":"user not found"}',status=404 )

    post = Post.query.filter(Post.post_id == post_id).first()
    if post is None:
        return Response('{"error":"post not found"}',status=404 )

    comment_to_update = Comment.query.filter(Comment.comment_id == comment_id).filter()
    if comment_to_update is None:
        #add new
        newcomment = Comment.fromjson(commentjson)
        db_session.add(newcomment)
        db_session.commit()
        response = Response(status=201)
        response.headers["Location"] = "/posts/" + str(newcomment.post_id) + "/users/" + str(newcomment.user_id) + "/comments/" + str(newcomment.comment_id)
        return response
    else:
        #update
        comment_to_update.update_from_json(commentjson)
        db_session.commit()
        return Response(status=204 )


@app.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required
def delete_comment(comment_id):
    current_identity = get_jwt_identity()
    if current_identity["group"] == "admin":
        comment_row = Comment.query.filter(Comment.comment_id == comment_id)
        comment = comment_row.first()
        if comment is None:
            return Response('{"error":"comment not found"}',status=404 )
        comment_row.delete()
        db_session.commit()
        return comment.serialize()
    else:
        return Response(status=403)

@app.route('/users/<int:user_id>/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required
def delete_user_comment(comment_id, user_id):
    current_identity = get_jwt_identity()
    if current_identity["group"] == "admin":
        user = User.query.filter(User.user_id == user_id).first()
        if user is None:
            return Response('{"error":"user not found"}',status=404 )
        
        comment_row = Comment.query.filter(Comment.user_id == user_id).filter(Comment.comment_id == comment_id)
        comment = comment_row.first()
        if comment is None:
            return Response('{"error":"comment not found"}',status=404 )

        comment_row.delete()
        db_session.commit()
        return comment.serialize()
    else:
        return Response(status=403)

@app.route('/posts/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_post_comment(comment_id, post_id):
    current_identity = get_jwt_identity()
    if current_identity["group"] == "admin":
        post = Post.query.filter(Post.post_id == post_id).first()
        if post is None:
            return Response('{"error":"post not found"}',status=404 )

        comment_row = Comment.query.filter(Comment.comment_id == comment_id).filter(Comment.post_id == post_id)
        comment = comment_row.first()

        if comment is None:
            return Response('{"error":"comment not found"}',status=404 )

        comment_row.delete()
        db_session.commit()
        return comment.serialize()
    else:
        return Response(status=403)


@app.route('/users/<int:user_id>/posts/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
@app.route('/posts/<int:post_id>/users/<int:user_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_user_post_comment(comment_id, post_id = None, user_id = None):
    current_identity = get_jwt_identity()
    if current_identity["group"] == "admin":
        user = User.query.filter(User.user_id == user_id).first()
        if user is None:
            return Response('{"error":"user not found"}',status=404 )

        post = Post.query.filter(Post.post_id == post_id).first()
        if post is None:
            return Response('{"error":"post not found"}',status=404 )

        comment_row = Comment.query.filter(Comment.user_id == user_id).filter(Comment.post_id == post_id).filter(Comment.comment_id == comment_id)
        comment = comment_row.first()
        if comment is None:
            return Response('{"error":"comment not found"}',status=404 )

        comment_row.delete()
        db_session.commit()
        return comment.serialize()
    else:
        return Response(status=403)