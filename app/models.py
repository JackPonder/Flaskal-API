from datetime import date, datetime
from . import db

voters_table = db.Table(
    "voters",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("poll_id", db.Integer, db.ForeignKey("polls.id")),
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(32))
    date_joined = db.Column(db.Date)
    polls = db.relationship("Poll", backref="user")
    comments = db.relationship("Comment", backref="user")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date_joined = date.today()
        self.role = "User"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "dateJoined": self.date_joined,
            "role": self.role,
            "comments": [comment.to_dict() for comment in self.comments],
            "polls": [poll.to_dict() for poll in self.polls],
        }

    def __repr__(self):
        return f"<User: {self.username}>"


class Poll(db.Model):
    __tablename__ = "polls"
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(128))
    options = db.relationship("PollOption", backref="poll")
    total_votes = db.Column(db.Integer)
    tag = db.Column(db.String(32))
    time_created = db.Column(db.DateTime)
    voters = db.relationship("User", secondary=voters_table, backref="voted_polls")
    comments = db.relationship("Comment", backref="poll")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_created = datetime.today()
        self.total_votes = 0

    def to_dict(self):
        return {
            "id": self.id,
            "creator": self.user.username,
            "title": self.title, 
            "options": [option.to_dict() for option in self.options],
            "totalVotes": self.total_votes,
            "tag": self.tag,
            "timeCreated": self.time_created,
            "comments": [comment.to_dict() for comment in self.comments],
            "voters": [voter.username for voter in self.voters],
        }

    def __repr__(self):
        return f"<Poll: {self.title}>"


class PollOption(db.Model):
    __tablename__ = "poll_options"
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey("polls.id"))
    name = db.Column(db.String(128))
    votes = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.votes = 0

    def to_dict(self):
        return {
            "name": self.name,
            "votes": self.votes,
        }

    def __repr__(self):
        return f"<Poll Option: {self.name}>"


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)    
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    poll_id = db.Column(db.Integer, db.ForeignKey("polls.id"))
    content = db.Column(db.Text)
    time_created = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_created = datetime.today()

    def to_dict(self):
        return {
            "id": self.id,
            "creator": self.user.username,
            "poll": { "title": self.poll.title, "id": self.poll.id },
            "content": self.content,
            "timeCreated": self.time_created,
        }

    def __repr__(self):
        return f"<Comment #{self.id}>"
