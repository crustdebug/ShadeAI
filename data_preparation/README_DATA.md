# ShadeAI Data Preparation Guide

This guide helps you prepare the necessary data for training and improving ShadeAI.

## 📊 What Data Do You Need?

### 1. Training Images (Monk Skin Tone Dataset)
### 2. Foundation Shade Database (CIELAB values)
### 3. Example Photos (Good/Bad UX examples)

---

## 1. Monk Skin Tone Dataset

### Option A: Use Google's Official MST Dataset

**Download from:**
- Google Research: https://skintone.google/mste-dataset
- GitHub: https://github.com/google/monk-skin-tone-scale

**What you get:**
- 1,000+ images across 10 MST classes
- Diverse lighting conditions
- Multiple ethnicities
- Pre-labeled with MST classes

**How to use:**
```bash
# 1. Visit https://skintone.google/mste-dataset and download the dataset
# 2. Place the downloaded ZIP in dataset/ folder
# 3. Run the download script to extract
python data_preparation/download_mst_dataset.py

# 4. Run annotation script
python data_preparation/annotate_mst_dataset.py
```

### Option B: Collect Your Own Dataset

**Requirements:**
- 240 images per MST class (2,400 total)
- Diverse subjects
- Controlled lighting (D65 illuminant)
- Front-facing portraits

**Directory structure:**
```
dataset/
├── mst_01_porcelain/
│   ├── img_001.jpg
│   ├── img_002.jpg
│   └── ...
├── mst_02_fair/
├── mst_03_light/
├── mst_04_light_medium/
├── mst_05_medium/
├── mst_06_medium_dark/
├── mst_07_tan/
├── mst_08_brown/
├── mst_09_deep_brown/
└── mst_10_deep/
```

**Annotation format (CSV):**
```csv
image_path,mst_class,undertone_score,L_star,a_star,b_star
dataset/mst_01/img_001.jpg,0,-0.5,88.2,5.1,12.3
dataset/mst_02/img_002.jpg,1,0.3,80.5,7.2,16.8
```

---

## 2. Foundation Shade Database

