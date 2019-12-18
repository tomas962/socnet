from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    age = Column(Integer)
    username = Column(String(45), unique=True)
    group = Column(String(45))
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    password = Column(String(45))

    @classmethod
    def fromjson(cls, userjson):
        newuser = cls(username=userjson["username"] if "username" in userjson else None,
         age=userjson["age"] if "age" in userjson else None,
         # group=userjson["group"] if "group" in userjson else None,
          group="regular",
          password=userjson["password"] if "password" in userjson else None)
        return newuser

    def __repr__(self):
        return '{"username":"'+ self.username +'", "age": "'+ str(self.age) +'", "user_id": "'+ str(self.user_id) +'"}'
    
    def serialize(self):
        user = {}
        user["username"] = self.username
        user["age"] = self.age
        user["user_id"] = self.user_id
        user["group"] = self.group
        return user
    
    def update_from_json(self, json):
        if "age" in json:
            self.age = json["age"]
        if "username" in json:
            self.username = json["username"]
        if "group" in json:
            self.group = json["group"]

class Post(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True)
    text = Column(Text)
    date = Column(TIMESTAMP, nullable=False, server_default=func.now())
    user = relationship("User", back_populates="posts")
    user_id = Column(Integer, ForeignKey('users.user_id'))
    comments = relationship("Comment", back_populates="post")

    @classmethod
    def fromjson(cls, postjson):
        newpost = cls(text=postjson["text"], user_id=postjson["user_id"])
        return newpost
    
    def serialize(self):
        post = {}
        post["text"] = self.text
        post["date"] = self.date
        post["user_id"] = self.user_id
        post["post_id"] = self.post_id
        return post
    
    def update_from_json(self, json):
        if "text" in json:
            self.text = json["text"]
        if "date" in json:
            self.date = json["date"]
        if "user_id" in json:
            self.user_id = json["user_id"]
        if "post_id" in json:
            self.post_id = json["post_id"]

class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True)
    text = Column(Text)
    date = Column(TIMESTAMP, nullable=False, server_default=func.now())
    user = relationship("User", back_populates="comments")
    user_id = Column(Integer, ForeignKey('users.user_id'))
    post = relationship("Post", back_populates="comments")
    post_id = Column(Integer, ForeignKey('posts.post_id'))

    @classmethod
    def fromjson(cls, commentjson):
        newc = cls(text=commentjson["text"], user_id=commentjson["user_id"], post_id=commentjson["post_id"])
        return newc
    
    def serialize(self):
        c = {}
        c["text"] = self.text
        c["date"] = self.date
        c["user_id"] = self.user_id
        c["post_id"] = self.post_id
        c["comment_id"] = self.comment_id
        return c
    
    def update_from_json(self, json):
        if "text" in json:
            self.text = json["text"]
        if "date" in json:
            self.date = json["date"]
        if "user_id" in json:
            self.user_id = json["user_id"]
        if "post_id" in json:
            self.post_id = json["post_id"]
        if "comment_id" in json:
            self.comment_id = json["comment_id"]