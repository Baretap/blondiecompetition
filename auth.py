from flask import request, redirect, url_for, render_template, session, flash
import base64
import uuid
import sqlite3
from database import add_user, get_user_by_referral_code
from points import calculate_referral_points

def register_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        profile_pic = request.files['profile_pic']
        referrer_code = request.form.get('referrer_code', '')

        referral_code = str(uuid.uuid4())[:8]
        profile_pic_data = base64.b64encode(profile_pic.read()).decode('utf-8')

        try:
            user_id = add_user(username, email, password, profile_pic_data, referral_code)

            if referrer_code:
                calculate_referral_points(referrer_code, user_id)
                referrer = get_user_by_referral_code(referrer_code)
                if referrer:
                    referrer_id = referrer[0]
                    conn = sqlite3.connect('users.db')
                    c = conn.cursor()
                    c.execute('UPDATE users SET referrer_id = ? WHERE id = ?', (referrer_id, user_id))
                    conn.commit()
                    conn.close()
        except sqlite3.IntegrityError:
            flash("Käyttäjänimi tai sähköposti on jo käytössä.")
            return render_template('register.html')

        return redirect(url_for('login'))
    return render_template('register.html')

def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT username, password FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()

        if user and user[1] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Virheellinen käyttäjänimi tai salasana.")
            return render_template('login.html')
    return render_template('login.html')
