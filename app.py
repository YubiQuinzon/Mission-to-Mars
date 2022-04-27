# Importing libraries
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping # Importing the python file we created with all of the scraping functions

# Setting up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection

#tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Defining the route for the html page
# This function is what links our visual representation of our work, our web app, to the code that powers it.

@app.route("/")
def index():

    # Uses PyMongo to find the mars collection in the database
   mars = mongo.db.mars.find_one()

   # Return an HTML template using an index.html file
   return render_template("index.html", mars=mars) # mars=mars indicates to Python to use the 'mars' 


# Setting up scraping route
# This route will be the 'button' of the web application - scrape updated data when we tell it to 
@app.route("/scrape")

# access, scrape, update databases we pass in - end with a return message
def scrape():
   mars = mongo.db.mars # Assign a variable pointing to our mars database
   mars_data = scraping.scrape_all() # Assigning a variable that holds all the scraped data
   mars.update_one({}, {"$set":mars_data}, upsert=True) # updating the mars database with scraped data / upsert indicates to mongo to create a new doc if one doesnt exist already
   return redirect('/', code=302) # redirect us back to the homepage to where we can see the updated content


if __name__ == "__main__":
   app.run()