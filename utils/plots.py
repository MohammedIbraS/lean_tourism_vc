# # utils/plots.py
# import plotly.graph_objects as go
# import plotly.express as px
# import numpy as np


# def make_surface_plotly(x_vals, y_vals, Z, x_label, y_label, z_label, title=None):
#     # ensure numpy arrays
#     x = np.array(x_vals)
#     y = np.array(y_vals)
#     Z = np.array(Z)
#     # symmetric color limits around zero for diverging palette
#     zmin = np.nanmin(Z); zmax = np.nanmax(Z); zabs = max(abs(zmin), abs(zmax))
#     colorscale = [
#         [0.0, "rgb(165,0,38)"],
#         [0.35, "rgb(215,48,39)"],
#         [0.5, "rgb(255,255,255)"],
#         [0.65, "rgb(26,150,65)"],
#         [1.0, "rgb(0,104,55)"]
#     ]
#     fig = go.Figure(data=[go.Surface(z=Z, x=x, y=y, colorscale=colorscale, cmin=-zabs, cmax=zabs)])
#     fig.update_layout(scene=dict(xaxis_title=x_label, yaxis_title=y_label, zaxis_title=z_label), height=700)
#     if title:
#         fig.update_layout(title=title)
#     return fig


# def make_4d_scatter_plotly(df, x_col, y_col, z_col, color_col, title=None):
#     """
#     Creates an interactive 4D scatter plot using plotly.express.
    
#     The first three dimensions are mapped to the X, Y, and Z axes.
#     The fourth dimension is mapped to the color of the markers.

#     Args:
#         df (pd.DataFrame): DataFrame containing the data.
#         x_col (str): Column name for the X axis.
#         y_col (str): Column name for the Y axis.
#         z_col (str): Column name for the Z axis.
#         color_col (str): Column name for the 4th dimension (color).
#         title (str, optional): The plot title.

#     Returns:
#         plotly.graph_objects.Figure: The generated figure object.
#     """
#     fig = px.scatter_3d(df, 
#                         x=x_col, 
#                         y=y_col, 
#                         z=z_col,
#                         color=color_col,
#                         color_continuous_scale=px.colors.sequential.Viridis,
#                         opacity=0.7,
#                         title=title,
#                         hover_data=[color_col]
#                        )

#     fig.update_layout(scene = dict(
#                         xaxis_title=f'{x_col}',
#                         yaxis_title=f'{y_col}',
#                         zaxis_title=f'{z_col}'),
#                         margin=dict(r=10, l=10, b=10, t=40))
    
#     return fig

# utils/plots.py
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd


def make_surface_plotly(x_vals, y_vals, Z, x_label, y_label, z_label, title=None):
    """Legacy surface plot function"""
    x = np.array(x_vals)
    y = np.array(y_vals)
    Z = np.array(Z)
    zmin = np.nanmin(Z)
    zmax = np.nanmax(Z)
    zabs = max(abs(zmin), abs(zmax))
    colorscale = [
        [0.0, "rgb(165,0,38)"],
        [0.35, "rgb(215,48,39)"],
        [0.5, "rgb(255,255,255)"],
        [0.65, "rgb(26,150,65)"],
        [1.0, "rgb(0,104,55)"]
    ]
    fig = go.Figure(data=[go.Surface(z=Z, x=x, y=y, colorscale=colorscale, cmin=-zabs, cmax=zabs)])
    fig.update_layout(
        scene=dict(xaxis_title=x_label, yaxis_title=y_label, zaxis_title=z_label),
        height=700
    )
    if title:
        fig.update_layout(title=title)
    return fig

