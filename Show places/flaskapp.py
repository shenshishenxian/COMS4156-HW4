from flask import Flask, render_template, abort


app = Flask(__name__)
class Scenic:
	def __init__(self, key, name, lat, lng):
		self.key = key
		self.name = name
		self.lat = lat
		self.lng = lng

scenics = {
	Scenic('NY', 'New York City', 40.730610, -73.935242)
	Scenic('PA', 'Paris',48.864716, 2.349014)
	Scenic('BJ','Beijing',39.913818	116.363625)
	Scenic('LD','London',51.508530	-0.076132)
}

scenic_by_key = {scenic.key: scenic for scenic in scenics}

@app.route("/")
def  index():
	return render_template('index.html',scenics = scenics)

@app.route("/<scenic_code>")
def show_scenic(scenic_code):
	scenic = scenic_by_key.get(scenic_code)
	if scenic:
		return render_template('map.html', scenic = scenic)
	else:
		abort(404)

app.run(debug = True)