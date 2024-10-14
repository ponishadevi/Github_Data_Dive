import streamlit as st
import pandas as pd
import seaborn as sns
import pymysql
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
from sqlalchemy import create_engine

# Load the page icon and set up the Streamlit configuration
icon = Image.open("download (1).png")
st.set_page_config(
    page_title="GitHub Data Dive  | By Ponishadevi",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': """# This Streamlit app is created by *Ponishadevi*!"""}
)

# Function to connect to MySQL database and fetch data
def load_data():
    try:
        # Create the SQLAlchemy engine
        engine = create_engine('mysql+pymysql://root:new_password@127.0.0.1:3306/github_data')
        query = "SELECT * FROM repositories"
        
        # Load data into DataFrame
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None  # Return None if there's an error
    finally:
        engine.dispose()  # Dispose of the engine to free up resources

# Load the data
df = load_data()

# Check if the DataFrame is not None before proceeding
if df is not None:
    # You can add any analysis or visualization code here instead of displaying the DataFrame
    pass  # Replace this with your analysis code
else:
    st.warning("No data available to display.")


# Creating option menu in the sidebar
with st.sidebar:
    page = option_menu(
        "Menu",
        ["Home", "Data Exploration", "Visualizations", "Conclusion"],
        icons=["house", "graph-up-arrow", "bar-chart-line"],
        menu_icon="menu-button-wide",
        default_index=0,
        styles={
            "nav-link": {
                "font-size": "20px",
                "text-align": "left",
                "margin": "-2px",
                "--hover-color": "#FF5A5F"
            },
            "nav-link-selected": {
                "background-color": "#FF5A5F"
            }
        }
    )

