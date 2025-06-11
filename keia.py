]import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai
import io
import requests
import base64
import plotly.io as pio
from scipy import stats

# --- KONFIGURASI HALAMAN & GAYA ---
st.set_page_config(
    page_title="Media Intelligence Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="auto"
)

def load_css():
    """
    Menyuntikkan CSS kustom dengan gaya UI/UX modern dan berbeda.
    """
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

            /* Resetting some default styles */
            body, .stApp {
                margin: 0;
                padding: 0;
                font-family: 'Poppins', sans-serif;
                background-color: #f7f9fc; /* Very light grey */
                color: #343a40; /* Dark grey */
            }

            /* Main Header - Clean and prominent */
            .main-header {
                text-align: left; /* Aligned to the left */
                padding: 2rem 3rem; /* More padding */
                background-color: #fff; /* White background */
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); /* Subtle shadow */
                margin-bottom: 3rem; /* Increased bottom margin */
            }
            .main-header h1 {
                font-size: 2.5rem; /* Slightly smaller, cleaner look */
                font-weight: 700;
                color: #2c3e50; /* Darker header color */
                margin-bottom: 0.5rem;
            }
            .main-header p {
                font-size: 1.1rem;
                color: #6c757d; /* Medium grey */
            }

            /* Card styles - Modern and minimal */
            .chart-container, .anomaly-card, .uploaded-file-info, .st-emotion-cache-1r6dm7m, .insight-hub-item {
                background-color: #fff;
                border-radius: 0.75rem;
                padding: 1.75rem; /* Increased padding */
                margin-bottom: 2.5rem; /* Increased bottom margin */
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04); /* Very subtle shadow */
                border: none; /* No border */
            }
            .anomaly-card {
                background-color: #f0f4ff; /* Light blue */
                border-left: 3px solid #6366f1; /* Indigo accent */
            }

            /* Insight Box - Clean and readable */
            .insight-box {
                background-color: #f8f9fa; /* Lighter grey */
                border-radius: 0.5rem;
                padding: 1.25rem;
                margin-top: 1.5rem;
                font-size: 0.9rem;
                color: #495057; /* Slightly darker grey */
                line-height: 1.6;
                white-space: pre-wrap;
                word-wrap: break-word;
            }

            /* Insight Hub Container - Modern layout */
            .insight-hub-container {
                display: flex;
                flex-wrap: wrap;
                gap: 1.75rem; /* Increased gap */
                margin-bottom: 3rem; /* Increased bottom margin */
                justify-content: center;
            }
            .insight-hub-item {
                flex: 1;
                min-width: 300px;
                max-width: 500px; /* Wider cards */
                display: flex;
                flex-direction: column;
            }
            .insight-hub-item h4 {
                color: #4c51bf; /* Darker blue */
                margin-bottom: 1.25rem;
            }

            /* Heading colors within containers */
            .chart-container h3, .insight-hub-item h3, .anomaly-card h3, .uploaded-file-info h3 {
                color: #4c51bf; /* Darker blue */
                margin-top: 0;
                margin-bottom: 1.5rem; /* Increased bottom margin */
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }

            .uploaded-file-info {
                color: #495057;
            }
            .uploaded-file-info p {
                margin-bottom: 0.75rem;
            }

            /* File Uploader - Clean and prominent */
            .stFileUploader > div {
                border: 2px dashed #ced4da; /* Light grey dashed border */
                border-radius: 0.75rem;
                padding: 2.75rem; /* Increased padding */
                background-color: #fff;
                margin-top: 2rem;
            }
            .stFileUploader label {
                color: #4c51bf; /* Darker blue */
                font-size: 1.1rem;
                font-weight: 500;
            }

            /* Button styles - Modern and clean */
            .stButton > button {
                border-radius: 0.5rem;
                padding: 0.9rem 1.75rem; /* Increased padding */
                font-weight: 500;
                border: none;
                transition: all 0.2s ease-in-out;
                cursor: pointer;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08); /* Subtle shadow */
            }
            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }

            /* Primary buttons - Distinct color */
            .stButton > button[data-testid="stFormSubmitButton"],
            .stButton > button[kind="primary"] {
                background-color: #6366f1 !important; /* Indigo */
                color: #fff !important;
            }
            .stButton > button[data-testid="stFormSubmitButton"]:hover,
            .stButton > button[kind="primary"]:hover {
                background-color: #4338ca !important; /* Darker indigo */
            }

            /* Download button - Same style as primary */
            .stButton > button[data-testid="stDownloadButton"] {
                background-color: #6366f1 !important;
                color: #fff !important;
                border: none !important;
            }
            .stButton > button[data-testid="stDownloadButton"]:hover {
                background-color: #4338ca !important;
            }

            /* Secondary buttons - Understated */
            .stButton > button[kind="secondary"] {
                background-color: #fff !important;
                color: #6366f1 !important; /* Indigo text */
                border: 1px solid #6366f1 !important; /* Indigo border */
            }
            .stButton > button[kind="secondary"]:hover {
                background-color: #f0f4ff !important; /* Light blue hover */
            }

            /* Selectbox styles - Clean */
            .stSelectbox > div > div > div {
                background-color: #fff;
                color: #495057;
                border: 1px solid #ced4da; /* Light grey border */
                border-radius: 0.5rem;
            }
            .stSelectbox > label {
                color: #4c51bf; /* Darker blue */
                font-weight: 500;
            }

            /* Radio button styles */
            div[data-testid="stRadio"] label {
                color: #4c51bf; /* Darker blue */
                font-weight: 500;
                margin-bottom: 0.5rem;
            }
            div[data-testid="stRadio"] div[role="radiogroup"] {
                background-color: #fff;
                border: 1px solid #ced4da;
                border-radius: 0.5rem;
                padding: 0.75rem 1rem;
            }
            div[data-testid="stRadio"] .st-emotion-cache-1ghf90p { /* Target the individual radio option */
                background-color: #f8f9fa; /* Slight background for options */
                border-radius: 0.3rem;
                padding: 0.5rem 0.75rem;
                margin-bottom: 0.4rem;
                border: 1px solid #e9ecef;
            }
            div[data-testid="stRadio"] .st-emotion-cache-1ghf90p:hover {
                background-color: #e2e6ea;
            }

            /* Expander styles - Clean and subtle */
            .stExpander > div > div {
                background-color: #fff;
                border: none; /* No border */
                border-radius: 0.75rem;
                padding: 1.75rem;
                margin-bottom: 2.5rem;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05); /* Subtle shadow */
            }
            .stExpander > div > div > div > p {
                color: #4c51bf; /* Darker blue */
                font-weight: 500;
                font-size: 1.1rem;
            }
            .stExpander div[data-testid="stExpanderForm"] {
                padding-top: 1rem;
            }

            /* Text input and chat input styles - Clean */
            .st-emotion-cache-10o5h6q {
                background-color: #fff;
                border: 1px solid #ced4da; /* Light grey border */
                border-radius: 0.5rem;
                color: #495057;
            }
            .st-emotion-cache-10o5h6q input,
            .st-emotion-cache-10o5h6q textarea {
                color: #495057;
            }
            .st-emotion-cache-10o5h6q label {
                color: #4c51bf; /* Darker blue */
                font-weight: 500;
            }

            /* Plotly chart font color adjustment */
            .js-plotly-plot .plotly .modebar-container {
                color: #495057;
            }
            .js-plotly-plot .plotly .g-gtitle {
                fill: #495057 !important;
            }
            .js-plotly-plot .plotly .xtick text,
            .js-plotly-plot .plotly .ytick text {
                fill: #495057 !important;
            }
            .js-plotly-plot .plotly .xaxislayer-above .axis-title text,
            .js-plotly-plot .plotly .yaxislayer-above .axis-title text {
                fill: #495057 !important;
            }
            .js-plotly-plot .plotly .legend .bg {
                fill: rgba(255,255,255,0.8) !important;
            }
            .js-plotly-plot .plotly .legendtext {
                fill: #495057 !important;
            }
            .js-plotly-plot .plotly .annotation-text {
                fill: #495057 !important;
            }

            /* Streamlit specific adjustments */
            div.stTabs [data-testid="stTabContent"] {
                padding: 2rem 0; /* Increased padding inside tabs */
            }
            .stProgress > div > div > div > div {
                background-color: #6366f1; /* Indigo progress bar */
            }

            /* Horizontal Line - Cleaner style */
            hr {
                border: none;
                height: 1px;
                background: #e9ecef; /* Very light grey */
                margin: 2rem 0;
            }
        </style>
    """, unsafe_allow_html=True)


# --- FUNGSI UTAMA & LOGIKA ---

def configure_gemini_api():
    """
    Mengkonfigurasi API Gemini menggunakan kunci API.
    Dalam aplikasi produksi, gunakan st.secrets.
    """
    # Pastikan Anda mengganti ini dengan st.secrets["GEMINI_API_KEY"] saat deploy!
    api_key = "AIzaSyC0VUu6xTFIwH3aP2R7tbhyu4O8m1ICxn4" 
    if not api_key:
        st.warning("API Key Gemini tidak ditemukan. Beberapa fitur AI mungkin tidak berfungsi.")
        return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Gagal mengkonfigurasi Gemini API: {e}. Pastikan API Key valid.")
        return False

@st.cache_resource # Cache the model to avoid re-initializing on every rerun
def get_gemini_model(model_name):
    """Mendapatkan instance model Gemini."""
    try:
        return genai.GenerativeModel(model_name)
    except Exception as e:
        st.error(f"Gagal memuat model AI '{model_name}': {e}")
        return None

def get_ai_insight(prompt, model_name):
    """
    Memanggil API GenAI untuk menghasilkan wawasan berdasarkan prompt dan model.
    """
    if not configure_gemini_api():
        return "Gagal membuat wawasan: API tidak terkonfigurasi."
    
    model = get_gemini_model(model_name)
    if model is None:
        return "Gagal membuat wawasan: Model AI tidak tersedia."

    try:
        response = model.generate_content(prompt)
        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            # Check for specific error reasons if response is empty
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                return f"Gagal membuat wawasan. Konten diblokir karena: {response.prompt_feedback.block_reason.name}"
            st.error(f"Model {model_name} tidak menghasilkan teks yang valid.")
            return "Gagal membuat wawasan."
    except Exception as e:
        st.error(f"Error saat memanggil model {model_name}: {e}. Coba lagi atau pilih model lain.")
        return "Gagal membuat wawasan: Terjadi masalah koneksi atau API."

def generate_html_report(campaign_summary, chart_insights, chart_figures_dict, charts_to_display_info, selected_ai_model):
    """
    Membuat laporan HTML dari wawasan dan grafik yang dihasilkan AI.
    """
    current_date = pd.Timestamp.now().strftime("%d-%m-%Y %H:%M")

    chart_figures_html_sections = ""
    if chart_figures_dict:
        for chart_info in charts_to_display_info:
            chart_key = chart_info["key"]
            chart_title = chart_info["title"]
            fig = chart_figures_dict.get(chart_key)
            
            insights_for_chart = chart_insights.get(chart_key, {})
            insight_text_for_model = insights_for_chart.get(selected_ai_model, "Wawasan belum dihasilkan atau data tidak tersedia.")
            
            insights_html = ""
            if insight_text_for_model:
                insights_html += f"""
                <h4>Wawasan AI (Gaya: {selected_ai_model.replace('_', ' ').title()}):</h4>
                <div class="insight-box">{insight_text_for_model}</div>
                """

            if fig:
                try:
                    fig_for_export = go.Figure(fig)
                    # Pastikan background putih untuk ekspor
                    fig_for_export.update_layout(paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF', font_color='#333333')
                    img_bytes = pio.to_image(fig_for_export, format="png", width=900, height=550, scale=1.5)
                    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                    chart_figures_html_sections += f"""
                    <div class="insight-sub-section">
                        <h3>{chart_title}</h3>
                        <img src="data:image/png;base64,{img_base64}" alt="{chart_title}" style="max-width: 100%; height: auto; display: block; margin: 10px auto; border: 1px solid #ddd; border-radius: 5px;">
                        {insights_html}
                    </div>
                    """
                except Exception as e:
                    chart_figures_html_sections += f"<p>Gagal menyertakan grafik {chart_title} (Error: {e}).</p>"
            elif insights_for_chart:
                chart_figures_html_sections += f"""
                <div class="insight-sub-section">
                    <h3>{chart_title}</h3>
                    <p>Tidak ada grafik yang tersedia.</p>
                    {insights_html}
                </div>
                """
    else:
        chart_figures_html_sections = "<p>Belum ada wawasan atau grafik yang dibuat.</p>"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Laporan Media Intelligence Dashboard</title>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Inter', sans-serif; line-height: 1.6; color: #333; margin: 20px; background-color: #f4f4f4; }}
            h1, h2, h3, h4 {{ color: #2c3e50; margin-top: 1.5em; margin-bottom: 0.5em; }}
            .section {{ background-color: #fff; padding: 15px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .insight-sub-section {{ margin-top: 1em; padding-left: 15px; border-left: 3px solid #eee; }}
            .insight-box {{ background-color: #e9ecef; padding: 10px; border-radius: 5px; font-size: 0.9em; white-space: pre-wrap; word-wrap: break-word; }}
        </style>
    </head>
    <body>
        <h1>Laporan Media Intelligence Dashboard</h1>
        <p>Tanggal Laporan: {current_date}</p>
        <div class="section">
            <h2>1. Ringkasan Strategi Kampanye</h2>
            <div class="insight-box">{campaign_summary or "Belum ada ringkasan."}</div>
        </div>
        <div class="section">
            <h2>2. Wawasan Grafik</h2>
            {chart_figures_html_sections}
        </div>
    </body>
    </html>
    """
    return html_content.encode('utf-8')

