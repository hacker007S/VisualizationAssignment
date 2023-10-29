# 1. Import modules
import pandas as pd
import matplotlib.pyplot as plt

# 2. Define functions

def line_plot(data, x_label, y_label, title, labels):
    """
    Create a line plot showing multiple lines with proper labels and legend.

    Args:
    data (list of lists): Data to be plotted. Each sublist represents a line.
    x_label (str): Label for the x-axis.
    y_label (str): Label for the y-axis.
    title (str): Title of the plot.
    labels (list of str): Labels for each line.

    Returns:
    None
    """
    for i in range(len(data)):
        plt.plot(data.index, data.iloc[:,i], label=labels[i])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.show()


def histogram_plot(data, x_label, y_label, title):
    """
    Create a histogram to show the distribution of a dataset.

    Args:
    data (list): Data to be plotted.
    x_label (str): Label for the x-axis.
    y_label (str): Label for the y-axis.
    title (str): Title of the plot.

    Returns:
    None
    """
    plt.hist(data, bins=10, alpha=0.7, rwidth=0.85)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()


def bar_chart(labels, data, x_label, y_label, title):
    """
    Create a bar chart to compare values.

    Args:
    data (list): Data to be plotted.
    labels (list of str): Labels for each bar.
    x_label (str): Label for the x-axis.
    y_label (str): Label for the y-axis.
    title (str): Title of the plot.

    Returns:
    None
    """
    # plt.bar(labels, data)
    plt.bar(labels, data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    plt.title(title)
    plt.show()


def pie_chart(data, labels, title):
    """
    Create a pie chart to compare sizes.

    Args:
    data (list): Data to be plotted.
    labels (list of str): Labels for each slice.
    title (str): Title of the plot.

    Returns:
    None
    """
    plt.pie(data, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    plt.show()


## custom function to generate age band out of age
def binnify(age):
    """
    Define Age Band of based on age

    Args:
    age (int): age of person.

    Returns:
    age_band (str)
    """

    if age<12:
        return 'Child (<12)'
    elif 12<age<20:
        return 'Teenager (12 - 20)'
    elif 20<=age<=30:
        return 'Young Adult (20 - 30)'
    elif 30<age<=40:
        return 'Adult (30 - 40)'
    elif 40<age<=50:
        return 'Older Adult (40 - 50)'
    elif 50<age:
        return 'Old (50+)'

# 3. Main program

## Visualization 1
data = pd.read_csv('dft-road-casualty-statistics-casualty-2022.csv')
histogram_plot(data['age_of_casualty'], 'Age of Casuality', 'Frequency', 'Which age has most casuality')

## Visualization 2
data = pd.read_csv('dft-road-casualty-statistics-vehicle-2022.csv')
data['age_band'] = data['age_of_driver'].apply(lambda x: binnify(x))
df = data['age_band'].value_counts()
print(df.head())
pie_chart(df.values, df.index, 'What age band is more involved in causing accident?')

data = pd.read_csv('dft-road-casualty-statistics-casualty-2022.csv')
data['age_band'] = data['age_of_casualty'].apply(lambda x: binnify(x))
df = data['age_band'].value_counts()
pie_chart(df.values, df.index, 'What age band suffers most life loss due to accident?')

## Visualization 3
data = pd.read_csv('dft-road-casualty-statistics-vehicle-2022.csv')
df = data['generic_make_model'].value_counts()
df = df.iloc[1:21]
bar_chart(df.index, df.values, 'Make Models', 'Casulities Caused', '20 Most involved cars in accidents')

## Visualization 4
data1 = pd.read_csv('dft-road-casualty-statistics-vehicle-last-5-years.csv')
data2 = pd.read_csv('dft-road-casualty-statistics-casualty-last-5-years.csv')
data = pd.merge(data1, data2, on='accident_index', how='inner')
top_n = data['generic_make_model'].value_counts().nlargest(8)
top_n_index = top_n.index[1:]
df = data[data['generic_make_model'].isin(top_n_index)]
df = pd.pivot_table(df, columns=['generic_make_model'], values = ['lsoa_of_casualty'], index='accident_year_x', aggfunc='count')
df.columns = df.columns.droplevel(level=0)
df.columns.name = None
line_plot(df, 'Make Models', 'Casualities Caused', 'Trends of casulities caused by different car models', top_n_index)