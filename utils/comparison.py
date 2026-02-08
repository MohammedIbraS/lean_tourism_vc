"""
Comparison utilities for scenario analysis
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def format_number(value, is_currency=False, is_percentage=False):
    """Format numbers for readability: K, M, B notation"""
    if value is None or (isinstance(value, str) and value == 'n/a'):
        return 'n/a'
    
    if is_percentage:
        return f"{value:.1f}%"
    
    prefix = "SAR " if is_currency else ""
    
    if abs(value) >= 1_000_000_000:
        return f"{prefix}{value/1_000_000_000:.2f}B"
    elif abs(value) >= 1_000_000:
        return f"{prefix}{value/1_000_000:.2f}M"
    elif abs(value) >= 10_000:
        return f"{prefix}{value/1_000:.1f}K"
    else:
        return f"{prefix}{value:,.0f}"

def create_scenario_comparison_chart(kpisA, kpisB, title="Scenario Comparison"):
    """Create a comprehensive comparison chart between scenarios"""
    metrics = ['Revenue (SAR)', 'Net Profit (SAR)', 'VC Cost (SAR)', 'Profit Margin']
    
    # Filter available metrics
    available_metrics = [m for m in metrics if m in kpisA and m in kpisB]
    
    fig = go.Figure()
    
    values_a = [kpisA[m] if isinstance(kpisA[m], (int, float)) else 0 for m in available_metrics]
    values_b = [kpisB[m] if isinstance(kpisB[m], (int, float)) else 0 for m in available_metrics]
    
    # Normalize for percentage metrics
    normalized_metrics = []
    normalized_values_a = []
    normalized_values_b = []
    
    for i, metric in enumerate(available_metrics):
        if 'Margin' in metric:
            normalized_metrics.append(metric)
            normalized_values_a.append(values_a[i])
            normalized_values_b.append(values_b[i])
        else:
            normalized_metrics.append(metric)
            normalized_values_a.append(values_a[i])
            normalized_values_b.append(values_b[i])
    
    fig.add_trace(go.Bar(
        name='Scenario A (Paid VC)',
        x=normalized_metrics,
        y=normalized_values_a,
        marker_color='#1f77b4',
        text=[format_number(v, is_currency='SAR' in m, is_percentage='Margin' in m) 
              for v, m in zip(normalized_values_a, normalized_metrics)],
        textposition='outside',
    ))
    
    fig.add_trace(go.Bar(
        name='Scenario B (Free VC)',
        x=normalized_metrics,
        y=normalized_values_b,
        marker_color='#ff7f0e',
        text=[format_number(v, is_currency='SAR' in m, is_percentage='Margin' in m) 
              for v, m in zip(normalized_values_b, normalized_metrics)],
        textposition='outside',
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Metrics",
        yaxis_title="Value",
        barmode='group',
        height=500,
        showlegend=True,
        margin=dict(t=60, b=80, l=80, r=80),
    )
    
    return fig

def create_profit_comparison_heatmap(df_a, df_b):
    """Create a histogram comparing profit distributions between A and B"""
    try:
        # Get profit ranges
        profit_a_min = df_a['net_profit'].min()
        profit_a_max = df_a['net_profit'].max()
        profit_b_min = df_b['net_profit'].min()
        profit_b_max = df_b['net_profit'].max()
        
        # Create bins that cover both ranges
        min_profit = min(profit_a_min, profit_b_min)
        max_profit = max(profit_a_max, profit_b_max)
        
        # Use a reasonable number of bins
        num_bins = 30
        
        # Create bin edges
        bin_edges = np.linspace(min_profit, max_profit, num_bins + 1)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Calculate histograms
        hist_a, _ = np.histogram(df_a['net_profit'], bins=bin_edges)
        hist_b, _ = np.histogram(df_b['net_profit'], bins=bin_edges)
        
        # Format bin labels for display
        bin_labels = [f"{bc/1e6:.1f}M" if abs(bc) >= 1e6 else f"{bc/1e3:.0f}K" for bc in bin_centers]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Scenario A (Paid VC)',
            x=bin_labels,
            y=hist_a,
            marker_color='#1f77b4',
            opacity=0.7,
            hovertemplate='Profit: %{x}<br>Count: %{y} scenarios<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            name='Scenario B (Free VC)',
            x=bin_labels,
            y=hist_b,
            marker_color='#ff7f0e',
            opacity=0.7,
            hovertemplate='Profit: %{x}<br>Count: %{y} scenarios<extra></extra>'
        ))
        
        fig.update_layout(
            title="Profit Distribution Comparison",
            xaxis_title="Profit Range (SAR)",
            yaxis_title="Number of Scenarios",
            barmode='overlay',
            height=400,
            showlegend=True,
            margin=dict(t=60, b=80, l=80, r=80),
            xaxis=dict(tickangle=-45)
        )
        
        return fig
    except Exception as e:
        # Return a simple error message figure
        fig = go.Figure()
        fig.add_annotation(
            x=0.5, y=0.5,
            text=f"Error creating distribution: {str(e)}",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=400)
        return fig

def create_win_loss_analysis(df_a, df_b, n, premium, vc_cost):
    """Analyze which scenario wins under different conditions"""
    # Sample a subset for comparison
    sample_size = min(1000, len(df_a), len(df_b))
    
    df_a_sample = df_a.sample(n=sample_size) if len(df_a) > sample_size else df_a
    df_b_sample = df_b.sample(n=sample_size) if len(df_b) > sample_size else df_b
    
    # Create matching scenarios based on similar parameters
    comparison_results = []
    
    for idx, row_a in df_a_sample.iterrows():
        # Find closest matching scenario B
        if len(df_b_sample) > 0:
            # Simple matching based on sick percentage
            closest_b = df_b_sample.iloc[(df_b_sample['Sick %'] - row_a['Sick %']).abs().argsort()[:1]]
            
            if len(closest_b) > 0:
                row_b = closest_b.iloc[0]
                comparison_results.append({
                    'Sick %': row_a['Sick %'],
                    'Profit A': row_a['net_profit'],
                    'Profit B': row_b['net_profit'],
                    'Winner': 'A' if row_a['net_profit'] > row_b['net_profit'] else 'B',
                    'Difference': row_a['net_profit'] - row_b['net_profit']
                })
    
    if not comparison_results:
        return None
    
    comp_df = pd.DataFrame(comparison_results)
    
    # Create visualization
    fig = go.Figure()
    
    # Scatter plot
    fig.add_trace(go.Scatter(
        x=comp_df['Profit A'],
        y=comp_df['Profit B'],
        mode='markers',
        marker=dict(
            color=comp_df['Winner'].map({'A': '#1f77b4', 'B': '#ff7f0e'}),
            size=8,
            opacity=0.6
        ),
        text=[f"Sick: {row['Sick %']:.1f}%" for _, row in comp_df.iterrows()],
        hovertemplate='Profit A: SAR %{x:,.0f}<br>Profit B: SAR %{y:,.0f}<br>%{text}<extra></extra>',
        name='Scenarios'
    ))
    
    # Add diagonal line (equal profit)
    max_profit = max(comp_df['Profit A'].max(), comp_df['Profit B'].max())
    min_profit = min(comp_df['Profit A'].min(), comp_df['Profit B'].min())
    
    fig.add_trace(go.Scatter(
        x=[min_profit, max_profit],
        y=[min_profit, max_profit],
        mode='lines',
        line=dict(color='gray', dash='dash'),
        name='Equal Profit Line'
    ))
    
    fig.update_layout(
        title="Scenario A vs Scenario B Profit Comparison",
        xaxis_title="Scenario A Profit (SAR)",
        yaxis_title="Scenario B Profit (SAR)",
        height=500,
        showlegend=True,
    )
    
    return fig, comp_df

def create_parameter_sensitivity_comparison(df_a, df_b):
    """Compare parameter sensitivity between scenarios"""
    # Calculate correlation with profit for each parameter
    params_a = ['Sick %', '% VC Uptake', 'VC Fee']
    params_b = ['Sick %', '% VC Uptake', 'EI Fee']
    
    correlations_a = {}
    correlations_b = {}
    
    for param in params_a:
        if param in df_a.columns:
            corr = df_a[param].corr(df_a['net_profit'])
            correlations_a[param] = corr if not np.isnan(corr) else 0
    
    for param in params_b:
        if param in df_b.columns:
            corr = df_b[param].corr(df_b['net_profit'])
            correlations_b[param] = corr if not np.isnan(corr) else 0
    
    # Create comparison chart
    all_params = list(set(list(correlations_a.keys()) + list(correlations_b.keys())))
    
    fig = go.Figure()
    
    values_a = [correlations_a.get(p, 0) for p in all_params]
    values_b = [correlations_b.get(p, 0) for p in all_params]
    
    fig.add_trace(go.Bar(
        name='Scenario A',
        x=all_params,
        y=values_a,
        marker_color='#1f77b4',
    ))
    
    fig.add_trace(go.Bar(
        name='Scenario B',
        x=all_params,
        y=values_b,
        marker_color='#ff7f0e',
    ))
    
    fig.update_layout(
        title="Parameter Sensitivity Comparison (Correlation with Profit)",
        xaxis_title="Parameter",
        yaxis_title="Correlation Coefficient",
        barmode='group',
        height=400,
        yaxis=dict(range=[-1, 1])
    )
    
    return fig

