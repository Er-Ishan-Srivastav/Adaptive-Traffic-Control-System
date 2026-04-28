# Save as mock_node_b.py and run it
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/status')
def status():
    # Returns 0.9 (90% full) to simulate gridlock, or 0.2 (clear)
    # Change this number while the main script is running to see Intersection A react!
    return jsonify({"pressure": 0.2}) 

if __name__ == '__main__':
    app.run(port=5000)