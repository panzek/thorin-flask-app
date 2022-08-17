# Step 1 – Create a flask app to render the main template 
# Step 2 – Create HTML Files

#1. IMPORTING
# importing os from the standard Python library
# importing Flask class and render_template() function from Flask
#The capital F indicates that it's a class name, so it's important to use a capital F here.
# render_template helps render our HTML
import os
import json
from flask import Flask, render_template, request, flash 
if os.path.exists("env.py"): #we only want to import env, if the system can find env.py file
    import env
# Once we save above, a new directory called 'pycache' is created.
# We don't need to bother push this to GitHub either, so we go add it to our .gitignore file: __pycache__/

#2. SETTING UP THE APPLICATION
# Next, we create an instance of this class and store it in a variable called 'app'.
# In Flask, the convention is that our variable is called 'app'.
# The first argument of the Flask class is the name of the application's module - our package.
# Since we're just using a single module, we can use __name__ which is a built-in Python variable.
# Flask needs this so that it knows where to look for templates and static files.
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

#2. MAKING ROUTE - ROUTING
# we use the app.route decorator to tell Flask what URL should trigger the function that follows.
# In Python, a decorator starts with the @ symbol, which is also called pie-notation. 
# Effectively, a decorator is a way of wrapping functions. 
# When we try to browse to the root directory, as indicated by the "/", then Flask triggers 
# the index function underneath and returns the "Hello, World" text.
@app.route("/")
def index(): #bind a new view to the route
    return render_template("index.html") #renders index.html template
    #instead of returning text, I'm going to return render_template("index.html").


@app.route("/about")
def about():
    data = []
    with open("data/company.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("about.html", page_title="About", company=data) 


@app.route("/about/<member_name>")
def about_member(member_name):
    with open("data/company.json") as json_data:
        data = json.load(json_data)
        for obj in data:
            if obj["url"] == member_name:
                member = obj
    return render_template("member.html", member=member) 
    #In 2n argument, first 'member' is the variable name being passed through into our html file.
    #The second 'member' is the member object we created above on line 24.


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # print(request.form.get("name")) //cos this is a dictionary, we can use a standard Python get() method of accessing the keys for that dictionary.
        # print(request.form["email"]) // alternatively, using square brackets, and not using the .get() method.
        flash("Thanks {}, we have received your message!".format(
            request.form.get("name")))
    return render_template("contact.html", page_title="Contact") 
    #page_title="Contact" is used to set data on our server-side, and get it to come through onto the client-side.

#3. RUNNING THE APPLICATION
#So far, this isn't enough to get our application running, so we need to add some extra functionality to do that.
#We can "import os" from the standard Python library, and then we're going to reference this built-in variable and say that:
if __name__ == "__main__": #The word 'main' wrapped in double-underscores (__main__) is the name of the default module in Python.
    app.run( # run our app with the following arguments.
        host=os.environ.get("IP", "0.0.0.0"), #using the os module from the standard library to get the 'IP' environment variable if it exists, but set a default value if it's not found.
        port=int(os.environ.get("PORT", "5000")), #same with 'PORT', but this time, we cast it as an integer, and set that default to "5000", a common port used by Flask.
        debug=True) #allow us to debug our code much easier during the development stage.

# run "python3 run.py" in the Terminal to start our Flask app.