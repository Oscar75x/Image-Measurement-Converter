import streamlit as st
from PIL import Image
import easyocr
import re

st.title("📏 Measurement Extractor & Converter")
st.write("Upload an image with measurements (e.g., 2' 3-1/2\") to convert them to decimal feet.")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
reader = easyocr.Reader(['en'], gpu=False)

def parse_and_convert(text):
    pattern = r"(\d+)'\s*(\d+)?(?:-(\d+)/(\d+))?\"?"
    results = []
    for match in re.finditer(pattern, text):
        feet = int(match.group(1))
        inches = int(match.group(2)) if match.group(2) else 0
        numerator = int(match.group(3)) if match.group(3) else 0
        denominator = int(match.group(4)) if match.group(4) else 1

        total_inches = inches + (numerator / denominator if denominator else 0)
        decimal_feet = round(feet + total_inches / 12, 4)

        original = f"{feet}' {inches}"
        if match.group(3) and match.group(4):
            original += f"-{numerator}/{denominator}\""
        else:
            original += '\"'

        results.append((original, decimal_feet))
    return results

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Extracting text..."):
        result = reader.readtext(image)
        combined_text = " ".join([item[1] for item in result])
        results = parse_and_convert(combined_text)

    if results:
        st.subheader("📐 Converted Measurements")
        for original, decimal in results:
            st.write(f"**{original}** ➡️ {decimal} ft")
    else:
        st.warning("No valid measurements found. Try a clearer image or different format.")