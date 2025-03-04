from flask import Flask, render_template, redirect, url_for, session
from auth import register_user, login_user
from database import init_db, get_user_by_username
from points import calculate_referral_points
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Alusta tietokanta käynnistyksessä
init_db()

# Funktio kävijämäärän tallentamiseen ja hakemiseen
def update_visitor_count():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Tarkista, onko visitor_count-taulu olemassa, jos ei, luo se
    c.execute('''CREATE TABLE IF NOT EXISTS visitor_count (id INTEGER PRIMARY KEY, count INTEGER)''')
    # Tarkista, onko laskurilla jo arvo
    c.execute("SELECT count FROM visitor_count WHERE id = 1")
    result = c.fetchone()
    if result is None:
        # Jos ei arvoa, alusta laskuri arvolla 0
        c.execute("INSERT INTO visitor_count (id, count) VALUES (1, 0)")
        count = 0
    else:
        count = result[0]
    # Kasvata laskuria yhdellä
    count += 1
    c.execute("UPDATE visitor_count SET count = ? WHERE id = 1", (count,))
    conn.commit()
    conn.close()
    return count

# Aloitussivu
@app.route('/')
def index():
    # Päivitä kävijämäärä ja hae nykyinen määrä
    visitor_count = update_visitor_count()
    return render_template('index.html', visitor_count=visitor_count)

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
