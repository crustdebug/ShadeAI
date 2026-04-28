"""
ShadeAI Streamlit Frontend
"""
import streamlit as st
import requests
from PIL import Image
import io
import os
import cv2
import numpy as np
from backend.utils.photo_quality import PhotoQualityChecker

st.set_page_config(
    page_title="ShadeAI — Find Your Foundation",
    page_icon="💄",
    layout="wide"
)

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1/analyze")

# Header
st.title("💄 ShadeAI — Personalized Foundation Shade Finder")
st.markdown(
    "Upload a well-lit selfie and get your top-5 matching foundation shades, "
    "ranked by perceptual color accuracy (CIEDE2000 ΔE)."
)

# Instructions
with st.expander("📸 How to take the perfect photo — click to expand", expanded=False):
    st.markdown("""
    ### ✅ DO:
    - Use a **WHITE or neutral-colored wall** as background
    - Face a **natural light source** (window) OR use soft indoor lighting
    - Hold the camera at **eye level**, 30–50 cm (12–20 inches) away
    - Look **directly at the camera** — face fully forward
    - Remove **heavy makeup**, especially foundation or color-correcting products
    - Remove **glasses and sunglasses**
    - Keep **hair away from your face**
    - Use a recent photo taken in **good lighting** (no filters!)
    - Take the photo in **DAYLIGHT** if possible (morning or overcast — no direct sun)

    ### ❌ AVOID:
    - **Flash photography** — causes harsh highlights and color distortion
    - **Strong shadows** across the face (e.g., from overhead lighting or hat)
    - **Colored lighting** (warm bulbs, neon, ring lights with color)
    - **Side profiles or angled poses** — face must be forward-facing
    - **Heavy filters, beauty modes, or AI skin smoothing**
    - **Very dark or very bright backgrounds**
    - **Sunglasses, scarves, or anything covering skin**
    - **Photos taken in car, bathroom mirror with mixed lighting**

    ### 💡 PRO TIP:
    Sit near a window on an overcast day. The even, diffused daylight produces
    the most accurate skin tone reading. Avoid direct sunlight which creates
    overexposed patches.
    """)

# Upload
uploaded_file = st.file_uploader(
    "Upload your photo (JPEG / PNG / WEBP)",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file:
    col1, col2 = st.columns([1, 2])

    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your uploaded photo", use_column_width=True)
        
        # Photo Quality Check
        st.markdown("### 📊 Photo Quality Check")
        img_array = np.array(image)
        if len(img_array.shape) == 2:  # Grayscale
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
        elif img_array.shape[2] == 4:  # RGBA
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
        else:  # RGB
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        checker = PhotoQualityChecker()
        quality_report = checker.check_quality(img_array)
        
        # Display quality badge
        badge = checker.get_quality_badge(quality_report['overall_score'])
        st.metric("Quality Score", f"{quality_report['overall_score']}/100", badge)
        
        # Show detailed scores in expander
        with st.expander("📈 Detailed Quality Scores"):
            for metric, score in quality_report['detailed_scores'].items():
                st.progress(score / 100, text=f"{metric.replace('_', ' ').title()}: {score}/100")
        
        # Show issues and warnings
        if quality_report['issues']:
            st.error("**Issues Found:**")
            for issue in quality_report['issues']:
                st.markdown(f"- {issue}")
        
        if quality_report['warnings']:
            st.warning("**Warnings:**")
            for warning in quality_report['warnings']:
                st.markdown(f"- {warning}")
        
        # Show suggestions
        if quality_report['suggestions']:
            st.info("**💡 Suggestions:**")
            for suggestion in quality_report['suggestions']:
                st.markdown(f"- {suggestion}")

    with col2:
        # Show quality warning if score is low, but never disable button
        if quality_report['overall_score'] < 60:
            st.warning(f"⚠️ Photo quality is {quality_report['quality_level'].lower()} ({quality_report['overall_score']}/100). Results may be less accurate.")
        
        if st.button("🔍 Analyze My Skin Tone", type="primary"):
            with st.spinner("Analyzing skin tone and matching shades..."):
                img_bytes = uploaded_file.getvalue()
                try:
                    response = requests.post(
                        API_URL,
                        files={"file": (uploaded_file.name, img_bytes, uploaded_file.type)}
                    )
                    if response.status_code == 200:
                        result = response.json()

                        # Skin Tone Result
                        st.success(
                            f"✅ Skin Tone: **{result['skin_tone']['label']}** "
                            f"(Group: {result['skin_tone']['group']})"
                        )
                        st.info(
                            f"🎨 Undertone: **{result['undertone']['label']}** — "
                            f"{result['undertone']['description']}"
                        )
                        st.caption(
                            f"ITA°: {result['ita_degrees']} | "
                            f"Mean L*: {result['mean_lab']['L']} | "
                            f"a*: {result['mean_lab']['a']} | "
                            f"b*: {result['mean_lab']['b']} | "
                            f"Inference: {result['inference_ms']} ms"
                        )

                        # Shade Recommendations
                        st.subheader("🏆 Top 5 Foundation Shade Recommendations")
                        for i, shade in enumerate(result['recommendations'], 1):
                            with st.container():
                                col_a, col_b, col_c = st.columns([1, 3, 1])
                                with col_a:
                                    # Color swatch
                                    st.color_picker(
                                        f"#{i}",
                                        shade.get('hex_approx', '#CCBBAA'),
                                        disabled=True,
                                        key=f"swatch_{i}"
                                    )
                                with col_b:
                                    delta_label = "✅" if shade['delta_e'] < 3.0 else "⚠️"
                                    st.markdown(
                                        f"**{shade['brand']}** — {shade['shade_name']}  \n"
                                        f"{shade['product']}  \n"
                                        f"Undertone: {shade.get('undertone','N/A')} | "
                                        f"Match: {delta_label} ΔE = {shade['delta_e']}"
                                    )
                                with col_c:
                                    st.link_button("🛒 Buy", shade.get('buy_url', '#'))
                    else:
                        detail = response.json().get('detail', 'Unknown error')
                        st.error(f"❌ Analysis failed: {detail}")
                except Exception as e:
                    st.error(f"❌ Could not connect to backend: {str(e)}")
                    st.info("Make sure the backend is running: `uvicorn backend.main:app --reload`")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>ShadeAI v1.0 — AI-Based Skin Tone Detection</p>
    <p>Based on Monk Skin Tone Scale & CIEDE2000 Color Matching</p>
</div>
""", unsafe_allow_html=True)
