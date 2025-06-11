import streamlit as st
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
    Mengkonfigurasi API Gemini menggunakan kunci API dari st.secrets.
    """
    try:
        # PENTING: Untuk deployment, gunakan st.secrets["GEMINI_API_KEY"]
        # Pastikan Anda telah membuat file .streamlit/secrets.toml
        # Contoh: GEMINI_API_KEY="AIzaSyC0VUu6xTFIwH3aP2R7tbhyu4O8m1ICxn4"
        api_key = st.secrets.get("GEMINI_API_KEY") 
        
        if not api_key:
            st.warning("API Key Gemini tidak ditemukan di st.secrets. Beberapa fitur AI mungkin tidak berfungsi.")
            st.info("Untuk mengaktifkan AI, buat file `.streamlit/secrets.toml` di folder proyek Anda dan tambahkan `GEMINI_API_KEY='YOUR_API_KEY'`.")
            return False
        
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Gagal mengkonfigurasi Gemini API: {e}. Pastikan API Key valid dan file secrets.toml sudah benar.")
        return False

@st.cache_resource # Cache the model to avoid re-initializing on every rerun
def get_gemini_model(model_name):
    """Mendapatkan instance model Gemini."""
    try:
        return genai.GenerativeModel(model_name)
    except Exception as e:
        st.error(f"Gagal memuat model AI '{model_name}': {e}. Pastikan nama model benar dan API Key valid.")
        return None

def get_ai_insight(prompt, model_name):
    """
    Memanggil API GenAI untuk menghasilkan wawasan berdasarkan prompt dan model.
    """
    if not configure_gemini_api():
        return "Gagal membuat wawasan: API tidak terkonfigurasi."
    
    model = get_gemini_model(model_name)
    if model is None:
        return "Gagal membuat wawasan: Model AI tidak tersedia atau tidak dapat dimuat."

    try:
        response = model.generate_content(prompt)
        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                return f"Gagal membuat wawasan. Konten diblokir karena: {response.prompt_feedback.block_reason.name}."
            st.error(f"Model {model_name} tidak menghasilkan teks yang valid. Respons kosong atau tidak lengkap.")
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
    # Menggunakan model yang lebih umum tersedia di Gemini API
    st.session_state.selected_ai_model = "gemini-pro"


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
                # Hapus semua state kecuali API key yang mungkin disimpan di st.secrets
                if key not in ['api_key', 'GEMINI_API_KEY'] and not key.startswith('filter_'): # Pertahankan filter terakhir untuk kenyamanan
                    st.session_state.pop(key, None)
            st.experimental_set_query_params() # Clear URL params
            st.rerun()

        st.markdown("---")
        with st.expander("⚙️ Filter Data", expanded=True):
            def get_multiselect(label, options):
                all_option = f"Pilih Semua {label}"
                # Set default value from session_state if exists, otherwise to "Pilih Semua"
                default_selection = st.session_state.get(f'filter_{label}', [all_option])
                
                # Filter out invalid default options (e.g., if data changes)
                valid_options = [opt for opt in default_selection if opt in ([all_option] + options)]
                
                selection = st.multiselect(label, [all_option] + options, default=valid_options)
                
                if all_option in selection:
                    if f'filter_{label}' in st.session_state:
                        del st.session_state[f'filter_{label}'] # Remove from state if "All" is selected
                    return options
                st.session_state[f'filter_{label}'] = selection # Save filter state
                return selection

            min_date, max_date = df['Date'].min().date(), df['Date'].max().date()
            
            # Initialize filter_date_range if it hasn't been set yet or if data changed
            if 'filter_date_range' not in st.session_state or st.session_state.filter_date_range is None or \
               not (min_date <= st.session_state.filter_date_range[0] <= max_date and \
                    min_date <= st.session_state.filter_date_range[1] <= max_date):
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
                "gemini-pro": "Anda adalah seorang analis media yang sangat kritis dan skeptis. Fokus pada potensi risiko, kelemahan data, dan anomali yang tidak terduga. Berikan 3 poin observasi tajam.",
                "gemini-1.5-flash": "Anda adalah seorang ahli strategi branding yang kreatif dan visioner. Lihat data ini sebagai kanvas. Berikan 3 ide kampanye atau konten yang inovatif dan out-of-the-box berdasarkan tren yang ada.",
                # Asumsi 'Mistral 7B Instruct' dan 'llama-3.3-8b-instruct' bisa diakses sebagai bagian dari GenAI API.
                # Jika tidak, ini perlu penyesuaian agar memanggil API yang benar (misalnya via Hugging Face Hub).
                "Mistral 7B Instruct": "Anda adalah seorang ahli strategi branding yang kreatif dan visioner. Lihat data ini sebagai kanvas. Berikan 3 ide kampanye atau konten yang inovatif dan out-of-the-box berdasarkan tren yang ada.",
                "llama-3.3-8b-instruct": "Anda adalah seorang pakar data yang sangat kuantitatif dan to-the-point. Berikan 3 kesimpulan actionable yang didukung langsung oleh angka-angka dalam data. Sebutkan angka spesifik jika memungkinkan."
            }

            persona = personas.get(answer_style, "Anda adalah asisten AI. Berikan 3 wawasan dari data berikut.")

            return f"{persona} Analisis data mengenai {prompts.get(key, 'data')}: {data_json}. Sajikan wawasan dalam format daftar bernomor yang jelas."
            
        # Pilihan model AI menggunakan radio button di sini agar bisa memicu wawasan per grafik
        st.markdown("---") # Garis pemisah sebelum pilihan AI
        st.subheader("🤖 Pengaturan AI Generatif")
        # Update pilihan model AI sesuai dengan yang umumnya tersedia
        available_ai_models = ["gemini-pro", "gemini-1.5-flash"] 
        # Tambahkan model lain jika Anda yakin bisa mengaksesnya melalui API Gemini
        if "Mistral 7B Instruct" not in available_ai_models:
            available_ai_models.append("Mistral 7B Instruct")
        if "llama-3.3-8b-instruct" not in available_ai_models:
            available_ai_models.append("llama-3.3-8b-instruct")

        st.session_state.selected_ai_model = st.radio(
            "Pilih **Model AI** untuk Wawasan",
            available_ai_models,
            index=available_ai_models.index(st.session_state.selected_ai_model) if st.session_state.selected_ai_model in available_ai_models else 0,
            help="Pilih model AI yang akan digunakan untuk menghasilkan wawasan. Pastikan API Key Anda mendukung model yang dipilih.",
            key="ai_model_selector_main" # Memberikan key unik
        )

        # Tombol untuk menghasilkan wawasan
        if st.button("Hasilkan Wawasan AI", type="primary", use_container_width=True, key="generate_ai_insights_btn"):
            if api_configured:
                with st.spinner("Menghasilkan wawasan AI... Proses ini mungkin memakan waktu beberapa detik per wawasan."):
                    # 1. Ringkasan Kampanye Global
                    summary_data_for_ai = {
                        "total_engagements": total_engagements,
                        "positive_sentiment_count": positive_sentiment_count,
                        "negative_sentiment_count": negative_sentiment_count,
                        "neutral_sentiment_count": neutral_sentiment_count,
                        "total_unique_platforms": total_unique_platforms,
                        "top_platforms": filtered_df['Platform'].value_counts().head(3).to_dict(),
                        "top_sentiments": filtered_df['Sentiment'].value_counts().to_dict(),
                        "engagement_trend_sample": filtered_df.set_index('Date').resample('W')['Engagements'].sum().tail(5).to_dict(), # Ambil 5 minggu terakhir
                        "top_headlines_sample": filtered_df.nlargest(3, 'Engagements')['Headline'].tolist() # 3 headline dengan engagement tertinggi
                    }

                    summary_prompt = (
                        f"Anda adalah seorang analis media yang cerdas. Berikan ringkasan strategi kampanye berdasarkan data metrik agregat berikut. Fokus pada tren keseluruhan, sentimen dominan, platform paling berpengaruh, dan rekomendasi strategis kunci (maksimal 5 poin, gunakan bahasa yang mudah dimengerti dan tanpa pengantar/penutup). "
                        f"Data Agregat: {summary_data_for_ai}"
                    )
                    st.session_state.campaign_summary = get_ai_insight(summary_prompt, st.session_state.selected_ai_model)
                    if st.session_state.campaign_summary == "Gagal membuat wawasan: API tidak terkonfigurasi.":
                        st.session_state.campaign_summary = "Tidak dapat menghasilkan ringkasan kampanye karena masalah konfigurasi API."


                    # 2. Wawasan per Grafik
                    st.session_state.chart_insights = {} # Reset insights
                    progress_text = "Menghasilkan wawasan grafik..."
                    chart_progress_bar = st.progress(0, text=progress_text)

                    for i, chart_info in enumerate(charts_to_display_info):
                        chart_key = chart_info["key"]
                        
                        chart_progress_bar.progress((i + 1) / len(charts_to_display_info), text=f"{progress_text} ({i+1}/{len(charts_to_display_info)})")

                        chart_data = None
                        if chart_key == "sentiment":
                            chart_data = filtered_df['Sentiment'].value_counts().reset_index()
                            chart_data.columns = ['Sentiment', 'Count']
                        elif chart_key == "platform":
                            chart_data = filtered_df.groupby('Platform')['Engagements'].sum().reset_index().nlargest(5, 'Engagements')
                        elif chart_key == "trend":
                            chart_data = filtered_df.set_index('Date').resample('D')['Engagements'].sum().reset_index()
                        elif chart_key == "mediaType":
                            chart_data = filtered_df['Media Type'].value_counts().reset_index()
                            chart_data.columns = ['Media Type', 'Count']
                        elif chart_key == "location":
                            chart_data = filtered_df.groupby('Location')['Engagements'].sum().reset_index().nlargest(5, 'Engagements')
                        
                        if chart_data is not None:
                            prompt = get_chart_prompt(chart_key, chart_data.to_json(orient='records'), st.session_state.selected_ai_model)
                            insight = get_ai_insight(prompt, st.session_state.selected_ai_model)
                            st.session_state.chart_insights.setdefault(chart_key, {})[st.session_state.selected_ai_model] = insight
                        else:
                             st.session_state.chart_insights.setdefault(chart_key, {})[st.session_state.selected_ai_model] = "Data untuk grafik ini tidak tersedia atau tidak mencukupi untuk menghasilkan wawasan."
                    
                    chart_progress_bar.empty() # Hapus progress bar setelah selesai
                    st.success("Wawasan AI berhasil dibuat!")
                    st.toast("Wawasan AI berhasil dibuat!")
            else:
                st.error("Tidak dapat menghasilkan wawasan AI karena API Key Gemini belum dikonfigurasi.")
        
        # Inisialisasi dictionary untuk menyimpan objek figure plotly
        st.session_state.chart_figures = {}

        # Baris pertama grafik: Sentimen & Platform
        with chart_cols[0]:
            with st.container(border=False):
                st.markdown("<div class='chart-container'><h3>📊 Analisis Sentimen</h3></div>", unsafe_allow_html=True)
                sentiment_counts = filtered_df['Sentiment'].value_counts().reset_index()
                sentiment_counts.columns = ['Sentiment', 'Count']
                fig_sentiment = px.pie(sentiment_counts, values='Count', names='Sentiment', title='Distribusi Sentimen',
                                       color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_sentiment.update_traces(textposition='inside', textinfo='percent+label')
                fig_sentiment.update_layout(showlegend=True, margin=dict(t=50, b=0, l=0, r=0))
                st.plotly_chart(fig_sentiment, use_container_width=True)
                st.session_state.chart_figures['sentiment'] = fig_sentiment
                if st.session_state.selected_ai_model in st.session_state.chart_insights.get('sentiment', {}):
                    st.markdown(f"<div class='insight-box'>{st.session_state.chart_insights['sentiment'][st.session_state.selected_ai_model]}</div>", unsafe_allow_html=True)
                else:
                    st.info("Klik 'Hasilkan Wawasan AI' untuk mendapatkan analisis sentimen.")
            
            st.markdown("<br>", unsafe_allow_html=True) # Spacer

            with st.container(border=False):
                st.markdown("<div class='chart-container'><h3>📈 Tren Keterlibatan</h3></div>", unsafe_allow_html=True)
                engagement_trend = filtered_df.set_index('Date').resample('D')['Engagements'].sum().reset_index()
                fig_trend = px.line(engagement_trend, x='Date', y='Engagements', title='Tren Keterlibatan Seiring Waktu',
                                   labels={'Date': 'Tanggal', 'Engagements': 'Total Keterlibatan'})
                fig_trend.update_xaxes(rangeslider_visible=True)
                st.plotly_chart(fig_trend, use_container_width=True)
                st.session_state.chart_figures['trend'] = fig_trend
                if st.session_state.selected_ai_model in st.session_state.chart_insights.get('trend', {}):
                    st.markdown(f"<div class='insight-box'>{st.session_state.chart_insights['trend'][st.session_state.selected_ai_model]}</div>", unsafe_allow_html=True)
                else:
                    st.info("Klik 'Hasilkan Wawasan AI' untuk mendapatkan analisis tren.")

        with chart_cols[1]:
            with st.container(border=False):
                st.markdown("<div class='chart-container'><h3>📊 Keterlibatan per Platform</h3></div>", unsafe_allow_html=True)
                platform_engagements = filtered_df.groupby('Platform')['Engagements'].sum().reset_index().nlargest(10, 'Engagements')
                fig_platform = px.bar(platform_engagements, x='Engagements', y='Platform', orientation='h', title='Keterlibatan Teratas per Platform',
                                      labels={'Engagements': 'Total Keterlibatan', 'Platform': 'Platform'},
                                      color='Platform', color_discrete_sequence=px.colors.qualitative.D3)
                fig_platform.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_platform, use_container_width=True)
                st.session_state.chart_figures['platform'] = fig_platform
                if st.session_state.selected_ai_model in st.session_state.chart_insights.get('platform', {}):
                    st.markdown(f"<div class='insight-box'>{st.session_state.chart_insights['platform'][st.session_state.selected_ai_model]}</div>", unsafe_allow_html=True)
                else:
                    st.info("Klik 'Hasilkan Wawasan AI' untuk mendapatkan analisis platform.")
            
            st.markdown("<br>", unsafe_allow_html=True) # Spacer

            with st.container(border=False):
                st.markdown("<div class='chart-container'><h3>📚 Distribusi Jenis Media</h3></div>", unsafe_allow_html=True)
                media_type_counts = filtered_df['Media Type'].value_counts().reset_index()
                media_type_counts.columns = ['Media Type', 'Count']
                fig_media_type = px.bar(media_type_counts, x='Media Type', y='Count', title='Jumlah Postingan per Jenis Media',
                                        labels={'Media Type': 'Jenis Media', 'Count': 'Jumlah Postingan'},
                                        color='Media Type', color_discrete_sequence=px.colors.qualitative.Set2)
                st.plotly_chart(fig_media_type, use_container_width=True)
                st.session_state.chart_figures['mediaType'] = fig_media_type
                if st.session_state.selected_ai_model in st.session_state.chart_insights.get('mediaType', {}):
                    st.markdown(f"<div class='insight-box'>{st.session_state.chart_insights['mediaType'][st.session_state.selected_ai_model]}</div>", unsafe_allow_html=True)
                else:
                    st.info("Klik 'Hasilkan Wawasan AI' untuk mendapatkan analisis jenis media.")

        # Baris ketiga grafik: Top Locations
        with st.container(border=False):
            st.markdown("<div class='chart-container'><h3>📍 Keterlibatan per Lokasi (5 Teratas)</h3></div>", unsafe_allow_html=True)
            location_engagements = filtered_df.groupby('Location')['Engagements'].sum().reset_index().nlargest(5, 'Engagements')
            fig_location = px.bar(location_engagements, x='Location', y='Engagements', title='Keterlibatan Teratas per Lokasi',
                                  labels={'Location': 'Lokasi', 'Engagements': 'Total Keterlibatan'},
                                  color='Location', color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_location, use_container_width=True)
            st.session_state.chart_figures['location'] = fig_location
            if st.session_state.selected_ai_model in st.session_state.chart_insights.get('location', {}):
                st.markdown(f"<div class='insight-box'>{st.session_state.chart_insights['location'][st.session_state.selected_ai_model]}</div>", unsafe_allow_html=True)
            else:
                st.info("Klik 'Hasilkan Wawasan AI' untuk mendapatkan analisis lokasi.")


        st.markdown("<hr>", unsafe_allow_html=True)

        # --- Bagian Ringkasan Kampanye & Insight Hub ---
        st.header("Ringkasan dan Wawasan AI")
        st.write("Dapatkan ringkasan strategi kampanye dan analisis mendalam yang dihasilkan oleh AI.")
        
        # Ringkasan Kampanye Global
        st.markdown(f"""
            <div class='chart-container'>
                <h3>✨ Ringkasan Strategi Kampanye</h3>
                <div class='insight-box'>
                    {st.session_state.campaign_summary if st.session_state.campaign_summary else "Klik 'Hasilkan Wawasan AI' untuk mendapatkan ringkasan strategi kampanye."}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Insight Hub untuk Teks Asli (Top Headlines & Anomaly Detection)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.header("Insight Mendalam")
        st.write("Analisis lebih lanjut dari data Anda.")

        insight_hub_cols = st.columns(2)

        with insight_hub_cols[0]:
            with st.container(border=False):
                st.markdown("<div class='chart-container'><h3>🔥 Headline Paling Berpengaruh</h3></div>", unsafe_allow_html=True)
                # Menampilkan 5 headline teratas berdasarkan engagements
                top_headlines = filtered_df.nlargest(5, 'Engagements')[['Headline', 'Engagements', 'Platform', 'Sentiment']]
                if not top_headlines.empty:
                    for index, row in top_headlines.iterrows():
                        st.markdown(f"""
                            <div class='insight-hub-item' style='margin-bottom: 1rem; padding: 1rem; border: 1px solid #e0e0e0; border-radius: 0.5rem;'>
                                <h4 style='margin-bottom: 0.5rem;'>{row['Headline']}</h4>
                                <p style='font-size: 0.9rem; color: #555;'><strong>Keterlibatan:</strong> {row['Engagements']:,}</p>
                                <p style='font-size: 0.9rem; color: #555;'><strong>Platform:</strong> {row['Platform']}</p>
                                <p style='font-size: 0.9rem; color: #555;'><strong>Sentimen:</strong> {row['Sentiment']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Tidak ada headline yang ditemukan untuk filter yang dipilih.")

        with insight_hub_cols[1]:
            with st.container(border=False):
                st.markdown("<div class='chart-container'><h3>🚨 Deteksi Anomali Keterlibatan</h3></div>", unsafe_allow_html=True)
                # Deteksi anomali menggunakan Z-score pada engagements
                if len(filtered_df) > 1:
                    df_engagements = filtered_df['Engagements']
                    # Hitung Z-score. Z-score yang besar menunjukkan anomali.
                    # Kita bisa tetapkan ambang batas Z-score, misal 2 atau 3 standar deviasi.
                    z_scores = stats.zscore(df_engagements)
                    anomaly_threshold = 2.5 # Sesuaikan ambang batas sesuai kebutuhan
                    anomalies = filtered_df[abs(z_scores) > anomaly_threshold]

                    if not anomalies.empty:
                        st.markdown("<div class='anomaly-card'><h4>Anomali Terdeteksi!</h4><p>Ada beberapa postingan dengan keterlibatan yang sangat tinggi atau rendah dibandingkan rata-rata:</p></div>", unsafe_allow_html=True)
                        for index, row in anomalies.nlargest(3, 'Engagements').iterrows(): # Tampilkan 3 anomali teratas
                            st.markdown(f"""
                                <div class='insight-hub-item' style='margin-bottom: 1rem; padding: 1rem; border: 1px solid #e0e0e0; border-radius: 0.5rem;'>
                                    <h4 style='margin-bottom: 0.5rem;'>{row['Headline']}</h4>
                                    <p style='font-size: 0.9rem; color: #555;'><strong>Keterlibatan:</strong> {row['Engagements']:,} (Anomali)</p>
                                    <p style='font-size: 0.9rem; color: #555;'><strong>Platform:</strong> {row['Platform']}</p>
                                    <p style='font-size: 0.9rem; color: #555;'><strong>Sentimen:</strong> {row['Sentiment']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("Tidak ada anomali keterlibatan signifikan yang terdeteksi.")
                else:
                    st.info("Tidak cukup data untuk mendeteksi anomali.")

        st.markdown("<hr>", unsafe_allow_html=True)

        # --- Bagian Download Laporan ---
        st.header("Unduh Laporan")
        st.write("Unduh laporan lengkap dalam format HTML, termasuk grafik dan wawasan AI yang dihasilkan.")
        if st.session_state.campaign_summary or st.session_state.chart_insights:
            html_report = generate_html_report(
                st.session_state.campaign_summary,
                st.session_state.chart_insights,
                st.session_state.chart_figures,
                charts_to_display_info,
                st.session_state.selected_ai_model
            )
            st.download_button(
                label="Unduh Laporan HTML",
                data=html_report,
                file_name=f"media_intelligence_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                type="primary",
                use_container_width=True
            )
        else:
            st.info("Hasilkan wawasan AI terlebih dahulu untuk mengaktifkan unduhan laporan.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.info("Unggah file CSV dan terapkan filter untuk melihat analisis.")
