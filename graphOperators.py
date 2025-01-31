import plotly.offline as po
import plotly.graph_objs as go



def getGraphOfPortfolio(data):
    values = [data[0]['stocks_curr_total'],data[0]['funds_curr_total']]
    labels = ['Hisse Senetleri','Yatırım Fonları']
    pie_fig = go.Figure([
        go.Pie(
            labels=labels,
            values=values,
            pull=[0.2],
            hole=0,
            textinfo=None,
            showlegend=True,
            textfont=dict(color='black'),
        )
    ])
    pie_fig.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            color="#fff",
            size=14,
            family="Arial, bold"

        ),
        legend=dict(
            font=dict(size=18, color='black'),
            orientation="h",
            x=0.93,
            xanchor='right',
            y=1.2,
            yanchor='middle'
        )
    )
    pie_fig.update_traces(
        marker=dict(line=dict(
            color='white',
            width=1)
        ),
        textposition='outside', hoverinfo='none')

    pie_div = po.plot(pie_fig, include_plotlyjs=False, output_type="div", config={'displayModeBar': False, 'staticPlot': True})
    return pie_div


def getGraphOfStockPortfolio(data):
    values = [item["total"] for item in data]
    labels = [item["stock_name"] for item in data]
    pie_fig = go.Figure([
        go.Pie(
            labels=labels,
            values=values,
            hole=0,
            textinfo='label+percent',
            hoverlabel=dict(
                bordercolor=None,
                font=dict(
                    family="Arial, sans-serif",
                    size=16,
                    color="black"
                ),
            ),
            showlegend=True,
            textfont=dict(color='black'),
        )
    ])
    pie_fig.update_layout(
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            color="#fff"
        ),
        legend=dict(
            font=dict(size=14, color='black'),
            orientation="h",
            x=-0.5,
            xanchor='right',
            y=0.5,
            yanchor='middle'
        )
    )
    pie_fig.update_traces(
        marker=dict(line=dict(
            color='white',
            width=1)
        ),
        textposition='outside', hoverinfo='none')

    pie_div = po.plot(pie_fig, include_plotlyjs=False, output_type="div", config={'displayModeBar': False, 'staticPlot': True})
    return pie_div



def getGraphOfFundsPortfolio(data):
    values = [item["total"] for item in data]
    labels = [item["symbol_graph"] for item in data]
    pie_fig = go.Figure([
        go.Pie(
            labels=labels,
            values=values,
            hole=0,
            textinfo=None,
            hoverlabel=dict(
                bordercolor=None,
                font=dict(
                    size=16,
                    color="black"
                ),
            ),
            showlegend=True,
            textfont=dict(color='black'),
        )
    ])
    pie_fig.update_layout(
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            color="#fff"
        ),
        legend=dict(
            font=dict(size=14, color='black'),
            orientation="h",
            x=-0.2,
            xanchor='right',
            y=0.5,
            yanchor='middle'
        )
    )
    pie_fig.update_traces(
        marker=dict(line=dict(
            color='white',
            width=1)
        ),
        textposition='outside', hoverinfo='none')

    pie_div = po.plot(pie_fig, include_plotlyjs=False, output_type="div", config={'displayModeBar': False, 'staticPlot': True})
    return pie_div

def getGraphOfSymbolPrice(raw_data):
    data = []
    for i in raw_data:
        data.append(
            {
                'time':i[4],
                'open':i[0],
                'high':i[1],
                'low':i[2],
                'close':i[3],
            }
        )
    time = [point['time'] for point in data]
    open = [point['open'] for point in data]
    high = [point['high'] for point in data]
    low = [point['low'] for point in data]
    close = [point['close'] for point in data]

    fig = go.Figure(data=[go.Candlestick(x=time,
                                         open=open, high=high,
                                         low=low, close=close)
                          ])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_rangeslider_visible=True,
        height=150,
        width=320,
        xaxis=dict(visible=False),
        margin=dict(
            l=60,
            r=0,
            b=0,
            t=30,
            pad=15
        ),
    )
    fig_div = po.plot(fig,include_plotlyjs=False, output_type="div", config={'displayModeBar': False, 'staticPlot': True})
    return fig_div
