from travel.app import app
from travel.routes import init_routes

init_routes()

app.run(host="127.0.0.1", port=5002)

