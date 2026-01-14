import streamlit as st
import requests
from io import BytesIO
from context_engineering import ContextEngineer
from vector_retrieval import VectorDB
from vision_execution import VisionAgent
import json
from PIL import Image

# -- Styling for attractive UI and full-width bottom result box --
st.markdown(
    """
    <style>
    .app-header{
        background: linear-gradient(90deg,#4b6cb7,#182848);
        color: #fff;
        padding: 14px;
        border-radius: 8px;
        font-family: "Segoe UI", Roboto, sans-serif;
        margin-bottom: 12px;
    }
    .card {
        background: linear-gradient(180deg, #ffffff, #f3f7ff);
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 6px 18px rgba(15,23,42,0.06);
    }
    .input-image img { border-radius:6px; border:2px solid #e6eefc; max-width:100%; height:auto; }
    .result-box {
        position: fixed;
        left: 8px;
        right: 8px;
        bottom: 8px;
        height: 48vh;
        background: linear-gradient(180deg,#061229,#092040);
        color: #e6f0ff;
        padding: 18px;
        border-radius: 10px;
        box-shadow: 0 12px 40px rgba(2,6,23,0.6);
        overflow: auto;
        z-index: 9999;
        font-family: "Segoe UI", Roboto, monospace;
        font-size: 15px;
        line-height: 1.5;
        border: 1px solid rgba(255,255,255,0.04);
    }
    .result-title { font-weight:700; color:#bfe1ff; margin-bottom:8px; }
    .result-text { white-space: pre-wrap; color:#e6f0ff; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="app-header"><h2 style="margin:0">Compliance Vision Agent</h2><div style="color:#dbe9ff;margin-top:6px;">Upload or link an image and ask a safety question — final result prints at the bottom.</div></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 1. Input Phase", unsafe_allow_html=True)

    input_mode = st.radio("Select Input Mode", ["Upload Image", "Image URL"])
    uploaded_file = None
    image_bytes = None

    if input_mode == "Upload Image":
        uploaded_file = st.file_uploader("Upload Site Photo", type=['jpg', 'png', 'jpeg'])
        if uploaded_file:
            image_bytes = uploaded_file.read()
    else:
        image_url = st.text_input("Enter Image URL")
        if image_url:
            try:
                resp = requests.get(image_url, timeout=10)
                resp.raise_for_status()
                image_bytes = resp.content
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to fetch image URL: {e}")
                image_bytes = None

    user_query = st.text_input("Query", "Check if this bedroom is safe.")
    run_btn = st.button("🚀 Run Compliance Check", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 2. Pipeline Status", unsafe_allow_html=True)

    # Everything below depends on the button being clicked
    if run_btn:
        if not image_bytes:
            st.error("Please provide a valid image input first.")
            st.stop()

        # Initialize modules
        vdb = VectorDB()
        ce = ContextEngineer()
        va = VisionAgent()  # <--- 'va' is created here

        # Step 2: vector retrieval
        retrieved_data = None
        try:
            retrieved_data = vdb.query(user_query)
            st.success("Step 2 (Vector): Retrieved safety constraints.")
        except Exception as e:
            st.error(f"Vector DB query failed: {e}")
            retrieved_data = None

        # Step 3: construct prompt
        prompt = ""
        try:
            prompt = ce.construct_prompt(retrieved_data)
            with st.expander("Step 3 (Engineered Prompt)"):
                st.code(prompt)
        except Exception as e:
            st.warning(f"Prompt construction failed: {e}")

        # Step 4: vision analysis
        # ALL of this must be indented to be inside 'if run_btn:'
        st.write("Step 4 (Vision): Analyzing image geometry...")
        st.markdown('<div class="input-image">', unsafe_allow_html=True)
        
        # Display Image safely
        try:
            # Requires: from PIL import Image (at top of file)
            image_source = Image.open(BytesIO(image_bytes))
            st.image(image_source, caption="Input Image", width=320)
        except Exception as e:
            st.error(f"Error displaying image: {e}")
            
        st.markdown('</div>', unsafe_allow_html=True)

        # Result Placeholder
        result_placeholder = st.empty()
        empty_html = '''
            <div class="result-box" role="region" aria-label="Final Result" style="position:relative; max-width:820px; margin-top:12px; height:120px; max-height:320px;">
                <div class="result-title">📋 Final Result</div>
                <div class="result-text"></div>
            </div>
        '''
        result_placeholder.markdown(empty_html, unsafe_allow_html=True)

        # Run Analysis
        result = None
        with st.spinner("Running vision analysis..."):
            try:
                # 'va' is now defined because we are inside the if block
                result = va.analyze(image_bytes, prompt)
            except Exception as e:
                result = f"Vision analysis failed: {e}"

        # Display Result
        if isinstance(result, (dict, list)):
            content_str = json.dumps(result, indent=2)
        else:
            content_str = str(result)

        safe_text = content_str.replace("<", "&lt;").replace(">", "&gt;")

        final_html = f'''
            <div class="result-box" role="region" aria-label="Final Result" style="position:relative; max-width:820px; margin-top:12px; height:auto; max-height:320px;">
                <div class="result-title">📋 Final Result</div>
                <div class="result-text">{safe_text}</div>
            </div>
        '''
        result_placeholder.markdown(final_html, unsafe_allow_html=True)
