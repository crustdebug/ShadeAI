# ShadeAI — AI-Based Skin Tone & Undertone Detection

Complete implementation of an AI-powered cosmetic shade recommendation system based on the Monk Skin Tone Scale and CIEDE2000 color matching.

## Features

- **Face Detection**: Automatic face detection using MTCNN or Haar Cascade
- **Skin Segmentation**: Rule-based skin pixel extraction using HSV + YCbCr
- **Skin Tone Classification**: 10-class Monk Skin Tone (MST) scale classification
- **Undertone Detection**: Warm/Cool/Neutral undertone analysis
- **Shade Matching**: Top-5 foundation shade recommendations using CIEDE2000 (ΔE < 3.0)
- **Multiple Interfaces**: CLI, FastAPI backend, and Streamlit web UI

## Installation

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
```

## Usage

### Option 1: Command Line Interface

```bash
python shadeai_cli.py your_photo.jpg
```

### Option 2: Web Application (Streamlit)

```bash
# Terminal 1: Start FastAPI backend
uvicorn backend.main:app --reload --port 8000

# Terminal 2: Start Streamlit frontend
streamlit run streamlit_app.py
```

Then open http://localhost:8501 in your browser.

### Option 3: API Only

```bash
# Start backend
uvicorn backend.main:app --reload --port 8000

# Test with curl
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -F "file=@your_photo.jpg"
```

API documentation available at: http://localhost:8000/docs

## Project Structure

```
shadeai/
├── backend/
│   ├── pipeline/
│   │   ├── preprocessor.py          # White balance, color spaces
│   │   ├── face_detector.py         # MTCNN / Haar face detection
│   │   ├── skin_segmentor.py        # HSV+YCbCr skin segmentation
│   │   ├── feature_extractor.py     # ITA°, LAB features
│   │   ├── classifier.py            # MST classification, undertone
│   │   └── shade_recommender.py     # CIEDE2000 matching
│   ├── utils/
│   │   ├── ciede2000.py             # CIEDE2000 implementation
│   │   └── color_utils.py           # Color space conversions
│   ├── api/
│   │   └── routes.py                # FastAPI endpoints
│   ├── data/
│   │   └── foundation_shades.json   # 30 foundation shades database
│   └── main.py                      # FastAPI app
├── streamlit_app.py                 # Streamlit web UI
├── shadeai_cli.py                   # Command line interface
└── requirements.txt
```

## Pipeline Stages

1. **Preprocessing**: Gray World white balance correction, color space conversion
2. **Face Detection**: MTCNN or Haar Cascade fallback
3. **Skin Segmentation**: HSV + YCbCr rule-based masking
4. **Feature Extraction**: ITA° calculation, CIELAB statistics
5. **Classification**: MST scale classification, undertone detection
6. **Recommendation**: CIEDE2000-based shade matching

## Monk Skin Tone Scale

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

## Photo Guidelines

### ✅ DO:
- Use natural or soft white lighting
- Face the camera directly
- Use a neutral background
- Remove heavy makeup
- Take photo in daylight (overcast is best)

### ❌ AVOID:
- Flash photography
- Strong shadows
- Colored lighting
- Side profiles
- Beauty filters
- Dark/bright backgrounds

## Foundation Database

Currently includes 30 shades from:
- MAC Studio Fix Fluid
- Fenty Beauty Pro Filt'r
- Maybelline Fit Me
- NARS Sheer Glow
- L'Oréal True Match

Each shade includes CIELAB values, undertone, and MST range.

## Performance Metrics

- **Inference Time**: < 100ms per image (without deep learning models)
- **Color Accuracy**: ΔE < 3.0 for top recommendations
- **Face Detection**: Works with MTCNN or Haar Cascade fallback

## Future Enhancements

1. **Deep Learning Models**:
   - EfficientNet-B3 for MST classification
   - U-Net for skin segmentation
   - SVR for undertone regression

2. **Expanded Database**:
   - 100+ foundation shades
   - Multiple brands and product lines

3. **Advanced Features**:
   - Webcam capture
   - Batch processing
   - Shade comparison tool
   - Virtual try-on

## References

Based on: *"AI-Based Skin Color and Undertone Detection for Cosmetic Shade Recommendation: System Implementation"* — Chauhan, Yadav, Nanda, Chauhan (JSS Academy of Technical Education, Noida)

## License

MIT License - See implementation_plan.md for full technical specification.
