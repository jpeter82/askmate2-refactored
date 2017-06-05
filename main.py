from flask import Flask, request, render_template, url_for, redirect
import logic


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def index():
    return render_template('index.html', questions=logic.get_questions())


@app.route("/search", methods=['GET'])
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
