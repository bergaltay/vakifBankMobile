import plotly.offline as po
import plotly.graph_objs as go

def getGraphOfPortfolio(data):
    values = [item["total"] for item in data]
    labels = [item["symbol"] for item in data]
    pie_fig = go.Figure([
        go.Pie(
            labels=labels,
            values=values,
            hole=0,
            textinfo='label+percent',
            hoverlabel=dict(
                bordercolor=None,  # Border color
                font=dict(
                    family="Arial, sans-serif",  # Font family
                    size=16,  # Font size
                    color="black"  # Font color
                ),
            ),
            showlegend=True,
            textfont=dict(color='black'),  # Set label text color to black
        )
    ])
    pie_fig.update_layout(
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent surrounding area
        font=dict(
            color="#fff"  # Change this to the desired text color
        ),
        legend=dict(
            font=dict(size=14, color='black'),  # Legend font size and color
            orientation="h",  # Horizontal legend
            x=0,  # Center the legend horizontally
            xanchor='right',  # Align legend by its center
            y=0.5,  # Position above the chart
            yanchor='middle'  # Align legend by its top
        )
    )
    pie_fig.update_traces(marker=dict(line=dict(color='white', width=4)),textposition='outside')
    pie_div = po.plot(pie_fig, include_plotlyjs=False, output_type="div",config={'displayModeBar': False})
    return pie_div
