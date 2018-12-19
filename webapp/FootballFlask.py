from flask import Flask, render_template, request, session, flash
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator
from checker import check_logged_in

from DBcm import UseDatabase


app = Flask(__name__)
app.secret_key = 'YouWillNeverGuess'

app.config['dbconfig'] = {  'host':'127.0.0.1',
                            'user':'kevin',
                            'password':'pass',
                            'database':'test_football',}


@app.route('/setuser/<user>')
def setuser(user: str) -> str:
    session['user'] = user
    return 'User value set to ' + session['user']

@app.route('/getuser')
def getuser() -> str:
    return 'User value is currently set to: ' + session['user']

@app.route('/')
def hello() -> str:
    return render_template('/index.html')


@app.route('/logUserIn')
def log_user_in() -> 'html':

    return render_template('/login.html')


@app.route('/login', methods=['POST'])
def do_login() -> str:
    user_name = request.form['username']
    pass_word = request.form['password']

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """ SELECT username, password FROM users"""

        cursor.execute(_SQL)
        contents = cursor.fetchall()

    for row in contents:
        if row[0] == user_name:
            if row[1] == pass_word:
                titles = ('Username', 'Password')
                session['logged_in'] = True
                flash('You are now logged in')
                return render_template('/index.html',
                                        the_row_titles=titles,
                                        the_data=contents,)

    flash('Login details incorrect. Try again')
    return render_template('/index.html')

@app.route('/logout')
def do_logout() -> str:
    if 'logged_in' in session:
        session.pop('logged_in')
    flash('You are now logged out')
    return render_template('/index.html')


@app.route('/status')
def check_status() -> str:
    if 'logged_in' in session:
        flash('Login Status: You are logged in')
        return render_template('/index.html')
    flash('Login status: You are not logged in')
    return render_template('/index.html')


#def check_logged_in() -> bool:
#    if 'logged_in' in session:
#        return True
#    return False


@app.route('/page1')
@check_logged_in
def show_book_reviews() -> 'html':

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """SELECT home_team, away_team, home_goals, away_goals FROM results"""

        cursor.execute(_SQL)
        contents = cursor.fetchall()

    titles = ('Home Team', 'Away Team', 'Home Score', 'Away Score')

    return render_template('bookReviews.html',
                           the_title='Match Results',
                           the_row_titles=titles,
                           the_data=contents,)


@app.route('/page2')
@check_logged_in
def show_red_cards() -> 'html':

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """SELECT team, total_yel_card, total_red_card, season FROM stats"""

        cursor.execute(_SQL)
        contents = cursor.fetchall()

    titles = ('Team', 'Yellows', 'Reds', 'Season')

    return render_template('cards.html',
                           the_title='Disciplinary Record',
                           the_row_titles=titles,
                           the_data=contents,)


@app.route('/page3')
@check_logged_in
def show_united_wins() -> 'html':

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """ SELECT team, season, wins FROM stats WHERE team='Manchester United' """

        cursor.execute(_SQL)
        contents = cursor.fetchall()

    titles = ('Team', 'Season', 'Wins')

    return render_template('cards.html',
                           the_title='Wins',
                           the_row_titles=titles,
                           the_data=contents, )


@app.route('/showTem')
def show_team() -> 'html':

    return "Show Teams"


if __name__ == '__main__':
    app.run(debug=True)