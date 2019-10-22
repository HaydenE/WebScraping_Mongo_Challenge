from flask import Flask, jsonify, render_template
import pymongo

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db




@app.route("/")
def home():
    data = list(db.data.find())
    print(data)

    return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)