import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd


def generate_mock_data():
    """
    Generates mock log data for testing purposes.
    Replace with DB queries in production.
    """
    data = {
        'ip': ['192.168.1.1', '10.0.0.2', '172.16.0.3', '192.168.1.1', '10.0.0.2', '10.0.0.2'],
        'severity': ['error', 'info', 'warning', 'info', 'error', 'warning'],
        'service': ['apache', 'ftp', 'apache', 'ssh', 'ftp', 'apache']
    }
    return pd.DataFrame(data)


def plot_grouped_events(data: pd.DataFrame, group_by='ip', chart_type='bar', export_path=None, interactive=False):
    """
    Generates a chart grouping events by a specific column (e.g., IP, severity).
    
    Parameters:
        data (pd.DataFrame): The dataframe containing log events.
        group_by (str): The column to group data by ('ip', 'severity', 'service').
        chart_type (str): Type of chart: 'bar' or 'pie'.
        export_path (str): File path to export the chart (png or html).
        interactive (bool): Use Plotly (True) or Matplotlib (False).
    """
    if group_by not in data.columns:
        raise ValueError(f"'{group_by}' not found in data columns: {list(data.columns)}")

    grouped = data[group_by].value_counts().head(10)

    if grouped.empty:
        print("No data to plot.")
        return

    title = f"Top 10 {group_by.capitalize()}s by Event Count"

    if interactive:
        fig = (
            px.pie(names=grouped.index, values=grouped.values, title=title)
            if chart_type == 'pie'
            else px.bar(x=grouped.index, y=grouped.values, title=title, labels={'x': group_by, 'y': 'Events'})
        )
        if export_path:
            fig.write_html(export_path)
            print(f"✅ Chart exported as HTML: {export_path}")
        else:
            fig.show()
    else:
        plt.figure(figsize=(10, 6))
        if chart_type == 'pie':
            plt.pie(grouped.values, labels=grouped.index, autopct='%1.1f%%')
        else:
            plt.bar(grouped.index, grouped.values)
            plt.xlabel(group_by.capitalize())
            plt.ylabel("Event Count")
        plt.title(title)
        plt.tight_layout()
        if export_path:
            plt.savefig(export_path)
            print(f"✅ Chart saved as PNG: {export_path}")
        else:
            plt.show()


# Manual test block (only runs when called directly)
if __name__ == "__main__":
    df = generate_mock_data()

    # Try different charts manually
    plot_grouped_events(df, group_by='ip', chart_type='bar', interactive=False)
    # plot_grouped_events(df, group_by='severity', chart_type='pie', export_path="severity_pie.html", interactive=True)
