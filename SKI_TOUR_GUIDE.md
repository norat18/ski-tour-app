# Ski Tour Decision App - Setup & Usage Guide

## 🎿 What We Built

A smart web app that helps you decide where to ski tour by combining:
- **Avalanche forecasts** from NWAC
- **Weather data** from Weather.gov
- **Your saved tour routes** from CalTopo
- **Personal fitness tracking**
- **Intelligent recommendations** based on all factors

## 📁 Files Created

1. **ski-tour-app-v2.html** - The main web application
2. **ski_tour_api.py** - Python backend for API integration
3. **ski-tour-app.html** - Original demo version

## 🚀 Quick Start

### Option 1: Use the Web App Directly

1. Open `ski-tour-app-v2.html` in your browser
2. Enter your home coordinates (get from Google Maps by dropping a pin)
3. Select your NWAC zone
4. Optionally add your CalTopo map ID
5. Click "Load Dashboard"

The app will:
- ✅ Fetch real Weather.gov data (works immediately!)
- ⚠️ Show placeholder NWAC data (requires custom scraping)
- 📍 Load your saved tours
- 🎯 Calculate smart recommendations

### Option 2: Run Python Backend

For full API integration:

```bash
# Install dependencies
pip install requests --break-system-packages

# Set up API keys (optional)
export OPENSNOW_API_KEY="your_key_here"
export CALTOPO_CRED_ID="your_cred_id"
export CALTOPO_CRED_SECRET="your_secret"

# Run the backend
python3 ski_tour_api.py
```

## 🔑 API Setup Guide

### 1. Weather.gov API ✅ FREE & WORKING

**Status:** Fully functional, no API key needed!

**What you get:**
- Temperature, wind, conditions
- 7-day forecast
- Hourly breakdown

**Already integrated:** The web app fetches this automatically.

### 2. NWAC Avalanche Forecasts 🟡 MANUAL

**Status:** No official public API (yet)

**Options:**
1. **Manual check:** Link to NWAC.us (current approach)
2. **Email NWAC:** Contact forecasters@nwac.us to request API access
3. **Build scraper:** Scrape their website (check robots.txt first)

**What you'd get with API:**
- Danger ratings by elevation
- Avalanche problems
- Bottom line summary
- Recent observations

### 3. OpenSnow 🔴 COMMERCIAL ONLY

**Status:** Requires commercial partnership

**What you get (if you get access):**
- Proprietary PEAKS forecast model
- Snow depth and accumulation
- Storm tracking
- Mountain-specific conditions

**Your paid account gives you:**
- Web/app access
- Expert daily forecasts
- But NOT API access (different product)

**To get API access:**
- Email: partnerships@opensnow.com
- Explain you're building a personal tool
- They may require a partnership agreement

**Workaround:** 
Keep using the OpenSnow app/website manually alongside this tool.

### 4. CalTopo 🟢 MOSTLY WORKING

**Status:** Public maps accessible, Team API available

**What works now:**
- Public map viewing
- Route coordinates (manual entry)

**For full integration:**
Need CalTopo Team account ($100/year):
1. Sign up at caltopo.com/teams
2. Create a service account
3. Get credential ID and secret
4. Use official Team API

**Team API gives you:**
- Programmatic map access
- Route/waypoint data
- Collaborative features
- Live tracking integration

**Workaround for now:**
Manually add your tour names/stats in the app.

## 🏔️ Adding Your Tours

Since full CalTopo API requires Team account, here's how to add tours manually:

### Edit the Sample Tours

In `ski-tour-app-v2.html`, find the `sampleTours` array (around line 467):

```javascript
const sampleTours = [
    {
        name: "YOUR TOUR NAME",
        location: "Trailhead Area",
        elevationGain: 3200,      // feet
        distance: 4.5,            // miles round trip
        maxElevation: 5784,       // feet
        aspect: "SW",             // compass direction
        terrain: "35-40° open slopes"  // description
    },
    // Add more tours...
];
```

### Quick Tour Template

```javascript
{
    name: "Kendall Peak SW",
    location: "Snoqualmie Pass", 
    elevationGain: 3200,
    distance: 4.5,
    maxElevation: 5784,
    aspect: "SW",
    terrain: "35-40° open slopes"
},
{
    name: "Chair Peak NE Couloir",
    location: "Alpental",
    elevationGain: 3800,
    distance: 6.5,
    maxElevation: 6238,
    aspect: "NE",
    terrain: "40-45° couloir"
}
```

## 🎯 How Recommendations Work

The app calculates a score based on:

1. **Avalanche Danger** (-5 to +2 points)
   - Low: +2
   - Moderate: +1
   - Considerable: -1
   - High: -3
   - Extreme: -5

