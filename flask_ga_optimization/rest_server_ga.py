from flask import Flask, jsonify, request, json
import two_bar_truss_GA as tbt
app = Flask(__name__)

# Simple server based Genetic Algorithm Optimization
# example call: http://127.0.0.1/ga?load=66&width=60
# This calls the GA optimization using load=66 and width=60
# The result is returned as a json file.

@app.route("/")
def index():
    return "Index page"
	
@app.route('/ga', methods=['GET'])
def ga():
    load = request.args.get('load') # Get load value
    width = request.args.get('width') # Get width value
    load = float(load.encode('ascii')) # Convert to float
    width = float(width.encode('ascii')) # Convert to float
    
    # Predefined values
    den = 0.3
    mod = 30000
    thick = 0.15

    # Create specification dictionary
    spec = {'density':den,'modulus':mod,'load':load,'width':width,'thickness':thick}
    
    # Optimize using GA to find best height/diameter to satisfy minimum weight 
    tt,weight,height,diam = tbt.run_ga(spec)

    # Return results as json file 
    return jsonify(weight=weight, height=height, diameter=diam, total_time=tt) 

if __name__ == "__main__":
	app.run(host='0.0.0.0')
