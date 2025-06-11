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
