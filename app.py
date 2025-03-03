from flask import Flask, render_template, redirect, url_for, session
from auth import register_user, login_user
from database import init_db, get_user_by_username
from points import calculate_referral_points
import sqlite3

app = Flask(__name__)  # Tässä määritellään app-objekti
app.secret_key = 'supersecretkey'

# Alusta tietokanta käynnistyksessä
init_db()

# Aloitussivu
@app.route('/')
def index():
    return render_template('index.html')

# Rekisteröityminen
@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_user()

# Sisäänkirjautuminen
@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_user()

# Käyttäjän pääsivu (dashboard)
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Profiilisivu
@app.route('/profile/<username>')
def profile(username):
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user_by_username(username)
    if user:
        # Laske referral-määrä (kutsutut käyttäjät)
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM users WHERE referrer_id = (SELECT id FROM users WHERE username = ?)', (username,))
        tier1_count = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM users WHERE referrer_id IN (SELECT id FROM users WHERE referrer_id = (SELECT id FROM users WHERE username = ?))', (username,))
        tier2_count = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM users WHERE referrer_id IN (SELECT id FROM users WHERE referrer_id IN (SELECT id FROM users WHERE referrer_id = (SELECT id FROM users WHERE username = ?)))', (username,))
        tier3_count = c.fetchone()[0]
        referral_count = tier1_count + tier2_count + tier3_count
        conn.close()

        return render_template('profile.html', user=user, referral_count=referral_count)
    return "User not found", 404

# Leaderboard
@app.route('/leaderboard')
def leaderboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    from database import get_leaderboard
    users = get_leaderboard()
    return render_template('leaderboard.html', users=users)

# Kirjaudu ulos
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
