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
            'Pay as you go': {'price_per_panel': 225, 'period_months': 1, 'duration_months': 12},
            '6-month plan': {'price_per_panel': 115, 'period_months': 1, 'duration_months': 6},
            '12-month plan': {'price_per_panel': 99, 'period_months': 1, 'duration_months': 12},
        },
        'Test Quarterly': {
            'Pay as you go': {'price_per_panel': 225, 'period_months': 3, 'duration_months': 12},
            '6-month plan': {'price_per_panel': 165, 'period_months': 3, 'duration_months': 6},
            '12-month plan': {'price_per_panel': 135, 'period_months': 3, 'duration_months': 12},
        },
        'Every 6 months': {
            'Pay as you go': {'price_per_panel': 225, 'period_months': 6, 'duration_months': 24},
            '12-month plan': {'price_per_panel': 185, 'period_months': 6, 'duration_months': 12},
            '24-month plan': {'price_per_panel': 149, 'period_months': 6, 'duration_months': 24},
        },
        'Just once': {
            'One-time': {'price_per_panel': 295, 'period_months': 0, 'duration_months': 1},
        }
    },
    'Heart & Metabolic Program': {
        'Test Quarterly': {
            'Pay as you go': {'price_per_panel': 297, 'period_months': 3, 'duration_months': 12},
            '6-month plan': {'price_per_panel': 225, 'period_months': 3, 'duration_months': 6},
            '12-month plan': {'price_per_panel': 195, 'period_months': 3, 'duration_months': 12},
        },
        'Every 6 months': {
            'Pay as you go': {'price_per_panel': 297, 'period_months': 6, 'duration_months': 24},
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

def calculate_schedule(program_name, test_frequency, payment_plan):
    plan = programs[program_name][test_frequency][payment_plan]
    duration_months = plan['duration_months']
    period_months = plan['period_months']
    price_per_panel = plan['price_per_panel']
    
    if period_months == 0:
        # Just once
        test_dates = [start_date]
    else:
        # Calculate number of tests, ensuring the last test is at duration_months
        num_tests = duration_months // period_months
        # If duration_months is exactly divisible by period_months, include the last test
        if duration_months % period_months == 0:
            num_tests += 1
        test_dates = [start_date + relativedelta(months=period_months * i) for i in range(num_tests)]
    
    # Generate all month labels up to the maximum duration
    total_months = duration_months
    all_months = [(start_date + relativedelta(months=i)).strftime('%b').upper() for i in range(total_months +1)]
    
    return test_dates, price_per_panel, all_months

# Calculate the test schedule
test_dates, price_per_panel, all_months = calculate_schedule(program_name, test_frequency, payment_plan)

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
        icon = '🧰' if i % 2 == 0 else '🧰'  # Alternating medical icons
        fig.add_annotation(
            x=month_offset, y=1.5,
            text=icon,
            showarrow=False,
            font=dict(size=24)
        )

# Update layout for better visuals
fig.update_layout(
    title=dict(
        text=f"Test Schedule Timeline - {program_name}",
        font=dict(size=24, color=colors['text']),
        x=0.5
    ),
    showlegend=False,
    height=500,
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
    margin=dict(l=20, r=20, t=100, b=20)
)

# Display the figure
st.plotly_chart(fig, use_container_width=True)

# Calculate and display total cost
total_cost = price_per_panel * len(test_dates)
duration_months = programs[program_name][test_frequency][payment_plan]['duration_months']
st.markdown(f"<h3 style='text-align: center; color: {colors['text']};'>💰 Total Cost: ${total_cost:.2f} over {duration_months} months ({len(test_dates)} tests)</h3>", unsafe_allow_html=True)

# Optionally, display the data table
if st.checkbox("Show Test Schedule Data"):
    df = pd.DataFrame({
        'Test Date': test_dates,
        'Cost': [price_per_panel] * len(test_dates)
    })
    df_display = df.copy()
    df_display['Test Date'] = df_display['Test Date'].strftime('%Y-%m-%d')
    st.dataframe(df_display.reset_index(drop=True))