def create_waterfall_chart(scenario_name, revenue, costs_breakdown, net_profit):
    """
    Create waterfall chart showing revenue to profit breakdown.
    
    Args:
        scenario_name (str): Name of the scenario
        revenue (float): Total revenue
        costs_breakdown (dict): Dictionary of cost categories and values
        net_profit (float): Net profit
    
    Returns:
        plotly.graph_objects.Figure: Waterfall chart
    """
    labels = ['Revenue'] + list(costs_breakdown.keys()) + ['Net Profit']
    values = [revenue] + [-v for v in costs_breakdown.values()] + [net_profit]
    
    # Format numbers for display
    def format_val(v):
        if abs(v) >= 1_000_000:
            return f"SAR {v/1_000_000:.2f}M"
        elif abs(v) >= 1_000:
            return f"SAR {v/1_000:.1f}K"
        else:
            return f"SAR {v:,.0f}"
    
    text_labels = [format_val(v) for v in values]
    
    fig = go.Figure(go.Waterfall(
        name=scenario_name,
        orientation="v",
        measure=["relative"] * len(values),
        x=labels,
        y=values,
        text=text_labels,
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "green"}},
        decreasing={"marker": {"color": "red"}},
        totals={"marker": {"color": "blue"}}
    ))
    
    fig.update_layout(
        title=f"{scenario_name} - Revenue to Profit",
        showlegend=False,
        height=500,
        margin=dict(t=60, b=80, l=100, r=60),
        autosize=True,
        yaxis=dict(
            automargin=True,
            fixedrange=False,
            title="Amount (SAR)"
        ),
        xaxis=dict(
            automargin=True,
            tickangle=-45
        )
    )
    
    return fig


def make_4d_scatter_plotly(df, x_col, y_col, z_col, color_col, title=None):
    """Legacy 4D scatter plot function"""
    fig = px.scatter_3d(
        df, 
        x=x_col, 
        y=y_col, 
        z=z_col,
        color=color_col,
        color_continuous_scale=px.colors.sequential.Viridis,
        opacity=0.7,
        title=title,
        hover_data=[color_col]
    )
    fig.update_layout(
        scene=dict(
            xaxis_title=f'{x_col}',
            yaxis_title=f'{y_col}',
            zaxis_title=f'{z_col}'
        ),
        margin=dict(r=10, l=10, b=10, t=40)
    )
    return fig


def create_tornado_chart(df, scenario_name):
    """
    Create a tornado chart showing sensitivity of net profit to each parameter.
    Shows the range of profit impact when each parameter varies.
    """
    params = ['Sick %', '% VC Uptake']
    if 'VC Fee' in df.columns:
        params.append('VC Fee')
    if 'EI Fee' in df.columns:
        params.append('EI Fee')
    
    impacts = []
    for param in params:
        grouped = df.groupby(param)['net_profit'].agg(['min', 'max', 'mean'])
        impact_range = grouped['max'].max() - grouped['min'].min()
        impacts.append({
            'Parameter': param,
            'Range': impact_range,
            'Min': grouped['min'].min(),
            'Max': grouped['max'].max()
        })
    
    impacts_df = pd.DataFrame(impacts).sort_values('Range', ascending=True)
    
    fig = go.Figure()
    
    # Add bars for negative and positive impacts
    for idx, row in impacts_df.iterrows():
        center = (row['Max'] + row['Min']) / 2
        width = row['Max'] - row['Min']
        
        fig.add_trace(go.Bar(
            name=row['Parameter'],
            y=[row['Parameter']],
            x=[width],
            orientation='h',
            marker=dict(color='#1f77b4'),
            text=[f"SAR {width/1e6:.2f}M"],
            textposition='outside'
        ))
    
    fig.update_layout(
        title=f"Parameter Sensitivity — {scenario_name}",
        xaxis_title="Profit Impact Range (SAR)",
        yaxis_title="Parameter",
        height=400,
        showlegend=False,
        margin=dict(l=150, r=50, t=60, b=50)
    )
    
    return fig


def create_2d_heatmap(df, x_col, y_col, z_col, title):
    """
    Create a 2D heatmap showing the relationship between two parameters and profit.
    More interpretable than 4D scatter plots.
    """
    # Pivot the data for heatmap
    pivot_df = df.pivot_table(values=z_col, index=y_col, columns=x_col, aggfunc='mean')
    
    # Create custom colorscale (red for loss, green for profit)
    colorscale = [
        [0.0, "rgb(165,0,38)"],    # Dark red
        [0.35, "rgb(215,48,39)"],  # Red
        [0.5, "rgb(255,255,255)"],  # White
        [0.65, "rgb(26,150,65)"],  # Green
        [1.0, "rgb(0,104,55)"]     # Dark green
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale=colorscale,
        zmid=0,
        colorbar=dict(title="Net Profit (SAR)"),
        hovertemplate=f'{x_col}: %{{x}}<br>{y_col}: %{{y}}<br>Profit: SAR %{{z:,.0f}}<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_col,
        height=500,
        margin=dict(l=80, r=80, t=60, b=60)
    )
    
    return fig


