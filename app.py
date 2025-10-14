import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

# Streamlit page setup
st.set_page_config(page_title="Dataset Info Generator", layout="wide")

st.title("Dataset Information Generator")
st.write("Get the basic information and structure of your dataset quickly and easily.")

# --- File input section ---
st.subheader("Step 1: Provide Your Dataset")
file_path = st.text_input("Enter the path to your dataset (e.g., C:/Users/yourname/data.csv):")

# Optional file uploader
uploaded_file = st.file_uploader("Or upload your dataset file (CSV only):", type=["csv"])

# --- Button to generate dataset info ---
if st.button("Generate Info"):
    try:
        # Load dataset from upload or path
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        elif file_path.strip() != "":
            df = pd.read_csv(file_path)
        else:
            st.error("Please enter a valid file path or upload a CSV file.")
            st.stop()

        st.success("Dataset loaded successfully!")

        # --- Dataset preview ---
        st.header("1. Dataset Overview")
        st.write("**Random 10 Samples:**")
        st.dataframe(df.sample(min(10, len(df))))

        st.write("**Top 5 Rows:**")
        st.dataframe(df.head())

        st.write("**Bottom 5 Rows:**")
        st.dataframe(df.tail())

        # --- Columns information ---
        st.header("2. Columns Information")
        st.write("**Columns present in the dataset:**")
        st.write(list(df.columns))

        # --- Basic info ---
        st.header("3. Basic Column Info")
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        st.text(info_str)

        # --- Numeric and categorical columns ---
        st.header("4. Numeric & Categorical Columns")
        numerical_columns = [col for col in df.columns if df[col].dtype != "object"]
        categorical_columns = [col for col in df.columns if df[col].dtype == "object"]

        if numerical_columns:
            st.write("**Numerical Columns:**", numerical_columns)
        else:
            st.warning("No numerical columns found.")

        if categorical_columns:
            st.write("**Categorical Columns:**", categorical_columns)
        else:
            st.warning("No categorical columns found.")

        # --- Null values ---
        st.header("5. Missing Values Summary")
        st.write(df.isnull().sum())

        # --- Duplicate values ---
        st.header("6. Duplicate Values Check")
        duplicate_count = df.duplicated().sum()

        if duplicate_count > 0:
            st.write(f"Number of duplicate rows: {duplicate_count}")
            if st.button("Remove Duplicates"):
                df = df.drop_duplicates()
                st.success("Duplicates removed successfully.")
                st.write("Remaining duplicates:", df.duplicated().sum())
        else:
            st.success("✅ There are no duplicate values in the dataset.")

        # --- Statistical summary ---
        st.header("7. Statistical Summary (Numerical Columns)")
        if not df.select_dtypes(include=["number"]).empty:
            st.dataframe(df.describe())
        else:
            st.warning("No numerical columns available for statistical summary.")

        # --- Correlation heatmap ---
        st.header("8. Correlation Heatmap")
        num_cols = df.select_dtypes(include=["number"])
        if not num_cols.empty:
            corr = num_cols.corr()
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)
        else:
            st.warning("No numerical columns available for heatmap.")

        # --- Thank you message ---
        st.markdown("---")
        st.markdown(
            "<h4 style='text-align: center; color: gray;'>"
            "Thank you for using Dataset Information Generator<br>Created by <b>Shalabh Mani Tripathi</b>"
            "</h4>",
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"Error: {e}")
