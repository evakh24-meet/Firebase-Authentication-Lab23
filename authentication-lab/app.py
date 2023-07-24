from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


Config = {
  'apiKey': "AIzaSyCdbFquN1JD0JFnZYi3Ej116igL7mHMDVs",
  'authDomain': "login-8a60e.firebaseapp.com",
  'projectId': "login-8a60e",
  'storageBucket': "login-8a60e.appspot.com",
  'messagingSenderId': "1015332372204",
  'appId': "1:1015332372204:web:446ba761bc83cf93eeafc9",
  'measurementId': "G-95K839TLCK",
  'databaseURL':'https://login-8a60e-default-rtdb.europe-west1.firebasedatabase.app/'
};

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            return render_template('signin.html')
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'email': email, 'password': password, 'full_name':full_name, 'username':username, 'bio':bio}
            db.child('Users').child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except:
            return render_template('signup.html')
    
    return render_template("signup.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == "POST":
        UID = login_session['user']['localId']
        text = request.form['text']
        title = request.form['title']
        try:
            tweet = {'text': text, 'title':title, 'UID':UID}
            print(UID)
            db.child('Tweets').push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            print("ERROR IN ADD TWEET :(")
    return render_template("add_tweet.html")

@app.route('/all_tweets', methods = ['GET', 'POST'])
def all_tweets():
    show_tweets = db.child('Tweets').get().val()
    return render_template('all_tweets.html', show = show_tweets)

if __name__ == '__main__':
    app.run(debug=True)
