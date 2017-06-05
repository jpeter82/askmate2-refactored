from flask import Flask, request, render_template, url_for, redirect
import logic


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def index():
    pass


@app.errorhandler(404)
def page_not_found(error):
    return 'Oops, page not found!', 404


if __name__ == '__main__':
    app.run(debug=True)
