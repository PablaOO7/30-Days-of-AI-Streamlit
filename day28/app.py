# Install: streamlit, pandas, plotly, numpy
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

# Page config
st.set_page_config(
    page_title="Data Dashboard",
    page_icon=":material/analytics:",
    layout="wide"
)

# Initialize session state
st.session_state.setdefault("df", None)
st.session_state.setdefault("uploaded_filename", None)

# Sidebar
with st.sidebar:
    st.header(":material/upload: Upload Data")
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        key="file_uploader"
    )
    
    if uploaded_file is not None:
        try:
            # Read the uploaded file
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.session_state.uploaded_filename = uploaded_file.name
            st.success(f"✓ Loaded {uploaded_file.name}")
            st.info(f"**Rows:** {len(df):,}  \n**Columns:** {len(df.columns)}")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    
    # Sample data option
    st.divider()
    st.subheader(":material/database: Sample Data")
    if st.button(":material/play_arrow: Load Sample Data", use_container_width=True):
        # Create sample sales data
        import numpy as np
        from datetime import datetime, timedelta
        
        np.random.seed(42)
        dates = [datetime.now() - timedelta(days=x) for x in range(365)]
        
        sample_df = pd.DataFrame({
            'Date': dates,
            'Sales': np.random.randint(1000, 5000, 365),
            'Profit': np.random.randint(100, 1000, 365),
            'Region': np.random.choice(['North', 'South', 'East', 'West'], 365),
            'Category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], 365),
            'Units_Sold': np.random.randint(10, 200, 365)
        })
        
        st.session_state.df = sample_df
        st.session_state.uploaded_filename = "sample_sales_data.csv"
        st.rerun()

# Main content
st.title(":material/analytics: Interactive Data Dashboard")
st.write("Upload a CSV file or load sample data to visualize your data with interactive Plotly charts")

