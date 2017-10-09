from flask_rest_api.application import create_app
app = create_app('development')

app.run(debug=True)
