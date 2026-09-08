import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai

# پیج سیٹنگز
st.set_page_config(page_title="AI Data Analytics Assistant", layout="wide")
st.title("📊 AI ایکسل اینالیٹکس اسسٹنٹ")

# Gemini API کی سیٹ اپ
api_key = st.sidebar.text_input("Gemini API Key درج کریں:", type="password")

# فائل اپلوڈ (100MB لمٹ)
uploaded_file = st.file_uploader("اپنی ایکسل یا CSV فائل اپلوڈ کریں (100MB limit)", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    # ڈیٹا ریڈ کرنا
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.subheader("📋 ڈیٹا کا خلاصہ (Data Preview)")
    st.dataframe(df.head(10))
    
    # صارف کی ہدایات
    user_prompt = st.text_area("AI کے لیے اپنی ہدایات یا سوالات درج کریں:", 
                              "اس ڈیٹا کا گہرا جائزہ لیں، اہم نکات (Key Insights) بتائیں اور اگلے ماہ/سال کی پلاننگ و تجاویز رہنمائی فراہم کریں۔")
    
    if st.button("تجزیہ شروع کریں (Analyze Data)"):
        if not api_key:
            st.warning("براہ کرم سائیڈ بار میں اپنی Gemini API Key درج کریں۔")
        else:
            client = genai.Client(api_key=api_key)
            
            # ڈیٹا کا بنیادی شماریاتی خلاصہ
            data_summary = f"""
            کالمز: {list(df.columns)}
            ڈیٹا کی کل قطاریں: {len(df)}
            ڈیٹا کا خلاصہ:
            {df.describe(include='all').to_string()}
            """
            
            full_instruction = f"""
            آپ ایک سینئر ڈیٹا اینالسٹ اور بزنس اسٹریٹیجسٹ ہیں۔ 
            درج ذیل ڈیٹا کے خلاصے پر غور کریں:
            {data_summary}
            
            صارف کی ہدایت: {user_prompt}
            
            براہ کرم تفصیلی جائزہ فراہم کریں جس میں شامل ہوں:
            1. ڈیٹا کا گہرا جائزہ اور اہم نکات (Key Findings)
            2. اعداد و شمار کی روشنی میں مسائل یا مواقع
            3. اگلے ہفتے، ماہ اور سال کی حکمت عملی اور پلاننگ (Forecasting & Strategy)
            """
            
            with st.spinner("AI ڈیٹا کا تجزیہ کر رہا ہے..."):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_instruction
                )
                st.markdown("### 📝 AI تجزیاتی رپورٹ اور تجاویز")
                st.write(response.text)
                
                # بنیادی آٹو-چارٹس
                st.markdown("### 📈 ویژولائزیشن (Auto Charts)")
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) >= 1:
                    fig = px.histogram(df, x=numeric_cols[0], title=f"{numeric_cols[0]} کی تقسیم")
                    st.plotly_chart(fig, use_container_width=True)
