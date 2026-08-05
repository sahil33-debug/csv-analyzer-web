import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="CSV Analyzer", page_icon="📊", layout="wide")

# Title
st.title("📊 Universal CSV Analyzer")
st.write("Upload any CSV file and get instant analysis!")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)
    
    st.success(f"✅ File loaded successfully!")
    
    # Basic info
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", len(df))
    col2.metric("Total Columns", len(df.columns))
    col3.metric("Missing Values", df.isnull().sum().sum())
    
    # Show raw data
    st.subheader("🔍 Raw Data")
    st.dataframe(df)
    
    # Basic statistics
    st.subheader("📈 Basic Statistics")
    st.dataframe(df.describe())
    # Get numeric columns
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    
    if len(numeric_cols) > 0:
        st.subheader("📊 Visualizations")
        
        # Chart 1 - Bar chart of averages
        st.write("**Average Values by Column**")
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        df[numeric_cols].mean().plot(kind='bar', color='skyblue', ax=ax1)
        ax1.set_title('Average Values by Column')
        ax1.set_xlabel('Columns')
        ax1.set_ylabel('Average')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig1)
        
        # Chart 2 - Box plot
        st.write("**Data Distribution**")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        df[numeric_cols].plot(kind='box', ax=ax2)
        ax2.set_title('Data Distribution by Column')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig2)
    else:
        st.warning("⚠️ No numeric columns found for visualization!")
    # Download Excel report
    st.subheader("📁 Download Report")
    
    import io
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Raw Data', index=False)
        df.describe().to_excel(writer, sheet_name='Statistics')
        if len(numeric_cols) > 0:
            df[numeric_cols].mean().reset_index().to_excel(writer, sheet_name='Averages', index=False)
    
    st.download_button(
        label="⬇️ Download Excel Report",
        data=output.getvalue(),
        file_name="analysis_report.xlsx",
        mime="application/vnd.ms-excel"
    )