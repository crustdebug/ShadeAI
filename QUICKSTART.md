# ShadeAI Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 2: Test with Command Line

```bash
# Analyze any image with a face
python shadeai_cli.py test1.jpg
```

Expected output:
```
🔍 Analyzing: test1.jpg
============================================================
Stage 1: Preprocessing...
Stage 2: Face Detection...
   ✓ Face detected (confidence: 0.900)
Stage 3: Skin Segmentation...
   ✓ Extracted 12,345 skin pixels
Stage 4: Feature Extraction...
   ✓ ITA°: 35.42
   ✓ Mean LAB: L*=72.15, a*=8.23, b*=18.67
Stage 5: Classification...
   ✓ Skin Tone: MST-03 Light (Light)
   ✓ Undertone: Warm — Golden, peachy, or yellow undertones
Stage 6: Shade Recommendation...

============================================================
📊 RESULTS
============================================================
Skin Tone:  MST-03 Light
Group:      Light
Undertone:  Warm
ITA°:       35.42
Inference:  87.3 ms

🏆 TOP 5 FOUNDATION SHADE RECOMMENDATIONS
============================================================

1. MAC — NC15
   Product:   Studio Fix Fluid
   Undertone: Warm
   Match:     ✅ ΔE = 2.145
   Buy:       https://www.maccosmetics.com
...
```

### Step 3: Launch Web Application

**Terminal 1 - Start Backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 - Start Frontend:**
```bash
streamlit run streamlit_app.py
```

**Open Browser:**
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

### Step 4: Upload Your Photo

1. Go to http://localhost:8501
2. Read the photo guidelines
3. Upload a clear, well-lit selfie
4. Click "🔍 Analyze My Skin Tone"
5. Get your personalized shade recommendations!

## 🐳 Docker Quick Start

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access:
# - Frontend: http://localhost:8501
# - Backend: http://localhost:8000
```

## 📸 Photo Tips for Best Results

### Perfect Photo Checklist:
- ✅ Natural daylight (near window, overcast day)
- ✅ Face forward, looking at camera
- ✅ Neutral background (white wall)
- ✅ No makeup or light makeup only
- ✅ Hair pulled back from face
- ✅ 30-50cm from camera

### Common Mistakes:
- ❌ Using flash
- ❌ Strong shadows on face
- ❌ Side profile or angled
- ❌ Heavy makeup/filters
- ❌ Colored lighting

## 🧪 Test with Sample Images

```bash
# Test with different images
python shadeai_cli.py test1.jpg
python shadeai_cli.py test2.png
python shadeai_cli.py ayush.png
```

## 🔧 Troubleshooting

### "No face detected"
- Ensure face is clearly visible and forward-facing
- Check lighting - avoid too dark or too bright
- Try a different photo

### "Could not extract sufficient skin pixels"
- Improve lighting conditions
- Remove glasses/accessories covering face
- Ensure face takes up reasonable portion of image

### "Module not found" errors
- Run: `pip install -r requirements.txt`
- Ensure you're in the correct directory
- Activate virtual environment if using one

### Backend connection error
- Ensure backend is running: `uvicorn backend.main:app --reload`
- Check port 8000 is not in use
- Verify API_URL in streamlit_app.py

## 📚 Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Read Full Documentation**: See README_SHADEAI.md
3. **Understand the Pipeline**: Check implementation_plan.md
4. **Customize Database**: Edit backend/data/foundation_shades.json

## 🎯 Key Features

- **10-Class MST Scale**: Monk Skin Tone classification
- **Undertone Detection**: Warm, Cool, or Neutral
- **CIEDE2000 Matching**: Industry-standard color difference (ΔE < 3.0)
- **30 Foundation Shades**: MAC, Fenty, Maybelline, NARS, L'Oréal
- **Fast Inference**: < 100ms per image

## 💡 Pro Tips

1. **Best Time to Take Photo**: Morning or late afternoon with natural light
2. **Best Location**: Near a window on an overcast day
3. **Camera Distance**: Arm's length (30-50cm)
4. **Background**: Plain white or light-colored wall
5. **Preparation**: Remove makeup, tie back hair, clean face

Enjoy using ShadeAI! 💄✨
