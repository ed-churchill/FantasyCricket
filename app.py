from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # download data here

    table_data = [("Ed Churchill", "Warwick"),
                ("Kacper", "Imperial"),
                ("Bronson Carrasco", "Essex"),
                ("Michael Roper-Cowley", "Bristol"),
                ("Alan Philip", "LSE"),
                ("James Morrison", "Oxford")]
    return render_template("index.html", users=table_data)

@app.route("/info")
def info():
    return render_template("info.html")


if __name__ == "__main__":
    app.run(debug=True)
