from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from bengaluru_station_finder import BengaluruStationFinder
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize the station finder
station_finder = BengaluruStationFinder()

def clean_for_json(obj):
    """Clean data for JSON serialization by handling NaN values"""
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(item) for item in obj]
    elif isinstance(obj, float) and (obj != obj):  # Check for NaN
        return None
    else:
        return obj

@app.route('/')
def index():
    """Serve the main page"""
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    return render_template('bengaluru_index.html', api_key=api_key)

@app.route('/find_routes', methods=['POST'])
def find_routes():
    """Find multi-modal routes between two addresses"""
    try:
        data = request.get_json()
        
        # Get coordinates directly from frontend
        initial_lat = data.get('initial_lat')
        initial_lng = data.get('initial_lng')
        dest_lat = data.get('dest_lat')
        dest_lng = data.get('dest_lng')
        initial_address = data.get('initial_address', 'Unknown')
        dest_address = data.get('dest_address', 'Unknown')
        
        if not all([initial_lat, initial_lng, dest_lat, dest_lng]):
            return jsonify({'error': 'Coordinates are required'}), 400
        
        print("\n" + "=" * 80)
        print("🚀 BENGALURU METRO JOURNEY PLANNER - NEW REQUEST")
        print("=" * 80)
        print(f"📍 Route Request:")
        print(f"   From: '{initial_address}'")
        print(f"   To: '{dest_address}'")
        print(f"   Origin Coordinates: ({initial_lat:.6f}, {initial_lng:.6f})")
        print(f"   Destination Coordinates: ({dest_lat:.6f}, {dest_lng:.6f})")
        
        # Find nearest metro stations
        print("\n" + "=" * 80)
        print("🎯 STEP 1: FINDING NEAREST METRO STATIONS")
        print("=" * 80)
        initial_stations = station_finder.find_nearest_stations(initial_lat, initial_lng, top_n=7)
        dest_stations = station_finder.find_nearest_stations(dest_lat, dest_lng, top_n=7)
        
        print(f"\n✅ Station Discovery Complete:")
        print(f"   • {len(initial_stations)} nearest stations to origin")
        print(f"   • {len(dest_stations)} nearest stations to destination")
        
        # Calculate all taxi legs and get convenience routes
        taxi_results = station_finder.calculate_all_taxi_legs(
            initial_lat, initial_lng, dest_lat, dest_lng, 
            initial_stations, dest_stations
        )
        
        # Get the convenience routes and direct taxi suggestion
        convenience_routes = station_finder.get_convenience_routes()
        direct_taxi_suggestion = station_finder.get_direct_taxi_suggestion()
        
        print(f"\n" + "=" * 80)
        print("✅ REQUEST COMPLETE - RETURNING RESULTS TO USER")
        print("=" * 80)
        print(f"🏆 Returning {len(convenience_routes)} top convenience routes to frontend")
        if direct_taxi_suggestion:
            print(f"🚕 Direct taxi suggestion: {'SUGGESTED' if direct_taxi_suggestion['suggest'] else 'NOT SUGGESTED'}")
        
        response = {
            'status': 'success',
            'convenience_routes': convenience_routes,
            'direct_taxi_suggestion': direct_taxi_suggestion
        }
        
        return jsonify(clean_for_json(response))
        
    except Exception as e:
        print(f"❌ Error in find_routes: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚇 Starting Bengaluru Metro Journey Planner...")
    print("📍 Server will be available at: http://localhost:5002")
    app.run(debug=True, host='0.0.0.0', port=5002)
