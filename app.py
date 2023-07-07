from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello():
    conn = sqlite3.connect('hello.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS greetings (message text)')
    c.execute('INSERT INTO greetings VALUES ("Hello World")')
    conn.commit()
    c.execute('SELECT message FROM greetings')
    result = c.fetchone()
    conn.close()

    
    html = f"""
    <html>
    <head>
        <style>
            body {{
                background-color: #16a085;
                font-family: Arial, sans-serif;
                text-align: center;
            }}
            h1 {{
                color: #be2edd;
                margin-top: 100px;
            }}
        </style>
    </head>
    <body>
        <h1>{result[0]}</h1>
    </body>
    </html>
    """

    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
