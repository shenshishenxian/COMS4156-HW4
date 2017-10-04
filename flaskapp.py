from flask import Flask, render_template, abort, jsonify, request
from sqlalchemy import *
from flask import Flask, request, render_template, g, redirect, Response
import traceback
from mst import Graph, Vertex, Edge
import re

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
scenic_by_coords = {'(scenic.lat, scenic.lng)': scenic for scenic in scenics}


@app.before_request
def before_request():
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

@app.route("/_findroute")
def findroute():
    username = request.args.get('a', 0, type=str)
    coordinates = request.args.get('b', 0, type=str)
    graph = Graph()
    order_num = 0
    coordinates = coordinates.split(';')
    coordinates = list(filter(None, coordinates))

    scenic = scenic_by_coords.get(coordinates[0])
    for location in coordinates:
        latlong = re.split(r'[(,)\s]+', location)
        latlong = list(filter(None, latlong))
        order_num += 1
        v = Vertex('location' + str(order_num), latlong[0], latlong[1])
        graph.vertices['location' + str(order_num)] = v
     
    for source in graph.vertices:
        for target in graph.vertices:
            if source != target:
                graph.add_edge(source, target, 1)

    first_stop = 'location' + '1'
    new_graph = graph.get_min_spanning_tree(first_stop)
    new_graph.preorder(new_graph.vertices[first_stop])
    save_route(username, new_graph.route)
    return render_template('map.html', scenic = scenic)
   
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

def save_route(user, route_stops):
    cur = g.conn.execute('SELECT user_id FROM map_user WHERE username = \'%s\'' % (user))
    row = cur.fetchone()
    if not row:
        cur = g.conn.execute('INSERT INTO map_user (username) VALUES (\'%s\') RETURNING user_id' % (user))
        user_id = cur.fetchone()[0]
    else:
        user_id = row['user_id']
    
    cur = g.conn.execute('INSERT INTO user_route (user_id) VALUES (\'%s\') RETURNING route_id' % (user_id))
    route_id = cur.fetchone()[0]

    ordernum = 0
    for route in route_stops:
        ordernum += 1
        cur = g.conn.execute('INSERT INTO location (name, latitude, longitude) VALUES (\'%s\', \'%s\', \'%s\') RETURNING location_id' % (route.name, route.latitude, route.longitude))
        location_id = cur.fetchone()[0]
        cur = g.conn.execute('INSERT INTO route_location_link (route_id, location_id, order_num) VALUES (\'%s\', \'%s\', \'%s\')' % (route_id, location_id, ordernum))
    print_new_route(user, route_stops)
    return 0

def print_new_route(user, route_stops):
    print '\nNew saved route for ' + user + ':'
    stop = ""
    for route in route_stops:
        stop += route.name + '(' + route.latitude + ',' + route.longitude + ')'
        if route != route_stops[-1]:
            stop += " -> "
    print stop + '\n'

app.run(debug = True)
