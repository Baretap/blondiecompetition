import sqlite3

def calculate_referral_points(referral_code, new_user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT id, points FROM users WHERE referral_code = ?', (referral_code,))
    referrer = c.fetchone()

    if not referrer:
        conn.close()
        return

    referrer_id, referrer_points = referrer
    c.execute('UPDATE users SET points = points + 10 WHERE id = ?', (referrer_id,))

    c.execute('SELECT referrer_id FROM users WHERE id = ?', (referrer_id,))
    tier2_referrer = c.fetchone()
    if tier2_referrer and tier2_referrer[0]:
        c.execute('UPDATE users SET points = points + 5 WHERE id = ?', (tier2_referrer[0],))

        c.execute('SELECT referrer_id FROM users WHERE id = ?', (tier2_referrer[0],))
        tier3_referrer = c.fetchone()
        if tier3_referrer and tier3_referrer[0]:
            c.execute('UPDATE users SET points = points + 2.5 WHERE id = ?', (tier3_referrer[0],))

    conn.commit()
    conn.close()
