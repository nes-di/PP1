import sqlite3

conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

cursor.execute('SELECT id, question, est_boss FROM questions WHERE theme="Culture Générale" ORDER BY id')
rows = cursor.fetchall()

print(f'Total: {len(rows)} questions\n')
for r in rows:
    print(f'ID {r[0]}: boss={r[2]} - {r[1][:60]}...')

conn.close()
