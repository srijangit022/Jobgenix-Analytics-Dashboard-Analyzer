import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Function to load the data file
def load_file():
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)
            st.success("File uploaded successfully!")
            return data
        except Exception as e:
            st.error(f"Failed to load file: {e}")
            return None
    return None

# Function to show the data table
def show_data_table(data):
    if data is not None:
        st.subheader("Data Table")
        st.dataframe(data)
    else:
        st.warning("Please upload a data file first!")

# Function to generate single visualization
def generate_visualization(data, plot_type, x_column, y_column):
    if x_column not in data.columns or y_column not in data.columns:
        st.error("Selected columns are invalid. Please choose valid columns.")
        return

    plt.figure(figsize=(8, 6))

    try:
        if plot_type == "Bar Chart":
            plt.bar(data[x_column], data[y_column])
        elif plot_type == "Horizontal Bar Chart":
            plt.barh(data[x_column], data[y_column])
        elif plot_type == "Line Graph":
            plt.plot(data[x_column], data[y_column])
        elif plot_type == "Pie Chart":
            data[y_column].value_counts().plot.pie(autopct="%1.1f%%")
        elif plot_type == "Histogram":
            plt.hist(data[y_column])
        elif plot_type == "Box Plot":
            plt.boxplot(data[y_column])
        elif plot_type == "Area Plot":
            plt.fill_between(data.index, data[y_column])

        plt.title(f"{plot_type} of {y_column} against {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        st.pyplot(plt)
    except Exception as e:
        st.error(f"Error generating visualization: {e}")

# Function to generate a complete dashboard
def generate_dashboard(data):
    if data is None:
        st.warning("Please upload a data file first!")
        return

    try:
        st.subheader("Dashboard View: Complete Visualization in Single Frame")

        # Separate numeric and categorical columns
        numeric_columns = data.select_dtypes(include=["number"]).columns.tolist()
        categorical_columns = data.select_dtypes(exclude=["number"]).columns.tolist()

        if not numeric_columns and not categorical_columns:
            st.warning("No data available for visualization!")
            return

        # Determine the number of rows
        total_plots = len(numeric_columns) + len(categorical_columns)
        fig, axs = plt.subplots(
            nrows=total_plots,
            ncols=1,
            figsize=(8, 4 * total_plots),
            dpi=100,
        )

        # Adjust when there's only one plot
        if total_plots == 1:
            axs = [axs]

        # Plot numeric columns
        for idx, col in enumerate(numeric_columns):
            axs[idx].bar(data.index, data[col])
            axs[idx].set_title(f"Bar Graph - {col}")
            axs[idx].set_xlabel("Index")
            axs[idx].set_ylabel(col)

        # Plot categorical columns
        for idx, col in enumerate(categorical_columns, start=len(numeric_columns)):
            data[col].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=axs[idx])
            axs[idx].set_title(f"Pie Chart - {col}")
            axs[idx].set_ylabel("")  # Remove default ylabel

        # Tighten layout
        plt.tight_layout()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Failed to generate dashboard: {e}")

# Main function for the Streamlit app
def main():
    # Add the logo using st.image()
    st.image("Jobgenix.jpg", use_column_width=True)  # Replace "path_to_logo.jpeg" with the actual path to the image file
    st.title("Jobgenix Analytics Dashboard")
    st.markdown("Upload your data file, explore the dataset, and create dynamic visualizations with ease.")

    # File upload and data loading
    data = load_file()

    if data is not None:
        # Create a layout with three tabs
        tab1, tab2, tab3 = st.tabs(["📊 Data Table", "📈 Single Visualizations", "🖥️ Dashboard View"])

        # Tab 1: Display the data table
        with tab1:
            if st.checkbox("Show Data Table", value=True):
                show_data_table(data)

        # Tab 2: Create single visualizations
        with tab2:
            st.subheader("Create Visualizations")

            # Dropdowns for visualization type and column selection
            plot_type = st.selectbox(
                "Choose Visualization Type",
                ["Bar Chart", "Horizontal Bar Chart", "Line Graph", "Pie Chart", "Stacked Bar Chart",
                 "Histogram", "Box Plot", "Area Plot"]
            )

            # Dynamic dropdowns for X and Y column selection
            columns = data.columns.tolist()
            x_column = st.selectbox("Select X-axis column", columns, index=0)
            y_column = st.selectbox("Select Y-axis column", columns, index=1)

            if st.button("Generate Visualization"):
                generate_visualization(data, plot_type, x_column, y_column)

        # Tab 3: Dashboard view
        with tab3:
            generate_dashboard(data)

if __name__ == "__main__":
    main()
