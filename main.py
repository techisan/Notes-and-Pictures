# The starting point to launch the app

from website import create_app

app = create_app() #Call to create the app in the init function

if __name__ == '__main__': #If the call is from the main file then run the app
    app.run(debug=True)