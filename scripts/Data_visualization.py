import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Function to plot histograms for numerical columns
def plot_numerical_distributions(data, numerical_columns, figsize=(12, 8)):
    
    plt.figure(figsize=figsize)
    for i, column in enumerate(numerical_columns, 1):
        plt.subplot((len(numerical_columns) // 3) + 1, 3, i)
        plt.hist(data[column], bins=30, alpha=0.7, color='blue')
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

# Function to plot bar charts for categorical columns
def plot_categorical_distributions(data, categorical_columns, figsize=(12, 8)):
    
    plt.figure(figsize=figsize)
    for i, column in enumerate(categorical_columns, 1):
        plt.subplot((len(categorical_columns) // 3) + 1, 3, i)
        data[column].value_counts().plot(kind='bar', alpha=0.7, color='orange')
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()


def calculate_variability_with_plot(car_insu):
    
    numerical_columns = car_insu.select_dtypes(include=['float64', 'int64']).columns
    variability = {
        'Feature': [],
        'Variance': [],
        'Standard Deviation': [],
        'Range': [],
        'IQR (Interquartile Range)': []
    }

    for column in numerical_columns:
        # Variability calculations
        variance = car_insu[column].var()
        std_dev = car_insu[column].std()
        value_range = car_insu[column].max() - car_insu[column].min()
        iqr = car_insu[column].quantile(0.75) - car_insu[column].quantile(0.25)

        # Appending results
        variability['Feature'].append(column)
        variability['Variance'].append(variance)
        variability['Standard Deviation'].append(std_dev)
        variability['Range'].append(value_range)
        variability['IQR (Interquartile Range)'].append(iqr)

    # Creating a DataFrame for variability
    variability_df = pd.DataFrame(variability)

    # Plotting variability metrics
    metrics = ['Variance', 'Standard Deviation', 'Range', 'IQR (Interquartile Range)']
    plt.figure(figsize=(12, 10))
    for i, metric in enumerate(metrics, 1):
        plt.subplot(2, 2, i)  # Adjust layout to 2x2
        plt.bar(variability_df['Feature'], variability_df[metric], color='skyblue')
        plt.title(f'{metric} by Feature')
        plt.xlabel('Feature')
        plt.ylabel(metric)
        plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    return variability_df


def explore_correlations(data, x_feature, y_feature, group_feature):
    
    # Filter numeric columns for correlation matrix
    numeric_data = data[[x_feature, y_feature]]
    correlation_matrix = numeric_data.corr()

    # Overall scatter plot for the entire dataset
    plt.figure(figsize=(10, 6))
    plt.scatter(data[x_feature], data[y_feature], alpha=0.7, color='blue')
    plt.title(f'Scatter Plot: {x_feature} vs {y_feature}')
    plt.xlabel(x_feature)
    plt.ylabel(y_feature)
    plt.grid(True)
    plt.show()

    # Scatter plots grouped by ZipCode
    plt.figure(figsize=(14, 10))
    unique_groups = data[group_feature].unique()

    for i, group in enumerate(unique_groups[:10], 1):  # Limiting to 10 groups for clarity
        plt.subplot(3, 4, i)  # Adjust the layout as needed
        subset = data[data[group_feature] == group]
        plt.scatter(subset[x_feature], subset[y_feature], alpha=0.6, label=f"{group_feature}: {group}")
        plt.title(f'{group_feature}: {group}')
        plt.xlabel(x_feature)
        plt.ylabel(y_feature)
        plt.legend(loc='best', fontsize=8)

    plt.tight_layout()
    plt.show()

    # Correlation matrix heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title(f'Correlation Matrix: {x_feature} & {y_feature}')
    plt.show()

    return correlation_matrix
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def remove_outliers(data, column):
    """
    Remove outliers based on 1.5*IQR rule and return the cleaned data.

    Parameters:
        data (pd.DataFrame): The input dataframe.
        column (str): The column name to remove outliers from.

    Returns:
        pd.DataFrame: The cleaned data with outliers removed for the specified column.
    """
    # Calculate Q1 (25th percentile), Q3 (75th percentile), and IQR
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1

    # Calculate the lower and upper bounds for outlier detection
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filter out the outliers
    cleaned_data = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]

    return cleaned_data

def detect_outliers_boxplots(data):
    """
    Generates box plots to detect and visualize outliers, both before and after removal.

    Parameters:
        data (pd.DataFrame): The input dataset.

    Returns:
        None: Displays the box plots before and after removing outliers for each numerical column.
    """
    # Select numerical columns
    numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns

    # Set up the matplotlib figure
    plt.figure(figsize=(14, 10))

    # Plot before removing outliers
    for i, column in enumerate(numerical_columns, 1):
        plt.subplot(3, 3, i)  # Adjust the layout as needed
        sns.boxplot(x=data[column], color='skyblue')
        plt.title(f'Before: {column}')
        plt.xlabel(column)

    plt.tight_layout()
    plt.show()

    # Remove outliers and plot after removal
    for i, column in enumerate(numerical_columns, 1):
        cleaned_data = remove_outliers(data, column)

        plt.subplot(3, 3, i)  # Adjust the layout as needed
        sns.boxplot(x=cleaned_data[column], color='lightgreen')
        plt.title(f'After: {column}')
        plt.xlabel(column)

    plt.tight_layout()
    plt.show()





   