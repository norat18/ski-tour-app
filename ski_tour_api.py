#!/usr/bin/env python3
"""
Ski Tour Decision API Backend
Fetches data from NWAC, Weather.gov, OpenSnow, and CalTopo
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import os

class SkiTourAPI:
    def __init__(self):
        self.nws_user_agent = "(SkiTourDecisionApp, your.email@example.com)"
        
        # Optional: Add your API keys here
        self.opensnow_api_key = os.environ.get('OPENSNOW_API_KEY', '')
        self.caltopo_credential_id = os.environ.get('CALTOPO_CRED_ID', '')
        self.caltopo_credential_secret = os.environ.get('CALTOPO_CRED_SECRET', '')
    
    def get_nwac_forecast(self, zone: str) -> Dict:
        """
        Fetch NWAC avalanche forecast for a given zone
        Note: NWAC doesn't have an official public API yet
        This is a placeholder showing the data structure
        """
        
        # In production, you would either:
        # 1. Scrape nwac.us (check their robots.txt and terms first)
        # 2. Use an unofficial API endpoint if available
        # 3. Contact NWAC for API access (forecasters@nwac.us)
        
        zone_urls = {
            'west-slopes-north': 'https://nwac.us/avalanche-forecast/#/west-slopes-north',
            'west-slopes-central': 'https://nwac.us/avalanche-forecast/#/west-slopes-central',
            'snoqualmie-pass': 'https://nwac.us/avalanche-forecast/#/snoqualmie-pass',
            'west-slopes-south': 'https://nwac.us/avalanche-forecast/#/west-slopes-south',
            'mt-hood': 'https://nwac.us/avalanche-forecast/#/mt-hood'
        }
        
        return {
            'zone': zone,
            'url': zone_urls.get(zone, 'https://nwac.us/'),
            'danger_levels': {
                'above_treeline': 'MODERATE',
                'near_treeline': 'MODERATE',
                'below_treeline': 'LOW'
            },
            'bottom_line': 'Check NWAC.us for current forecast',
            'problems': ['Wind Slab', 'Storm Slab'],
            'updated': datetime.now().isoformat()
        }
    
    def get_weather_forecast(self, lat: float, lon: float) -> Dict:
        """
        Fetch weather forecast from Weather.gov API
        This is a free, public API with no auth required
        """
        try:
            # Step 1: Get grid coordinates
            points_url = f"https://api.weather.gov/points/{lat},{lon}"
            headers = {'User-Agent': self.nws_user_agent}
            
            points_response = requests.get(points_url, headers=headers, timeout=10)
            points_response.raise_for_status()
            points_data = points_response.json()
            
            # Step 2: Get forecast
            forecast_url = points_data['properties']['forecast']
            forecast_hourly_url = points_data['properties']['forecastHourly']
            grid_data_url = points_data['properties']['forecastGridData']
            
            forecast_response = requests.get(forecast_url, headers=headers, timeout=10)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            # Get hourly for more detail
            hourly_response = requests.get(forecast_hourly_url, headers=headers, timeout=10)
            hourly_data = hourly_response.json() if hourly_response.ok else None
            
            periods = forecast_data['properties']['periods']
            current = periods[0]
            
            return {
                'temperature': current['temperature'],
                'temperature_unit': current['temperatureUnit'],
                'wind_speed': current['windSpeed'],
                'wind_direction': current['windDirection'],
                'short_forecast': current['shortForecast'],
                'detailed_forecast': current['detailedForecast'],
                'is_daytime': current['isDaytime'],
                'periods': periods[:7],  # Next 7 periods
                'hourly': hourly_data['properties']['periods'][:24] if hourly_data else [],
                'updated': datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Failed to fetch weather data from NWS'
            }
    
    def get_opensnow_forecast(self, lat: float, lon: float) -> Dict:
        """
        Fetch OpenSnow forecast data
        NOTE: OpenSnow API requires commercial partnership
        You'll need to contact them at partnerships@opensnow.com
        """
        if not self.opensnow_api_key:
            return {
                'error': 'No API key',
                'message': 'OpenSnow API requires a commercial partnership. Contact partnerships@opensnow.com',
                'manual_check': f'https://opensnow.com/location/closest?lat={lat}&lon={lon}'
            }
        
        # If you have an API key:
        try:
            url = f"https://api.opensnow.com/forecast/{lon},{lat}"
            params = {
                'api_key': self.opensnow_api_key,
                'v': 1,
                'elev': 5000  # Elevation in feet
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Failed to fetch OpenSnow data'
            }
    
    def get_caltopo_map_data(self, map_id: str) -> Dict:
        """
        Fetch CalTopo map data
        This uses the public map JSON endpoint (no auth required)
        For team features, you need Team API credentials
        """
        try:
            # Public map data endpoint
            url = f"https://caltopo.com/m/{map_id}"
            
            # Try to get the JSON data
            json_url = f"https://caltopo.com/api/v1/map/offline/latest/{map_id}"
            
            response = requests.get(json_url, timeout=10)
            
            if response.ok:
                data = response.json()
                
                # Extract useful information
                features = []
                if 'features' in data:
                    for feature in data['features']:
                        if feature['properties'].get('class') == 'Shape':
                            # This is a route or area
                            features.append({
                                'title': feature['properties'].get('title', 'Unnamed'),
                                'description': feature['properties'].get('description', ''),
                                'coordinates': feature['geometry'].get('coordinates', [])
                            })
                
                return {
                    'map_id': map_id,
                    'features': features,
                    'url': url,
                    'updated': datetime.now().isoformat()
                }
            else:
                return {
                    'map_id': map_id,
                    'url': url,
                    'message': 'Map data requires direct API access or team credentials',
                    'note': 'For full integration, sign up for CalTopo Team and use the official API'
                }
        
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Failed to fetch CalTopo data',
                'map_url': f'https://caltopo.com/m/{map_id}'
            }
    
    def calculate_tour_recommendation(
        self, 
        tour: Dict, 
        avalanche_danger: str,
        fitness_level: int,
        weather: Dict
    ) -> Dict:
        """
        Calculate a recommendation for a tour based on multiple factors
        """
        score = 0
        warnings = []
        
        # Avalanche danger factor
        danger_scores = {
            'LOW': 2,
            'MODERATE': 1,
            'CONSIDERABLE': -1,
            'HIGH': -3,
            'EXTREME': -5
        }
        score += danger_scores.get(avalanche_danger.upper(), 0)
        
        if avalanche_danger in ['CONSIDERABLE', 'HIGH', 'EXTREME']:
            warnings.append(f'{avalanche_danger} avalanche danger')
        
        # Fitness vs elevation gain
        elev_gain = tour.get('elevation_gain', 0)
        if elev_gain < 2000 and fitness_level >= 5:
            score += 2
        elif elev_gain < 3000 and fitness_level >= 6:
            score += 1
        elif elev_gain >= 3500 and fitness_level < 7:
            score -= 2
            warnings.append('Significant elevation gain vs fitness level')
        
        # Terrain considerations
        terrain = tour.get('terrain', '').lower()
        if 'tree' in terrain or 'forest' in terrain:
            score += 1
        if 'exposed' in terrain or 'ridge' in terrain:
            score -= 1
            warnings.append('Exposed terrain')
        
        # Weather factors
        temp = weather.get('temperature', 32)
        wind_speed_str = weather.get('wind_speed', '0 mph')
        wind_speed = int(''.join(filter(str.isdigit, wind_speed_str.split()[0]))) if wind_speed_str else 0
        
        if temp < 10:
            warnings.append('Very cold temperatures')
            score -= 1
        if wind_speed > 25:
            warnings.append('High winds')
            score -= 1
        
        # Determine recommendation
        if score >= 2:
            level = 'go'
            text = '✅ Good to Go'
            analysis = 'Conditions and terrain align well. Enjoy responsibly!'
        elif score >= 0:
            level = 'cautious'
            text = '⚠️ Cautious Go'
            analysis = 'Feasible but requires careful decision-making. Stay conservative.'
        else:
            level = 'no'
            text = '🛑 Skip It'
            analysis = 'Consider an easier objective or wait for better conditions.'
        
        return {
            'level': level,
            'text': text,
            'analysis': analysis,
            'score': score,
            'warnings': warnings
        }
    
    def get_complete_dashboard(
        self, 
        lat: float, 
        lon: float, 
        nwac_zone: str,
        caltopo_map_id: Optional[str] = None,
        fitness_level: int = 7
    ) -> Dict:
        """
        Fetch all data needed for the dashboard
        """
        print(f"Fetching data for {lat}, {lon}...")
        
        # Fetch all data in parallel (in production, use async)
        avalanche = self.get_nwac_forecast(nwac_zone)
        weather = self.get_weather_forecast(lat, lon)
        opensnow = self.get_opensnow_forecast(lat, lon)
        
        caltopo = None
        if caltopo_map_id:
            caltopo = self.get_caltopo_map_data(caltopo_map_id)
        
        return {
            'location': {'lat': lat, 'lon': lon},
            'avalanche': avalanche,
            'weather': weather,
            'opensnow': opensnow,
            'caltopo': caltopo,
            'fitness_level': fitness_level,
            'timestamp': datetime.now().isoformat()
        }


# Example usage
if __name__ == '__main__':
    api = SkiTourAPI()
    
    # Example: Get complete dashboard for Stevens Pass area
    print("=== Ski Tour Decision Dashboard ===\n")
    
    dashboard = api.get_complete_dashboard(
        lat=47.745,
        lon=-121.089,
        nwac_zone='west-slopes-central',
        caltopo_map_id='V106Q',
        fitness_level=7
    )
    
    print(json.dumps(dashboard, indent=2))
    
    # Example: Test weather API
    print("\n=== Testing Weather.gov API ===")
    weather = api.get_weather_forecast(47.745, -121.089)
    if 'error' not in weather:
        print(f"Temperature: {weather['temperature']}°{weather['temperature_unit']}")
        print(f"Wind: {weather['wind_speed']} from {weather['wind_direction']}")
        print(f"Conditions: {weather['short_forecast']}")
    else:
        print(f"Error: {weather['message']}")
    
    # Example: Calculate tour recommendation
    print("\n=== Sample Tour Recommendation ===")
    sample_tour = {
        'name': 'Kendall Peak',
        'elevation_gain': 3200,
        'terrain': 'Open slopes, exposed'
    }
    
    rec = api.calculate_tour_recommendation(
        tour=sample_tour,
        avalanche_danger='MODERATE',
        fitness_level=7,
        weather=weather
    )
    
    print(f"{sample_tour['name']}: {rec['text']}")
    print(f"Analysis: {rec['analysis']}")
    if rec['warnings']:
        print(f"Warnings: {', '.join(rec['warnings'])}")
