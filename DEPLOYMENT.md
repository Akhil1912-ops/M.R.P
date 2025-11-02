# 🚀 Deployment Guide - Bengaluru Metro Journey Planner

## 📋 Quick Summary

**Currently**: Running on `localhost:5002` (only you can access)  
**Goal**: Deploy to a public domain so anyone can use it

---

## 🌐 Best Deployment Options (Easiest First)

### **Option 1: Render.com** ⭐ RECOMMENDED (Easiest + Free)

**Why**: Free tier available, automatic HTTPS, easy setup

**Steps**:

1. **Create Account**: Go to [render.com](https://render.com) and sign up

2. **Create New Web Service**:
   - Click "New" → "Web Service"
   - Connect your GitHub repository (or upload code)

3. **Configure Service**:
   - **Name**: `bengaluru-metro-planner`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn bengaluru_app:app --bind 0.0.0.0:$PORT`
   - **Port**: `5002` (or leave blank for auto)

4. **Add Environment Variables**:
   - Go to "Environment" tab
   - Add: `GOOGLE_MAPS_API_KEY` = `your_api_key_here`

5. **Deploy**: Click "Create Web Service"
   - Takes ~5 minutes
   - You'll get a URL like: `https://bengaluru-metro-planner.onrender.com`

6. **Custom Domain** (Optional):
   - Go to "Settings" → "Custom Domain"
   - Add your domain name

**Cost**: FREE (with limitations) or $7/month for better performance

---

### **Option 2: Railway.app** ⚡ Fast Deployment

**Why**: Very fast, pay-as-you-go pricing

**Steps**:

1. **Sign up**: Go to [railway.app](https://railway.app)

2. **New Project**: Click "New Project" → "Deploy from GitHub"

3. **Configure**:
   - **Start Command**: `gunicorn bengaluru_app:app --bind 0.0.0.0:$PORT`
   - **Port**: Auto-detected

4. **Add Environment Variables**:
   - Click "Variables" tab
   - Add: `GOOGLE_MAPS_API_KEY`

5. **Deploy**: Automatic after setup

**Cost**: $5/month credit (pay as you go)

---

### **Option 3: PythonAnywhere** 🐍 Python-Specific

**Why**: Great for Python apps, simple interface

**Steps**:

1. **Sign up**: [pythonanywhere.com](https://www.pythonanywhere.com) (free tier available)

2. **Upload Files**:
   - Go to "Files" tab
   - Upload all project files

3. **Create Web App**:
   - Go to "Web" tab → "Add a new web app"
   - Choose Flask, Python 3.10
   - Set WSGI file to: `/home/yourusername/bengaluru_app.py`

4. **Configure**:
   - Add environment variables in "Web" → "Static files" and "WSGI configuration"
   - Set `GOOGLE_MAPS_API_KEY` in WSGI file or environment

5. **Reload**: Click "Reload" button

**Cost**: FREE (basic) or $5/month (hacker plan)

---

### **Option 4: Heroku** 💜 Classic Choice

**Why**: Very popular, good documentation

**Steps**:

1. **Install Heroku CLI**: [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login**:
   ```bash
   heroku login
   ```

3. **Create App**:
   ```bash
   heroku create bengaluru-metro-planner
   ```

4. **Set Environment Variable**:
   ```bash
   heroku config:set GOOGLE_MAPS_API_KEY=your_key_here
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   ```

**Cost**: $5/month (no free tier anymore)

---

## 🔧 Important Changes for Production

### 1. **Update Flask App for Production**

The current `bengaluru_app.py` runs in debug mode. For production, you should:

```python
# At the bottom of bengaluru_app.py
if __name__ == '__main__':
    # Development
    app.run(debug=True, host='0.0.0.0', port=5002)
```

This is fine because production servers (like gunicorn) won't use this block.

### 2. **Environment Variables**

Make sure `GOOGLE_MAPS_API_KEY` is set in your deployment platform's environment variables (NOT in code).

### 3. **Port Configuration**

- **Render/Railway**: Use `$PORT` environment variable (auto-set)
- **PythonAnywhere**: Usually port 80 or 443
- **Heroku**: Uses `$PORT` automatically

### 4. **HTTPS**

All platforms above provide HTTPS automatically. Make sure your Google Maps API key allows HTTPS origins.

---

## 🔐 Security Checklist

- [ ] API key is in environment variables (NOT in code)
- [ ] `.env` file is in `.gitignore`
- [ ] Google Maps API key has HTTPS origins allowed
- [ ] CORS is configured (already done with Flask-CORS)

---

## 📱 Testing After Deployment

1. **Visit your deployed URL**
2. **Test a route**: Enter two addresses
3. **Check terminal logs** (if available on platform)
4. **Test on mobile** to ensure responsive design works

---

## 🌍 Custom Domain Setup

After deployment, you can add a custom domain:

1. **Buy domain**: From Namecheap, GoDaddy, etc.
2. **Add DNS records**: Point to your deployment platform
3. **Configure in platform**: Add custom domain in settings

---

## 🆘 Common Issues

### **"Module not found"**
- Make sure `requirements.txt` includes all dependencies
- Check build logs for missing packages

### **"Port already in use"**
- Remove hardcoded port, use `$PORT` environment variable
- Update start command: `gunicorn bengaluru_app:app --bind 0.0.0.0:$PORT`

### **"API key error"**
- Check environment variable is set correctly
- Verify API key allows your deployment URL in Google Cloud Console

### **"Timeout errors"**
- Increase timeout in gunicorn config
- Check Google Maps API quota limits

---

## 💡 Recommendation

**Start with Render.com** - It's the easiest for beginners:
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Simple setup
- ✅ Good documentation
- ✅ Custom domains supported

---

## 📞 Need Help?

If you get stuck, check:
1. Platform-specific documentation
2. Build/deployment logs
3. Terminal output for errors
4. Google Maps API console for quota/errors

**Happy Deploying! 🚀**

