# ⛷️ Ski Tour Decision Dashboard

A web-based decision support tool for backcountry skiers in the Pacific Northwest. Get real-time avalanche forecasts, weather data, snow conditions, and personalized tour recommendations all in one place.

**🌐 Live App:** [https://norat18.github.io/ski-tour-app/](https://norat18.github.io/ski-tour-app/)

---

## 🎯 Features

### 📍 Zone Selection
- **11 NWAC forecast zones** covering Washington and Oregon
- West Slopes: Mt Baker, Stevens Pass, Central, Snoqualmie, White Pass
- East Slopes: North, Central (Mission Ridge), South
- Olympics and Mt Hood

### 📅 Date Planning
- Select tour dates up to 7 days in advance
- Weather forecasts update for selected date
- Warning displayed when viewing future dates (avalanche forecast is daily)

### 🏔️ Live Avalanche Data
- **Source:** [Avalanche.org](https://avalanche.org) API (aggregates NWAC data)
- Displays current danger rating with official color coding
- Travel advice based on conditions
- Direct links to full NWAC forecast

### ⛅ Weather Forecasts
- **Source:** [National Weather Service](https://weather.gov) API
- Temperature (high/low for selected date)
- Wind speed and conditions
- Detailed forecast text
- 7-day forecast support

### ❄️ Snow Conditions
- **Source:** [Synoptic Data](https://synopticdata.com) API (same source as OpenSnow)
- Current snow depth at nearest high-elevation station
- 24-hour new snowfall
- 7-day snowfall totals
- Station name and elevation displayed

### 🎯 Personalized Tour Recommendations
- **199+ ski tours** across all zones
- Dual slider system:
  - **Energy Level (1-10):** How you're feeling today
  - **Skill Level (1-10):** Your backcountry experience
- Smart matching algorithm considers:
  - Elevation gain and distance
  - Terrain difficulty (slope angle, exposure)
  - Special requirements (glacier, couloir, alpine)
- Color-coded recommendations: ✅ Go / ⚠️ Maybe / 🛑 Not Today
- **"New Top 5" button** to explore more tour options

---

## 🧮 Recommendation Algorithm

The algorithm calculates a match score based on your profile and tour characteristics:

### Physical Difficulty (based on elevation gain)
| Elevation Gain | Difficulty Rating |
|----------------|-------------------|
| < 1,000 ft | 1 |
| 1,000 - 1,500 ft | 2 |
| 1,500 - 2,000 ft | 3 |
| 2,000 - 2,500 ft | 4 |
| 2,500 - 3,000 ft | 5 |
| 3,000 - 4,000 ft | 6 |
| 4,000 - 5,000 ft | 7 |
| 5,000 - 6,500 ft | 8 |
| 6,500 - 8,000 ft | 9 |
| 8,000+ ft | 10 |

*Distance adjustments: +0.5 at 10mi, +0.5 at 14mi, +1 at 18mi, +1 at 25mi*

### Technical Difficulty (based on terrain)
| Terrain Type | Difficulty Rating |
|--------------|-------------------|
| Mellow, < 25° | 1-2 |
| Treed, 25-30° | 2-3 |
| Moderate, 30-35° | 4 |
| Steep, 35-40° | 5 |
| Very steep, 40-45° | 7 |
| Couloir, 45-50° | 8-9 |
| Extreme, 50°+ | 9-10 |

*Modifiers: Glacier +3, Exposed +1, Ridge +0.5, Alpine +0.5, High elevation +0.5 to +2*

### Matching Logic
- **Ideal match:** Tour difficulty is 0-2 points below your level → +3 points
- **Comfortable:** Tour is 2-4 points easier → +2 points
- **Challenging:** Tour is 1-2 points harder → 0 to -2 points
- **Too hard:** Tour is 3+ points harder → -3 to -5 points
- **Synergy bonus:** Good match on BOTH fitness and skill → +2 points

### Recommendation Tiers
| Score | Recommendation |
|-------|----------------|
| 5+ | ✅ Perfect Match |
| 3 to 5 | ✅ Good Choice |
| 1 to 3 | ⚠️ Doable |
| -1 to 1 | ⚠️ Stretch |
| -3 to -1 | 🛑 Not Ideal |
| < -3 | 🛑 Not Today |

### Special Considerations
- **Glacier terrain:** Requires skill ≥ 6, warns about crevasse rescue
- **Couloir skiing:** Requires skill ≥ 7
- **High alpine (10,000+ ft):** Adds difficulty for lower skill/fitness
- **Long days (6,000+ ft or 20+ mi):** Requires fitness ≥ 6
- **Multi-day (10,000+ ft or 30+ mi):** Requires both fitness and skill ≥ 7

---

## 🛠️ Technical Details

### Data Sources
| Data | Source | Update Frequency |
|------|--------|------------------|
| Avalanche Forecast | [Avalanche.org API](https://avalanche.org) | Daily at 6 PM |
| Weather | [NWS API](https://weather.gov) | Hourly |
| Snow Conditions | [Synoptic Data API](https://synopticdata.com) | Varies by station |
| Tour Database | Built-in | Static |

### API Endpoints Used
```
# Avalanche (no auth required)
GET https://api.avalanche.org/v2/public/products/map-layer/NWAC

# Weather (no auth required)
GET https://api.weather.gov/points/{lat},{lon}
GET https://api.weather.gov/gridpoints/{office}/{x},{y}/forecast

# Snow Data (requires free API key)
GET https://api.synopticdata.com/v2/stations/latest?token={key}&radius={lat},{lon},50&vars=snow_depth,snow_accum...
GET https://api.synopticdata.com/v2/stations/precip?token={key}&radius={lat},{lon},50&start={date}&end={date}
```

### Setting Up Snow Data
1. Sign up for free at [Synoptic Data](https://customer.synopticdata.com/signup)
2. Get your API token (free tier: 5,000 requests/month)
3. Edit `index.html` and replace `YOUR_SYNOPTIC_TOKEN` with your token:
```javascript
const SYNOPTIC_TOKEN = 'your-token-here';
```

---

## 📁 Project Structure

```
ski-tour-app/
├── index.html      # Complete single-file application
└── README.md       # This file
```

The entire app is contained in a single HTML file with embedded CSS and JavaScript for easy deployment.

---

## 🚀 Deployment

### GitHub Pages (Recommended)
1. Fork this repository
2. Go to Settings → Pages
3. Set source to "Deploy from a branch"
4. Select `main` branch and `/ (root)` folder
5. Your app will be live at `https://yourusername.github.io/ski-tour-app/`

### Local Development
Simply open `index.html` in a web browser. No build tools required.

---

## 🗺️ Tour Database

Tours are organized by NWAC zone in the `toursByZone` object. Each tour has:

```javascript
{
  name: "Tour Name",
  location: "Area",
  elevationGain: 3500,      // feet
  distance: 10,              // miles round-trip
  maxElevation: 7500,        // feet
  aspect: "North",           // or "Multiple", "South", etc.
  terrain: "Open slopes, 35-40°"  // description with slope angle
}
```

### Adding Tours
Edit the `toursByZone` object in `index.html`:

```javascript
const toursByZone = {
  'stevens-pass': [
    { name: "New Tour", location: "Stevens Pass", elevationGain: 2500, distance: 8, maxElevation: 6000, aspect: "North", terrain: "Treed, 30-35°" },
    // ... more tours
  ],
  // ... other zones
};
```

---

## ⚠️ Disclaimer

**This is a decision support tool, not a replacement for proper backcountry education and judgment.**

- Always check the official [NWAC forecast](https://nwac.us) before heading out
- Take an avalanche course and carry rescue gear
- Make your own informed decisions in the backcountry
- Conditions change rapidly in the mountains

---

## 🤝 Contributing

Contributions welcome! Here's how you can help:

- **Add tours:** Submit PRs with new tour data for any zone
- **Bug reports:** Open an issue with steps to reproduce
- **Feature requests:** Open an issue describing the feature
- **Code improvements:** Fork, make changes, submit PR

---

## 📜 License

MIT License - feel free to use, modify, and distribute.

---

## 🙏 Acknowledgments

- [Northwest Avalanche Center (NWAC)](https://nwac.us) - Avalanche forecasting
- [National Avalanche Center](https://avalanche.org) - API and data aggregation
- [National Weather Service](https://weather.gov) - Weather data
- [Synoptic Data](https://synopticdata.com) - Snow observations
- [CalTopo](https://caltopo.com) - Mapping inspiration

---

Built with ❄️ for the PNW backcountry community
