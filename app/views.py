#These 5 lines imports all the necessary libraries required in this file
from flask import render_template, flash, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, models
from .forms import *
import logging

#This is the intitial route that is first loaded
@app.route('/', methods=['GET', 'POST'])
def Home():
	logging.info('Home page route request')
	if session.get('logged_in') == True: #Checks if the user is already logged in
		logging.debug('User already logged in')
		return redirect("/Dashboard") #If the user is already logged in, then it redirects to the users dashboard
	logging.debug('User not logged in')
	return render_template('Home.html',
						   title='Home Page',
						   Home=Home)

#This is the route to the Login webpage
@app.route('/Login', methods=['GET', 'POST'])
def Login():
	logging.info('Login page route request')
	form = LoginForm() #Assigns the login form
	if form.validate_on_submit(): #Checks if the form is submitted
		username1 = request.form['username'] #Stores username from form
		password1 = request.form['password'] #Stores password from form
		temp = (db.session.query(models.Account).filter_by(username=username1).first()) #Stores users details
		if temp:
			if check_password_hash(temp.password, password1): #Checks the password entered to the password in the database
				session['logged_in'] = True	#Session set so that the user is kept logged in
				session['current_id'] = temp.id
				session['username'] = username1
				session['password'] = password1
				logging.debug('User login successful')
				return redirect("/Dashboard") #Redirects the user to the Dashboard webpage
			else:
				flash("Incorrect user details") #Alerts the user the login details are wrong
				logging.debug('User login unsuccessful')
				return redirect("/Login") #Redirects the user to the Login webpage
		else:
			flash("Incorrect user details") #Alerts the user the login details are wrong
			logging.debug('User login unsuccessful')
			return redirect("/Login") #Redirects the user to the Login webpage
	return render_template('Login.html',
						   title='Login Page',
						   Login=Login,
						   form=form)

#This route logs the user out of their account
@app.route('/Logout/', methods=['GET', 'POST'])
def Logout():
	logging.info('Logout route request')
	session['logged_in'] = False #Session set to flase so user is no longer signed in
	logging.debug('User logout successful')
	return redirect("/") #redirects to the inital webpage
	return render_template('Logout.html',
						   title='Logout Page',
						   Logout=Logout)

#This is the route to the Register webpage
@app.route('/Register', methods=['GET', 'POST'])
def Register():
	logging.info('Register page route request')
	form = RegisterForm() #Assigns the Register form
	if form.validate_on_submit(): #Checks if the form is submitted
		username1 = request.form['username'] #Stores username from form
		password1 = request.form['password'] #Stores password from form
		first_name = request.form['first_name'] #Stores first name from form
		last_name = request.form['last_name'] #Stores last name from form
		number = request.form['number'] #stores phone number from form
		email = request.form['email'] #Stores email from form
		password1 = generate_password_hash(password1, "sha256") #Hashes the password
		exists = db.session.query(models.Account.username).filter_by(username=username1).first() #Checks if a user with the same username exists already
		if exists == None: #Checks if a user with the username exists
			record = models.Account(username1, password1, first_name, last_name, number, email) #Stores all the fields above into a record
			db.session.add(record) #Adds the record to the database
			db.session.commit()	#Commits any changes that are made to the database
			flash("User Register Successful") #Alerts the user the register is successful
			logging.debug('User register successful')
			return redirect("/Register") #redirects to the register webpage
		else:
			logging.debug('User register unsuccessful')
			flash("User Register Unsuccessful") #Alerts the user the register is unsuccessful
			return redirect("/Register")  #redirects to the register webpage
	return render_template('Register.html',
						   title='Register Page',
						   Register=Register,
						   form=form)

