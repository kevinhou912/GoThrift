from flask import Flask, render_template, request, redirect,session
from google.auth.transport import requests
import google.oauth2.id_token
from firebase import firebase
from pyrebase import pyrebase
import dbInsert
import re


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'
firebase = firebase.FirebaseApplication('https://gothriftdb-default-rtdb.firebaseio.com/', None)
firebase_request_adapter = requests.Request()

pyrebaseconfig = {
    'apiKey': "AIzaSyCk8BXwGFhwIf2Ul18EdrNyWPwKisnHrAg",
    'authDomain': "gothriftdb.firebaseapp.com",
    'databaseURL': "https://gothriftdb-default-rtdb.firebaseio.com",
    'projectId': "gothriftdb",
    'storageBucket': "gothriftdb.appspot.com",
    'messagingSenderId': "432431784686",
    'appId': "1:432431784686:web:e9c25d2392188c0faa09ff",
    'measurementId': "G-8JLSP6PC2Z"
}

firebase_storage = pyrebase.initialize_app(pyrebaseconfig)
image_storage = firebase_storage.storage()
claims = {}

@app.route('/')
def root():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None

    if id_token:
        try:

            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            
            # Check if user is already there in the database or not
            users_data = firebase.get('/User', None)
            user_exists = False
            if users_data:
                for user in users_data:
                    if users_data[user]['user_email'] == claims['email']:
                        user_exists = True
                        session['user_id'] = user
                        session.modified = True
                        break

            # if user don't exist add it into the database
            if not user_exists:
                new_data = dbInsert.create_user_request(claims)
                firebase.post("/User", new_data)

                users_data = firebase.get('/User', None)
                if users_data:
                    for user in users_data:
                        if users_data[user]['user_email'] == claims['email']:
                            session['user_id'] = user
                            session.modified = True
                            break

            username = 'User'
            if claims:
                if 'name' in claims:
                    username = claims['name']

            session['username'] = username

            return render_template('Home.html',user_data=claims, error_message=error_message)

        except ValueError as exc:
            error_message = str(exc)


    return render_template(
        'index.html',
        user_data=claims, error_message=error_message)


@app.route('/Home')
def go_home():
    return render_template('Home.html')

@app.route('/Error')
def error():
    return render_template('Error.html')

@app.route('/Management')
def create_management():
    all_themes = firebase.get('/Theme', None)
    all_reports = firebase.get('/Report', None)
    user_themes = firebase.get('/User/' + session['user_id'] + '/Theme', None)
    user_reports = firebase.get('/User/' + session['user_id'] + '/reports', None)
    theme_data = dbInsert.get_user_subscribed_themes(all_themes,user_themes)
    report_data = dbInsert.get_user_reports(all_reports,user_reports)

    return render_template('Management.html', user_reports=report_data['user_reports'], user_theme=theme_data['subscribed_themes'])


@app.route('/CreateTheme')
def create_theme():        
    return render_template('CreateTheme.html')


@app.route('/CreateReport')
def create_report():
    all_themes = firebase.get('/Theme', None)
    theme_data = dbInsert.get_all_themes(all_themes)
    return render_template('CreateReport.html', Theme=theme_data['all_themes'])


@app.route('/SubmitTheme', methods=['GET', 'POST'])
def submit_theme():
    result_theme = firebase.get('/Theme', None)
    user_input = request.form['location']
    error_msg = "Your input location already exists"
    
    # Checking for theme if it already exists or not, if yeas throw an error message to user
    if result_theme:
        for theme in result_theme.values():
            cur_theme = user_input + '+'
            search_results = re.findall(str(cur_theme), theme['location'])
            if search_results:
                return render_template('CreateTheme.html', error_msg=error_msg)


    # If it doesn't exists create a new one
    if request.method == 'POST' and len(dict(request.form)) > 0:
        new_data = dbInsert.submit_theme_request(request,image_storage)
        firebase.post("/Theme", new_data)

        # save the theme in users subscribed themes too because when user creates a theme user is automatically
        # subscribed to it
        firebase.post('/User/' + session['user_id'] + '/Theme', new_data)
        return redirect("/ViewLocations")
    else:
        return redirect("/Error")

# show all the themes to User
@app.route('/ViewLocations')
def view_locations():
    all_themes = firebase.get('/Theme', None)
    user_themes = firebase.get('/User/' + session['user_id'] + '/Theme', None)
    data = dbInsert.get_user_subscribed_themes(all_themes, user_themes)
    return render_template('ViewAllTheme.html', Subscribed_themes=data['subscribed_themes'],
                           Unsubscribed_themes=data['unsubscribed_themes'])

# Call made when user click on a theme subscribe button
@app.route('/SubscribeTheme', methods=['GET', 'POST'])
def subscribe_theme():
    # If no , add this to user subscribed themes, fetch the them,e data from the request form
    if request.method == 'POST':
        new_data = dbInsert.subscribe_theme_request(request)
        firebase.post('/User/' + session['user_id'] + '/Theme', new_data)
        return redirect("/ViewLocations")
    else:
        return redirect("/Error")


@app.route('/UnsubscribeTheme/<key>', methods=['GET', 'POST'])
def unsubscribe_theme(key):
    user_themes = firebase.get('/User/' + session['user_id'] + '/Theme', None)
    key_for_unsubscribed_theme = dbInsert.unsubscribe_theme_request(request, user_themes,key)
    firebase.delete('/User/' + session['user_id'] + '/Theme', key_for_unsubscribed_theme)
    if request.method == 'POST':
        return redirect("/ViewLocations")
    else:
        return redirect("/Error")


@app.route('/SubmitReport', methods=['GET', 'POST'])
def submit_report():
    if request.method == 'POST' and len(dict(request.form)) > 0:
        all_themes = firebase.get('/Theme', None)
        new_data = dbInsert.submit_report_request(request,image_storage,all_themes)
        firebase.post("/Report", new_data)
        firebase.post('/User/' + session['user_id'] + '/reports', new_data)
        return redirect("/Search")
    else:
        return redirect("/Error")


@app.route('/Search')
def search():
    all_reports = firebase.get('/Report', None)
    data = dbInsert.get_reports(all_reports)
    return render_template('SearchReport.html', Report=data['all_reports'])

@app.route('/SearchReport', methods=['GET', 'POST'])
def search_report():
    result_reports = firebase.get('/Report', None)
    result_search_report = dbInsert.search_report_request(request, result_reports)
    searchText = "Showing search results for " + request.form['searchText']
    return render_template('SearchReport.html', Report=result_search_report, searchText=searchText)

@app.route('/Maps')
def map():
    all_reports = firebase.get('/Report', None)
    all_locations = dbInsert.get_locations(all_reports)
    return render_template('Maps.html', all_locations=all_locations)


@app.route('/ViewReport/<key>', methods=['GET', 'POST'])
def view_report(key):
    reports_list = firebase.get('/Report', None)
    return render_template('ViewReport.html', Report=reports_list[key])


@app.route('/ViewTheme/<key>', methods=['GET', 'POST'])
def view_theme(key):
    result = firebase.get('/Theme', None)
    reports_list = firebase.get('/Report', None)
    report_result = {}
    if reports_list:
        for report in reports_list:
            if reports_list[report]['theme_id'] == result[key]['id']:
                report_result[report] = reports_list[report]


    return render_template('ViewTheme.html', Theme=result[key], Reports=report_result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=True)
