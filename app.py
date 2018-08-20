"""
Allows navigating and score recording (in session) through
archery games:
`Liga 15/20/25m` and
`ścieżka łucznicza` (prepared for one in Las Osobowicki)
"""
import os
from flask import Flask, flash, render_template, request, redirect, \
                  session, url_for
from predefined_archery_games import LIGA, create_sciezka


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def home():
    """
    Lists and give access to all prepared archery games.

    :return: homepage
    """
    return render_template('homepage.html')


def store_prev_end_points(current_end_number):
    """
    Store points from previous end (round) as session variable.
    Key is string for that end number.

    :param current_end_number: int representing ordinal number
    for current game end
    :return: nothing
    """
    prev_end_score = int(request.form['points_for_end'])
    session[str(current_end_number - 1)] = prev_end_score


@app.route('/liga', methods=['GET', 'POST'])
def liga_page():
    """
    Allows navigating and score recording (in session) through each end
    of 'Liga 15/20/25m' up to results page. Allows redirecting to homepage
    at each step.

    :return: webpage for 'Liga 15/20/25m' end or results page if finished
    """
    global LIGA
    if request.method == 'POST' \
            and request.form['submit'] == 'następna seria >':
        session['current_end_number'] = int(request.form[
                                                'current_end_number']) + 1
        current_end_number = session['current_end_number']
        store_prev_end_points(current_end_number)
        session_results = [int(session[k]) for k in list(session.keys())
                           if k != 'current_end_number']
        result_so_far = sum(session_results)
        if current_end_number <= len(LIGA.ends):
            return render_template(
                'liga.html',
                current_end_number=current_end_number,
                current_end=LIGA.ends[current_end_number - 1],
                liga_points=LIGA.ends[
                    current_end_number - 1].end_scoring_list,
                result=result_so_far)
        else:
            return redirect(url_for('wyniki', result=result_so_far))
    else:
        session.clear()
        session['current_end_number'] = 1
        return render_template(
            'liga.html',
            current_end_number=session['current_end_number'],
            current_end=LIGA.ends[0],
            liga_points=LIGA.ends[0].end_scoring_list,
            result=0)


@app.route('/sciezka/menu', methods=['GET', 'POST'])
def sciezka_menu():
    """
    Defining `ścieżka łucznicza` parameters (distances, arrows number
    and scoring system). For distances at least one marker must be checked.

    :return: form page for choosing `ścieżka łucznicza` arguments
    """
    if request.method == 'POST' and request.form['submit'] == 'ZATWIERDŹ':
        pass
    return render_template('sciezka_menu.html')


@app.route('/sciezka', methods=['GET', 'POST'])
def sciezka_page():
    """
    Allows navigating and score recording (in session) through each end
    of 'ścieżka łucznicza' up to results page. Allows redirecting to homepage
    at each step.

    :return: webpage for 'ścieżka łucznicza' end or results page if finished
    """
    global sciezka
    if request.method == 'POST' \
            and request.form['submit'] == 'następna seria >':
        session['current_end_number'] = int(request.form
                                            ['current_end_number']) + 1
        current_end_number = session['current_end_number']
        store_prev_end_points(current_end_number)
        session_results = [int(session[k]) for k in list(session.keys())
                           if k != 'current_end_number']
        result_so_far = sum(session_results)
        if current_end_number <= len(sciezka.ends):
            return render_template(
                'sciezka.html',
                current_end_number=current_end_number,
                current_end=sciezka.ends[current_end_number - 1],
                sciezka_points=sciezka.ends[
                    current_end_number - 1].end_scoring_list,
                result=result_so_far
                )
        else:
            return redirect(url_for('wyniki', result=result_so_far))
    else:
        distances = request.form.getlist('marker')
        if not distances:
            flash('Nie wybrałeś/-aś żadnego palika')
            return render_template('sciezka_menu.html')
        arrows_number = int(request.form['arrows-number'])
        max_scoring_per_arrow = int(request.form['max-scoring-per-arrow'])
        sciezka = create_sciezka(
            distances, arrows_number, max_scoring_per_arrow
            )
        session.clear()
        session['current_end_number'] = 1
        return render_template(
            'sciezka.html',
            current_end_number=session['current_end_number'],
            current_end=sciezka.ends[0],
            sciezka_points=sciezka.ends[0].end_scoring_list,
            result=0)


@app.route('/wyniki', methods=['GET', 'POST'])
def wyniki():
    """
    Result page for finished archery game. Allows redirecting to homepage.

    :return: results page
    """
    return render_template('results.html', result=request.args.get('result'))


if __name__ == '__main__':
    app.run(debug=True)