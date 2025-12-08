# ⛷️ Ski Tour Decision Dashboard

**A smart web app to help you choose the best ski tour based on avalanche conditions, weather, and how you're feeling.**

Built with vibe coding principles - start simple, iterate fast, make it work!

## 🎯 What This Does

Combines multiple data sources to give you intelligent tour recommendations:

- 🏔️ **Avalanche forecasts** from NWAC
- ⛅ **Weather data** from Weather.gov (live!)
- 📍 **Your tour routes** from CalTopo
- 💪 **Personal fitness** tracking
- 🎯 **Smart recommendations** that factor everything

## 🚀 Quick Start

1. Open `ski-tour-app-v2.html` in your browser
2. Enter your coordinates (Seattle: `47.606, -122.332`)
3. Pick your NWAC zone
4. Add your fitness level
5. Get recommendations!

## 📦 What's Included

- **ski-tour-app-v2.html** - Main web application (use this one!)
- **ski_tour_api.py** - Python backend for API integration
- **SKI_TOUR_GUIDE.md** - Complete setup & customization guide
- **ski-tour-app.html** - Original demo version

## ⚡ Key Features

### Already Working ✅
- Real-time weather from Weather.gov
- Personal fitness tracking
- Tour comparison
- Recommendation algorithm
- Mobile responsive
- Saves your settings

### Easy To Add 🔧
- Your custom tour list (edit the `sampleTours` array)
- Additional NWAC zones
- Custom recommendation logic
- More weather metrics

### Requires API Setup 🔑
- Full NWAC integration (email them)
- CalTopo Team API ($100/year)
- OpenSnow API (commercial partnership)

## 🎨 Design Philosophy

This app uses a **topographic/backcountry aesthetic**:
- Earth tones (burnt orange, forest green)
- Clean typography
- Trustworthy feel
- Professional but approachable

It's designed to feel like a tool you'd actually trust in the mountains.

## 🏔️ Sample Tours Included

1. **Kendall Peak SW** - Snoqualmie Pass classic
2. **Tye Ridge** - Stevens Pass mellow trees
3. **Granite Mountain** - Big summit push

**Add your own:** Edit the tours in the HTML file (instructions in the guide)

## 📊 How It Works

The recommendation algorithm considers:

1. **Avalanche danger** level (biggest factor)
2. **Your fitness** vs elevation gain
3. **Terrain type** (treed vs exposed)
4. **Weather conditions** (temp, wind)

Output: Go / Cautious / Skip It

## 🔒 Safety First

**⚠️ This is a decision SUPPORT tool, not a decision MAKER.**

Always:
- Check official forecasts
- Have proper training
- Use correct gear
- Travel with partners
- Trust your judgment

## 🛠️ Customization

Want to modify it?

- **Add tours:** Edit `sampleTours` array
- **Change zones:** Add to dropdown
- **Adjust scoring:** Modify `calculateRecommendation()`
- **New features:** Check the guide for ideas

## 📖 Full Documentation

See **SKI_TOUR_GUIDE.md** for:
- Complete API setup instructions
- How to get API keys
- Customization examples
- Troubleshooting guide
- Future enhancement ideas

## 🐛 Known Limitations

- NWAC forecast requires manual scraping or API access
- OpenSnow API needs commercial partnership
- CalTopo integration needs Team account for full features
- Tours must be added manually (for now)

## 🚀 Next Steps

**Right now:**
1. Open the app and enter your info
2. Add your favorite tours to the list
3. Use it tomorrow morning!

**Soon:**
1. Email NWAC for API access
2. Consider CalTopo Team if you use it heavily
3. Build out your custom features

**Later:**
1. Add historical tracking
2. Share with your ski partners
3. Contribute improvements back!

## 💻 Tech Stack

- **Frontend:** Vanilla HTML/CSS/JavaScript (no dependencies!)
- **APIs:** Weather.gov, NWAC, CalTopo, OpenSnow
- **Backend:** Python (optional)
- **Storage:** LocalStorage (all client-side)

## 🤝 Contributing

This is a personal vibe coding project, but feel free to:
- Fork it and make it your own
- Share improvements
- Report bugs
- Suggest features

## 📝 License

Built for the backcountry community. Use responsibly and stay safe!

---

**Built with ❄️ for powder days and ☕ for early mornings.**

**Happy touring! 🎿**
