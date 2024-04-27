from models import app
from routes import new_routes
app.register_blueprint(new_routes)


# Define a route and a view function
@app.route('/')
def hello():
    return 'Hello, World!'


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
