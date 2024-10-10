import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta  # For accurate month increments

# Set up the page configuration
st.set_page_config(page_title="Test Schedule Timeline", layout="wide")

# Define the start date
start_date = datetime.date(2024, 10, 10)

# Updated programs and pricing structure
programs = {
    'CORE HEALTH': {
        'Test Monthly': {
            'Pay as you go': {'price_per_panel': 225, 'period_months': 1},
            '6-month plan': {'price_per_panel': 115, 'period_months': 1, 'duration_months': 6},
            '12-month plan': {'price_per_panel': 99, 'period_months': 1, 'duration_months': 12},
        },
        'Test Quarterly': {
            'Pay as you go': {'price_per_panel': 225, 'period_months': 3},
            '6-month plan': {'price_per_panel': 165, 'period_months': 3, 'duration_months': 6},
            '12-month plan': {'price_per_panel': 135, 'period_months': 3, 'duration_months': 12},
        },
        'Every 6 months': {
            'Pay as you go': {'price_per_panel': 225, 'period_months': 6},
            '12-month plan': {'price_per_panel': 185, 'period_months': 6, 'duration_months': 12},
            '24-month plan': {'price_per_panel': 149, 'period_months': 6, 'duration_months': 24},
        },
        'Just once': {
            'One-time': {'price_per_panel': 295, 'period_months': 0, 'duration_months': 1},
        }
    },
    'Heart & Metabolic Program': {
        'Test Quarterly': {
            'Pay as you go': {'price_per_panel': 297, 'period_months': 3},
            '6-month plan': {'price_per_panel': 225, 'period_months': 3, 'duration_months': 6},
            '12-month plan': {'price_per_panel': 195, 'period_months': 3, 'duration_months': 12},
        },
        'Every 6 months': {
            'Pay as you go': {'price_per_panel': 297, 'period_months': 6},
            '12-month plan': {'price_per_panel': 245, 'period_months': 6, 'duration_months': 12},
            '24-month plan': {'price_per_panel': 220, 'period_months': 6, 'duration_months': 24},
        },
        'Just once': {
            'One-time': {'price_per_panel': 345, 'period_months': 0, 'duration_months': 1},
        }
    }
}

st.title("🩺 Test Schedule Timeline Visualization")

# Sidebar selections
st.sidebar.header("Select Options")

program_name = st.sidebar.selectbox("Program", list(programs.keys()))
test_frequency = st.sidebar.selectbox("Test Frequency", list(programs[program_name].keys()))
payment_plan = st.sidebar.selectbox("Payment Plan", list(programs[program_name][test_frequency].keys()))

# Initialize variable for custom duration
custom_duration = None

# Check if the selected payment plan is 'Pay as you go'
if payment_plan.lower() == 'pay as you go':
    custom_duration = st.sidebar.slider(
        "Select Duration (Months)",
        min_value=1,
        max_value=24,
        value=12,  # default value
        step=1
    )

def calculate_schedule(program_name, test_frequency, payment_plan, custom_duration=None):
    plan = programs[program_name][test_frequency][payment_plan]
    duration_months = plan.get('duration_months')  # Use get to handle missing keys
    period_months = plan['period_months']
    price_per_panel = plan['price_per_panel']
    
    # Override duration_months if custom_duration is provided
    if custom_duration is not None:
        duration_months = custom_duration
    
    if period_months == 0:
        # Just once
        test_dates = [start_date]
    else:
        # Calculate number of tests without adding an extra one
        num_tests = duration_months // period_months
        test_dates = [
            start_date + relativedelta(months=period_months * i) 
            for i in range(num_tests)
            if (start_date + relativedelta(months=period_months * i)) <= start_date + relativedelta(months=duration_months)
        ]
    
    # Generate all month labels up to the maximum duration
    total_months = duration_months
    all_months = [
        (start_date + relativedelta(months=i)).strftime('%b').upper() 
        for i in range(total_months + 1)
    ]
    
    return test_dates, price_per_panel, all_months, duration_months

def get_year_boundaries(start_date, duration_months):
    """
    Returns a dictionary with year numbers as keys and their corresponding month indices on the timeline.
    """
    boundaries = {}
    current_year = start_date.year
    for month in range(1, duration_months + 1):
        date = start_date + relativedelta(months=month)
        if date.month == 1:
            boundaries[current_year + 1] = month
            current_year += 1
    return boundaries

# Calculate the test schedule
test_dates, price_per_panel, all_months, duration_months = calculate_schedule(
    program_name, test_frequency, payment_plan, custom_duration
)

# Calculate year boundaries
year_boundaries = get_year_boundaries(start_date, duration_months)

# Create a new timeline figure using Plotly
fig = go.Figure()

# Color palette
colors = {
    'background': '#FDF5E6',      # Old Lace (light beige)
    'timeline': '#FF7F50',        # Coral (orange)
    'month_markers': '#2E8B57',   # Sea Green
    'test_markers': '#FF4500',    # Orange Red
    'arrow_color': 'blue',        # Arrow color
    'text': '#333333'              # Dark Gray
}