### Current Status
✅ **31 shades** included (MAC, Fenty, Maybelline, NARS, L'Oréal)

### Goal
🎯 **80-100 shades** for comprehensive coverage

### How to Measure CIELAB Values

#### Option A: Use Spectrophotometer (Most Accurate)
1. **Equipment**: X-Rite ColorMunki, Datacolor SpyderX
2. **Illuminant**: D65 (daylight)
3. **Observer**: 10° standard observer
4. **Measurement**: 3 readings per shade, average

#### Option B: Use Published Data
Many brands publish shade data:
- **Fenty Beauty**: 50 shades with LAB values
- **MAC**: Pro shade charts available
- **NARS**: Technical specifications online

#### Option C: Estimate from Swatch Photos
1. Take photo under D65 lighting
2. Use ColorMeter app or similar
3. Convert RGB → CIELAB
4. Validate with multiple samples

### Extended Database Template

See `foundation_shades_extended.json` for 80+ shades including:
- **MAC**: 15 shades (NW/NC series)
- **Fenty Beauty**: 20 shades (100-498)
- **Maybelline**: 12 shades (Fit Me series)
- **NARS**: 10 shades (Sheer Glow)
- **L'Oréal**: 12 shades (True Match)
- **Estée Lauder**: 8 shades (Double Wear)
- **Charlotte Tilbury**: 8 shades (Airbrush Flawless)

---

## 3. Example Photos for UX

### Good Photo Examples (6 images needed)

**example_good_1.jpg** - Perfect lighting
- Natural window light
- Face forward
- Neutral background
- No makeup
- Clear skin visible

**example_good_2.jpg** - Overcast daylight
- Soft diffused light
- Even skin tone
- No shadows
- Hair pulled back

**example_good_3.jpg** - Indoor soft lighting
- Warm white LED
- Face at eye level
- Clean background
- Proper distance (30-50cm)

### Bad Photo Examples (6 images needed)

**example_bad_flash.jpg** - Flash photography
- Harsh highlights
- Washed out skin
- Color distortion
- Overexposed areas

**example_bad_shadow.jpg** - Strong shadows
- Uneven lighting
- Face partially dark
- Harsh contrast
- Side lighting

**example_bad_angle.jpg** - Side profile
- Face not forward
- Angled pose
- Partial face visible
- Poor for analysis

**example_bad_filter.jpg** - Beauty filter
- AI smoothing
- Color adjustment
- Altered skin tone
- Unrealistic appearance

**example_bad_makeup.jpg** - Heavy makeup
- Foundation covering skin
- Color correction
- Concealer visible
- Not natural tone

**example_bad_lighting.jpg** - Colored lighting
- Warm/cool bulbs
- Mixed lighting
- Tinted windows
- Artificial color cast

### How to Create Example Photos

#### Option 1: Take Your Own
```bash
# Use provided script
python data_preparation/create_example_photos.py
```

#### Option 2: Use Stock Photos
- **Unsplash**: Search "portrait natural light"
- **Pexels**: Free stock photos
- **Pixabay**: Royalty-free images

#### Option 3: Generate with AI
```bash
# Use Stable Diffusion or similar
python data_preparation/generate_example_photos.py
```

---

## 📁 Final Directory Structure

```
shadeai/
├── dataset/
│   ├── mst/
│   │   ├── mst_01_porcelain/
│   │   ├── mst_02_fair/
│   │   └── ...
│   ├── annotations.csv
│   └── README.md
├── backend/data/
│   └── foundation_shades.json (80+ shades)
├── frontend/assets/
│   ├── example_good_1.jpg
│   ├── example_good_2.jpg
│   ├── example_good_3.jpg
│   ├── example_bad_flash.jpg
│   ├── example_bad_shadow.jpg
│   ├── example_bad_angle.jpg
│   ├── example_bad_filter.jpg
│   ├── example_bad_makeup.jpg
│   ├── example_bad_lighting.jpg
│   └── monk_scale_chart.png
└── data_preparation/
    ├── annotate_mst_dataset.py
    ├── measure_foundation_shades.py
    ├── create_example_photos.py
    └── validate_data.py
```

---

## 🚀 Quick Start Scripts

### 1. Download MST Dataset
```bash
python data_preparation/download_mst_dataset.py
```

### 2. Annotate Images
```bash
python data_preparation/annotate_mst_dataset.py \
  --input dataset/mst/ \
  --output dataset/annotations.csv
```

### 3. Validate Foundation Database
```bash
python data_preparation/validate_foundation_db.py \
  --input backend/data/foundation_shades.json
```

### 4. Generate Example Photos
```bash
python data_preparation/create_example_photos.py \
  --output frontend/assets/
```

---

## 📊 Data Quality Checklist

### Training Images
- [ ] 2,400+ images (240 per MST class)
- [ ] Diverse subjects (age, gender, ethnicity)
- [ ] Controlled lighting (D65 or equivalent)
- [ ] Front-facing portraits
- [ ] High resolution (>512x512)
- [ ] Annotated with MST class
- [ ] Undertone scores (-1 to +1)
- [ ] Mean CIELAB values

### Foundation Database
- [ ] 80-100 shades minimum
- [ ] 5+ major brands
- [ ] CIELAB values measured under D65
- [ ] Undertone labels (Warm/Cool/Neutral)
- [ ] MST range mappings
- [ ] Hex color approximations
- [ ] Purchase URLs

### Example Photos
- [ ] 3 good examples
- [ ] 6 bad examples (different issues)
- [ ] Clear visual differences
- [ ] Properly labeled
- [ ] Compressed for web (<500KB each)
- [ ] Consistent dimensions (800x600)

---

## 🔬 Advanced: Measuring Your Own Shades

### Equipment Needed
- Spectrophotometer (X-Rite ColorMunki ~$500)
- D65 light box (~$200)
- Foundation samples
- White calibration tile

### Measurement Protocol
1. Calibrate spectrophotometer with white tile
2. Apply foundation to white card (thin, even layer)
3. Let dry for 5 minutes
4. Measure under D65 illuminant
5. Take 3 readings, average results
6. Record L*, a*, b* values

### Python Script
```python
# See data_preparation/measure_foundation_shades.py
python data_preparation/measure_foundation_shades.py \
  --brand "MAC" \
  --product "Studio Fix Fluid" \
  --shade "NC42" \
  --L 48.5 \
  --a 13.2 \
  --b 20.8
```

---

## 📞 Need Help?

- **MST Dataset**: https://skintone.google/mste-dataset
- **CIELAB Conversion**: https://colormine.org/convert/rgb-to-lab
- **Spectrophotometer Guide**: See `docs/spectrophotometer_guide.pdf`
- **Stock Photos**: Unsplash, Pexels, Pixabay

---

**Status**: Ready for data collection  
**Last Updated**: April 2026
