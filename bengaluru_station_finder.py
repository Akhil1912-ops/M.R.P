import math
import os
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from bengaluru_metro_stations import STATION_COORDINATES, METRO_LINES
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BengaluruStationFinder:
    def __init__(self):
        self.stations = STATION_COORDINATES
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY not found in .env file")
        self.base_url = "https://maps.googleapis.com/maps/api"
        
        # Load metro data
        self.metro_data = self.load_metro_data()
    
    def load_metro_data(self):
        """Load metro route data from CSV"""
        try:
            df = pd.read_csv('bengaluru_station_pairs_final.csv')
            metro_data = {}
            
            for _, row in df.iterrows():
                station1 = row['start_station']
                station2 = row['end_station']
                metro_data[(station1, station2)] = {
                    'distance': row.get('metro_distance_km', 0),
                    'time': row.get('directions_time_min', 0),
                    'same_line': row.get('same_line', False),
                    'interchange': row.get('interchange_station', ''),
                    'transfer_count': row.get('transfer_count', 0),
                    'start_line': row.get('start_line', ''),
                    'end_line': row.get('end_line', '')
                }
            
            print(f"✅ Loaded {len(metro_data)} Bengaluru metro routes")
            return metro_data
            
        except Exception as e:
            print(f"❌ Error loading metro data: {e}")
            return {}
    
    def calculate_simple_distance(self, lat1, lng1, lat2, lng2):
        """Calculate simple distance using |lat1-lat2| + |lng1-lng2|"""
        return abs(lat1 - lat2) + abs(lng1 - lng2)
    
    def find_nearest_stations(self, lat, lng, top_n=7):
        """Find top N nearest stations to given coordinates with walking/taxi mode selection"""
        print(f"🎯 Finding {top_n} nearest metro stations to coordinates ({lat:.6f}, {lng:.6f})...")
        
        # Calculate distances to all stations
        station_distances = []
        
        for station_name, (station_lat, station_lng) in self.stations.items():
            simple_dist = self.calculate_simple_distance(lat, lng, station_lat, station_lng)
            straight_line_dist = self.calculate_straight_line_distance(lat, lng, station_lat, station_lng)
            
            # Determine mode based on straight-line distance
            mode = 'walking' if straight_line_dist <= 0.5 else 'taxi'  # 500m = 0.5km
            
            station_distances.append({
                'name': station_name,
                'lat': station_lat,
                'lng': station_lng,
                'distance': simple_dist,
                'straight_line_distance': straight_line_dist,
                'mode': mode
            })
        
        # Sort by distance and get top N
        station_distances.sort(key=lambda x: x['distance'])
        nearest_stations = station_distances[:top_n]
        
        print(f"✅ Found {len(nearest_stations)} nearest stations:")
        for i, station in enumerate(nearest_stations, 1):
            mode_icon = "🚶" if station['mode'] == 'walking' else "🚗"
            print(f"   {i}. {station['name']} (distance: {station['distance']:.4f}) {mode_icon} {station['mode'].upper()}")
        
        return nearest_stations
    
    def calculate_taxi_leg(self, origin_lat, origin_lng, dest_lat, dest_lng):
        """Calculate single taxi leg using Google Directions API with traffic"""
        url = f"{self.base_url}/directions/json"
        params = {
            'origin': f"{origin_lat},{origin_lng}",
            'destination': f"{dest_lat},{dest_lng}",
            'mode': 'driving',
            'departure_time': 'now',
            'traffic_model': 'best_guess',
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data['status'] == 'OK' and data['routes']:
                route = data['routes'][0]
                leg = route['legs'][0]
                
                distance_km = leg['distance']['value'] / 1000
                
                # Use traffic-aware duration if available
                if 'duration_in_traffic' in leg:
                    duration_seconds = leg['duration_in_traffic']['value']
                    traffic_status = "Current Traffic"
                else:
                    duration_seconds = leg['duration']['value']
                    traffic_status = "Normal"
                
                # Convert to meaningful time format
                duration_min = int(duration_seconds // 60)
                duration_sec = int(duration_seconds % 60)
                
                if duration_sec == 0:
                    time_display = f"{duration_min} min"
                else:
                    time_display = f"{duration_min} min {duration_sec} sec"
                
                return {
                    'distance_km': distance_km,
                    'duration_min': duration_min,
                    'duration_sec': duration_sec,
                    'time_display': time_display,
                    'traffic_status': traffic_status,
                    'success': True
                }
            else:
                return {'success': False, 'error': data.get('status')}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def calculate_walking_leg(self, origin_lat, origin_lng, dest_lat, dest_lng):
        """Calculate single walking leg using Google Directions API"""
        url = f"{self.base_url}/directions/json"
        params = {
            'origin': f"{origin_lat},{origin_lng}",
            'destination': f"{dest_lat},{dest_lng}",
            'mode': 'walking',
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data['status'] == 'OK' and data['routes']:
                route = data['routes'][0]
                leg = route['legs'][0]
                
                distance_km = leg['distance']['value'] / 1000
                duration_seconds = leg['duration']['value']
                
                # Convert to meaningful time format
                duration_min = int(duration_seconds // 60)
                duration_sec = int(duration_seconds % 60)
                
                if duration_sec == 0:
                    time_display = f"{duration_min} min"
                else:
                    time_display = f"{duration_min} min {duration_sec} sec"
                
                return {
                    'distance_km': distance_km,
                    'duration_min': duration_min,
                    'duration_sec': duration_sec,
                    'time_display': time_display,
                    'mode': 'walking',
                    'success': True
                }
            else:
                return {'success': False, 'error': data.get('status')}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def calculate_straight_line_distance(self, lat1, lng1, lat2, lng2):
        """Calculate straight-line distance between two points in kilometers"""
        # Using Haversine formula for accurate distance calculation
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def calculate_direct_taxi(self, origin_lat, origin_lng, dest_lat, dest_lng):
        """Calculate direct taxi route from origin to destination"""
        print(f"🚕 Calculating direct taxi route...")
        result = self.calculate_taxi_leg(origin_lat, origin_lng, dest_lat, dest_lng)
        
        if result['success']:
            print(f"✅ Direct taxi: {result['distance_km']:.1f} km ({result['time_display']})")
            return result
        else:
            print(f"❌ Failed to calculate direct taxi: {result.get('error', 'Unknown error')}")
            return None
    
    def check_direct_taxi_conditions(self, direct_taxi, best_multimodal_route, leg_results, initial_stations, dest_stations):
        """Check if direct taxi should be suggested based on 6 rules"""
        if not direct_taxi:
            return {'suggest': False, 'reasons': []}
        
        direct_distance = direct_taxi['distance_km']
        direct_time_min = direct_taxi['duration_min'] + (direct_taxi['duration_sec'] / 60)
        
        # Get best multimodal route data
        best_multimodal_time = best_multimodal_route['total_journey_time']
        best_transfer_count = best_multimodal_route['transfer_count']
        
        # Calculate first+last mile access distances for best route
        best_initial = best_multimodal_route['initial']
        best_dest = best_multimodal_route['destination']
        
        leg1_key = f"initial_to_station_{best_initial}"
        leg2_key = f"station_to_dest_{best_dest}"
        
        first_access_km = 0
        last_access_km = 0
        
        if leg1_key in leg_results:
            first_access_km = leg_results[leg1_key]['distance_km']
        if leg2_key in leg_results:
            last_access_km = leg_results[leg2_key]['distance_km']
        
        total_first_last_km = first_access_km + last_access_km
        
        # Check 6 rules
        reasons = []
        
        # Rule 1: Direct distance ≤ 7 km
        if direct_distance <= 7:
            reasons.append(f"Direct distance ≤ 7 km ({direct_distance:.1f} km)")
        
        # Rule 2: Multimodal time ≥ 1.5 × direct time
        if best_multimodal_time >= 1.5 * direct_time_min:
            reasons.append(f"Multimodal time ≥ 1.5× direct time ({best_multimodal_time:.1f} min ≥ {1.5 * direct_time_min:.1f} min)")
        
        # Rule 3: Absolute saving ≥ 20 minutes
        time_saving = best_multimodal_time - direct_time_min
        if time_saving >= 20:
            reasons.append(f"Time saving ≥ 20 minutes ({time_saving:.1f} min)")
        
        # Rule 4: (first_access_km + last_access_km) ≥ 0.8 × direct_distance
        if total_first_last_km >= 0.8 * direct_distance:
            reasons.append(f"First+last mile ≥ 80% of direct distance ({total_first_last_km:.1f} km ≥ {0.8 * direct_distance:.1f} km)")
        
        # Rule 5: Either first OR last access leg ≥ 0.7 × direct_distance
        if first_access_km >= 0.7 * direct_distance or last_access_km >= 0.7 * direct_distance:
            reasons.append(f"First or last leg ≥ 70% of direct distance (first: {first_access_km:.1f} km, last: {last_access_km:.1f} km)")
        
        # Rule 6: Transfers ≥ 2 AND multimodal time ≥ 1.3 × direct time
        if best_transfer_count >= 2 and best_multimodal_time >= 1.3 * direct_time_min:
            reasons.append(f"Transfers ≥ 2 AND multimodal time ≥ 1.3× direct time ({best_transfer_count} transfers, {best_multimodal_time:.1f} min ≥ {1.3 * direct_time_min:.1f} min)")
        
        suggest = len(reasons) > 0
        
        if suggest:
            print(f"🎯 DIRECT TAXI SUGGESTED - Rules triggered:")
            for i, reason in enumerate(reasons, 1):
                print(f"   {i}. {reason}")
        else:
            print(f"🚕 Direct taxi not suggested - No rules triggered")
            print(f"   Direct: {direct_distance:.1f} km, {direct_time_min:.1f} min")
            print(f"   Best multimodal: {best_multimodal_time:.1f} min ({best_transfer_count} transfers)")
        
        return {
            'suggest': suggest,
            'reasons': reasons,
            'direct_distance': direct_distance,
            'direct_time': direct_time_min,
            'time_saving': time_saving
        }
    
    def calculate_all_taxi_legs(self, initial_lat, initial_lng, dest_lat, dest_lng, initial_stations, dest_stations):
        """Calculate all 14 access legs (walking + taxi) in parallel"""
        print("\n" + "=" * 80)
        print("🚶🚗 STEP 2: CALCULATING ACCESS LEGS")
        print("=" * 80)
        print("📋 Calculating 14 access legs using Google Maps API...")
        
        # Prepare all leg calculations (walking + taxi)
        leg_calculations = []
        
        print(f"\n📍 Preparing access leg calculations:")
        print(f"   • 7 legs: Origin → Nearest Metro Stations")
        print(f"   • 7 legs: Nearest Metro Stations → Destination")
        
        # Initial location to its 7 stations
        for station in initial_stations:
            leg_calculations.append({
                'type': 'initial_to_station',
                'station_name': station['name'],
                'origin_lat': initial_lat,
                'origin_lng': initial_lng,
                'dest_lat': station['lat'],
                'dest_lng': station['lng'],
                'mode': station['mode']
            })
        
        # Destination's 7 stations to destination
        for station in dest_stations:
            leg_calculations.append({
                'type': 'station_to_dest',
                'station_name': station['name'],
                'origin_lat': station['lat'],
                'origin_lng': station['lng'],
                'dest_lat': dest_lat,
                'dest_lng': dest_lng,
                'mode': station['mode']
            })
        
        # Count walking vs taxi legs
        walking_count = sum(1 for calc in leg_calculations if calc['mode'] == 'walking')
        taxi_count = sum(1 for calc in leg_calculations if calc['mode'] == 'taxi')
        
        print(f"\n🌐 Calling Google Maps API for {len(leg_calculations)} routes:")
        print(f"   • {walking_count} walking legs")
        print(f"   • {taxi_count} taxi legs")
        
        # Calculate all legs in parallel
        leg_results = {}
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_calc = {}
            
            for calc in leg_calculations:
                if calc['mode'] == 'walking':
                    future = executor.submit(self.calculate_walking_leg, calc['origin_lat'], calc['origin_lng'], 
                                           calc['dest_lat'], calc['dest_lng'])
                else:  # taxi
                    future = executor.submit(self.calculate_taxi_leg, calc['origin_lat'], calc['origin_lng'], 
                                           calc['dest_lat'], calc['dest_lng'])
                future_to_calc[future] = calc
            
            for future in as_completed(future_to_calc):
                calc = future_to_calc[future]
                try:
                    result = future.result()
                    if result['success']:
                        key = f"{calc['type']}_{calc['station_name']}"
                        # Add mode to result
                        result['mode'] = calc['mode']
                        leg_results[key] = result
                except Exception as e:
                    print(f"❌ Error calculating {calc['mode']} leg to {calc['station_name']}: {e}")
        
        print(f"✅ Successfully calculated {len(leg_results)} access legs")
        
        # Display results - organized by mode
        print(f"\n🚶 WALKING LEGS: Origin → Metro Stations")
        print("-" * 50)
        walking_found = False
        for station in initial_stations:
            if station['mode'] == 'walking':
                key = f"initial_to_station_{station['name']}"
                if key in leg_results:
                    result = leg_results[key]
                    print(f"   {station['name']}: {result['distance_km']:.1f} km ({result['time_display']})")
                    walking_found = True
        if not walking_found:
            print("   No walking legs found")
        
        print(f"\n🚗 TAXI LEGS: Origin → Metro Stations")
        print("-" * 50)
        taxi_found = False
        for station in initial_stations:
            if station['mode'] == 'taxi':
                key = f"initial_to_station_{station['name']}"
                if key in leg_results:
                    result = leg_results[key]
                    print(f"   {station['name']}: {result['distance_km']:.1f} km ({result['time_display']})")
                    taxi_found = True
        if not taxi_found:
            print("   No taxi legs found")
        
        print(f"\n🚶 WALKING LEGS: Metro Stations → Destination")
        print("-" * 50)
        walking_found = False
        for station in dest_stations:
            if station['mode'] == 'walking':
                key = f"station_to_dest_{station['name']}"
                if key in leg_results:
                    result = leg_results[key]
                    print(f"   {station['name']}: {result['distance_km']:.1f} km ({result['time_display']})")
                    walking_found = True
        if not walking_found:
            print("   No walking legs found")
        
        print(f"\n🚗 TAXI LEGS: Metro Stations → Destination")
        print("-" * 50)
        taxi_found = False
        for station in dest_stations:
            if station['mode'] == 'taxi':
                key = f"station_to_dest_{station['name']}"
                if key in leg_results:
                    result = leg_results[key]
                    print(f"   {station['name']}: {result['distance_km']:.1f} km ({result['time_display']})")
                    taxi_found = True
        if not taxi_found:
            print("   No taxi legs found")
        
        # ===============================================================
        # STEP 3: DIRECT TAXI CALCULATION
        # ===============================================================
        print("\n" + "=" * 80)
        print("🚕 STEP 3: DIRECT TAXI CALCULATION")
        print("=" * 80)
        
        # Calculate direct taxi in parallel with existing calculations
        direct_taxi = self.calculate_direct_taxi(initial_lat, initial_lng, dest_lat, dest_lng)
        
        # Store direct taxi for later use
        self.direct_taxi = direct_taxi
        
        if direct_taxi:
            print(f"✅ Direct taxi calculation successful: {direct_taxi['distance_km']:.1f} km, {direct_taxi['time_display']}")
        else:
            print(f"❌ Direct taxi calculation failed - will skip suggestion check")
        
        # ===============================================================
        # STEP 4: ACCESS COMBINATIONS
        # ===============================================================
        print("\n" + "=" * 80)
        print("🔄 STEP 4: CREATING ACCESS COMBINATIONS")
        print("=" * 80)
        print(f"📊 Creating 49 combinations (7×7 station pairs)...")
        combinations = []
        
        for initial_station in initial_stations:
            for dest_station in dest_stations:
                leg1_key = f"initial_to_station_{initial_station['name']}"
                leg2_key = f"station_to_dest_{dest_station['name']}"
                
                if leg1_key in leg_results and leg2_key in leg_results:
                    leg1 = leg_results[leg1_key]
                    leg2 = leg_results[leg2_key]
                    total_access = leg1['distance_km'] + leg2['distance_km']

                    combinations.append({
                        'initial': initial_station['name'],
                        'destination': dest_station['name'],
                        'leg1_distance': leg1['distance_km'],
                        'leg2_distance': leg2['distance_km'],
                        'leg1_mode': leg1['mode'],
                        'leg2_mode': leg2['mode'],
                        'total_access': total_access
                    })
        
        # Sort by total access distance (ascending)
        combinations.sort(key=lambda x: x['total_access'])
        
        print(f"✅ Created {len(combinations)} valid access combinations")
        print(f"\n🏆 TOP 10 ACCESS COMBINATIONS (Shortest Total Distance):")
        print("-" * 60)
        for i, combo in enumerate(combinations[:10], 1):
            leg1_icon = "🚶" if combo['leg1_mode'] == 'walking' else "🚗"
            leg2_icon = "🚶" if combo['leg2_mode'] == 'walking' else "🚗"
            print(f"{i:2d}. {combo['initial']} → {combo['destination']}: {combo['leg1_distance']:.1f} {leg1_icon} + {combo['leg2_distance']:.1f} {leg2_icon} = {combo['total_access']:.1f} km")
        
        # ===============================================================
        # STEP 5: METRO ROUTE ANALYSIS
        # ===============================================================
        print("\n" + "=" * 80)
        print("🚇 STEP 5: METRO ROUTE ANALYSIS")
        print("=" * 80)
        print(f"📋 Looking up metro routes for all 49 station combinations...")
        metro_combinations = []
        
        for initial_station in initial_stations:
            for dest_station in dest_stations:
                initial_name = initial_station['name']
                dest_name = dest_station['name']
                
                # Check if metro route exists
                metro_key = (initial_name, dest_name)
                if metro_key in self.metro_data:
                    metro_info = self.metro_data[metro_key]
                    initial_line = metro_info.get('start_line', 'Unknown')
                    dest_line = metro_info.get('end_line', 'Unknown')
                    
                    metro_combinations.append({
                        'initial': initial_name,
                        'destination': dest_name,
                        'distance': metro_info['distance'],
                        'time': metro_info['time'],
                        'same_line': metro_info['same_line'],
                        'interchange': metro_info['interchange'],
                        'transfer_count': metro_info['transfer_count'],
                        'initial_line': initial_line,
                        'dest_line': dest_line
                    })
        
        # Sort metro combinations by time (ascending)
        metro_combinations.sort(key=lambda x: x['time'])
        
        print(f"✅ Found {len(metro_combinations)} valid metro routes")
        print(f"\n🚇 TOP 10 METRO ROUTES (Fastest):")
        print("-" * 60)
        for i, combo in enumerate(metro_combinations[:10], 1):
            if combo['same_line']:
                line_info = f"Same Line ({combo['initial_line']})"
            else:
                if combo['transfer_count'] == 2:
                    # Parse enhanced interchange info
                    interchange_parts = combo['interchange'].split('|')
                    if len(interchange_parts) > 1:
                        line_sequence = interchange_parts[0]
                        interchange_details = interchange_parts[1]
                        line_info = f"Double Transfer: {line_sequence} ({interchange_details})"
                    else:
                        line_info = f"Double Transfer: {combo['interchange']} ({combo['initial_line']} → {combo['dest_line']})"
                elif combo['transfer_count'] == 1:
                    line_info = f"Single Transfer: {combo['interchange']} ({combo['initial_line']} → {combo['dest_line']})"
                else:
                    line_info = f"Different Lines ({combo['initial_line']} → {combo['dest_line']})"
            
            print(f"{i:2d}. {combo['initial']} → {combo['destination']}: {combo['distance']:.1f} km ({combo['time']:.0f} min) [{line_info}]")
        
        # ===============================================================
        # STEP 6: CONVENIENCE SCORING & RANKING
        # ===============================================================
        print("\n" + "=" * 80)
        print("🏆 STEP 6: CONVENIENCE SCORING & RANKING")
        print("=" * 80)
        print(f"🧮 Calculating convenience scores for all {len(combinations)} combinations...")
        print(f"📊 Scoring factors:")
        print(f"   • Access Score: Based on total access distance (walking + taxi, shorter = better)")
        print(f"   • Metro Score: Based on transfer count (fewer transfers = better)")
        print(f"   • Fixed Weighting: Based on transfer count only (0 transfers: 80/20, 1 transfer: 65/35, 2+ transfers: 60/40)")
        
        # Create convenience scoring for all combinations
        convenience_combinations = []
        
        for initial_station in initial_stations:
            for dest_station in dest_stations:
                initial_name = initial_station['name']
                dest_name = dest_station['name']
                
                # Get access leg data
                leg1_key = f"initial_to_station_{initial_name}"
                leg2_key = f"station_to_dest_{dest_name}"
                
                # Get metro data
                metro_key = (initial_name, dest_name)
                
                if leg1_key in leg_results and leg2_key in leg_results and metro_key in self.metro_data:
                    leg1 = leg_results[leg1_key]
                    leg2 = leg_results[leg2_key]
                    metro_info = self.metro_data[metro_key]
                    
                    # Calculate access score (walking + taxi)
                    total_access_distance = leg1['distance_km'] + leg2['distance_km']
                    shortest_access = min([combo['total_access'] for combo in combinations])
                    access_score = (shortest_access / total_access_distance) * 100
                    
                    # Metro scoring based on transfer count
                    access_factor = min(total_access_distance / 20, 1.0)  # 0 to 1
                    
                    transfer_count = metro_info.get('transfer_count', 0)
                    if transfer_count == 0:
                        metro_score = 100  # Same line
                    elif transfer_count == 1:
                        penalty = 40 * access_factor  # 0 to 40 points
                        metro_score = 100 - penalty
                    elif transfer_count == 2:
                        penalty = 80 * access_factor  # 0 to 80 points
                        metro_score = 100 - penalty
                    else:
                        metro_score = 100
                    
                    # Fixed weighting based on transfer count only
                    if transfer_count == 0:
                        # Same line: 80% access, 20% metro
                        total_convenience_score = (access_score * 0.8) + (metro_score * 0.2)
                    elif transfer_count == 1:
                        # Single transfer: 65% access, 35% metro
                        total_convenience_score = (access_score * 0.65) + (metro_score * 0.35)
                    elif transfer_count == 2:
                        # Double transfer: 60% access, 40% metro
                        total_convenience_score = (access_score * 0.6) + (metro_score * 0.4)
                    else:
                        # More than 2 transfers: 60% access, 40% metro
                        total_convenience_score = (access_score * 0.6) + (metro_score * 0.4)
                    
                    # Calculate actual time values for convenience routes
                    leg1_time_min = leg1['duration_min'] + (leg1['duration_sec'] / 60)
                    leg2_time_min = leg2['duration_min'] + (leg2['duration_sec'] / 60)
                    total_access_time = leg1_time_min + leg2_time_min
                    
                    # Calculate total journey time with Bengaluru transfer times
                    metro_interchange_time = transfer_count * 3  # 3 min per transfer
                    access_metro_interchange_time = 6  # 3 min each side
                    total_journey_time = total_access_time + metro_info['time'] + metro_interchange_time + access_metro_interchange_time
                    
                    convenience_combinations.append({
                        'initial': initial_name,
                        'destination': dest_name,
                        'leg1_distance': leg1['distance_km'],
                        'leg2_distance': leg2['distance_km'],
                        'leg1_mode': leg1['mode'],
                        'leg2_mode': leg2['mode'],
                        'total_access_distance': total_access_distance,
                        'leg1_time': leg1['time_display'],
                        'leg2_time': leg2['time_display'],
                        'leg1_time_min': leg1_time_min,
                        'leg2_time_min': leg2_time_min,
                        'total_access_time': total_access_time,
                        'metro_distance': metro_info['distance'],
                        'metro_time': metro_info['time'],
                        'metro_interchange_time': metro_interchange_time,
                        'access_metro_interchange_time': access_metro_interchange_time,
                        'total_journey_time': total_journey_time,
                        'metro_score': metro_score,
                        'access_score': access_score,
                        'total_convenience_score': total_convenience_score,
                        'same_line': metro_info['same_line'],
                        'interchange': metro_info['interchange'],
                        'transfer_count': transfer_count,
                        'initial_line': metro_info.get('start_line', 'Unknown'),
                        'dest_line': metro_info.get('end_line', 'Unknown')
                    })
        
        # Sort by convenience score (highest first)
        convenience_combinations.sort(key=lambda x: x['total_convenience_score'], reverse=True)
        
        print(f"✅ Calculated convenience scores for {len(convenience_combinations)} combinations")
        print(f"\n🏆 TOP 10 CONVENIENCE ROUTES (Highest Scores):")
        print("-" * 70)
        
        for i, combo in enumerate(convenience_combinations[:10], 1):
            if combo['same_line']:
                line_info = f"Same Line ({combo['initial_line']})"
            else:
                if combo['transfer_count'] == 2:
                    interchange_parts = combo['interchange'].split('|')
                    if len(interchange_parts) > 1:
                        line_sequence = interchange_parts[0]
                        line_info = f"Double Transfer: {line_sequence}"
                    else:
                        line_info = f"Double Transfer: {combo['interchange']}"
                elif combo['transfer_count'] == 1:
                    line_info = f"Single Transfer: {combo['interchange']}"
                else:
                    line_info = f"Different Lines ({combo['initial_line']} → {combo['dest_line']})"
            
            leg1_icon = "🚶" if combo['leg1_mode'] == 'walking' else "🚗"
            leg2_icon = "🚶" if combo['leg2_mode'] == 'walking' else "🚗"
            
            print(f"{i:2d}. {combo['initial']} → {combo['destination']}")
            print(f"    Score: {combo['total_convenience_score']:.1f} | Time: {combo['total_journey_time']:.1f} min | Access: {combo['total_access_distance']:.1f} km | Metro: {combo['metro_distance']:.1f} km")
            print(f"    Access: {combo['leg1_distance']:.1f} km {leg1_icon} + {combo['leg2_distance']:.1f} km {leg2_icon}")
            print(f"    Route: {line_info}")
        
        # ===============================================================
        # STEP 7: DIRECT TAXI SUGGESTION CHECK
        # ===============================================================
        print("\n" + "=" * 80)
        print("🚕 STEP 7: DIRECT TAXI SUGGESTION CHECK")
        print("=" * 80)
        
        # Check direct taxi conditions against best multimodal route
        best_multimodal_route = convenience_combinations[0] if convenience_combinations else None
        direct_taxi_suggestion = None
        
        print(f"🔍 Checking direct taxi suggestion conditions...")
        print(f"   Direct taxi available: {'Yes' if self.direct_taxi else 'No'}")
        print(f"   Best multimodal route available: {'Yes' if best_multimodal_route else 'No'}")
        
        if best_multimodal_route and self.direct_taxi:
            print(f"   Best multimodal route: {best_multimodal_route['initial']} → {best_multimodal_route['destination']}")
            print(f"   Best multimodal time: {best_multimodal_route['total_journey_time']:.1f} min")
            print(f"   Best multimodal transfers: {best_multimodal_route['transfer_count']}")
            
            direct_taxi_suggestion = self.check_direct_taxi_conditions(
                self.direct_taxi, best_multimodal_route, leg_results, initial_stations, dest_stations
            )
        else:
            print(f"   ⚠️ Cannot check direct taxi conditions - missing data")
            if not self.direct_taxi:
                print(f"      - Direct taxi calculation failed")
            if not best_multimodal_route:
                print(f"      - No multimodal routes found")
        
        # Store direct taxi suggestion for API access
        self.direct_taxi_suggestion = direct_taxi_suggestion
        
        # ===============================================================
        # STEP 8: FINAL RECOMMENDATIONS
        # ===============================================================
        print("\n" + "=" * 80)
        print("🎯 STEP 8: FINAL RECOMMENDATIONS")
        print("=" * 80)
        
        # Get top 5 convenience routes
        top_convenience = convenience_combinations[:5]
        
        print(f"🏆 TOP 5 CONVENIENCE ROUTES FOR USER:")
        print("=" * 50)
        
        for i, combo in enumerate(top_convenience, 1):
            if combo['same_line']:
                line_info = f"Same Line ({combo['initial_line']})"
            else:
                if combo['transfer_count'] == 2:
                    interchange_parts = combo['interchange'].split('|')
                    if len(interchange_parts) > 1:
                        line_sequence = interchange_parts[0]
                        line_info = f"Double Transfer: {line_sequence}"
                    else:
                        line_info = f"Double Transfer: {combo['interchange']}"
                elif combo['transfer_count'] == 1:
                    line_info = f"Single Transfer: {combo['interchange']}"
                else:
                    line_info = f"Different Lines ({combo['initial_line']} → {combo['dest_line']})"
            
            leg1_icon = "🚶" if combo['leg1_mode'] == 'walking' else "🚗"
            leg2_icon = "🚶" if combo['leg2_mode'] == 'walking' else "🚗"
            
            print(f"\n{i}. {combo['initial']} → {combo['destination']}")
            print(f"   🏆 Convenience Score: {combo['total_convenience_score']:.1f}")
            print(f"   ⏱️  Total Journey Time: {combo['total_journey_time']:.1f} min")
            print(f"   🚶🚗 Access Distance: {combo['total_access_distance']:.1f} km ({combo['leg1_distance']:.1f} km {leg1_icon} + {combo['leg2_distance']:.1f} km {leg2_icon})")
            print(f"   🚇 Metro Distance: {combo['metro_distance']:.1f} km")
            print(f"   🔄 Route Type: {line_info}")
        
        print(f"\n✅ Analysis complete! Returning top 5 routes to user.")
        
        # Store convenience routes for API access
        self.convenience_routes = convenience_combinations[:5]
        
        return leg_results
    
    def get_convenience_routes(self):
        """Get the top 5 convenience routes for API response"""
        return getattr(self, 'convenience_routes', [])
    
    def get_direct_taxi_suggestion(self):
        """Get direct taxi suggestion for API response"""
        return getattr(self, 'direct_taxi_suggestion', None)

    def get_station_line_color(self, station_name):
        """Get the line color for a given station"""
        for line_name, info in METRO_LINES.items():
            if station_name in info['stations']:
                return info['name']
        return "Unknown"

def main():
    """Multi-modal journey planner with step-by-step processing"""
    finder = BengaluruStationFinder()
    
    # ===============================================================
    # STEP 1: Input & Validation
    # ===============================================================
    print("=" * 60)
    print("STEP 1: Input & Validation")
    print("=" * 60)
    
    # Get initial location coordinates
    print("Enter initial location coordinates:")
    initial_lat = float(input("Latitude: "))
    initial_lng = float(input("Longitude: "))
    
    # Get destination coordinates
    print("\nEnter destination coordinates:")
    dest_lat = float(input("Latitude: "))
    dest_lng = float(input("Longitude: "))
    
    print(f"✅ Initial Location: ({initial_lat:.6f}, {initial_lng:.6f})")
    print(f"✅ Destination: ({dest_lat:.6f}, {dest_lng:.6f})")
    
    # ===============================================================
    # STEP 2: Station Discovery
    # ===============================================================
    print("\n" + "=" * 60)
    print("STEP 2: Station Discovery")
    print("=" * 60)
    
    # Find nearest stations for initial location
    print(f"\n📍 Initial Location - Top 7 nearest stations:")
    initial_stations = finder.find_nearest_stations(initial_lat, initial_lng, top_n=7)
    
    for i, station in enumerate(initial_stations, 1):
        distance = abs(initial_lat - station['lat']) + abs(initial_lng - station['lng'])
        print(f"{i}. {station['name']} - {station['lat']:.6f}, {station['lng']:.6f}")
        print(f"   Distance: |{initial_lat:.6f} - {station['lat']:.6f}| + |{initial_lng:.6f} - {station['lng']:.6f}| = {distance:.6f}")
    
    # Find nearest stations for destination
    print(f"\n🎯 Destination - Top 7 nearest stations:")
    dest_stations = finder.find_nearest_stations(dest_lat, dest_lng, top_n=7)
    
    for i, station in enumerate(dest_stations, 1):
        distance = abs(dest_lat - station['lat']) + abs(dest_lng - station['lng'])
        print(f"{i}. {station['name']} - {station['lat']:.6f}, {station['lng']:.6f}")
        print(f"   Distance: |{dest_lat:.6f} - {station['lat']:.6f}| + |{dest_lng:.6f} - {station['lng']:.6f}| = {distance:.6f}")
    
    # ===============================================================
    # STEP 3: Taxi Leg Calculations
    # ===============================================================
    print("\n" + "=" * 60)
    print("STEP 3: Taxi Leg Calculations")
    print("=" * 60)
    
    # Calculate taxi legs
    taxi_legs = finder.calculate_all_taxi_legs(initial_lat, initial_lng, dest_lat, dest_lng, initial_stations, dest_stations)

if __name__ == '__main__':
    main()