# Add the main timeline
fig.add_shape(
    type="line",
    x0=-0.5, y0=0, x1=len(all_months)-0.5, y1=0,
    line=dict(color=colors['timeline'], width=10)
)

# Add month markers and labels
for i, month in enumerate(all_months):
    fig.add_trace(go.Scatter(
        x=[i], y=[0],
        mode='markers+text',
        marker=dict(size=20, color=colors['month_markers'], symbol='circle'),
        text=month,
        textposition='bottom center',
        textfont=dict(size=14, color=colors['text']),
        hoverinfo='none'
    ))

# Add year boundary lines and labels
for year, month_index in year_boundaries.items():
    # Add a vertical dashed line to indicate the start of a new year
    fig.add_shape(
        type="line",
        x0=month_index - 0.5, y0=-0.5, x1=month_index - 0.5, y1=1.5,
        line=dict(color='gray', width=2, dash='dash')
    )
    
    # Add a label for the year
    fig.add_annotation(
        x=month_index - 0.5, y=1.6,
        text=str(year),
        showarrow=False,
        font=dict(size=12, color='gray'),
        xanchor='center',
        yanchor='bottom'
    )

# Add test markers and annotations
for i, date in enumerate(test_dates):
    # Calculate the month index relative to the start date
    month_offset = (date.year - start_date.year) * 12 + (date.month - start_date.month)
    
    # Ensure month_offset is within the range
    if month_offset >= len(all_months):
        # Extend all_months and add additional month markers if necessary
        additional_months = month_offset - len(all_months) + 1
        for j in range(additional_months):
            new_month = (start_date + relativedelta(months=len(all_months)+j)).strftime('%b').upper()
            all_months.append(new_month)
            fig.add_trace(go.Scatter(
                x=[len(all_months)-1 + j], y=[0],
                mode='markers+text',
                marker=dict(size=20, color=colors['month_markers'], symbol='circle'),
                text=new_month,
                textposition='bottom center',
                textfont=dict(size=14, color=colors['text']),
                hoverinfo='none'
            ))
        # Update timeline line
        fig.add_shape(
            type="line",
            x0=len(all_months)-1, y0=0, x1=len(all_months)-1, y1=0,
            line=dict(color=colors['timeline'], width=10)
        )
        # Recalculate year boundaries if new months extend into a new year
        year_boundaries = get_year_boundaries(start_date, duration_months)
        for year, month_index in year_boundaries.items():
            if month_index - 0.5 not in [shape['x0'] for shape in fig.layout.shapes if shape['type'] == 'line']:
                # Add the new year boundary lines and labels
                fig.add_shape(
                    type="line",
                    x0=month_index - 0.5, y0=-0.5, x1=month_index - 0.5, y1=1.5,
                    line=dict(color='gray', width=2, dash='dash')
                )
                fig.add_annotation(
                    x=month_index - 0.5, y=1.6,
                    text=str(year),
                    showarrow=False,
                    font=dict(size=12, color='gray'),
                    xanchor='center',
                    yanchor='bottom'
                )
    
    if month_offset < len(all_months):
        fig.add_trace(go.Scatter(
            x=[month_offset], y=[1],
            mode='markers+text',
            marker=dict(size=15, color=colors['test_markers'], symbol='triangle-down'),
            text=[f"${price_per_panel}"],
            textposition='top center',
            textfont=dict(size=12, color=colors['text']),
            hoverinfo='text',
            hovertext=[date.strftime('%B %d, %Y')]
        ))
        
        # Add custom icons
        icon = '🧰'   # Alternating medical icons
        fig.add_annotation(
            x=month_offset, y=1.5,
            text=icon,
            showarrow=False,
            font=dict(size=24)
        )

# Update layout for better visuals
fig.update_layout(
    title=dict(
        text=f"{program_name} - {test_frequency} - {payment_plan} ",
        font=dict(size=24, color=colors['text']),
        x= 0.3
    ),
    showlegend=False,
    height=600,  # Increased height to accommodate year labels
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    xaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        range=[-0.5, len(all_months)-0.5]
    ),
    yaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        range=[-1, 2]
    ),
    dragmode = False,
    margin=dict(l=20, r=20, t=100, b=20)
)

# Display the figure
st.plotly_chart(fig, use_container_width=True)

# Calculate and display total cost
total_cost = price_per_panel * len(test_dates)
st.markdown(f"<h3 style='text-align: center; color: {colors['text']};'>💰 Total Cost: ${total_cost:.2f} over {duration_months} months ({len(test_dates)} tests)</h3>", unsafe_allow_html=True)

# Optionally, display the data table
if st.checkbox("Show Test Schedule Data"):
    df = pd.DataFrame({
        'Test Date': test_dates,
        'Cost': [price_per_panel] * len(test_dates)
    })
    df_display = df.copy()
    
    # Convert 'Test Date' to datetime if it's not already
    df_display['Test Date'] = pd.to_datetime(df_display['Test Date'])
    
    # Format 'Test Date' as 'YYYY-MM-DD'
    df_display['Test Date'] = df_display['Test Date'].dt.strftime('%Y-%m-%d')
    
    st.dataframe(df_display.reset_index(drop=True))
