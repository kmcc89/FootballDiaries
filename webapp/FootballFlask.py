from flask import Flask, render_template, request
#from flask_nav import Nav
#from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator
from DBcm import UseDatabase


app = Flask(__name__)

app.config['dbconfig'] = {  'host':'172.20.10.5',
                            'user':'kevin',
                            'port': '3306',
                            'password':'pass',
                            'database':'test_football',}



@app.route('/')
def hello() -> str:
    return 'Hello from football diary!'

@app.route('/about')
def viewabout() -> 'html':
    return render_template('aboutpage.html',)

@app.route('/login')
def viewlogin() -> 'html':
    return render_template('login.html',)

@app.route('/statstable')
def viewstatstable() -> 'html':
    return render_template('statstable.html',)

@app.route('/statsbar')
def viewstatsbar() -> 'html':
    return render_template('statsbar.html',)

@app.route('/statsgraph')
def viewstatsgraph() -> 'html':
    return render_template('statsgraph.html',)

@app.route('/statsQandA')
def viewstatsQandA() -> 'html':
    return render_template('statsQandA.html',)

@app.route('/statsmatches')
def viewstatsmatches() -> 'html':
    return render_template('statsmatches.html',)

@app.route('/viewResults')
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


@app.route('/viewRedCards')
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

@app.route('/unitedWins')
def show_united_wins() -> 'html':

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """ SELECT team, season, wins FROM stats WHERE team='Manchester United' """

        cursor.execute(_SQL)
        contents = cursor.fetchall()

    titles = ('Team', 'Season', 'Wins')

    return render_template('cards.html',
                           the_title='Wins',
                           my_name='Mike', )
app.run(debug=True)



