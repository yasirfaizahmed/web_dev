from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
  db.create_all()


class Drink(db.Model):
  def __init__(self, name):
    self.name = name
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))


@app.route("/")
def index():
  return "hello"


@app.route("/drinks", methods=["POST"])
def drinks():
  drink = Drink(name=request.json['name'])
  with app.app_context():
    db.session.add(drink)
    db.session.commit()
    return {"drink": drink.name}


if __name__ == '__main__':
  app.run()
