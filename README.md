# 🚇 Hyderabad Metro Journey Planner

**Find the best way to travel in Hyderabad using a mix of taxi and metro!**

## 🌟 What This App Does

Imagine you want to go from your home to a shopping mall. This app finds the smartest way to get there by combining:
- 🚗 **Taxi** from your home to the nearest metro station
- 🚇 **Metro** ride between stations  
- 🚗 **Taxi** from the metro station to your destination

**It's like having a smart travel assistant that knows all the best routes!**

## 🎯 Why Use This App?

✅ **Saves Time**: Finds the fastest routes automatically  
✅ **Saves Money**: Shows you the most cost-effective options  
✅ **No More Confusion**: Clear step-by-step directions  
✅ **Real Traffic Data**: Uses live traffic information  
✅ **Multiple Options**: Shows you 5 different route choices  

## 🚀 How to Use (Super Simple!)

### **Step 1: Open the App**
- Run the app: `python app.py`
- Open your browser and go to: `http://localhost:5000`

### **Step 2: Enter Your Journey**
- Type your starting address (e.g., "My Home")
- Type your destination (e.g., "Hitech City Mall")
- Click "Find Route" 

### **Step 3: Choose Your Route**
The app shows you 5 different options:
1. **Fastest Route** - Gets you there quickest
2. **Most Convenient** - Easiest journey with fewer changes
3. **Cheapest** - Best value for money
4. **Same Metro Line** - No need to change trains
5. **Direct Route** - Just taxi (if it's faster)

### **Step 4: Book Your Journey**
- Click "Preview" to see route details
- Click "Book" to reserve your journey
- Get confirmation and travel details

## 🎨 What You'll See

### **Route Information**
- 📍 **Starting Point**: Your exact location
- 🚗 **Taxi 1**: Home → Metro Station (time & cost)
- 🚇 **Metro**: Station → Station (time & fare)
- 🚗 **Taxi 2**: Metro Station → Destination (time & cost)
- ⏱️ **Total Time**: Complete journey duration
- 💰 **Total Cost**: Complete journey cost

### **Smart Features**
- 🎯 **Station Finder**: Automatically finds nearest metro stations
- 🚦 **Traffic Aware**: Considers current traffic conditions
- 🔄 **Interchange Info**: Shows if you need to change metro lines
- 📱 **Mobile Friendly**: Works perfectly on phones and tablets

## 🏗️ How It Works Behind the Scenes

### **The Smart Brain**
1. **Finds Nearest Stations**: Locates the 7 closest metro stations to your start and end points
2. **Calculates Taxi Routes**: Works out taxi times and costs to/from each station
3. **Checks Metro Routes**: Finds metro connections between stations
4. **Combines Everything**: Creates 49 different route combinations
5. **Ranks Routes**: Uses smart scoring to show you the best options

### **Smart Scoring System**
- **Same Metro Line**: Gets bonus points (no changing trains!)
- **Short Taxi Rides**: Preferred over long taxi journeys
- **Interchange Routes**: Scored based on taxi distance
- **Overall Convenience**: Balances time, cost, and ease

## 🛠️ For Developers

### **What You Need**
- Python 3.7+
- Google Maps API key
- Internet connection

### **Quick Setup**
```bash
# Install Python packages
pip install -r requirements.txt

# Add your Google Maps API key to .env file
echo "GOOGLE_MAPS_API_KEY=your_key_here" > .env

# Run the app
python app.py
```

### **Files Explained**
- `app.py` - Main web application
- `station_finder.py` - Route calculation engine
- `custom_route_calculator.py` - Manual route builder
- `hyderabad_metro_stations.py` - Metro station database
- `templates/index.html` - User interface

## 🌍 Real-World Example

**Journey**: Home in Banjara Hills → Office in Hitech City

**What the App Finds**:
1. **Option 1**: Taxi → Ameerpet Metro → Green Line → Hitech City → Taxi
   - Time: 45 minutes
   - Cost: ₹180
   - Convenience: ⭐⭐⭐⭐⭐

2. **Option 2**: Taxi → Begumpet Metro → Blue Line → Ameerpet → Green Line → Hitech City → Taxi
   - Time: 52 minutes  
   - Cost: ₹165
   - Convenience: ⭐⭐⭐⭐

3. **Option 3**: Direct taxi
   - Time: 35 minutes
   - Cost: ₹350
   - Convenience: ⭐⭐⭐

**Smart Choice**: Option 1 - saves money, good time, no metro changes!

## 🎯 Perfect For

- 🏠 **Daily Commuters**: Find the best route to work
- 🛍️ **Shoppers**: Plan trips to malls and markets
- 🏥 **Medical Visits**: Navigate to hospitals and clinics
- 🎓 **Students**: Plan routes to colleges and universities
- 🚶 **Tourists**: Explore Hyderabad efficiently
- 🏢 **Business Travel**: Professional meetings and conferences

## 💡 Tips for Best Results

1. **Use Specific Addresses**: "Hitech City Mall" works better than "Hitech City"
2. **Check Multiple Options**: Don't just pick the first route
3. **Consider Time of Day**: Traffic affects taxi times
4. **Metro Frequency**: Some lines have more frequent trains
5. **Interchange Stations**: Ameerpet is a major interchange hub

## 🆘 Need Help?

### **Common Issues**
- **"No routes found"**: Try a different address or nearby landmark
- **"API error"**: Check your internet connection
- **"Loading..." takes long**: The app is calculating many route options

### **Best Practices**
- Use Google Places autocomplete for accurate addresses
- Try both "Auto" and "Manual" modes
- Check the terminal for detailed route calculations

## 🎉 What Makes This Special

✨ **Hyderabad-Focused**: Built specifically for Hyderabad metro network  
✨ **Real-Time Data**: Uses live traffic and current conditions  
✨ **Smart Algorithms**: Finds routes humans might miss  
✨ **User-Friendly**: Simple interface for everyone  
✨ **Cost-Aware**: Shows you exactly what you'll pay  
✨ **Time-Optimized**: Gets you there as fast as possible  

---

**🚇 Built with love for Hyderabad commuters! 🚇**

*Making your daily journeys smarter, faster, and more convenient.* 