# Check if data is loaded
if st.session_state.df is not None:
    df = st.session_state.df
    
    # Data preview section
    st.header(":material/table_chart: Data Preview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Rows", f"{len(df):,}")
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        numeric_cols = df.select_dtypes(include=['number']).columns
        st.metric("Numeric Columns", len(numeric_cols))
    with col4:
        st.metric("File", st.session_state.uploaded_filename)
    
    # Display dataframe
    with st.expander(":material/visibility: View Data", expanded=False):
        st.dataframe(df, use_container_width=True, height=300)
    
    st.divider()
    
    # Chart configuration
    st.header(":material/bar_chart: Visualizations")
    
    # Get column types
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Try to detect date columns
    for col in df.columns:
        if col not in datetime_cols:
            try:
                pd.to_datetime(df[col])
                datetime_cols.append(col)
            except:
                pass
    
    # Chart type selector
    chart_type = st.selectbox(
        ":material/query_stats: Select Chart Type",
        ["Line Chart", "Bar Chart", "Scatter Plot", "Box Plot", "Histogram", "Pie Chart", "Heatmap"],
        key="chart_type"
    )
    
    # Chart configuration based on type
    if chart_type == "Line Chart":
        col1, col2 = st.columns(2)
        with col1:
            if datetime_cols:
                x_col = st.selectbox("X-axis (Time)", datetime_cols, key="line_x")
            else:
                x_col = st.selectbox("X-axis", df.columns, key="line_x")
        with col2:
            y_col = st.selectbox("Y-axis (Values)", numeric_cols if numeric_cols else df.columns, key="line_y")
        
        if datetime_cols and x_col in datetime_cols:
            df[x_col] = pd.to_datetime(df[x_col])
        
        color_by = None
        if categorical_cols:
            color_by = st.selectbox("Color by (optional)", ["None"] + categorical_cols, key="line_color")
            color_by = None if color_by == "None" else color_by
        
        fig = px.line(df, x=x_col, y=y_col, color=color_by,
                     title=f"{y_col} over {x_col}")
        
    elif chart_type == "Bar Chart":
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("X-axis (Categories)", df.columns, key="bar_x")
        with col2:
            y_col = st.selectbox("Y-axis (Values)", numeric_cols if numeric_cols else df.columns, key="bar_y")
        
        color_by = None
        if categorical_cols:
            color_by = st.selectbox("Color by (optional)", ["None"] + categorical_cols, key="bar_color")
            color_by = None if color_by == "None" else color_by
        
        fig = px.bar(df, x=x_col, y=y_col, color=color_by,
                    title=f"{y_col} by {x_col}")
        
    elif chart_type == "Scatter Plot":
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("X-axis", numeric_cols if numeric_cols else df.columns, key="scatter_x")
        with col2:
            y_col = st.selectbox("Y-axis", numeric_cols if numeric_cols else df.columns, key="scatter_y")
        
        color_by = None
        size_by = None
        if categorical_cols:
            color_by = st.selectbox("Color by (optional)", ["None"] + categorical_cols, key="scatter_color")
            color_by = None if color_by == "None" else color_by
        if numeric_cols:
            size_by = st.selectbox("Size by (optional)", ["None"] + numeric_cols, key="scatter_size")
            size_by = None if size_by == "None" else size_by
        
        fig = px.scatter(df, x=x_col, y=y_col, color=color_by, size=size_by,
                        title=f"{y_col} vs {x_col}")
        
    elif chart_type == "Box Plot":
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("Category", categorical_cols if categorical_cols else df.columns, key="box_x")
        with col2:
            y_col = st.selectbox("Values", numeric_cols if numeric_cols else df.columns, key="box_y")
        
        color_by = None
        if categorical_cols:
            color_by = st.selectbox("Color by (optional)", ["None"] + categorical_cols, key="box_color")
            color_by = None if color_by == "None" else color_by
        
        fig = px.box(df, x=x_col, y=y_col, color=color_by,
                    title=f"Distribution of {y_col} by {x_col}")
        
    elif chart_type == "Histogram":
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("Column", numeric_cols if numeric_cols else df.columns, key="hist_x")
        with col2:
            bins = st.slider("Number of bins", 5, 100, 30, key="hist_bins")
        
        color_by = None
        if categorical_cols:
            color_by = st.selectbox("Color by (optional)", ["None"] + categorical_cols, key="hist_color")
            color_by = None if color_by == "None" else color_by
        
        fig = px.histogram(df, x=x_col, nbins=bins, color=color_by,
                          title=f"Distribution of {x_col}")
        
    elif chart_type == "Pie Chart":
        col1, col2 = st.columns(2)
        with col1:
            names_col = st.selectbox("Categories", categorical_cols if categorical_cols else df.columns, key="pie_names")
        with col2:
            values_col = st.selectbox("Values", numeric_cols if numeric_cols else df.columns, key="pie_values")
        
        # Aggregate data for pie chart
        pie_data = df.groupby(names_col)[values_col].sum().reset_index()
        
        fig = px.pie(pie_data, names=names_col, values=values_col,
                    title=f"{values_col} by {names_col}")
        
    elif chart_type == "Heatmap":
        # Only show numeric columns for correlation heatmap
        if len(numeric_cols) >= 2:
            correlation = df[numeric_cols].corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=correlation.values,
                x=correlation.columns,
                y=correlation.columns,
                colorscale='RdBu',
                zmid=0,
                text=correlation.values.round(2),
                texttemplate='%{text}',
                textfont={"size": 10}
            ))
            
            fig.update_layout(
                title="Correlation Heatmap",
                xaxis_title="Features",
                yaxis_title="Features"
            )
        else:
            st.warning("Heatmap requires at least 2 numeric columns")
            fig = None
    
    # Display the chart
    if fig is not None:
        fig.update_layout(
            height=600,
            hovermode='closest',
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Download chart
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button(":material/download: Download Chart", key="download_chart"):
                st.info("Right-click on the chart and select 'Save as PNG' or use the camera icon in the chart toolbar")
    
    # Summary statistics
    st.divider()
    st.header(":material/query_stats: Summary Statistics")
    
    if numeric_cols:
        stats_df = df[numeric_cols].describe().T
        stats_df['missing'] = df[numeric_cols].isnull().sum()
        stats_df = stats_df[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max', 'missing']]
        
        st.dataframe(
            stats_df.style.format("{:.2f}"),
            use_container_width=True
        )
    else:
        st.info("No numeric columns available for statistics")

else:
    # Empty state
    st.info(":material/info: Upload a CSV file or load sample data to get started")
    
    st.markdown("""
    ### Features
    
    - **Multiple Chart Types**: Line, Bar, Scatter, Box, Histogram, Pie, and Heatmap
    - **Interactive Visualizations**: Zoom, pan, and hover for details
    - **Flexible Configuration**: Choose columns and customize your charts
    - **Summary Statistics**: Automatic statistical analysis
    - **Sample Data**: Try it out with built-in sample data
    
    Get started by uploading your data using the sidebar!
    """)