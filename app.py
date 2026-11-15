import sqlite3

DB = "base.db"

 
def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT NOT NULL UNIQUE) """)
    cur.execute(""" CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, contenu TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id)) """)
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(""" SELECT users.nom, messages.contenu FROM messages JOIN users ON messages.user_id = users.id ORDER BY messages.id DESC """).fetchall()
    conn.close()
    return rows

def get_users():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return rows

 
def add_user(nom):
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO users (nom) VALUES (?)", (nom,))
    conn.commit()
    conn.close()

def add_message(user_id, contenu):
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO messages (user_id, contenu) VALUES (?, ?)", (user_id, contenu))
    conn.commit()
    conn.close()

 
def create_conversation(titre):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO conversations (titre) VALUES (?)", (titre,))
    conn.commit()
    new_id = cur.lastrowid   
    conn.close()
    return new_id

 
def get_messages_by_conversation(conversation_id):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT users.nom, messages.contenu
        FROM messages
        JOIN users ON messages.user_id = users.id
        WHERE messages.conversation_id = ?
        ORDER BY messages.id ASC
    """, (conversation_id,)).fetchall()
    conn.close()
    return rows

def get_all_conversations():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM conversations").fetchall()
    conn.close()
    return rows

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
     
    cur.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL
        )
    """)
  
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            contenu TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    add_user("Ahmed")
    add_message(1, "Salam, hedha awel message")
    for m in get_messages():
        print(m["nom"], ":", m["contenu"])