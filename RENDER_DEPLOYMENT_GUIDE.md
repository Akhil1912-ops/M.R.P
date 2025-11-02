# 🚀 Step-by-Step: Deploy to Render.com

## ✅ Prerequisites Checklist

Before starting, make sure you have:
- [ ] GitHub account (or be ready to upload files)
- [ ] Google Maps API key ready
- [ ] All project files committed/ready

---

## 📝 Step-by-Step Instructions

### **STEP 1: Prepare Your Code**

#### **Option A: Using GitHub (Recommended)**

1. **Create GitHub Repository**:
   - Go to [github.com](https://github.com)
   - Click "+" → "New repository"
   - Name: `bengaluru-metro-planner` (or any name)
   - Make it **Public** (or Private with Render account upgrade)
   - Click "Create repository"

2. **Upload Your Code**:
   ```bash
   # In your project folder
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/bengaluru-metro-planner.git
   git push -u origin main
   ```

#### **Option B: Manual Upload (No GitHub)**

You can upload files directly to Render (we'll cover this)

---

### **STEP 2: Sign Up for Render**

1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with:
   - **GitHub** (recommended - auto-connects repos)
   - **Google** 
   - **Email** (email verification required)

---

### **STEP 3: Create Web Service**

1. **After login**, you'll see the Dashboard
2. Click **"New +"** button (top right)
3. Select **"Web Service"**

---

### **STEP 4: Connect Repository**

#### **If using GitHub:**
- Click **"Connect account"** (if not already connected)
- Authorize Render to access GitHub
- Select your repository: `bengaluru-metro-planner`
- Click **"Connect"**

#### **If uploading manually:**
- Click **"Public Git repository"** toggle to turn it OFF
- You'll see option to upload files
- Upload your project folder

---

### **STEP 5: Configure Service Settings**

Fill in these details:

```
Name: bengaluru-metro-planner
    (or any name you like - this will be in your URL)

Region: Singapore (or closest to India)
    (Optional: Choose closest to your users)

Branch: main
    (or master, depending on your Git branch)

Root Directory: (leave empty)
    (if your files are in root folder)

Runtime: Python 3
    (Auto-detected, but verify)

Build Command: pip install -r requirements.txt
    (This installs all dependencies)

Start Command: gunicorn bengaluru_app:app --bind 0.0.0.0:$PORT
    (This starts your app)

Instance Type: Free
    (or upgrade to Starter for $7/month)
```

**Important Settings:**
- ✅ **Auto-Deploy**: Leave ON (deploys on every Git push)
- ✅ **Health Check Path**: Leave blank
- ✅ **Pull Request Previews**: Optional (for testing)

---

### **STEP 6: Add Environment Variable**

**Before clicking "Create Web Service":**

1. Scroll down to **"Environment Variables"** section
2. Click **"Add Environment Variable"**
3. Add:
   ```
   Key: GOOGLE_MAPS_API_KEY
   Value: your_actual_google_maps_api_key_here
   ```
4. Click **"Add"**

⚠️ **Important**: Make sure this is your REAL API key, not placeholder text!

---

### **STEP 7: Deploy!**

1. **Click "Create Web Service"** (bottom of page)
2. Render will start building your app
3. You'll see build logs in real-time
4. Wait **3-5 minutes** for first deployment

---

### **STEP 8: Monitor Deployment**

Watch the build logs:

**You should see:**
```
✅ Cloning repository...
✅ Installing dependencies...
✅ Starting service...
✅ Your service is live!
```

**If you see errors:**
- Check build logs for specific error
- Most common: Missing dependencies, wrong start command

---

### **STEP 9: Get Your URL**

After successful deployment:

1. You'll see: **"Your service is live at..."**
2. Your URL will be: `https://bengaluru-metro-planner.onrender.com`
   (or whatever name you chose)

3. **Click the URL** to open your app!

---

## ✅ Verify Deployment

1. **Open your Render URL** in browser
2. **Test the app**:
   - Enter a starting address
   - Enter destination
   - Click "Find Routes"
   - Should work exactly like localhost!

3. **Check logs** (if needed):
   - Go to Render dashboard
   - Click on your service
   - Click "Logs" tab
   - See all print statements from your Python code

---

## 🔧 Troubleshooting Common Issues

### **Issue: Build Failed**

**Error**: "Module not found"
**Fix**: Check `requirements.txt` has all packages

**Error**: "Port already in use"
**Fix**: Make sure start command uses `$PORT` not hardcoded port

---

### **Issue: App Works but API Key Error**

**Symptom**: Routes not found, API errors
**Fix**: 
1. Go to "Environment" tab
2. Verify `GOOGLE_MAPS_API_KEY` is set correctly
3. Make sure no extra spaces in value
4. Click "Save Changes" and "Manual Deploy"

---

### **Issue: Slow First Load**

**Normal on Free Tier**: First load after 15 min inactivity takes ~30 seconds
**Fix**: Upgrade to Starter plan ($7/month) for instant loading

---

### **Issue: 500 Error**

**Check logs**:
1. Go to "Logs" tab in Render
2. Look for Python errors
3. Common: Missing file (check CSV file path)
4. Common: Environment variable not set

---

## 📱 Adding Custom Domain (Optional)

After deployment works:

1. **Buy domain** (Namecheap, GoDaddy, etc.)
2. **In Render dashboard**:
   - Go to "Settings" tab
   - Scroll to "Custom Domains"
   - Click "Add Custom Domain"
   - Enter your domain
3. **Update DNS**:
   - Render will show DNS records to add
   - Add them in your domain registrar
   - Wait 24-48 hours for DNS propagation

---

## 🔄 Updating Your App

**If using GitHub (Auto-Deploy ON):**
1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```
3. Render automatically redeploys!

**Manual Update:**
1. Go to Render dashboard
2. Click "Manual Deploy" → "Deploy latest commit"

---

## 📊 Monitoring Your App

**Render Dashboard shows:**
- ✅ Service status (Live/Down)
- ✅ Recent deployments
- ✅ Resource usage (CPU, Memory)
- ✅ Logs (real-time)
- ✅ Metrics (requests, response times)

---

## 💰 Pricing Reminder

**Free Tier:**
- ✅ Works great for testing
- ⚠️ Spins down after 15 min inactivity
- ⚠️ First load ~30 seconds after spin-down

**Starter Plan ($7/month):**
- ✅ Always on (instant loading)
- ✅ Better performance
- ✅ 512MB RAM, 0.5 CPU
- ✅ Recommended for public use

---

## ✅ Final Checklist

Before going live:
- [ ] App loads correctly
- [ ] Routes calculation works
- [ ] Google Maps autocomplete works
- [ ] All features tested
- [ ] Environment variable set
- [ ] Logs show no errors

---

## 🎉 You're Done!

Your Bengaluru Metro Journey Planner is now:
- ✅ Accessible from anywhere
- ✅ HTTPS secured
- ✅ Auto-updating (if using GitHub)
- ✅ Production-ready

**Share your URL**: `https://your-app.onrender.com`

---

## 🆘 Need Help?

If you get stuck:
1. Check Render dashboard logs
2. Check terminal output for errors
3. Verify environment variables
4. Test locally first to ensure app works

**Ready to deploy? Follow the steps above!** 🚀

