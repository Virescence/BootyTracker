from flask import *
from config import Config
import work
import forms
import os

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = forms.MerchantForm()

    if form.validate_on_submit():
        if any([form.pig_bool.data, form.chicken_bool.data, form.snake_bool.data, form.gunpowder_bool.data]):
            flash("We're going on an adventure from {} to {}!".format(form.starting_position.data,
                                                                      form.destination.data))
            return render_template('main.html', form=form, nav_messages=work.navigate(form.starting_position.data, form.destination.data, work.determineResources(form.pig_bool.data, form.chicken_bool.data, form.snake_bool.data, form.gunpowder_bool.data)))

        elif form.starting_position.data != form.destination.data:
            return render_template('main.html', form=form, nav_messages=work.navigateNoResources(form.starting_position.data, form.destination.data))

    print("nothing selected")
    return render_template('main.html', form=form)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'styles'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# if __name__ == "__main__":
    # app.run(host="0.0.0.0", threaded=True)