def create_parameter_impact_lines(df, scenario_name):
    """
    Create line plots showing how profit changes with each parameter individually.
    """
    params = ['Sick %', '% VC Uptake']
    fee_col = 'VC Fee' if 'VC Fee' in df.columns else 'EI Fee'
    params.append(fee_col)
    
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    for idx, param in enumerate(params):
        grouped = df.groupby(param)['net_profit'].mean().reset_index()
        
        fig.add_trace(go.Scatter(
            x=grouped[param],
            y=grouped['net_profit'],
            mode='lines+markers',
            name=param,
            line=dict(color=colors[idx], width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title=f"Parameter Impact on Average Net Profit — {scenario_name}",
        xaxis_title="Parameter Value",
        yaxis_title="Average Net Profit (SAR)",
        height=500,
        hovermode='x unified',
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)'),
        margin=dict(l=80, r=50, t=60, b=60)
    )
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even")
    
    return fig


def create_breakeven_chart(df, fixed_sick, fixed_vc, breakeven_fee):
    """
    Create a chart showing profit vs VC Fee at fixed sick% and VC uptake%.
    Highlights the break-even point.
    """
    # Filter data close to fixed parameters
    filtered = df[
        (np.abs(df['Sick %'] - fixed_sick*100) < 0.5) &
        (np.abs(df['% VC Uptake'] - fixed_vc*100) < 0.5)
    ]
    
    if len(filtered) == 0:
        filtered = df  # Fallback to all data
    
    grouped = filtered.groupby('VC Fee')['net_profit'].mean().reset_index()
    
    fig = go.Figure()
    
    # Add profit line
    fig.add_trace(go.Scatter(
        x=grouped['VC Fee'],
        y=grouped['net_profit'],
        mode='lines+markers',
        name='Net Profit',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    # Add break-even line
    fig.add_hline(y=0, line_dash="dash", line_color="red", 
                  annotation_text="Break-even", annotation_position="right")
    
    # Add break-even point marker
    fig.add_trace(go.Scatter(
        x=[breakeven_fee],
        y=[0],
        mode='markers',
        name='Break-even Point',
        marker=dict(color='red', size=15, symbol='star')
    ))
    
    fig.update_layout(
        title=f"Break-Even Analysis: Sick={fixed_sick*100:.1f}%, VC Uptake={fixed_vc*100:.1f}%",
        xaxis_title="VC Fee (SAR)",
        yaxis_title="Net Profit (SAR)",
        height=500,
        hovermode='x unified',
        margin=dict(l=80, r=50, t=60, b=60)
    )
    
    return fig


def create_breakeven_chart_b(df, fixed_sick, fixed_vc, breakeven_ei):
    """
    Create a chart showing profit vs EI Fee at fixed sick% and VC uptake% for Scenario B.
    """
    # Filter data close to fixed parameters
    filtered = df[
        (np.abs(df['Sick %'] - fixed_sick*100) < 0.5) &
        (np.abs(df['% VC Uptake'] - fixed_vc*100) < 0.5)
    ]
    
    if len(filtered) == 0:
        filtered = df
    
    grouped = filtered.groupby('EI Fee')['net_profit'].mean().reset_index()
    
    fig = go.Figure()
    
    # Add profit line
    fig.add_trace(go.Scatter(
        x=grouped['EI Fee'],
        y=grouped['net_profit'],
        mode='lines+markers',
        name='Net Profit',
        line=dict(color='#ff7f0e', width=3),
        marker=dict(size=8)
    ))
    
    # Add break-even line
    fig.add_hline(y=0, line_dash="dash", line_color="red",
                  annotation_text="Break-even", annotation_position="right")
    
    # Add break-even point marker
    fig.add_trace(go.Scatter(
        x=[breakeven_ei],
        y=[0],
        mode='markers',
        name='Break-even Point',
        marker=dict(color='red', size=15, symbol='star')
    ))
    
    fig.update_layout(
        title=f"Break-Even Analysis: Sick={fixed_sick*100:.1f}%, VC Uptake={fixed_vc*100:.1f}%",
        xaxis_title="Emergency Insurance Fee (SAR)",
        yaxis_title="Net Profit (SAR)",
        height=500,
        hovermode='x unified',
        margin=dict(l=80, r=50, t=60, b=60)
    )
    
    return fig


def create_correlation_heatmap(df, scenario_name):
    """
    Create a correlation matrix heatmap showing relationships between parameters and outcomes.
    """
    # Select relevant columns
    if 'VC Fee' in df.columns:
        cols = ['Sick %', '% VC Uptake', 'VC Fee', 'revenue', 'cost_vc', 'net_profit']
    else:
        cols = ['Sick %', '% VC Uptake', 'EI Fee', 'revenue', 'cost_vc', 'cost_emergency', 'net_profit']
    
    corr_df = df[cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_df.values,
        x=corr_df.columns,
        y=corr_df.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_df.values,
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title=f"Parameter Correlation Matrix — {scenario_name}",
        height=600,
        margin=dict(l=100, r=50, t=60, b=100)
    )
    
    return fig


def create_3d_profit_zones(df, x_col, y_col, z_col, color_col, scenario_name):
    """
    Create a 3D scatter plot with color-coded profit zones.
    Better than the original 4D scatter with improved colors and zones.
    """
    # Define profit zones
    max_profit = df[color_col].max()
    min_profit = df[color_col].min()
    
    df['profit_zone'] = pd.cut(
        df[color_col],
        bins=[-np.inf, 0, max_profit*0.3, max_profit*0.7, np.inf],
        labels=['Loss', 'Low Profit', 'Medium Profit', 'High Profit']
    )
    
    color_map = {
        'Loss': '#d62728',           # Red
        'Low Profit': '#ff7f0e',     # Orange
        'Medium Profit': '#2ca02c',  # Green
        'High Profit': '#1f77b4'     # Blue
    }
    
    fig = go.Figure()
    
    for zone in ['Loss', 'Low Profit', 'Medium Profit', 'High Profit']:
        zone_df = df[df['profit_zone'] == zone]
        if len(zone_df) > 0:
            fig.add_trace(go.Scatter3d(
                x=zone_df[x_col],
                y=zone_df[y_col],
                z=zone_df[z_col],
                mode='markers',
                name=zone,
                marker=dict(
                    size=4,
                    color=color_map[zone],
                    opacity=0.7
                ),
                hovertemplate=f'{x_col}: %{{x}}<br>{y_col}: %{{y}}<br>{z_col}: %{{z}}<br>Profit: SAR %{{text:,.0f}}<extra></extra>',
                text=zone_df[color_col]
            ))
    
    fig.update_layout(
        title=f"3D Profit Zones — {scenario_name}",
        scene=dict(
            xaxis_title=x_col,
            yaxis_title=y_col,
            zaxis_title=z_col
        ),
        height=700,
        margin=dict(r=10, l=10, b=10, t=60),
        legend=dict(x=0.7, y=0.9, bgcolor='rgba(255,255,255,0.8)')
    )
    
    return fig


def create_optimal_ranges_chart(df):
    """
    Create a chart showing the optimal ranges for each parameter based on profitability.
    """
    # Get top 10% most profitable scenarios
    threshold = df['net_profit'].quantile(0.9)
    optimal_df = df[df['net_profit'] >= threshold]
    
    params = ['Sick %', '% VC Uptake']
    if 'VC Fee' in df.columns:
        params.append('VC Fee')
    if 'EI Fee' in df.columns:
        params.append('EI Fee')
    
    fig = go.Figure()
    
    for param in params:
        param_range = [optimal_df[param].min(), optimal_df[param].max()]
        param_mean = optimal_df[param].mean()
        
        fig.add_trace(go.Box(
            y=[param],
            x=optimal_df[param],
            name=param,
            orientation='h',
            boxmean='sd',
            marker=dict(color='#1f77b4')
        ))
    
    fig.update_layout(
        title="Optimal Parameter Ranges (Top 10% Profitable Scenarios)",
        xaxis_title="Parameter Value",
        yaxis_title="Parameter",
        height=400,
        showlegend=False,
        margin=dict(l=150, r=50, t=60, b=50)
    )
    
    return fig