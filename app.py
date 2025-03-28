from flask import Flask, request, render_template,Response,stream_with_context,jsonify
import subprocess
# from utils import generate_dork_query
from utils.dorking import generate_dork_query, generate_ai_powered_dork
from flask_cors import CORS
import re
app = Flask(__name__,template_folder='templates',static_folder='/',static_url_path='/')
CORS(app)

@app.route('/')
def greet():
	return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# --------------------------This code block belongs to subdomain enumeration -----------------------

@app.route('/subdomain_enum')
def subdomain_enum():
    return render_template('subdomain_enum.html')

@app.route('/start_scan', methods=['POST'])
def start_scan():
    domain = request.form.get('domain')
    if not domain:
        return "No domain provided", 400

    def run_scan(domain):
        """Generator function to yield live output of the subfinder command."""
        process = subprocess.Popen(
            ['subfinder', '-d', domain, '-silent'],  # Run subfinder command
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Stream output line by line
        for line in iter(process.stdout.readline, ''):
            yield  f"{line.strip()} \n"  

        process.stdout.close()
        process.wait()
        yield "[ SCAN COMPLETED ]\n\n"

    return Response(run_scan(domain), mimetype='text/event-stream')



# --------------------------This code block belongs to dorking -----------------------


@app.route('/generate_query', methods=['POST'])
def generate_query():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid input format"}), 400
    
    query = generate_dork_query(data)
    return jsonify({"query": query})


@app.route('/generate_ai_query', methods=['POST'])
def generate_ai_query():
    data = request.get_json()
    # if not isinstance(data, dict):
    #     return jsonify({"error": "Invalid input format"}), 400
    if(len(data.get("prompt",""))==0):
        return jsonify({"error": "Invalid input format"}), 400
    
    
    query = generate_ai_powered_dork(data)
    print(query.split(" $ "))
    return jsonify({"query": query})

# --------------------------------------------------------------------------------------------------

#this code belongs to google dorking

@app.route('/dorking')
def dorking():
    return render_template('dorking.html')



#----------------------------------------------------------------------------------------------------
@app.route('/network_scan')
def network_scan():
    return render_template('network_scan.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)