#This is the route to the users Dashboard webpage
@app.route('/Dashboard', methods=['GET', 'POST'])
def Dashboard():
	logging.info('Dashboard page route request')
	form = PasswordForm() #Assigns the password change form
	assessment = models.Account.query.filter_by(username=session.get('username')).first() #Retrieves details on the user
	if form.validate_on_submit(): #Checks if the form is submitted
		password_change1 = request.form['password_change1'] #Stores the new password from form
		password_change2 = request.form['password_change2'] #Stores the confirmation of the new passsword from form
		if (password_change1 != password_change2): #Checks if the passswords are not the samae
			logging.debug('User password change unsuccessful')
			flash("Passwords are not the same") #Alerts the user the passwords dont match
		else:
			logging.debug('User password change successful')
			assessment.password = generate_password_hash(password_change1, "sha256") #Hashes the password adn stores it in the database
			db.session.commit()
			session['password'] = password_change1 #Resets the session password
			flash("Password change successful") #Alerts the user the password change was successful
		return redirect("/Dashboard")
	return render_template('Dashboard.html',
						   title='Dashboard Page',
						   assessment=assessment,
						   Dashboard=Dashboard,
						   form=form)

#This is the route for the Reading List webpage
@app.route('/ReadingList', methods=['GET', 'POST'])
def ReadingList():
	book = models.Books.query.filter_by(account_id=session.get('current_id'), status="Uncomplete").all() #This stores all the book entries that have been marked as uncomplete, that the user has added
	logging.info('Reading List page route request')
	return render_template('ReadingList.html',
						   title='ReadingList Page',
						   ReadingList=ReadingList,
						   book=book)
#This is the route to move a book from the reading list to the read books list
@app.route('/ReadingList/<int:id>', methods=['POST', 'GET'])
def update(id):
	logging.debug('Moving book from reading list to read list')
	book_to_update = models.Books.query.get_or_404(id) #This stores the entry for the id that has been passed to this route
	book_to_update.status = 'Complete' #This then updates the status to complete for the id that was passed here
	db.session.commit() #Commits any changes that have been made to the database
	return redirect('/ReadingList') #Redirects to the Reading List webpage

#This is the route for the Read Books List webpage
@app.route('/ReadList', methods=['GET', 'POST'])
def ReadList():
	book = models.Books.query.filter_by(account_id=session.get('current_id'), status='Complete').all() #This stores all the book entries that have been marked as complete, that the user has added
	logging.info('Read Books page route request')
	return render_template('ReadList.html',
						   title='ReadList Page',
						   ReadList=ReadList,
						   book=book)
#This is the route for the Add Books webpage
@app.route('/AddBook', methods=['GET', 'POST'])
def AddBook():
	logging.info('Add Books page route request')
	form = AddBookForm() #Add Book Form
	if form.validate_on_submit(): #Checks if the form has been submitted
		account = session.get('current_id') #Stores the id
		name = request.form['title'] #Stores the title from form
		author = request.form['author'] #Stores the author from form
		status = "Uncomplete" #Stores the status of the book
		record = models.Books(name, author, status, account_id=account) #Stores the variables in the database
		db.session.add(record) #Adds the record to the database
		db.session.commit()	#Commits any changes that are made to the database
		logging.debug('Book added to reading list')
		flash('Book Added')
	return render_template('AddBook.html',
						   title='Add Book Page',
						   AddBook=AddBook,
						   form=form)

@app.route('/AddReview', methods=['GET', 'POST'])
def AddReview():
	logging.info('Add Reviews page route request')
	form = AddReviewForm() #Add Review Form
	if form.validate_on_submit(): #Checks if the form has been submitted
		account = session.get('current_id') #Stores the id
		title = request.form['title'] #Stores the title from form
		author = request.form['author'] #Stores the author from form
		book_name = request.form['book_name'] #Stores the book name from form
		description = request.form['description'] #Stores the description from form
		record = models.Reviews(title, book_name, author, description, poster_id=account) #Stores the variables in the database
		db.session.add(record) #Adds the record to the database
		db.session.commit()	#Commits any changes that are made to the database
		logging.debug('Review added')
		flash('Review Added') #Alerts the user that the review has been added
	return render_template('AddReview.html',
						   title='Add Review Page',
						   AddReview=AddReview,
						   form=form)

#This is the route for the Review webpage
@app.route('/Review', methods=['GET', 'POST'])
def Review():
	reviews = models.Reviews.query.all() #Stores all the reviews made
	logging.info('Books Review page route request')
	return render_template('Review.html',
						   title='Review Page',
						   Review=Review,
						   reviews=reviews)

#This is the route for the Notes webpage
@app.route('/Notes', methods=['GET', 'POST'])
def Notes():
	logging.info('Notes page route request')
	return render_template('Notes.html',
						   title='Notes Page',
						   Notes=Notes)
