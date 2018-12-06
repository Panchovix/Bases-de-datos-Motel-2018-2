from flask import Flask,redirect, url_for, request, render_template, flash
from forms import ContactForm
app = Flask(__name__)

 
@app.route('/home')
def home():		

	return render_template('index.html')

@app.route('/ingreso', methods=['GET', 'POST'])
def ingreso():
    if request.method == 'POST':
    	if request.form['submit']=='algo':

        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        	return redirect(url_for('home'))

    # show the form, it wasn't submitted
    return render_template('ingreso_cliente.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/cool_form', methods=['GET', 'POST'])
def cool_form():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('ingreso'))

    # show the form, it wasn't submitted
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug= True)