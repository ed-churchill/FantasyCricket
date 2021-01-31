from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    
    table_data = [("Ed", 20, "Warwick"), 
    ("Alan", 20, "LSE"), 
    ("Kacper", 20, "Imperial"), 
    ("Bronson", 21, "Essex"), 
    ("James", 21, "Oxford"), 
    ("Michael", 20, "Bristol")]
    return render_template("index.html", users=table_data)

@app.route("/info")
def info():
    return render_template("info.html")


if __name__ == "__main__":
    app.run(debug=True)
