import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("AquaShield: Flood Assessment Tool")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        st.info("Processing data...")
        progress_bar = st.progress(0)

        df = pd.read_csv(uploaded_file)

        # Data validation
        if not df.columns.isin(['Altitude (m)', 'Water Body Proximity (km)', 'Rainfall (cm)', 'Slope (%)', 'Proximity (km)']).all():
            st.warning("CSV file must contain 'Altitude (m)', 'Water Body Proximity (km)', 'Rainfall (cm)', 'Slope (%)', and 'Proximity (km)' columns.")

        st.subheader("Data Preview")
        st.write(df.head())

        st.subheader("Data Summary")
        st.write(df.describe())

        st.subheader("Filter Data")
        columns = df.columns.tolist()
        selected_column = st.selectbox("Select column to filter by", columns)
        unique_values = df[selected_column].unique()
        selected_value = st.selectbox("Select value", unique_values)

        filtered_df = df[df[selected_column] == selected_value]
        st.write(filtered_df)

        st.subheader("Visualizations")

        # Scatter Plot: Land Altitude vs. Rainfall
        st.pyplot(plt.scatter(df['Altitude (m)'], df['Rainfall (cm)']))
        plt.xlabel("Altitude (m)")
        plt.ylabel("Rainfall (cm)")
        plt.title("Land Altitude vs. Rainfall")

        # Bar Chart: Rainfall Distribution
        st.bar_chart(df['Rainfall (cm)'])
        plt.xlabel("Rainfall (cm)")
        plt.ylabel("Frequency")
        plt.title("Rainfall Distribution")

        # 3D Visualization (optional)
        # Use Plotly or Matplotlib for 3D plotting

        # Define thresholds
        rainfall_threshold = st.number_input("Rainfall Threshold (cm)", value=df['Rainfall (cm)'].quantile(0.95))
        water_level_threshold = st.number_input("Water Level Threshold (m)", value=df['Water Level (m)'].quantile(0.90))
        slope_threshold = st.number_input("Slope Threshold (%)", value=df['Slope (%)'].quantile(0.75))
        proximity_threshold = st.number_input("Proximity Threshold (km)", value=df['Proximity (km)'].quantile(0.25))

        # Check for alerts
        if df['Rainfall (cm)'].max() > rainfall_threshold:
            st.warning(f"High rainfall detected! Threshold: {rainfall_threshold} cm")
        if df['Water Level (m)'].max() > water_level_threshold:
            st.warning(f"High water level detected! Threshold: {water_level_threshold} m")
        # ... add more checks for other attributes

        progress_bar.progress(100)
        st.success("Data processing complete!")

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.write("Please upload a CSV file.")