@st.cache_data
def parse_csv(uploaded_file):
    """Membaca dan membersihkan file CSV."""
    try:
        df = pd.read_csv(uploaded_file)
        
        if 'Media_Type' in df.columns:
            df.rename(columns={'Media_Type': 'Media Type'}, inplace=True)

        # Konversi kolom 'Date' dan 'Engagements' dengan penanganan error
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Engagements'] = pd.to_numeric(df['Engagements'], errors='coerce')
        
        # Hapus baris di mana Date atau Engagements adalah NaN setelah konversi
        initial_rows = len(df)
        df.dropna(subset=['Date', 'Engagements'], inplace=True)
        if len(df) < initial_rows:
            st.warning(f"Menghapus {initial_rows - len(df)} baris karena nilai 'Date' atau 'Engagements' tidak valid.")
        
        # Pastikan Engagements adalah integer
        df['Engagements'] = df['Engagements'].astype(int)

        # Isi kolom yang mungkin hilang dengan 'N/A'
        for col in ['Platform', 'Sentiment', 'Media Type', 'Location', 'Headline']:
            if col not in df.columns:
                df[col] = 'N/A'
                st.warning(f"Kolom '{col}' tidak ditemukan, mengisi dengan 'N/A'.")
        df[['Platform', 'Sentiment', 'Media Type', 'Location', 'Headline']] = df[['Platform', 'Sentiment', 'Media Type', 'Location', 'Headline']].fillna('N/A')
        
        if df.empty:
            st.error("File CSV Anda tidak mengandung data yang valid setelah pembersihan. Pastikan format kolom 'Date' dan 'Engagements' benar.")
            return None

        return df
    except Exception as e:
        st.error(f"Gagal memproses file CSV. Pastikan formatnya benar dan semua kolom penting ada. Error: {e}")
        return None

