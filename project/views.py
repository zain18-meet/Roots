from flask import render_template, request, Flask, session, redirect, url_for
from flask import session as login_session
from flask_login import login_required
from . import app, db

from project.models import Journey, User

@app.route('/browse')
def browse():
	user_id = session['user_id']
	current_user = User.query.filter_by(id=user_id).first()
	all_journeys = Journey.query.all()
	return render_template('browse.html', all_journeys=all_journeys, current_user=current_user)

@app.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
	user_id = session['user_id']
	user = User.query.filter_by(id=user_id).first()
	print(user.name)
	user_info = User.query.filter_by(id=request.form.get('user_id')).first()
	if request.method=='POST':
		user_info.country = request.form.get('country')
		user_info.profession = request.form.get('profession')
		user_info.birthday = request.form.get('birthday')
		user_info.city = request.form.get('city')
		user_info.number = request.form.get('number')
		user_info.is_storyteller = True
		db.session.add(user_info)
		db.session.commit()
		return render_template('st_profile.html', current_user=user, user=user_info, is_user=True)
	else:
		if user.is_storyteller==True:
			return render_template('st_profile.html', current_user=user, user=user_info, is_user=True)
		else:
			return render_template('apply.html', current_user=user)


@app.route('/profile/<int:user_id>')
def profile(user_id):
	user=User.query.filter_by (id=user_id).first()
	is_user=False
	current_user_id = session['user_id']
	current_user = User.query.filter_by(id=current_user_id).first()
	if user.id==current_user.id:
		is_user=True
	if user.is_storyteller==True:
		print('i am here!!!!!!!!!')
		st_journeys = Journey.query.filter_by(creator_id=user_id).all()
		print(st_journeys)
		return render_template('st_profile.html', user=user, is_user=is_user, current_user=current_user,st_journeys=st_journeys, is_storyteller=True)
	else:
		return render_template('profile.html',user=user, is_user=is_user, current_user=current_user, is_storyteller=False)




@app.route('/add_journey', methods=['GET', 'POST'])
@login_required
def add_journey():
	user_id = session['user_id']
	user = User.query.filter_by(id=user_id).first()
	if request.method=='POST':
		new_journey = Journey()
		new_journey.creator_id = request.form.get('user_id')
		print('session user id--->', user_id)
		print('request form user id --->', request.form.get('user_id'))
		new_journey.title = request.form.get('title')
		new_journey.description = request.form.get('description')
		new_journey.location  = request.form.get('location')
		new_journey.duration  = request.form.get('duration')
		new_journey.category  = request.form.get('category')
		new_journey.requirements  = request.form.get('requirements')
		new_journey.people_range  = request.form.get('people_range')
		new_journey.price  = request.form.get('price')
		new_journey.picture  = request.form.get('picture')
		db.session.add(new_journey)
		db.session.commit()
		return render_template('journey.html', journey=new_journey, current_user=user, creator=user)
	else:
		return render_template('add_journey.html', current_user=user)






@app.route('/journeys/<int:journey_id>')
def display_journey(journey_id):
        journey = Journey.query.filter_by(id=journey_id).first()
        creator = User.query.filter_by(id=journey.creator_id).first()
        print('creator ---->', creator)
        return render_template('journey.html', journey=journey, creator=creator)




@app.route('/about')
def about():
	return render_template("about.html")





if __name__ == "__main__":
	app.run()
