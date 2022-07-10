from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Poll, PollOption, Comment
from . import db

views = Blueprint("views", __name__)


@views.route("/api/polls")
@views.route("/api/polls/<sort>")
def get_polls(sort=None):
    polls = Poll.query.order_by(Poll.time_created).all()
    polls.reverse()
    if sort != None:
        polls = Poll.query.filter_by(tag=sort).order_by(Poll.time_created).all()
        polls.reverse()

    poll_list = []
    for poll in polls:
        poll_list.append(poll.to_dict())

    return jsonify(polls=poll_list)


@views.route("/api/poll/<poll_id>")
def get_poll(poll_id):
    poll = Poll.query.get(poll_id)
    return jsonify(poll=poll.to_dict())


@views.route("/api/user/<username>")
def get_profile(username=None):
    user = User.query.filter_by(username=username).first()

    polls = []
    for poll in user.polls:
        polls.append(poll.to_dict())
        
    comments = []
    for comment in user.comments:
        comments.append(comment.to_dict())

    return jsonify(user=user.to_dict(), polls=polls, comments=comments)


@views.route("/api/vote-poll", methods=["POST"])
def vote_poll():
    form_data = request.get_json()
    poll = Poll.query.get(form_data["pollId"])
    user = User.query.filter_by(username=form_data["username"]).first()
    vote = form_data["vote"]

    if user in poll.voters:
        return jsonify(status="failure", message="User has already voted on this poll")

    for option in poll.options:
        if option.name == vote:
            option.votes += 1
            poll.total_votes += 1
            user.voted_polls.append(poll)
            break

    db.session.commit()

    return jsonify(status="success")


@views.route("/api/create-poll", methods=["POST"])
def create_poll():
    form_data = request.get_json()
    user = User.query.filter_by(username=form_data["username"]).first()
    title = form_data["title"]
    tag = form_data["tag"]
    options = form_data["options"]

    new_poll = Poll(title=title, user=user, tag=tag)
    db.session.add(new_poll)        
    for option in options:
        if not option:
            continue
        poll_option = PollOption(poll=new_poll, name=option)
        db.session.add(poll_option)

    db.session.commit()

    return jsonify(status="success", message="Poll successfully created")


@views.route("/api/create-comment", methods=["POST"])
def create_comment():
    form_data = request.get_json()
    user = User.query.filter_by(username=form_data["username"]).first()
    poll = Poll.query.get(form_data["pollId"])
    content = form_data["content"]

    new_comment = Comment(user=user, poll=poll, content=content)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify(status="success")


@views.route("/api/create-user", methods=["POST"])
def create_user():
    form_data = request.get_json()
    username = form_data["username"]
    email = form_data["email"]
    password = form_data["password"]

    if User.query.filter_by(username=username).first():
        return jsonify(status="failure", message="Username already in use")
    if User.query.filter_by(email=email).first():
        return jsonify(status="failure", message="Email already in use")

    new_user = User(username=username, email=email, password=generate_password_hash(password, method="sha256"))
    db.session.add(new_user)
    db.session.commit()

    return jsonify(status="success")


@views.route("/api/delete-poll/<poll_id>", methods=["POST"])
def delete_poll(poll_id):
    deleted_poll = Poll.query.get(poll_id)
    for option in deleted_poll.options:
        db.session.delete(option)  

    db.session.delete(deleted_poll)
    db.session.commit()
        
    return jsonify(status="success")


@views.route("/api/delete-comment/<comment_id>", methods=["POST"])
def delete_comment(comment_id):
    deleted_comment = Comment.query.get(comment_id)
    db.session.delete(deleted_comment)
    db.session.commit()

    return jsonify(status="success")


@views.route("/api/delete-user/<user_id>", methods=["POST"])
def delete_user(user_id):
    deleted_user = User.query.get(user_id)
    db.session.delete(deleted_user)
    db.session.commit()

    return jsonify(status="success")


@views.route("/api/login", methods=["POST"])
def login():
    form_data = request.get_json()
    username = form_data["username"]
    password = form_data["password"]
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(status="failure", message="Incorrect username")
    if not check_password_hash(user.password, password):
        return jsonify(status="failure", message="Incorrect password")

    return jsonify(status="success", message=f"Logged in as {user.username}")