# --- UI STREAMLIT ---
load_css() # Memuat CSS kustom
api_configured = configure_gemini_api() # Mengkonfigurasi API Gemini

st.markdown("<div class='main-header'><h1>Media Intelligence Dashboard</h1><p>Rooby Farhan Intelligence</p></div>", unsafe_allow_html=True)

# Inisialisasi State (PASTIKAN BAGIAN INI ADA DI ATAS SEBELUM KODE UI LAINNYA)
if 'data' not in st.session_state:
    st.session_state.data = None
if 'chart_insights' not in st.session_state:
    st.session_state.chart_insights = {} # Store insights per chart, per model
if 'campaign_summary' not in st.session_state:
    st.session_state.campaign_summary = None
if 'chart_figures' not in st.session_state:
    st.session_state.chart_figures = {}
if 'last_uploaded_file_name' not in st.session_state:
    st.session_state.last_uploaded_file_name = None
if 'last_uploaded_file_size' not in st.session_state:
    st.session_state.last_uploaded_file_size = None
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False
if 'last_filter_state' not in st.session_state:
    st.session_state.last_filter_state = {}
if 'filter_date_range' not in st.session_state:
    st.session_state.filter_date_range = None
if 'selected_ai_model' not in st.session_state: # Inisialisasi model AI default
    st.session_state.selected_ai_model = "gemini-2.0-flash"


