#!/usr/bin/env python3
"""
Quick setup script for Ski Tour Decision App
Helps you configure API keys and test connections
"""

import os
import json
import sys

def banner():
    print("""
    ╔═══════════════════════════════════════════╗
    ║   🎿 SKI TOUR DECISION APP SETUP 🏔️      ║
    ╚═══════════════════════════════════════════╝
    """)

def test_imports():
    """Check if required packages are installed"""
    print("📦 Checking dependencies...")
    try:
        import requests
        print("✅ requests module installed")
        return True
    except ImportError:
        print("❌ requests module not found")
        print("\nInstall with:")
        print("  pip install requests --break-system-packages")
        return False

def get_config():
    """Interactive configuration"""
    print("\n🔧 Configuration Setup\n")
    
    config = {}
    
    # Home location
    print("1️⃣  HOME LOCATION")
    print("   Get coordinates from Google Maps (drop a pin)")
    lat = input("   Enter latitude (e.g., 47.606): ").strip()
    lon = input("   Enter longitude (e.g., -122.332): ").strip()
    
    try:
        config['home_location'] = {
            'lat': float(lat),
            'lon': float(lon)
        }
        print(f"   ✅ Set to {lat}, {lon}\n")
    except ValueError:
        print("   ❌ Invalid coordinates\n")
        return None
    
    # NWAC zone
    print("2️⃣  NWAC ZONE")
    print("   Options:")
    print("   1) West Slopes North (Mt Baker)")
    print("   2) West Slopes Central (Stevens Pass)")
    print("   3) Snoqualmie Pass")
    print("   4) West Slopes South (White Pass)")
    print("   5) Mt Hood")
    
    zone_map = {
        '1': 'west-slopes-north',
        '2': 'west-slopes-central',
        '3': 'snoqualmie-pass',
        '4': 'west-slopes-south',
        '5': 'mt-hood'
    }
    
    zone_choice = input("   Choose zone (1-5): ").strip()
    if zone_choice in zone_map:
        config['nwac_zone'] = zone_map[zone_choice]
        print(f"   ✅ Selected {zone_map[zone_choice]}\n")
    else:
        print("   ⚠️  Invalid choice, skipping\n")
    
    # CalTopo
    print("3️⃣  CALTOPO MAP (Optional)")
    print("   Find your map ID in the URL: caltopo.com/m/XXXXX")
    map_id = input("   Enter map ID (or press Enter to skip): ").strip()
    if map_id:
        config['caltopo_map_id'] = map_id.upper()
        print(f"   ✅ Will load map {map_id}\n")
    else:
        print("   ⏭️  Skipped\n")
    
    # API Keys (optional)
    print("4️⃣  API KEYS (Optional - for advanced features)")
    print("   Press Enter to skip any you don't have yet\n")
    
    opensnow_key = input("   OpenSnow API key: ").strip()
    if opensnow_key:
        config['opensnow_api_key'] = opensnow_key
        print("   ✅ OpenSnow key saved\n")
    
    caltopo_id = input("   CalTopo credential ID: ").strip()
    caltopo_secret = input("   CalTopo credential secret: ").strip()
    if caltopo_id and caltopo_secret:
        config['caltopo_credentials'] = {
            'id': caltopo_id,
            'secret': caltopo_secret
        }
        print("   ✅ CalTopo credentials saved\n")
    
    return config

def save_config(config):
    """Save configuration to file"""
    config_path = 'ski_tour_config.json'
    with open(config_path, 'w') as f:
        json.dump(config, indent=2, fp=f)
    print(f"💾 Configuration saved to {config_path}")

def test_weather_api(lat, lon):
    """Test Weather.gov API connection"""
    print("\n🌤️  Testing Weather.gov API...")
    try:
        import requests
        url = f"https://api.weather.gov/points/{lat},{lon}"
        headers = {'User-Agent': '(SkiTourApp, test@example.com)'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.ok:
            data = response.json()
            print("✅ Weather.gov API working!")
            print(f"   Grid: {data['properties']['gridId']}")
            return True
        else:
            print(f"⚠️  Got response code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def create_env_file(config):
    """Create .env file for environment variables"""
    env_content = []
    
    if 'opensnow_api_key' in config:
        env_content.append(f"export OPENSNOW_API_KEY=\"{config['opensnow_api_key']}\"")
    
    if 'caltopo_credentials' in config:
        env_content.append(f"export CALTOPO_CRED_ID=\"{config['caltopo_credentials']['id']}\"")
        env_content.append(f"export CALTOPO_CRED_SECRET=\"{config['caltopo_credentials']['secret']}\"")
    
    if env_content:
        with open('.env', 'w') as f:
            f.write('\n'.join(env_content))
        print("📝 Created .env file with API keys")
        print("   Run: source .env")

def main():
    banner()
    
    # Check dependencies
    if not test_imports():
        print("\n⚠️  Install dependencies first, then run this script again.")
        sys.exit(1)
    
    # Get configuration
    config = get_config()
    if not config:
        print("❌ Configuration failed")
        sys.exit(1)
    
    # Save config
    save_config(config)
    
    # Create env file if needed
    create_env_file(config)
    
    # Test Weather API
    if 'home_location' in config:
        test_weather_api(
            config['home_location']['lat'],
            config['home_location']['lon']
        )
    
    # Final instructions
    print("\n" + "="*50)
    print("🎉 SETUP COMPLETE!")
    print("="*50)
    print("\n📋 Next Steps:")
    print("   1. Open ski-tour-app-v2.html in your browser")
    print("   2. Enter the coordinates you just configured")
    print("   3. Start planning your tours!")
    print("\n💡 Tips:")
    print("   - Edit sampleTours array to add your routes")
    print("   - Check SKI_TOUR_GUIDE.md for full docs")
    print("   - Update your fitness level honestly each day")
    print("\n🏔️  Stay safe out there!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled")
        sys.exit(0)