2. **Fitness vs Effort**
   - Light tour + decent fitness: +2
   - Moderate tour + good fitness: +1
   - Big tour + lower fitness: -2

3. **Terrain Type**
   - Treed/protected: +1
   - Exposed/ridge: -1

4. **Weather Factors**
   - Very cold (<10°F): -1
   - High winds (>25mph): -1

**Final Score:**
- ≥2: ✅ Good to Go
- 0-1: ⚠️ Cautious Go  
- <0: 🛑 Skip It

## 🔧 Customization Ideas

### 1. Add More Zones

Edit the zone dropdown in the setup panel:

```html
<option value="custom-zone-id">Custom Zone Name</option>
```

### 2. Adjust Recommendation Algorithm

In `calculateRecommendation()` function, modify the scoring logic to match your risk tolerance.

### 3. Add More Weather Metrics

The Weather.gov API provides:
- Dewpoint
- Humidity
- Precipitation probability
- Sky cover
- Hazard warnings

Add these to the weather display grid.

### 4. Save Favorite Tours

Add localStorage for tour management:

```javascript
// Save tours
localStorage.setItem('myTours', JSON.stringify(tours));

// Load tours
const saved = JSON.parse(localStorage.getItem('myTours'));
```

### 5. Add Notifications

Use browser notifications when conditions are good:

```javascript
if (Notification.permission === "granted") {
    new Notification("Great day for Tye Ridge!", {
        body: "Low danger + fresh snow = go!"
    });
}
```

## 📊 Sample Workflow

**Saturday morning:**

1. Open your dashboard
2. Check fitness slider (honest assessment!)
3. Review avalanche danger
4. See weather conditions
5. Look at tour recommendations
6. Pick your tour
7. Check NWAC.us for latest details
8. Have a great day!

## 🐛 Troubleshooting

### Weather Not Loading

- Check your coordinates format: `47.606, -122.332`
- Make sure you have internet connection
- Weather.gov API rate limits: wait 5 seconds and retry

### Tours Not Showing

- Make sure `sampleTours` array has data
- Check browser console (F12) for errors
- Verify tour objects have all required fields

### Recommendations Seem Wrong

- Adjust your fitness level honestly
- Check the tour elevation gain is accurate
- Review the scoring algorithm

## 🚀 Future Enhancements

### Phase 1 (Easy)
- [ ] Add more NWAC zones
- [ ] Export tour plans as PDF
- [ ] Mobile app version
- [ ] Dark mode

### Phase 2 (Medium)
- [ ] Custom NWAC scraper
- [ ] CalTopo Team API integration
- [ ] Historical tracking (where I went, conditions)
- [ ] Social sharing

### Phase 3 (Advanced)
- [ ] Machine learning for better recommendations
- [ ] Real-time GPS tracking integration
- [ ] Group coordination features
- [ ] Automated alerts when conditions improve

## 🤝 Getting API Access - Summary

**Priority Order:**

1. ✅ **Weather.gov** - Already working!
2. 🟡 **NWAC** - Email them for API access
3. 🟢 **CalTopo** - Get Team account ($100/yr)
4. 🔴 **OpenSnow** - Contact for partnership (or use manually)

## 📝 Important Notes

### Safety Disclaimer

⚠️ **This is a decision SUPPORT tool, not a decision MAKER.**

Always:
- Check official avalanche forecasts
- Use proper backcountry gear
- Have avalanche training
- Travel with partners
- Tell someone your plans
- Trust your gut

### Data Freshness

- Weather.gov: Updates hourly
- NWAC: Published daily at 6pm (winter)
- Your fitness: Update honestly each day!

### Privacy

- All data stored locally in your browser
- No tracking or analytics
- Your API keys stay on your machine

## 💡 Pro Tips

1. **Bookmark the app** - Add to home screen on mobile
2. **Update fitness honestly** - It affects recommendations
3. **Check NWAC comments** - The app can't capture expert nuance
4. **Use with other tools** - Complement with Mountain Forecast, etc.
5. **Share with partners** - Send them the link!
6. **Keep tours updated** - Add new routes as you discover them

## 🆘 Need Help?

For issues with:
- **Weather.gov API**: Check their docs at weather.gov/documentation/services-web-api
- **NWAC**: Email forecasters@nwac.us
- **CalTopo**: Help docs at training.caltopo.com
- **OpenSnow**: Contact partnerships@opensnow.com

## 📜 License & Credits

**Built with:**
- Weather.gov API (public domain)
- NWAC data (public service)
- CalTopo (with respect to their terms)
- Your expertise and local knowledge!

**Vibe Coded** with ❄️ and ☕ for the backcountry community.

Stay safe out there! 🎿⛷️