# Tampilan Unggah File Awal
if st.session_state.data is None: 
    c1, c2, c3 = st.columns([1,2,1]) 
    with c2:
        with st.container(border=False):
            st.markdown("### ☁️ Unggah File CSV Kamu di sini!")
            st.markdown("Pastikan file memiliki kolom: **`Date`**, **`Engagements`**, **`Sentiment`**, **`Platform`**, **`Media Type`**, **`Location`**, dan **`Headline`**.")
            uploaded_file = st.file_uploader(" ", type="csv", label_visibility="collapsed")
            
            if uploaded_file:
                # Cek jika file yang diunggah sama dengan yang terakhir
                if st.session_state.last_uploaded_file_name != uploaded_file.name or \
                   st.session_state.last_uploaded_file_size != uploaded_file.size:
                    
                    st.info(f"Mengunggah file: **{uploaded_file.name}**...")
                    parsed_df = parse_csv(uploaded_file)
                    
                    if parsed_df is not None:
                        st.session_state.data = parsed_df
                        st.session_state.last_uploaded_file_name = uploaded_file.name
                        st.session_state.last_uploaded_file_size = uploaded_file.size
                        st.session_state.show_analysis = True # Langsung tampilkan analisis setelah berhasil
                        st.rerun() # Memuat ulang aplikasi untuk menampilkan dashboard
                    else:
                        st.error("Gagal memproses file. Mohon periksa kembali format CSV Anda.")
                        # Reset session state agar user bisa upload ulang
                        st.session_state.data = None
                        st.session_state.last_uploaded_file_name = None
                        st.session_state.last_uploaded_file_size = None
                        st.session_state.show_analysis = False
                else:
                    # Jika file yang diunggah sama, mungkin user klik ulang.
                    # Asumsikan data sudah di session_state dan lanjutkan ke analisis.
                    st.info("File sudah diunggah sebelumnya. Melanjutkan ke analisis.")
                    st.session_state.show_analysis = True
                    st.rerun()


