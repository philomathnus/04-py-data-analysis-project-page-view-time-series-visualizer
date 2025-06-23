import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')
df.columns = ['views']

# Clean data
df.index = pd.to_datetime(df.index, format='ISO8601')
df = df[(df.views > df.views.quantile(0.025)) & (df.views < df.views.quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(20, 8))
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.plot(df.index, df['views'])

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)
    df_bar['year'] = [d.year for d in df_bar.date]

    # Getting the list of month names
    list_of_months = list(pd.date_range(start='2025-01-01', 
                                        periods=12, 
                                        freq='ME').strftime('%B'))
    df_bar['month'] = pd.Categorical(df.index.strftime('%B'), categories=list_of_months, ordered=True)
    df_bar = df_bar.pivot_table(values='views', index='year', columns='month', aggfunc='mean', observed=True)
    
    # Draw bar plot
    ax = df_bar.plot(kind='bar', figsize=(10, 8))
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    fig = ax.get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    #df_box['month'] = [d.strftime('%b') for d in df_box.date]
    # Getting the list of month names
    list_of_months = list(pd.date_range(start='2025-01-01', 
                                        periods=12, 
                                        freq='ME').strftime('%b'))
    df_box['month'] = pd.Categorical(df.index.strftime('%b'), categories=list_of_months, ordered=True)
    #df_box = df_box.pivot_table(values='views', index='year', columns='month', aggfunc='mean', observed=True)
    #print(df_box)
    
    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(1, 2, figsize=(20, 8))
    sns.boxplot(ax=axs[0], data=df_box, x='year', y='views', hue='year')
    axs[0].set_title('Year-wise Box Plot (Trend)')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Page Views')

    sns.boxplot(ax=axs[1], data=df_box, x='month', y='views', hue='month')
    axs[1].set_title('Month-wise Box Plot (Seasonality)')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Page Views')

    plt.tight_layout()
    
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
