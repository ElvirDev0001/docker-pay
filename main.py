import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
import os

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Savings Over Time for Single and Double Earners"),
    html.Div([
        html.Div([
            html.Label('Netto Pay'),
            dcc.Input(id='netto-pay-input', type='number', value=3000),
            html.Label('Rent'),
            dcc.Input(id='rent-input', type='number', value=1000),
            html.Label('Food Costs'),
            dcc.Input(id='food-input', type='number', value=500),
            html.Label('Extra Costs'),
            dcc.Input(id='extra-input', type='number', value=200),
        ], className='three columns'),

        html.Div([
            dcc.Graph(id='savings-graph'),
        ], className='nine columns'),
    ], className='row')
])

# Define callback to update graph
@app.callback(
    Output('savings-graph', 'figure'),
    [
        Input('netto-pay-input', 'value'),
        Input('rent-input', 'value'),
        Input('food-input', 'value'),
        Input('extra-input', 'value')
    ]
)
def update_figure(netto_pay, rent, food, extra_costs):
    # Compute savings for single and double earner situations
    single_earner_savings = np.zeros(24)
    double_earner_savings = np.zeros(24)

    for i in range(24):
        # Add the normal month's savings
        single_earner_savings[i] = (single_earner_savings[i-1] if i > 0 else 0) + netto_pay - rent - food - extra_costs
        double_earner_savings[i] = (double_earner_savings[i-1] if i > 0 else 0) + 2 * (netto_pay - (rent + food + extra_costs)/2)

        # Add an additional netto_pay on the 6th, 12th, 18th, and 24th month
        if (i+1) % 6 == 0:
            single_earner_savings[i] += netto_pay
            double_earner_savings[i] += 2*netto_pay

    # Create a plotly graph object
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.arange(1, 25, 1), y=single_earner_savings,
                             mode='lines+markers', name='Single Earner'))
    fig.add_trace(go.Scatter(x=np.arange(1, 25, 1), y=double_earner_savings,
                             mode='lines+markers', name='Double Earner'))

    fig.update_layout(title='Savings Over Time',
                      xaxis_title='Months',
                      yaxis_title='Savings (€)')

    return fig

# Expose the Flask server for Gunicorn to use
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
