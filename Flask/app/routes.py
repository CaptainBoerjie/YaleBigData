from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Random Text Random Text"