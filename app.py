# from flask import Flask, render_template, redirect
# import pymongo
# import scrape_mars

# app = Flask(__name__)
# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)
# db = client.mars_db
# db.mars_db.drop()
# collection = mars_db['mars']
# collection.insert(mars_data)

# @app.route('/')
# def index():
#     try:
#         mars = db.mars_db.find_one()
#         return render_template('index.html', mars=mars)
#     except:
#         redirect("/scrape", code=302)


# @app.route('/scrape')
# def scrape():
#     mars = mongo.db.mars
#     mars_data = scrape_mars.scrape()
#     mars.update(
#         {},
#         mars_data,
#         upsert=True
#     )
#     return ''

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, redirect
import pymongo
import scrape_mars 
from flask_pymongo import PyMongo


app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def home():
    mars_data = mongo.db.mars_db.find_one()
    return  render_template('index.html', mars_data=mars_data)

@app.route("/scrape")
def scrape():
    mars_db = mongo.db.mars_db
    mars_scrape = scrape_mars.scrape()
    mars_db.update({}, mars_scrape, upsert=True)
    upsert=True
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)