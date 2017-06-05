from flask import Flask, request, render_template, url_for, redirect
import logic


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')


@app.route('/')
@app.route('/list', strict_slashes=False)
def index():
    if request.path == '/':
        five = True
        link = None
        questions = logic.get_questions(None, five=True)
    else:
        five = False
        link = logic.generate_links(logic.url_helper(request.url))
        questions = logic.get_questions(request.args.items())
    return render_template('index.html', questions=questions, five=five, link=link)


@app.route('/search')
def search_questions():
    data = None
    search_phrase = request.args.get('q', None)
    if search_phrase is not None:
        data = logic.user_search(search_phrase)
    return render_template('search.html', search_phrase=search_phrase, data=data)


@app.errorhandler(404)
def page_not_found(error):
    return 'Oops, page not found!', 404


if __name__ == '__main__':
    app.run(debug=True)
