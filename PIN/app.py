from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("pages/index.html") 

@app.route("/learning")
def learning():
    return render_template("pages/learning_page.html") 

@app.route('/team')
def inteam():
    return render_template('pages/team.html')

@app.route('/contacts')
def contacts():
    return render_template('pages/contacts.html')

@app.route('/test')
def test():
    return render_template('pages/test_chinese.html')

if __name__ == "__main__":
    app.run(debug=True)