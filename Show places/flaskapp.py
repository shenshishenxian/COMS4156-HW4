from flask import Flask, render_template, abort
from sqlalchemy import *
from flask import Flask, request, render_template, g, redirect, Response
import traceback
from mst import Graph, Vertex, Edge

DATABASEURI = "postgresql://fortytwo:coms4156@coms4156instance.cf4dw5ld7jgf.us-east-2.rds.amazonaws.com:5432/ToyComs4156"
engine = create_engine(DATABASEURI)

app = Flask(__name__)
class Scenic:
    def __init__(self, key, name, lat, lng):
        self.key = key
        self.name = name
        self.lat = lat
        self.lng = lng

scenics = {
    Scenic('NY', 'New York City', 40.730610, -73.935242),
    Scenic('PA', 'Paris',48.864716, 2.349014),
    Scenic('BJ','Beijing',39.913818 ,116.363625),
    Scenic('LD','London',51.508530  ,-0.076132)
}

scenic_by_key = {scenic.key: scenic for scenic in scenics}


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass


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

@app.route("/calculate_route", methods=['POST'])
def calculate_route(city, destinations):
    # order = 0
    # for location in destinations:
    #     location_id = g.conn.execute('INSERT INTO locations (name,latitude,longitude) VALUES (%s, %s, %s)', city, location[0],location[1])
    #     order += 1
    #     g.conn.execute('INSERT INTO user_route (user_id) VALUES (%s)', user)

    graph = Graph()
    order_num = 0
    for location in destinations:
        order_num += 1
        v = Vertex(city + str(order_num), location[0], location[1])
        graph.vertices[city + str(order_num)] = v
       
        for source in graph.vertices:
            for target in graph.vertices:
                if source != target:
                    graph.add_edge(source, target, 1)

    new_graph = graph.get_min_spanning_tree(city + '1')
    new_graph.preorder(city + '1')
    print new_graph.route
    # else:
    #     abort(404)

app.run(debug = True)
