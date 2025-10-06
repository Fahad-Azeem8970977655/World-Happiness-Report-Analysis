import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ==============================
# Page Configuration
# ==============================
st.set_page_config(page_title="🌍 World Happiness Report 2023 Dashboard", layout="wide")

# ==============================
# Load Dataset
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("WHR2023.csv")

    # Normalize column names (remove spaces, lowercase, underscores)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Dynamic column renaming for different dataset versions
    rename_map = {
        'country_name': 'country',
        'ladder_score': 'happiness_score',
        'logged_gdp_per_capita': 'gdp_per_capita',
        'social_support': 'social_support',
        'healthy_life_expectancy': 'life_expectancy',
        'freedom_to_make_life_choices': 'freedom',
        'perceptions_of_corruption': 'corruption',
        'regional_indicator': 'region'
    }

    for old, new in rename_map.items():
        if old in df.columns:
            df.rename(columns={old: new}, inplace=True)

    return df

df = load_data()

# ==============================
# Title and Description
# ==============================
st.title("🌍 World Happiness Report 2023 Dashboard")
st.markdown("""
Gain insights into **global happiness trends** and explore how factors like 
**GDP**, **social support**, **health**, and **freedom** contribute to well-being across nations.
""")

# ==============================
# Sidebar Navigation
# ==============================
st.sidebar.title("📊 Dashboard Navigation")
page = st.sidebar.radio(
    "Choose a Visualization:",
    [
        "Top & Bottom 10 Countries",
        "GDP vs Happiness",
        "Social Support vs Happiness",
        "Happiness Distribution",
        "Correlation Heatmap",
        "Pairwise Relationships"
    ]
)

# ==============================
# Helper Function for Validation
# ==============================
def safe_col(col_name):
    """Return True if column exists."""
    return col_name in df.columns

# ==============================
# Visualization 1: Top & Bottom 10
# ==============================
if page == "Top & Bottom 10 Countries":
    if not safe_col('happiness_score') or not safe_col('country'):
        st.error("⚠️ Required columns not found in dataset.")
    else:
        st.header("🏆 Top & Bottom 10 Happiest Countries")

        top_10 = df.nlargest(10, 'happiness_score')
        bottom_10 = df.nsmallest(10, 'happiness_score')

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top 10 Happiest Countries")
            fig, ax = plt.subplots(figsize=(9, 6))
            sns.barplot(x='happiness_score', y='country', data=top_10, palette='Greens_r', ax=ax)
            ax.set_xlabel("Happiness Score")
            ax.set_ylabel("Country")
            st.pyplot(fig)

        with col2:
            st.subheader("Bottom 10 Happiest Countries")
            fig, ax = plt.subplots(figsize=(9, 6))
            sns.barplot(x='happiness_score', y='country', data=bottom_10, palette='Reds_r', ax=ax)
            ax.set_xlabel("Happiness Score")
            ax.set_ylabel("Country")
            st.pyplot(fig)

# ==============================
# Visualization 2: GDP vs Happiness
# ==============================
elif page == "GDP vs Happiness":
    if not safe_col('gdp_per_capita') or not safe_col('happiness_score'):
        st.error("⚠️ GDP or Happiness Score column missing.")
    else:
        st.header("💰 GDP per Capita vs Happiness Score")
        fig, ax = plt.subplots(figsize=(9, 6))
        sns.scatterplot(
            x='gdp_per_capita',
            y='happiness_score',
            hue='region' if safe_col('region') else None,
            data=df,
            palette='viridis',
            s=80,
            ax=ax
        )
        ax.set_xlabel("GDP per Capita")
        ax.set_ylabel("Happiness Score")
        ax.set_title("GDP vs Happiness Across Regions")
        st.pyplot(fig)

# ==============================
# Visualization 3: Social Support vs Happiness
# ==============================
elif page == "Social Support vs Happiness":
    if not safe_col('social_support') or not safe_col('happiness_score'):
        st.error("⚠️ Social Support or Happiness Score column missing.")
    else:
        st.header("👫 Social Support vs Happiness Score")
        fig, ax = plt.subplots(figsize=(9, 6))
        sns.scatterplot(
            x='social_support',
            y='happiness_score',
            hue='region' if safe_col('region') else None,
            data=df,
            palette='coolwarm',
            s=80,
            ax=ax
        )
        ax.set_xlabel("Social Support")
        ax.set_ylabel("Happiness Score")
        ax.set_title("Social Support vs Happiness Across Regions")
        st.pyplot(fig)

# ==============================
# Visualization 4: Distribution of Happiness
# ==============================
elif page == "Happiness Distribution":
    if not safe_col('happiness_score'):
        st.error("⚠️ Happiness Score column missing.")
    else:
        st.header("📈 Distribution of Happiness Scores")
        fig, ax = plt.subplots(figsize=(9, 6))
        sns.histplot(df['happiness_score'], kde=True, color='skyblue', ax=ax)
        ax.set_xlabel("Happiness Score")
        ax.set_ylabel("Number of Countries")
        ax.set_title("Distribution of Global Happiness Scores")
        st.pyplot(fig)

# ==============================
# Visualization 5: Correlation Heatmap
# ==============================
elif page == "Correlation Heatmap":
    st.header("🔥 Correlation Between Key Happiness Factors")
    numeric_df = df.select_dtypes(include=['number'])
    fig, ax = plt.subplots(figsize=(11, 7))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
    ax.set_title("Correlation Heatmap of Happiness Factors")
    st.pyplot(fig)

# ==============================
# Visualization 6: Pairwise Relationships
# ==============================
elif page == "Pairwise Relationships":
    possible_cols = ['happiness_score', 'gdp_per_capita', 'social_support', 'life_expectancy', 'freedom']
    valid_cols = [col for col in possible_cols if safe_col(col)]

    if len(valid_cols) < 2:
        st.error("⚠️ Not enough numeric columns for pairwise visualization.")
    else:
        st.header("🔗 Pairwise Relationships Between Key Factors")
        df_clean = df[valid_cols].dropna()
        fig = sns.pairplot(df_clean, diag_kind='kde')
        fig.fig.suptitle("Relationships Between Key Happiness Indicators", y=1.02)
        st.pyplot(fig)

# ==============================
# Footer
# ==============================
st.markdown("---")
st.markdown("**Developed by:** Fahad Azeem | 🌐 *World Happiness Report 2023 Visualization*")
