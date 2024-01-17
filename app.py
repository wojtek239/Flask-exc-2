from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = 'notes.db'


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


create_table()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Note added successfully'}), 201

    return render_template('index.html')


@app.route('/add_note', methods=['POST'])
def add_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if title and content:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Note added succesfully'}), 201
    else:
        return jsonify({'error': 'Enter title and text for note'}), 400


@app.route('/delete_note/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Note deleted succesfully'}), 200


@app.route('/get_notes', methods=['GET'])
def get_notes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    conn.close()

    notes_list = [{'id': note[0], 'title': note[1], 'content': note[2]} for note in notes]
    return jsonify({'notes': notes_list})


@app.route('/edit_note/<int:note_id>', methods=['PUT'])
def edit_note(note_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if title and content:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('UPDATE notes SET title=?, content=? WHERE id=?', (title, content, note_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Note updated succesfully'}), 200
    else:
        return jsonify({'error': 'Enter title and text for note'}), 400


if __name__ == '__main__':
    app.run(debug=True)
