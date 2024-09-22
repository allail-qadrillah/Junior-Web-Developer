from flask import Blueprint, redirect, url_for, session, render_template, request, flash

# Create a Blueprint for the authentication routes
auth = Blueprint('auth', __name__)

# * Route endpoint login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # check username and password is correct and set as role session
        if username == 'cashier' and password == 'cashier':
            session['role'] = 'Cashier'
        elif username == 'admingudang' and password == 'admingudang':
            session['role'] = 'Admin Gudang'
        elif username == 'superadmin' and password == 'superadmin':
            session['role'] = 'Super Admin'
        else:
            return redirect(url_for('auth.login'))

        return redirect(url_for('main.products'))

    return render_template('login.html')

# * Route endpoint logout
@auth.route('/logout')
def logout():
    # remove role session
    session.pop('role', None)
    return redirect(url_for('main.index'))
