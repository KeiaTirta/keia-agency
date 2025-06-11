# Tampilan Dasbor Utama dengan Layout Baru
if st.session_state.show_analysis and st.session_state.data is not None:
    df = st.session_state.data

    # --- Header Utama yang Lebih Luas ---
    st.markdown("<div class='main-header' style='padding: 2rem 3rem; margin-bottom: 2rem;'><h1>Media Intelligence Dashboard</h1><p style='font-size: 1.2rem; color: #6c757d;'>Analisis Mendalam Data Media Anda</p></div>", unsafe_allow_html=True)

    # --- Sidebar Filter ---
    with st.sidebar:
        st.markdown(f"""<div class="uploaded-file-info"><h3>📂 File Terunggah:</h3><p><strong>Nama:</strong> {st.session_state.last_uploaded_file_name}</p></div>""", unsafe_allow_html=True)
        if st.button("Unggah File Baru", key="clear_file_btn", use_container_width=True, type="secondary"):
            for key in list(st.session_state.keys()):
                if key not in ['api_key']: # Keep API key if it exists
                    del st.session_state.get(key)
            st.experimental_set_query_params()
            st.rerun()

        st.markdown("---")
        with st.expander("⚙️ Filter Data", expanded=True):
            def get_multiselect(label, options):
                all_option = f"Pilih Semua {label}"
                selection = st.multiselect(label, [all_option] + options, default=st.session_state.get(f'filter_{label}', [all_option]))
                if all_option in selection:
                    st.session_state.pop(f'filter_{label}', None) # Remove from state if "All" is selected
                    return options
                st.session_state.setdefault(f'filter_{label}', selection) # Save filter state
                return selection

            min_date, max_date = df['Date'].min().date(), df['Date'].max().date()

            platform = get_multiselect("Platform", sorted(df['Platform'].unique()))
            media_type = get_multiselect("Media Type", sorted(df['Media Type'].unique()))
            sentiment = get_multiselect("Sentiment", sorted(df['Sentiment'].unique()))
            location = get_multiselect("Location", sorted(df['Location'].unique()))
            date_range = st.date_input("Rentang Tanggal", (min_date, max_date), min_date, max_date, format="DD/MM/YYYY")
            start_date, end_date = date_range if len(date_range) == 2 else (min_date, max_date)

    # Filter dan proses data
    query = "(Date >= @start_date) & (Date <= @end_date)"
    params = {'start_date': pd.to_datetime(start_date), 'end_date': pd.to_datetime(end_date)}
    if platform: query += " & Platform in @platform"; params['platform'] = platform
    if sentiment: query += " & Sentiment in @sentiment"; params['sentiment'] = sentiment
    if media_type: query += " & `Media Type` in @media_type"; params['media_type'] = media_type
    if location: query += " & Location in @location"; params['location'] = location

    try:
        filtered_df = df.query(query, local_dict=params)
    except Exception as e:
        st.error(f"Error saat memfilter data: {e}. Pastikan pilihan filter valid.")
        filtered_df = df

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- Bagian Statistik Utama (Contoh - bisa Anda kembangkan sesuai kebutuhan) ---
    if not filtered_df.empty:
        total_engagements = filtered_df['Engagements'].sum()
        positive_sentiment_count = filtered_df['Sentiment'].value_counts().get('Positive', 0)
        negative_sentiment_count = filtered_df['Sentiment'].value_counts().get('Negative', 0)

        cols_stats = st.columns(3)
        with cols_stats:
            st.markdown(f"<div class='chart-container' style='padding: 1.5rem;'><h3>Total Keterlibatan</h3><p style='font-size: 1.5rem; font-weight: bold;'>{total_engagements:,}</p></div>", unsafe_allow_html=True)
        with cols_stats:
            st.markdown(f"<div class='chart-container' style='padding: 1.5rem;'><h3>Sentimen Positif</h3><p style='font-size: 1.5rem; font-weight: bold;'>{positive_sentiment_count}</p></div>", unsafe_allow_html=True)
        with cols_stats:
            st.markdown(f"<div class='chart-container' style='padding: 1.5rem;'><h3>Sentimen Negatif</h3><p style='font-size: 1.5rem; font-weight: bold;'>{negative_sentiment_count}</p></div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # --- Tampilan Grafik dalam Grid ---
        charts_to_display = [
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

        for i, chart in enumerate(charts_to_display):
            with chart_cols[(i) % 2]: # распределение по двум колонкам
                with st.container(border=True):
                    st.markdown(f'<h3>📊 {chart["title"]}</h3>', unsafe_allow_html=True)
                    fig, data_for_prompt = None, None
                    try:
                        if chart["key"] == "sentiment":
                            data = filtered_df['Sentiment'].value_counts().reset_index()
                            data.columns = ['Sentiment', 'count']
                            fig = px.pie(data, names='Sentiment', values='count', title='Distribusi Sentimen')
                        elif chart["key"] == "trend":
                            data = filtered_df.groupby(filtered_df['Date'].dt.date)['Engagements'].sum().reset_index()
                            data.columns = ['Date', 'Engagements']
                            fig = px.line(data, x='Date', y='Engagements', title='Tren Keterlibatan Seiring Waktu')
                        elif chart["key"] == "platform":
                            data = filtered_df.groupby('Platform')['Engagements'].sum().nlargest(10).reset_index()
                            data.columns = ['Platform', 'Engagements']
                            fig = px.bar(data, x='Platform', y='Engagements', color='Platform', title='Keterlibatan per Platform (Top 10)')
                        elif chart["key"] == "mediaType":
                            data = filtered_df['Media Type'].value_counts().reset_index()
                            data.columns = ['Media Type', 'count']
                            fig = px.pie(data, names='Media Type', values='count', hole=.3, title='Distribusi Jenis Media')
                        elif chart["key"] == "location":
                            data = filtered_df.groupby('Location')['Engagements'].sum().nlargest(5).reset_index()
                            data.columns = ['Location', 'Engagements']
                            fig = px.bar(data, y='Location', x='Engagements', orientation='h', title='5 Lokasi Teratas berdasarkan Keterlibatan')

                        if fig:
                            st.session_state.chart_figures.setdefault(chart["key"], fig)
                            fig.update_layout(
                                paper_bgcolor='#FFFFFF',
                                plot_bgcolor='#FFFFFF',
                                font_color='#2D3748',
                                legend_title_text='',
                                xaxis=dict(tickfont=dict(color='#2D3748'), title_font=dict(color='#2D3748'), showgrid=False),
                                yaxis=dict(tickfont=dict(color='#2D3748'), title_font=dict(color='#2D3748'), showgrid=False),
                                title_font=dict(color='#2D3748')
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            data_for_prompt = data.to_json(orient='records')
                        else:
                            st.warning(f"Tidak ada data untuk ditampilkan pada grafik '{chart['title']}' dengan filter ini.")

                        answer_styles = ["gemini-2.0-flash", "Mistral 7B Instruct", "llama-3.3-8b-instruct"]
                        selected_style = st.selectbox(
                            "Pilih Model AI:",
                            answer_styles,
                            key=f"sel_{chart['key']}"
                        )

                        if st.button("Lihat Insight", key=f"btn_{chart['key']}", use_container_width=True, type="primary"):
                            if data_for_prompt and api_configured:
                                with st.spinner(f"Menganalisis {chart['title']} dengan gaya '{selected_style}'..."):
                                    prompt = get_chart_prompt(chart['key'], data_for_prompt, selected_style)
                                    st.session_state.chart_insights.setdefault(chart['key'], {})
                                    st.session_state.chart_insights.get(chart['key'])[selected_style] = get_ai_insight(prompt)
                                    st.rerun()
                            elif not api_configured:
                                st.error("API Gemini tidak terkonfigurasi. Tidak dapat membuat wawasan AI.")
                            else:
                                st.warning("Tidak ada data valid untuk membuat insight AI.")

                        insight_text = st.session_state.chart_insights.get(chart.get("key"), {}).get(selected_style, "Pilih model AI untuk melihat insight.")
                        st.markdown(f'<div class="insight-box">{insight_text}</div>', unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"Terjadi kesalahan saat membuat atau menampilkan grafik '{chart['title']}': {e}")

    else:
        st.info("Tidak ada data yang sesuai dengan filter yang Anda terapkan.")

    st.markdown("<hr style='margin-top: 3rem;'>", unsafe_allow_html=True)

    # --- Bagian Ringkasan Strategi ---
    with st.container(border=True):
        st.markdown("<h3>💡 Ringkasan Strategi & Rekomendasi</h3>", unsafe_allow_html=True)
        if st.button("Buat Ringkasan Strategi", use_container_width=True, type="primary", key="btn_summary"):
            if not filtered_df.empty and api_configured:
                with st.spinner("Membuat ringkasan..."):
                    st.session_state.campaign_summary = get_ai_insight(f"Data: {filtered_df.describe().to_json()}. Buat ringkasan eksekutif yang menarik dan berikan 3 rekomendasi strategis yang bisa ditindaklanjuti berdasarkan data ini.")
            elif not api_configured:
                st.error("API Gemini tidak terkonfigurasi. Tidak dapat membuat ringkasan AI.")
            else:
                st.warning("Tidak ada data valid untuk membuat ringkasan AI.")
        st.markdown(f'<div class="insight-box">{st.session_state.campaign_summary or "Klik \'Buat Ringkasan Strategi\' untuk mendapatkan wawasan berbasis AI."}</div>', unsafe_allow_html=True)

    st.markdown("<hr style='margin-top: 3rem;'>", unsafe_allow_html=True)

    # --- Tombol Download Laporan ---
    with st.container(border=True):
        st.markdown("<h3>📄 Unduh Laporan Analisis</h3>", unsafe_allow_html=True)
        if st.download_button(
            "Unduh Laporan Lengkap (HTML)",
            data=generate_html_report(st.session_state.campaign_summary, st.session_state.chart_insights, st.session_state.chart_figures, charts_to_display),
            file_name="Laporan_Media_Intelligence.html",
            mime="text/html",
            use_container_width=True,
            type="primary" # Menggunakan primary agar lebih menonjol
        ):
            st.success("Laporan berhasil dibuat dan siap diunduh!")
