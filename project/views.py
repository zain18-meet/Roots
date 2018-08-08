from flask import render_template, request, Flask, session, redirect, url_for
from flask import session as login_session
from flask_login import login_required, current_user
from . import app, db
import time
from project.forms import RegisterForm, LoginForm

from project.models import Journey, User, Ratings, Notification, Wishlist, Question, Answer


@app.route('/')
def browse():
	form = None
	all_journeys = Journey.query.all()
	if not current_user.is_authenticated:
		form = RegisterForm(request.form)
	return render_template('browse.html', all_journeys=all_journeys, form=form)


@app.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
	if request.method=='POST':
		current_user.country    	= request.form.get('country')
		current_user.profession 	= request.form.get('profession')
		current_user.birthday   	= request.form.get('birthday')
		current_user.city      		= request.form.get('city')
		current_user.number         = request.form.get('number')
		current_user.bio            = request.form.get('bio')
		current_user.profile_img    = request.form.get('picture')
		current_user.is_storyteller = True
		db.session.commit()
		return redirect(url_for('profile', user_id=current_user.id))
	else:
		if current_user.is_storyteller==True:
			return redirect(url_for('profile', user_id=current_user.id))
		else:
			return render_template('apply.html')



@app.route('/profile/<int:user_id>')
def profile(user_id):
	profile = User.query.filter_by(id=user_id).first()
	if profile.is_storyteller==True:
		st_journeys = Journey.query.filter_by(creator_id=user_id).all()
		return render_template('st_profile.html',st_journeys=st_journeys, profile=profile)
	else:
		return render_template('profile.html', profile=profile)



@app.route('/add_journey', methods=['GET', 'POST'])
@login_required
def add_journey():
	if request.method=='POST':
		new_journey = Journey()
		new_journey.creator_id    = current_user.id
		new_journey.title         = request.form.get('title')
		new_journey.description   = request.form.get('description')
		new_journey.location      = request.form.get('location')
		new_journey.duration      = request.form.get('duration')
		new_journey.category      = request.form.get('category')
		new_journey.requirements  = request.form.get('requirements')
		new_journey.people_range  = request.form.get('people_range')
		new_journey.price         = request.form.get('price')
		new_journey.picture       = request.form.get('picture')
		db.session.add(new_journey)
		db.session.commit()
		return redirect(url_for('display_journey', journey_id=new_journey.id))
	else:
		return render_template('add_journey.html')


@app.route('/im_interested/<int:journey_id>', methods=['POST'])
def im_interested(journey_id):
	journey = Journey.query.filter_by(id=journey_id).first()
	new_notification                      = Notification()
	new_notification.st_id                = journey.creator_id
	new_notification.journey_id           = journey_id
	new_notification.interested_user_id   = current_user.id
	new_notification.interested_user_name = current_user.name
	new_notification.journey_title        = journey.title
	localtime = time.localtime(time.time())
	new_notification.time  = str(localtime[1])+"/"+str(localtime[2])+"/"+str(localtime[0])+" at "+str(localtime[3])+":"+str(localtime[4])
	new_wish               = Wishlist()
	new_wish.user_id       = current_user.id
	new_wish.journey_id    = journey_id
	new_wish.journey_title = journey.title
	db.session.add(new_notification)
	db.session.add(new_wish)
	db.session.commit()
	return redirect(url_for('display_wishlist', user_id=current_user.id))


@app.route('/ratings/<int:journey_id>', methods=['POST'])
@login_required
def add_rating(journey_id):
	journey     = Journey.query.filter_by(id=journey_id).first()
	all_ratings = Ratings.query.filter_by(journey_id=journey_id).all()
	creator     = User.query.filter_by(id=journey.creator_id).first()
	new_rating            = Ratings()
	new_rating.journey_id = journey_id
	new_rating.user       = current_user.name
	new_rating.stars      = request.form.get('stars')
	new_rating.title      = request.form.get('title')
	new_rating.review     = request.form.get('review')
	localtime             = time.localtime(time.time())
	new_rating.time       = str(localtime[1])+"/"+str(localtime[2])+"/"+str(localtime[0])+" at "+str(localtime[3])+":"+str(localtime[4])
	db.session.add(new_rating)
	db.session.commit() # I had a bug with this line. The problem was that I did "new_rating.user = current_user" and current_user in an object, but in the DB it is defined as a String.
	return redirect(url_for('display_journey', journey_id=journey_id))


@app.route('/question/<int:journey_id>',  methods=['POST'])	
def question(journey_id):
	journey = Journey.query.filter_by(id=journey_id).first()
	creator = User.query.filter_by(id=journey.creator_id).first()
	new_question = Question()
	new_question.journey_id = journey_id
	new_question.user_id    = current_user.id
	new_question.title      = request.form.get('title')
	new_question.question    = request.form.get('question')
	localtime = time.localtime(time.time())
	new_question.time = str(localtime[1])+"/"+str(localtime[2])+"/"+str(localtime[0])+" at "+str(localtime[3])+":"+str(localtime[4])
	db.session.add(new_question)
	db.session.commit() #bug is here
	return redirect(url_for('display_journey', journey_id=journey_id))


@app.route('/answer/<int:question_id>', methods=['POST'])
def answer(question_id):
	question = Question.query.filter_by(id=question_id).first()
	journey = Journey.query.filter_by(id=question.journey_id).first()
	new_answer = Answer()
	new_answer.question_id = question_id
	new_answer.journey_id = question.journey_id
	new_answer.title = request.form.get('title')
	new_answer.answer = request.form.get('answer')
	localtime = time.localtime(time.time())
	new_answer.time = str(localtime[1])+"/"+str(localtime[2])+"/"+str(localtime[0])+" at "+str(localtime[3])+":"+str(localtime[4])
	db.session.add(new_answer)
	db.session.commit()
	return redirect(url_for('display_journey', journey_id=journey.id))


@app.route('/journey/<int:journey_id>')
def display_journey(journey_id):
	journey = Journey.query.filter_by(id=journey_id).first()
	print(journey.creator_id)
	creator = User.query.filter_by(id=journey.creator_id).first()
	all_ratings = Ratings.query.filter_by(journey_id=journey_id).all()
	all_questions = Question.query.filter_by(journey_id=journey_id).all()
	all_answers = Answer.query.filter_by(journey_id=journey_id).all()
	return render_template('journey.html', journey=journey, all_questions=all_questions, all_answers=all_answers, creator=creator, all_ratings=all_ratings)


@app.route('/notification/<int:st_id>', methods=['GET'])
@login_required
def display_notifications(st_id):
	all_notifications = Notification.query.filter_by(st_id=st_id)
	return render_template('notifications.html', all_notifications=all_notifications)


@app.route('/wishlist/<int:user_id>', methods=['GET'])
@login_required
def display_wishlist(user_id):
	all_wishes = Wishlist.query.filter_by(user_id=user_id).all()
	return render_template('wishlist.html', all_wishes=all_wishes)


if __name__ == "__main__":
	app.run()




# Ratings doesn't display