# Streamlit app layout with multi-page navigation
st.title("GitHub Data Dive: Insights and Trends")
# Enhanced Home Page Layout
if page == "Home":
    st.markdown(
        """
        <style>
        .big-font {
            font-size:50px !important;
            font-weight: bold;
            color: #FF5A5F;
        }
        .header-text {
            font-size:25px !important;
            font-style: italic;
        }
        .description {
            font-size:18px;
            text-align: justify;
        }
        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .button-container a {
            background-color: #FF5A5F;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            font-size: 18px;
            margin: 10px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Displaying a banner image (Optional: Replace 'home_image.png' with your banner image)
    home_image = Image.open("download (3).png")
    st.image(home_image, use_column_width=True)

    # Main Title with large font
    st.markdown('<p class="big-font">Welcome to GitHub Data Dive 🌐</p>', unsafe_allow_html=True)

    # Subtitle in italic
    st.markdown('<p class="header-text">Explore Trends, Analyze Repositories, and Discover Insights!</p>', unsafe_allow_html=True)

    # Descriptive text
    st.markdown(
        """
        <p class="description">
        GitHub Data Dive is your gateway to explore the ever-evolving open-source ecosystem. 
        This interactive app empowers developers, researchers, and organizations to unlock valuable 
        insights from GitHub repositories. Dive deep into trends, identify popular technologies, 
        and make informed decisions about collaboration and learning.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Summary of pages with emojis for visual appeal
    st.markdown(
        """
        **🚀 Features at a Glance:**
        - 🔍 **Data Exploration**: Filter repositories by programming language, stars, and more.
        - 📊 **Visualizations**: Explore interactive charts to uncover trends and patterns.
        - 📑 **Conclusion**: Review key insights from the analyzed data.

        """,
    )

    # Buttons for quick navigation
    st.markdown(
        """
        <div class="button-container">
            <a href="#data-exploration">Explore Data</a>
            <a href="#visualizations">View Visualizations</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Footer text
    st.markdown(
        """
        <p style="text-align: center; margin-top: 50px;">
        Built with ❤️ by Ponishadevi | Inspiring the Open-Source Future 🌐
        </p>
        """,
        unsafe_allow_html=True,
    )



# Data Exploration Page
elif page == "Data Exploration":
    st.header("Explore GitHub Repositories")

    # Sidebar filters for user input
    st.sidebar.header("Filter Repositories")
    selected_language = st.sidebar.multiselect("Select Programming Language", df['Programming_Language'].unique())
    selected_license = st.sidebar.multiselect("Select License Type", df['License_Type'].unique())
    min_stars = st.sidebar.slider("Minimum Stars", 0, int(df['Number_of_Stars'].max()), 0)

    # Apply filters to the dataframe
    filtered_data = df[
        (df['Number_of_Stars'] >= min_stars) & 
        (df['Programming_Language'].isin(selected_language) | (len(selected_language) == 0)) &
        (df['License_Type'].isin(selected_license) | (len(selected_license) == 0))
    ]

    # Create columns for the dashboard layout with adjusted widths
    col1, col2 = st.columns([3, 2])  # Adjust column proportions

    # Column 1: Filtered Data Table
    with col1:
        st.subheader(f"Filtered Repositories ({len(filtered_data)} found)")
        if not filtered_data.empty:
            st.dataframe(filtered_data[['Repository_Name', 'Number_of_Stars', 'Number_of_Forks', 'Description']])
        else:
            st.write("No data matches the selected filters.")

        # Download options for filtered data
        if st.button("Download Filtered Data as CSV"):
            csv = filtered_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='filtered_repositories.csv',
                mime='text/csv',
            )     

    # Column 2: Count of Repositories by Programming Language
    with col2:
        st.subheader("Count of Repositories by Programming Language")
        language_counts = filtered_data['Programming_Language'].value_counts()

        # Create bar chart only if there are filtered repositories
        if not language_counts.empty:
            fig1, ax1 = plt.subplots()
            sns.barplot(x=language_counts.index, y=language_counts.values, ax=ax1, palette='viridis')
            ax1.set_xlabel("Programming Language")
            ax1.set_ylabel("Number of Repositories")
            ax1.set_title("Number of Repositories by Programming Language")
            plt.xticks(rotation=45)  # Rotate x-axis labels for readability
            st.pyplot(fig1)
        else:
            st.write("No data available for the selected filters.")

    # Column 1: Top Repositories by Stars
    with col1:
        # Distribution of Stars
        st.subheader("Distribution of Stars")
        fig2, ax2 = plt.subplots()
        sns.histplot(filtered_data['Number_of_Stars'], bins=30, kde=True, color='blue', ax=ax2)
        ax2.set_xlabel("Stars")
        ax2.set_ylabel("Frequency")
        ax2.set_title("Distribution of Stars")
        st.pyplot(fig2)

    # Column 2: Summary Statistics and Distribution
    with col2:
        st.subheader("Summary Statistics of Filtered Data")
        if not filtered_data.empty:
            total_stars = filtered_data['Number_of_Stars'].sum()
            total_forks = filtered_data['Number_of_Forks'].sum()
            st.write(f"**Total Stars**: {total_stars}")
            st.write(f"**Total Forks**: {total_forks}")

            st.subheader("Top 10 Repositories by Stars")
            top_10_by_stars = filtered_data[['Repository_Name', 'Number_of_Stars']].nlargest(10, 'Number_of_Stars')
            st.dataframe(top_10_by_stars)

    # Column 1: License Type Distribution
    with col1:
        st.subheader("License Type Distribution")
        license_counts = filtered_data['License_Type'].value_counts()
        if not license_counts.empty:
            fig3, ax3 = plt.subplots()
            ax3.pie(license_counts, labels=license_counts.index, autopct='%1.1f%%', startangle=90)
            ax3.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
            st.pyplot(fig3)
        else:
            st.write("No license data available to generate the distribution chart.")
    with col2:        
        # License Type Insights
        st.subheader("Insights on License Types")
        if not filtered_data.empty:
            license_summary = filtered_data['License_Type'].value_counts(normalize=True) * 100
            for license_type, percent in license_summary.items():
                st.write(f"**{license_type}**: {percent:.2f}% of repositories")


    # Group and aggregate filtered data
    grouped_data = (
        filtered_data.groupby(['Programming_Language', 'Repository_Name'])['Number_of_Open_Issues']
        .sum()
        .reset_index()
    )

    # Limit to top N repositories based on Number of Open Issues
    top_n = 10  # Adjust as necessary
    top_repositories = grouped_data.groupby('Repository_Name')['Number_of_Open_Issues'].sum().nlargest(top_n).index
    grouped_data = grouped_data[grouped_data['Repository_Name'].isin(top_repositories)]

    # Plotting the grouped bar chart
    fig, ax = plt.subplots(figsize=(8, 6))  # Adjust width and height as needed
    sns.barplot(
        data=grouped_data, 
        x='Programming_Language', 
        y='Number_of_Open_Issues', 
        hue='Repository_Name', 
        ax=ax
    )

    # Customizing the chart
    ax.set_xlabel('Programming Language', fontsize=12)
    ax.set_ylabel('Number of Open Issues', fontsize=12)
    ax.set_title('Number of Open Issues per Repository by Programming Language', fontsize=16)
    plt.xticks(rotation=45)  # Rotate x-axis labels for readability

    # Specify legend location and format
    ax.legend(title='Repository Name', bbox_to_anchor=(1.05, 1), loc='upper left')  # Legend outside

    # Ensure the plot layout is tight
    plt.tight_layout()

    # Display in Streamlit
    st.pyplot(fig)

            
# Visualizations Page
elif page == "Visualizations":
    st.header("Data Visualizations")

    # Selecting visualization type using radio buttons
    visualization_type = st.radio("Select Visualization Type", ("Bar Chart", "Pie Chart", "Scatter Plot"))

    # Visualization based on selected type
    if visualization_type == "Bar Chart":
        # 3. Bar Chart: Total Repositories by Programming Language
        st.subheader("Total Repositories by Programming Language")
        language_counts =df['Programming_Language'].value_counts()
        st.bar_chart(language_counts)

    elif visualization_type == "Pie Chart":
        st.subheader("Distribution of Programming Languages")
        language_counts = df['Programming_Language'].value_counts()
        fig_pie = px.pie(language_counts, values=language_counts.values, names=language_counts.index, title='Distribution of Programming Languages')
        st.plotly_chart(fig_pie, use_container_width=True)

    elif visualization_type == "Scatter Plot":
            # 2. Scatter Plot: Stars vs. Forks
        st.subheader("Stars vs. Forks by Programming Language")
        fig4 = px.scatter(df, x='Number_of_Stars', y='Number_of_Forks', 
                        color='Programming_Language', title="Stars vs. Forks")
        st.plotly_chart(fig4)

        


    # Sidebar filters for user input
    st.sidebar.header("Filter Visualizations")
    selected_language = st.sidebar.multiselect(
    "Select Programming Language", 
    df['Programming_Language'].unique(),
    help="Choose one or more programming languages to filter the repositories."
)

    selected_license = st.sidebar.multiselect("Select License Type", df['License_Type'].unique())

    # Apply filters to the dataframe
    filtered_data = df[
        (df['Programming_Language'].isin(selected_language) | (len(selected_language) == 0)) &
        (df['License_Type'].isin(selected_license) | (len(selected_license) == 0))
    ]


    # Subheader with the count of filtered repositories
    st.subheader(f"Visualizations for Filtered Repositories ({len(filtered_data)} found)")

    # Convert 'Last_Updated_Date' to datetime and calculate days since the last update
    filtered_data['Last_Updated_Date'] = pd.to_datetime(filtered_data['Last_Updated_Date'], errors='coerce')
    filtered_data['Days_Since_Last_Update'] = (
        pd.to_datetime('today').normalize() - filtered_data['Last_Updated_Date']
    ).dt.days

    # Drop rows with invalid dates (if any)
    filtered_data = filtered_data.dropna(subset=['Days_Since_Last_Update'])

    # 1. Histogram: Days Since Last Update
    st.subheader("Activity Analysis: Days Since Last Update")
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.histplot(filtered_data['Days_Since_Last_Update'], bins=30, kde=True, color='blue', ax=ax1)

    # Customize the plot
    ax1.set_title('Distribution of Days Since Last Update', fontsize=16)
    ax1.set_xlabel('Days Since Last Update', fontsize=14)
    ax1.set_ylabel('Frequency', fontsize=14)
    ax1.grid(True, linestyle='--', alpha=0.7)

    # Display the plot in Streamlit
    st.pyplot(fig1)

    # 2. Repository Age Chart (as earlier)
    st.subheader("Repository Age Distribution")
    filtered_data['Repository_Age'] = (pd.to_datetime('today') - filtered_data['Creation_Date']).dt.days
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.histplot(filtered_data['Repository_Age'], bins=30, kde=True, ax=ax2, color='green')
    ax2.set_xlabel('Repository Age (Days)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of Repository Age')
    st.pyplot(fig2)

    
    



    # Ensure 'filtered_data' is defined earlier in the code with the required filters
    filtered_data['Creation_Date'] = pd.to_datetime(filtered_data['Creation_Date'])

    # Group data by Month and Programming Language, and sum the stars
    stars_over_time = filtered_data.groupby(
        [filtered_data['Creation_Date'].dt.to_period('M'), 'Programming_Language']
    )['Number_of_Stars'].sum().unstack().fillna(0)

    # Streamlit page content
    st.subheader("Trend of Programming Language Popularity Over Time (Stars)")

    # Plot the multi-line chart using Streamlit
    st.line_chart(stars_over_time)

    
    # Repositories Last Updated Over Time (Line Chart)
    update_counts = filtered_data['Last_Updated_Date'].dt.to_period('M').value_counts().sort_index()

    fig8, ax8 = plt.subplots(figsize=(12, 6))
    update_counts.plot(kind='line', color='orange', ax=ax8, linestyle='-', marker='o')
    ax8.set_title('Repositories Last Updated Over Time', fontsize=16)
    ax8.set_xlabel('Date', fontsize=14)
    ax8.set_ylabel('Number of Repositories Updated', fontsize=14)
    plt.xticks(rotation=45)
    ax8.grid(True)  # Add gridlines for better readability
    st.pyplot(fig8)

        # Repositories Created Over Time (Line Chart)
    df['Creation_Date'] = pd.to_datetime(df['Creation_Date'])
    creation_counts = df['Creation_Date'].dt.to_period('M').value_counts().sort_index()
    fig7, ax7 = plt.subplots(figsize=(12, 6))
    creation_counts.plot(kind='line', ax=ax7)
    ax7.set_title('Repositories Created Over Time')
    ax7.set_xlabel('Date')
    ax7.set_ylabel('Number of Repositories Created')
    plt.xticks(rotation=45)
    st.pyplot(fig7)

    



    # 5. License Analysis Bar Chart
    st.subheader("Number of Repositories by License Type")
    license_counts = filtered_data['License_Type'].value_counts()
    fig6, ax6 = plt.subplots(figsize=(12, 6))
    sns.barplot(x=license_counts.index, y=license_counts.values, palette='cubehelix', ax=ax6)
    ax6.set_xlabel('License Type')
    ax6.set_ylabel('Number of Repositories')
    ax6.set_title('Number of Repositories by License Type')
    plt.xticks(rotation=45)
    st.pyplot(fig6)
    

    # Word Cloud for Repository Descriptions
    st.subheader("Word Cloud of Repository Descriptions")
    if not filtered_data['Description'].isnull().all():
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(filtered_data['Description'].dropna()))
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        ax4.imshow(wordcloud, interpolation='bilinear')
        ax4.axis('off')  # Hide axes
        st.pyplot(fig4)
    else:
        st.write("No descriptions available to generate a word cloud.")




    # 6. Top 10 Repositories by Stars (Filtered)
    st.subheader("Top 10 Repositories by Stars")
    top_stars = filtered_data.nlargest(10, 'Number_of_Stars')[['Repository_Name', 'Number_of_Stars']]
    fig7, ax7 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_stars, x='Number_of_Stars', y='Repository_Name', palette='viridis', ax=ax7)
    ax7.set_title('Top 10 Repositories by Stars')
    ax7.set_xlabel('Number of Stars')
    ax7.set_ylabel('Repository Name')
    st.pyplot(fig7)

    # 7. Top 10 Repositories by Forks (Filtered)
    st.subheader("Top 10 Repositories by Forks")
    top_forks = filtered_data.nlargest(10, 'Number_of_Forks')[['Repository_Name', 'Number_of_Forks']]
    fig8, ax8 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_forks, x='Number_of_Forks', y='Repository_Name', palette='plasma', ax=ax8)
    ax8.set_title('Top 10 Repositories by Forks')
    ax8.set_xlabel('Number of Forks')
    ax8.set_ylabel('Repository Name')
    st.pyplot(fig8)

# Conclusion Page
elif page == "Conclusion":
    st.header("Key Insights and Conclusion")

    # Summary of key insights
    st.subheader("Summary of Key Insights")
    st.markdown(
        """
        - **Programming Languages**: Python and JavaScript are the most popular languages in GitHub repositories.
        - **Repository Trends**: Machine Learning and Web Development projects show significant growth.
        - **License Types**: MIT and Apache licenses dominate the open-source landscape.
        - **Developer Engagement**: Repositories with higher stars tend to attract more forks and contributors.
        """
    )

    # Conclusion and Future Directions
    st.subheader("Conclusion and Future Directions")
    st.markdown(
        """
        GitHub Data Dive has provided valuable insights into the dynamics of open-source repositories. 
        Future enhancements could include real-time updates, advanced machine learning models for trend prediction, 
        and integration with additional data sources to enrich analysis capabilities.
        """
    )

    # Footer text
    st.markdown(
        """
        <p style="text-align: center; margin-top: 50px;">
        Built with ❤️ by Ponishadevi | Inspiring the Open-Source Future 🌐
        </p>
        """,
        unsafe_allow_html=True,
    )
