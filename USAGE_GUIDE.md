# ShadeAI Complete Usage Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Command Line Interface](#command-line-interface)
3. [Web Application](#web-application)
4. [API Usage](#api-usage)
5. [Docker Deployment](#docker-deployment)
6. [Understanding Results](#understanding-results)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python test_installation.py
```

### First Analysis
```bash
# Analyze an image
python shadeai_cli.py test1.jpg
```

---

## Command Line Interface

### Basic Usage
```bash
python shadeai_cli.py <image_path>
```

### Examples
```bash
# Analyze a JPEG
python shadeai_cli.py my_selfie.jpg

# Analyze a PNG
python shadeai_cli.py photo.png

# Analyze test images
python shadeai_cli.py test1.jpg
python shadeai_cli.py test2.png
python shadeai_cli.py ayush.png
```

### Output Format
```
🔍 Analyzing: test1.jpg
============================================================
Stage 1: Preprocessing...
Stage 2: Face Detection...
   ✓ Face detected (confidence: 0.900)
Stage 3: Skin Segmentation...
   ✓ Extracted 9,609 skin pixels
Stage 4: Feature Extraction...
   ✓ ITA°: -15.79
   ✓ Mean LAB: L*=45.68, a*=11.54, b*=15.26
Stage 5: Classification...
   ✓ Skin Tone: MST-08 Brown (Dark)
   ✓ Undertone: Neutral
Stage 6: Shade Recommendation...

============================================================
📊 RESULTS
============================================================
Skin Tone:  MST-08 Brown
Group:      Dark
Undertone:  Neutral
ITA°:       -15.79
Inference:  5789.2 ms

🏆 TOP 5 FOUNDATION SHADE RECOMMENDATIONS
============================================================

1. MAC — NC45
   Product:   Studio Fix Fluid
   Undertone: Warm
   Match:     ⚠️ ΔE = 3.279
   Buy:       https://www.maccosmetics.com
...
```

---

## Web Application

### Starting the Application

**Method 1: Two Terminals**

Terminal 1 - Backend:
```bash
uvicorn backend.main:app --reload --port 8000
```

Terminal 2 - Frontend:
```bash
streamlit run streamlit_app.py
```

**Method 2: Background Process**

```bash
# Start backend in background
uvicorn backend.main:app --reload --port 8000 &

# Start frontend
streamlit run streamlit_app.py
```

### Accessing the Application

- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/api/v1/health

### Using the Web Interface

1. **Open Browser**: Navigate to http://localhost:8501
2. **Read Guidelines**: Expand "📸 How to take the perfect photo"
3. **Upload Photo**: Click "Browse files" or drag & drop
4. **Analyze**: Click "🔍 Analyze My Skin Tone"
5. **View Results**: See skin tone, undertone, and top 5 shade matches
6. **Shop**: Click "🛒 Buy" buttons to visit brand websites

### Web UI Features

- ✅ Photo upload (JPEG, PNG, WEBP)
- ✅ Comprehensive photo guidelines
- ✅ Real-time analysis
- ✅ Color swatches for each shade
- ✅ Match quality indicators (✅ ΔE < 3.0, ⚠️ ΔE ≥ 3.0)
- ✅ Direct purchase links
- ✅ Technical details (ITA°, LAB values, inference time)

---

## API Usage

### Starting the API Server

```bash
uvicorn backend.main:app --reload --port 8000
```

### Endpoints

#### 1. Health Check
```bash
curl http://localhost:8000/api/v1/health
```

Response:
```json
{
  "status": "ok",
  "service": "ShadeAI"
}
```

#### 2. Analyze Image
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -F "file=@photo.jpg"
```

Response:
```json
{
  "skin_tone": {
    "class_index": 7,
    "label": "MST-08 Brown",
    "group": "Dark",
    "confidence": null,
    "probabilities": null,
    "method": "ITA_based"
  },
  "undertone": {
    "score": 0.1,
    "label": "Neutral",
    "description": "Balanced mix of warm and cool undertones"
  },
  "ita_degrees": -15.79,
  "mean_lab": {
    "L": 45.68,
    "a": 11.54,
    "b": 15.26
  },
  "recommendations": [
    {
      "id": "MAC-NC45",
      "brand": "MAC",
      "product": "Studio Fix Fluid",
      "shade_name": "NC45",
      "L": 46.0,
      "a": 14.0,
      "b": 21.0,
      "undertone": "Warm",
      "mst_range": ["MST-07", "MST-08"],
      "hex_approx": "#A87E3C",
      "buy_url": "https://www.maccosmetics.com",
      "delta_e": 3.279,
      "undertone_match": false,
      "within_threshold": false
    }
  ],
  "inference_ms": 5789.2,
  "face_detected": true,
  "face_confidence": 0.900
}
```

### Python API Client

```python
import requests

# Analyze image
with open('photo.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/analyze',
        files={'file': ('photo.jpg', f, 'image/jpeg')}
    )

if response.status_code == 200:
    result = response.json()
    print(f"Skin Tone: {result['skin_tone']['label']}")
    print(f"Undertone: {result['undertone']['label']}")
    print(f"Top Match: {result['recommendations'][0]['brand']} "
          f"{result['recommendations'][0]['shade_name']}")
else:
    print(f"Error: {response.json()['detail']}")
```

### JavaScript API Client

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/v1/analyze', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Skin Tone:', data.skin_tone.label);
  console.log('Undertone:', data.undertone.label);
  console.log('Top Match:', data.recommendations[0].brand);
})
.catch(error => console.error('Error:', error));
```

---

## Docker Deployment

### Build and Run

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Access Services

- **Frontend**: http://localhost:8501
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Custom Configuration

Edit `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8080:8000"  # Change port
    environment:
      - MODEL_DIR=/app/backend/models
      - DATA_DIR=/app/backend/data
```

---

## Understanding Results

### Skin Tone Classification

**Monk Skin Tone (MST) Scale** - 10 classes:

| Class | Label | ITA° Range | Description |
|-------|-------|------------|-------------|
| MST-01 | Porcelain | > 55° | Very fair, cool/pink |
| MST-02 | Fair | 41–55° | Fair, warm/peachy |
| MST-03 | Light | 28–41° | Light beige |
| MST-04 | Light-Medium | 19–28° | Light medium |
| MST-05 | Medium | 10–19° | Medium beige |
| MST-06 | Medium-Dark | 0–10° | Warm medium |
| MST-07 | Tan | -10–0° | Tan/olive |
| MST-08 | Brown | -20–-10° | Brown |
| MST-09 | Deep Brown | -30–-20° | Deep brown |
| MST-10 | Deep | < -30° | Deep/ebony |

**Groups**:
- **Light**: MST-01, MST-02, MST-03
- **Medium**: MST-04, MST-05, MST-06
- **Dark**: MST-07, MST-08, MST-09, MST-10

### Undertone Detection

**3 Categories**:

1. **Warm** (score > 0.3)
   - Golden, peachy, or yellow undertones
   - Best with: Gold jewelry, warm colors
   - Veins appear: Greenish

2. **Cool** (score < -0.3)
   - Pink, red, or bluish undertones
   - Best with: Silver jewelry, cool colors
   - Veins appear: Bluish

3. **Neutral** (-0.3 ≤ score ≤ 0.3)
   - Balanced mix of warm and cool
   - Best with: Both gold and silver
   - Veins appear: Blue-green

### ITA° (Individual Typology Angle)

**Formula**: ITA° = arctan((L* - 50) / b*) × (180/π)

**Interpretation**:
- Higher values → Lighter skin
- Lower values → Darker skin
- Continuous scale (more precise than discrete classes)

### CIEDE2000 (ΔE)

**Color Difference Metric**:

| ΔE Value | Perception | Indicator |
|----------|------------|-----------|
| < 1.0 | Not perceptible | ✅✅✅ |
| 1.0 - 3.0 | Barely perceptible | ✅ |
| 3.0 - 6.0 | Noticeable | ⚠️ |
| > 6.0 | Obvious difference | ❌ |

**Industry Standard**: ΔE < 3.0 = Excellent match

### CIELAB Color Space

**L* (Lightness)**: 0 (black) → 100 (white)  
**a* (Red-Green)**: -128 (green) → +127 (red)  
**b* (Yellow-Blue)**: -128 (blue) → +127 (yellow)

Example:
- L*=45.68 → Medium-dark tone
- a*=11.54 → Slightly red
- b*=15.26 → Yellow undertone

---

## Troubleshooting

### Common Issues

#### 1. "No face detected"

**Causes**:
- Face not visible or too small
- Poor lighting
- Side profile or angled face
- Accessories covering face

**Solutions**:
- Use a clear, front-facing photo
- Ensure good lighting
- Remove glasses, hats, scarves
- Face should occupy 30-50% of image

#### 2. "Could not extract sufficient skin pixels"

**Causes**:
- Very dark or very bright lighting
- Heavy makeup or filters
- Colored lighting

**Solutions**:
- Use natural daylight
- Remove heavy makeup
- Avoid flash photography
- Use neutral background

#### 3. "Module not found" errors

**Solution**:
```bash
pip install -r requirements.txt
```

#### 4. Backend connection error (Streamlit)

**Check**:
```bash
# Is backend running?
curl http://localhost:8000/api/v1/health

# Start backend if not running
uvicorn backend.main:app --reload
```

#### 5. Port already in use

**Solution**:
```bash
# Use different port
uvicorn backend.main:app --reload --port 8001

# Update API_URL in streamlit_app.py
API_URL = "http://localhost:8001/api/v1/analyze"
```

#### 6. MTCNN not available

**Not a problem!** System automatically falls back to Haar Cascade.

**Optional**: Install MTCNN for better accuracy:
```bash
pip install mtcnn
```

### Performance Issues

#### Slow first inference

**Normal**: First run loads models and initializes detectors (~5-6 seconds)  
**Subsequent runs**: < 100ms

#### Memory usage

**Typical**: 200-500 MB  
**High usage**: Check image size, resize large images before upload

### Photo Quality Tips

#### Best Results:
1. **Lighting**: Overcast daylight near window
2. **Distance**: 30-50 cm from camera
3. **Angle**: Face directly at camera
4. **Background**: Plain white or neutral wall
5. **Preparation**: Clean face, no makeup, hair back

#### Avoid:
1. ❌ Flash photography
2. ❌ Bathroom mirror selfies (mixed lighting)
3. ❌ Car selfies (tinted windows)
4. ❌ Outdoor direct sunlight (overexposed)
5. ❌ Beauty filters or AI smoothing

---

## Advanced Usage

### Batch Processing

```python
import os
from shadeai_cli import analyze_image_file

# Process all images in a folder
for filename in os.listdir('photos/'):
    if filename.endswith(('.jpg', '.png')):
        print(f"\n{'='*60}")
        print(f"Processing: {filename}")
        print('='*60)
        analyze_image_file(f'photos/{filename}')
```

### Custom Database

Edit `backend/data/foundation_shades.json`:

```json
{
  "id": "CUSTOM-001",
  "brand": "Your Brand",
  "product": "Product Name",
  "shade_name": "Shade Name",
  "L": 70.0,
  "a": 8.0,
  "b": 18.0,
  "undertone": "Warm",
  "mst_range": ["MST-03", "MST-04"],
  "hex_approx": "#E0C8A0",
  "buy_url": "https://yourbrand.com"
}
```

### Environment Variables

Create `.env` file:

```bash
MODEL_DIR=backend/models
DATA_DIR=backend/data
API_PORT=8000
API_HOST=0.0.0.0
```

---

## Support

### Documentation
- **Quick Start**: QUICKSTART.md
- **Full Docs**: README_SHADEAI.md
- **Technical Spec**: implementation_plan.md
- **Summary**: IMPLEMENTATION_SUMMARY.md

### Testing
```bash
# Verify installation
python test_installation.py

# Test CLI
python shadeai_cli.py test1.jpg

# Test API
curl http://localhost:8000/api/v1/health
```

### Common Commands

```bash
# Install
pip install -r requirements.txt

# Test
python test_installation.py

# CLI
python shadeai_cli.py photo.jpg

# Backend
uvicorn backend.main:app --reload

# Frontend
streamlit run streamlit_app.py

# Docker
docker-compose up --build
```

---

**Version**: 1.0.0  
**Last Updated**: April 2026  
**Status**: Production Ready ✅