# --- Tampilan Dasbor Utama dengan Layout Baru ---
if st.session_state.show_analysis and st.session_state.data is not None:
    df = st.session_state.data

    # --- Sidebar Filter ---
    with st.sidebar:
        st.markdown(f"""<div class="uploaded-file-info"><h3>📂 File Terunggah:</h3><p><strong>Nama:</strong> {st.session_state.last_uploaded_file_name}</p></div>""", unsafe_allow_html=True)
        if st.button("Unggah File Baru", key="clear_file_btn", use_container_width=True, type="secondary"):
            for key in list(st.session_state.keys()):
                if key not in ['api_key', 'GEMINI_API_KEY']:
                    st.session_state.pop(key, None)
            st.experimental_set_query_params()
            st.rerun()

        st.markdown("---")
        with st.expander("⚙️ Filter Data", expanded=True):
            def get_multiselect(label, options):
                all_option = f"Pilih Semua {label}"
                # Set default value from session_state if exists, otherwise to "Pilih Semua"
                default_selection = st.session_state.get(f'filter_{label}', [all_option])
                
                valid_options = [opt for opt in default_selection if opt in ([all_option] + options)]
                
                selection = st.multiselect(label, [all_option] + options, default=valid_options)
                
                if all_option in selection:
                    if f'filter_{label}' in st.session_state:
                        del st.session_state[f'filter_{label}'] # Remove from state if "All" is selected
                    return options
                st.session_state[f'filter_{label}'] = selection # Save filter state
                return selection

            min_date, max_date = df['Date'].min().date(), df['Date'].max().date()
            
            # Initialize filter_date_range if it hasn't been set yet
            if 'filter_date_range' not in st.session_state or st.session_state.filter_date_range is None:
                st.session_state.filter_date_range = (min_date, max_date)

            date_range = st.date_input("Rentang Tanggal", 
                                        value=st.session_state.filter_date_range, 
                                        min_value=min_date, 
                                        max_value=max_date, 
                                        format="DD/MM/YYYY")
            
            # Update session state for date range
            if len(date_range) == 2:
                start_date, end_date = date_range
                st.session_state.filter_date_range = (start_date, end_date)
            else: # If only one date is selected, assume it's the start date
                start_date = date_range[0]
                end_date = max_date # Default end date to max if only start is picked
                st.session_state.filter_date_range = (start_date, end_date)


            platform = get_multiselect("Platform", sorted(df['Platform'].unique()))
            media_type = get_multiselect("Media Type", sorted(df['Media Type'].unique()))
            sentiment = get_multiselect("Sentiment", sorted(df['Sentiment'].unique()))
            location = get_multiselect("Location", sorted(df['Location'].unique()))
            
    # Filter dan proses data
    query = "(Date >= @start_date) & (Date <= @end_date)"
    params = {'start_date': pd.to_datetime(start_date), 'end_date': pd.to_datetime(end_date)}
    if platform: query += " & Platform in @platform"; params['platform'] = platform
    if sentiment: query += " & Sentiment in @sentiment"; params['sentiment'] = sentiment
    if media_type: query += " & `Media Type` in @media_type"; params['media_type'] = media_type
    if location: query += " & Location in @location"; params['location'] = location

    try:
        filtered_df = df.query(query, local_dict=params)
        if filtered_df.empty:
            st.warning("Tidak ada data yang cocok dengan filter yang dipilih. Silakan sesuaikan filter Anda.")
    except Exception as e:
        st.error(f"Error saat memfilter data: {e}. Pastikan pilihan filter valid.")
        filtered_df = pd.DataFrame() # Set to empty DataFrame on filter error

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- Bagian Statistik Utama (Top Cards) ---
    if not filtered_df.empty:
        total_engagements = filtered_df['Engagements'].sum()
        positive_sentiment_count = filtered_df['Sentiment'].value_counts().get('Positive', 0)
        negative_sentiment_count = filtered_df['Sentiment'].value_counts().get('Negative', 0)
        neutral_sentiment_count = filtered_df['Sentiment'].value_counts().get('Neutral', 0)
        total_unique_platforms = filtered_df['Platform'].nunique()

        avg_engagements_per_post = filtered_df['Engagements'].mean() if not filtered_df.empty and len(filtered_df) > 0 else 0
        
        # Menggunakan 4 kolom untuk tampilan yang lebih padat dan informatif
        cols_stats = st.columns(4) 
        
        with cols_stats[0]:
            st.markdown(f"<div class='chart-container' style='padding: 1.5rem; text-align: center;'><h3>Total Keterlibatan</h3><p style='font-size: 2rem; font-weight: bold; color: #6366f1;'>{total_engagements:,}</p></div>", unsafe_allow_html=True)
        with cols_stats[1]:
            st.markdown(f"<div class='chart-container' style='padding: 1.5rem; text-align: center;'><h3>Sentimen Positif</h3><p style='font-size: 2rem; font-weight: bold; color: #28a745;'>{positive_sentiment_count}</p></div>", unsafe_allow_html=True)
        with cols_stats[2]:
            st.markdown(f"<div class='chart-container' style='padding: 1.5rem; text-align: center;'><h3>Sentimen Negatif</h3><p style='font-size: 2rem; font-weight: bold; color: #dc3545;'>{negative_sentiment_count}</p></div>", unsafe_allow_html=True)
        with cols_stats[3]:
            st.markdown(f"<div class='chart-container' style='padding: 1.5rem; text-align: center;'><h3>Platform Unik</h3><p style='font-size: 2rem; font-weight: bold; color: #ffc107;'>{total_unique_platforms}</p></div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # --- Tampilan Grafik dalam Grid ---
        st.header("Visualisasi Data Utama")
        st.write("Jelajahi berbagai metrik penting dari data media Anda melalui grafik interaktif.")
        
        charts_to_display_info = [
            {"key": "sentiment", "title": "Analisis Sentimen"},
            {"key": "platform", "title": "Keterlibatan per Platform"},
            {"key": "trend", "title": "Tren Keterlibatan"},
            {"key": "mediaType", "title": "Distribusi Jenis Media"},
            {"key": "location", "title": "5 Lokasi Teratas"}
        ]

        # Mengatur grafik dalam dua kolom
        chart_cols = st.columns(2)

        def get_chart_prompt(key, data_json, answer_style):
            prompts = {
                "sentiment": "distribusi sentimen",
                "trend": "tren keterlibatan",
                "platform": "keterlibatan per platform",
                "mediaType": "distribusi jenis media",
                "location": "keterlibatan per lokasi"
            }

            personas = {
                "gemini-2.0-flash": "Anda adalah seorang analis media yang sangat kritis dan skeptis. Fokus pada potensi risiko, kelemahan data, dan anomali yang tidak terduga. Berikan 3 poin observasi tajam.",
                "Mistral 7B Instruct": "Anda adalah seorang ahli strategi branding yang kreatif dan visioner. Lihat data ini sebagai kanvas. Berikan 3 ide kampanye atau konten yang inovatif dan out-of-the-box berdasarkan tren yang ada.",
                "llama-3.3-8b-instruct": "Anda adalah seorang pakar data yang sangat kuantitatif dan to-the-point. Berikan 3 kesimpulan actionable yang didukung langsung oleh angka-angka dalam data. Sebutkan angka spesifik jika memungkinkan."
            }

            persona = personas.get(answer_style, "Anda adalah asisten AI. Berikan 3 wawasan dari data berikut.")

            return f"{persona} Analisis data mengenai {prompts.get(key, 'data')}: {data_json}. Sajikan wawasan dalam format daftar bernomor yang jelas."
        
        # Pilihan model AI menggunakan radio button di sini agar bisa memicu wawasan per grafik
        st.markdown("---") # Garis pemisah sebelum pilihan AI
        st.subheader("🤖 Pengaturan AI Generatif")
        st.session_state.selected_ai_model = st.radio(
            "Pilih **Model AI** untuk Wawasan",
            ["gemini-2.0-flash", "Mistral 7B Instruct", "llama-3.3-8b-instruct"],
            index=["gemini-2.0-flash", "Mistral 7B Instruct", "llama-3.3-8b-instruct"].index(st.session_state.selected_ai_model) if st.session_state.selected_ai_model in ["gemini-2.0-flash", "Mistral 7B Instruct", "llama-3.3-8b-instruct"] else 0,
            help="Pilih model AI yang akan digunakan untuk menghasilkan wawasan.",
            key="ai_model_selector_main" # Memberikan key unik
        )

        # Tombol untuk menghasilkan wawasan
        if st.button("Hasilkan Wawasan AI", type="primary", use_container_width=True, key="generate_ai_insights_btn"):
            if api_configured:
                with st.spinner("Menghasilkan wawasan AI..."):
                    # 1. Ringkasan Kampanye Global
                    summary_prompt = (
                        f"Anda adalah seorang analis media yang cerdas. Berikan ringkasan strategi kampanye berdasarkan data berikut. Fokus pada tren keseluruhan, sentimen dominan, platform paling berpengaruh, dan rekomendasi strategis kunci (maksimal 5 poin, gunakan bahasa yang mudah dimengerti). "
                        f"Data: {filtered_df.head(20).to_json(orient='records')}" # Mengambil sebagian kecil data untuk ringkasan global
                    )
                    st.session_state.campaign_summary = get_ai_insight(summary_prompt, st.session_state.selected_ai_model)

                    # 2. Wawasan per Grafik
                    for chart_info in charts_to_display_info:
                        chart_key = chart_info["key"]
                        
                        # Pastikan data_for_prompt sudah ada dan tidak kosong
                        if chart_key not in st.session_state.chart_insights or "data_for_prompt" not in st.session_state.chart_insights[chart_key]:
                            st.session_state.chart_insights.setdefault(chart_key, {})[st.session_state.selected_ai_model] = "Data grafik tidak tersedia untuk analisis AI."
                            continue

                        data_json = st.session_state.chart_insights[chart_key]["data_for_prompt"]
                        
                        if data_json and data_json != '[]': # Pastikan ada data untuk dianalisis
                            prompt = get_chart_prompt(chart_key, data_json, st.session_state.selected_ai_model)
                            insight = get_ai_insight(prompt, st.session_state.selected_ai_model)
                            st.session_state.chart_insights.setdefault(chart_key, {})[st.session_state.selected_ai_model] = insight
                        else:
                            st.session_state.chart_insights.setdefault(chart_key, {})[st.session_state.selected_ai_model] = "Tidak cukup data untuk menghasilkan wawasan ini."
                st.success("Wawasan AI berhasil dihasilkan!")
            else:
                st.error("Tidak dapat menghasilkan wawasan AI karena API key belum dikonfigurasi.")
        
        # Tampilkan Ringkasan Kampanye
        if st.session_state.campaign_summary:
            st.markdown("<div class='insight-hub-item'><h4>🎯 Ringkasan Strategi Kampanye</h4></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='insight-box'>{st.session_state.campaign_summary}</div>", unsafe_allow_html=True)
        else:
            st.info("Klik 'Hasilkan Wawasan AI' untuk mendapatkan ringkasan kampanye.")

        # Iterasi untuk menampilkan setiap grafik dan wawasannya
        for i, chart in enumerate(charts_to_display_info):
            with chart_cols[(i) % 2]: # distribusi ke dua kolom
                with st.container(border=True): # Gunakan container untuk setiap grafik dan wawasannya
                    st.markdown(f'<h3>📊 {chart["title"]}</h3>', unsafe_allow_html=True)
                    fig, data_for_prompt = None, None
                    try:
                        if filtered_df.empty:
                            st.warning(f"Tidak ada data untuk ditampilkan pada grafik '{chart['title']}' dengan filter ini.")
                            st.session_state.chart_insights.setdefault(chart["key"], {})["data_for_prompt"] = None # Reset data_for_prompt
                            st.session_state.chart_figures[chart["key"]] = None
                            # Pastikan wawasan tetap kosong jika tidak ada data
                            st.markdown(f"<div class='insight-box'>Tidak ada data untuk grafik ini, tidak dapat menghasilkan wawasan.</div>", unsafe_allow_html=True)
                            continue

                        if chart["key"] == "sentiment":
                            data = filtered_df['Sentiment'].value_counts().reset_index()
                            data.columns = ['Sentiment', 'count']
                            fig = px.pie(data, names='Sentiment', values='count', title='Distribusi Sentimen', color_discrete_map={'Positive':'#28a745', 'Negative':'#dc3545', 'Neutral':'#ffc107'})
                            data_for_prompt = data.to_json(orient='records')
                        elif chart["key"] == "trend":
                            data = filtered_df.groupby(filtered_df['Date'].dt.date)['Engagements'].sum().reset_index()
                            data.columns = ['Date', 'Engagements']
                            fig = px.line(data, x='Date', y='Engagements', title='Tren Keterlibatan Seiring Waktu', markers=True, line_shape='spline')
                            data_for_prompt = data.to_json(orient='records')
                        elif chart["key"] == "platform":
                            data = filtered_df.groupby('Platform')['Engagements'].sum().nlargest(10).reset_index()
                            data.columns = ['Platform', 'Engagements']
                            fig = px.bar(data, x='Platform', y='Engagements', color='Platform', title='Keterlibatan per Platform (Top 10)')
                            data_for_prompt = data.to_json(orient='records')
                        elif chart["key"] == "mediaType":
                            data = filtered_df['Media Type'].value_counts().reset_index()
                            data.columns = ['Media Type', 'count']
                            fig = px.pie(data, names='Media Type', values='count', hole=.3, title='Distribusi Jenis Media', color_discrete_map={'Social Media':'#6366f1', 'News Article':'#ef4444', 'Blog Post':'#06b6d4', 'Forum':'#f59e0b'})
                            data_for_prompt = data.to_json(orient='records')
                        elif chart["key"] == "location":
                            data = filtered_df.groupby('Location')['Engagements'].sum().nlargest(5).reset_index()
                            data.columns = ['Location', 'Engagements']
                            fig = px.bar(data, y='Location', x='Engagements', orientation='h', title='5 Lokasi Teratas Berdasarkan Keterlibatan')
                            data_for_prompt = data.to_json(orient='records')

                        if fig:
                            fig.update_layout(height=400, margin=dict(t=50, b=0, l=0, r=0))
                            st.plotly_chart(fig, use_container_width=True)
                            st.session_state.chart_figures[chart["key"]] = fig
                            
                            # Simpan data untuk prompt AI, ini penting!
                            st.session_state.chart_insights.setdefault(chart["key"], {})["data_for_prompt"] = data_for_prompt
                        else:
                            st.session_state.chart_insights.setdefault(chart["key"], {})["data_for_prompt"] = None # Pastikan ini di-reset jika tidak ada grafik
                            st.session_state.chart_figures[chart["key"]] = None
                            st.warning(f"Tidak dapat membuat grafik {chart['title']}.")

                        # Tampilkan wawasan AI tepat di bawah grafik ini
                        insight_text = st.session_state.chart_insights.get(chart["key"], {}).get(st.session_state.selected_ai_model, "Klik 'Hasilkan Wawasan AI' untuk analisis.")
                        st.markdown(f"<h4>Wawasan AI untuk {chart['title']}</h4>", unsafe_allow_html=True)
                        st.markdown(f"<div class='insight-box'>{insight_text}</div>", unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"Gagal membuat grafik {chart['title']} atau wawasan: {e}")
                        st.session_state.chart_figures[chart["key"]] = None
                        st.session_state.chart_insights.setdefault(chart["key"], {})["data_for_prompt"] = None
                        st.markdown(f"<div class='insight-box'>Terjadi kesalahan saat memuat grafik atau wawasan ini.</div>", unsafe_allow_html=True)


        st.markdown("---")

        ## Analisis Anomali
        st.header("Deteksi Anomali")
        st.write("Identifikasi titik data yang tidak biasa atau tren yang signifikan.")

        if not filtered_df.empty:
            mean_engagements = filtered_df['Engagements'].mean()
            std_engagements = filtered_df['Engagements'].std()

            if std_engagements > 0: # Hindari pembagian nol
                filtered_df['z_score'] = (filtered_df['Engagements'] - mean_engagements) / std_engagements
                # Definisikan threshold untuk anomali (misalnya, z-score > 2 atau < -2)
                anomaly_threshold = 2.0 
                anomalies = filtered_df[(filtered_df['z_score'].abs() > anomaly_threshold)].copy()

                if not anomalies.empty:
                    st.markdown("<div class='anomaly-card'><h3>⚠️ Anomali Terdeteksi!</h3>", unsafe_allow_html=True)
                    for idx, row in anomalies.iterrows():
                        st.write(f"- Tanggal: **{row['Date'].strftime('%Y-%m-%d')}**, Platform: **{row['Platform']}**, Engagements: **{row['Engagements']:,}**")
                        st.write(f"  *Headline:* \"{row['Headline']}\"")
                        st.write(f"  *(Z-score: {row['z_score']:.2f})*")
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("Tidak ada anomali signifikan terdeteksi dalam data keterlibatan berdasarkan Z-score (threshold 2.0).")
            else:
                st.info("Variasi keterlibatan terlalu kecil untuk mendeteksi anomali (standar deviasi nol).")
        else:
            st.info("Tidak ada data untuk mendeteksi anomali.")
        
        st.markdown("<hr>", unsafe_allow_html=True)

        # Tombol Download Laporan
        if st.session_state.campaign_summary or any(st.session_state.chart_insights.values()):
            html_report = generate_html_report(
                st.session_state.campaign_summary, 
                st.session_state.chart_insights, 
                st.session_state.chart_figures,
                charts_to_display_info, # Teruskan info chart untuk judul di laporan
                st.session_state.selected_ai_model # Teruskan model yang dipilih untuk laporan
            )
            st.download_button(
                label="Unduh Laporan HTML",
                data=html_report,
                file_name=f"media_intelligence_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                use_container_width=True,
                type="primary"
            )
        else:
            st.info("Hasilkan wawasan AI terlebih dahulu untuk mengaktifkan unduhan laporan.")

    else:
        st.info("Unggah file CSV dan terapkan filter untuk melihat analisis.")
