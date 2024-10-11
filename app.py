import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Test Schedule Timeline", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #FDF5E6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

start_date = datetime.date.today()

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
    },
    'Ultimate Program': {
        'Every 6 weeks': {
            '6-month plan': {
                'price_per_panel': 99,
                'period_weeks': 6,
                'duration_months': 6,
                'tests_included': 4,
                'test_details': [
                    "Thyroid + Core Health",
                    "Hormones",
                    "Metabolic + Core Health)",
                    "Minerals"
                ]
            },
            '12-month plan': {
                'price_per_panel': 85,
                'period_weeks': 6,
                'duration_months': 12,
                'tests_included': 8,
                'test_details': [
                    "Thyroid + Core Health",
                    "Hormones",
                    "Metabolic + Core Health)",
                    "Minerals",
                    "Thyroid + Core Health",
                    "Hormones",
                    "Metabolic + Core Health)",
                    "Minerals"
                ]
            },
        }
    }
}

st.markdown(
    "<h1 style='text-align: center; color: #FF7F50;'>🩺 Test Schedule Timeline Visualization</h1>",
    unsafe_allow_html=True
)

st.sidebar.header("Select Options")

program_name = st.sidebar.selectbox("Program", list(programs.keys()))
test_frequency = st.sidebar.selectbox("Test Frequency", list(programs[program_name].keys()))
payment_plan = st.sidebar.selectbox("Payment Plan", list(programs[program_name][test_frequency].keys()))

custom_duration = None

if payment_plan.lower() == 'pay as you go':
    custom_duration = st.sidebar.slider(
        "Select Duration (Months)",
        min_value=1,
        max_value=24,
        value=12,
        step=1
    )

def calculate_schedule(program_name, test_frequency, payment_plan, custom_duration=None):
    plan = programs[program_name][test_frequency][payment_plan]
    duration_months = plan.get('duration_months')
    period_months = plan.get('period_months')
    period_weeks = plan.get('period_weeks')
    price_per_panel = plan['price_per_panel']
    tests_included = plan.get('tests_included')
    test_details = plan.get('test_details', [])

    if custom_duration is not None:
        duration_months = custom_duration

    test_dates = []

    if period_months:
        if period_months == 0:
            test_dates = [start_date]
        else:
            num_tests = duration_months // period_months
            for i in range(num_tests):
                test_date = start_date + relativedelta(months=period_months * i)
                if test_date <= start_date + relativedelta(months=duration_months):
                    test_dates.append(test_date)
    elif period_weeks:
        if period_weeks == 0:
            test_dates = [start_date]
        else:
            if tests_included:
                num_tests = tests_included
            else:
                num_tests = int((duration_months * 4.34524) // period_weeks)
            for i in range(1, num_tests + 1):
                test_date = start_date + relativedelta(weeks=period_weeks * i)
                if test_date <= start_date + relativedelta(months=duration_months):
                    test_dates.append(test_date)
    else:
        test_dates = []

    total_months = duration_months
    all_months = [
        (start_date + relativedelta(months=i)).strftime('%b').upper()
        for i in range(total_months + 1)
    ]

    return test_dates, price_per_panel, all_months, duration_months, test_details

def get_month_offset(start_date, test_date):
    delta = test_date - start_date
    return delta.days / 30.4375

def get_year_boundaries(start_date, duration_months):
    boundaries = {}
    current_year = start_date.year
    for month in range(1, duration_months + 1):
        date = start_date + relativedelta(months=month)
        if date.month == 1:
            boundaries[current_year + 1] = month
            current_year += 1
    return boundaries

test_dates, price_per_panel, all_months, duration_months, test_details = calculate_schedule(
    program_name, test_frequency, payment_plan, custom_duration
)

year_boundaries = get_year_boundaries(start_date, duration_months)

fig = go.Figure()

colors = {
    'background': '#FDF5E6',
    'timeline': '#FF7F50',
    'month_markers': '#2E8B57',
    'test_markers': '#FF4500',
    'arrow_color': 'blue',
    'text': '#333333'
}

fig.add_shape(
    type="line",
    x0=-0.5, y0=0, x1=len(all_months)-0.5, y1=0,
    line=dict(color=colors['timeline'], width=10)
)

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

for year, month_index in year_boundaries.items():
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

for idx, date in enumerate(test_dates):
    month_offset = get_month_offset(start_date, date)
    if month_offset >= len(all_months):
        additional_months = int(month_offset - len(all_months) + 1)
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
        fig.add_shape(
            type="line",
            x0=len(all_months)-1, y0=0, x1=len(all_months)-1, y1=0,
            line=dict(color=colors['timeline'], width=10)
        )
        year_boundaries = get_year_boundaries(start_date, duration_months)
        for year, month_index in year_boundaries.items():
            if month_index - 0.5 not in [shape['x0'] for shape in fig.layout.shapes if shape['type'] == 'line']:
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
        if program_name == 'Ultimate Program':
            if idx < len(test_details):
                test_detail = test_details[idx]
            else:
                test_detail = ""
            text = f"🧰 ${price_per_panel}\n {test_detail}"
        else:
            text = f"🧰"

        fig.add_trace(go.Scatter(
            x=[month_offset], y=[1],
            mode='markers+text',
            marker=dict(size=15, color=colors['test_markers'], symbol='triangle-down'),
            text=[text],
            textposition='bottom center',
            textfont=dict(size=12, color=colors['text']),
            hoverinfo='text',
            hovertext=[date.strftime('%B %d, %Y')]
        ))

fig.update_layout(
    title=dict(
        text=f"{program_name} - {test_frequency} - {payment_plan}",
        font=dict(size=24, color=colors['text']),
        x=0.5
    ),
    showlegend=False,
    height=600,
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    xaxis=dict(
        showticklabels=True,
        showgrid=False,
        zeroline=False,
        range=[-0.5, len(all_months)-0.5],
        fixedrange=True
    ),
    yaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        range=[-1, 2],
        fixedrange=True
    ),
    dragmode=False,
    margin=dict(l=20, r=20, t=100, b=20)
)

st.plotly_chart(fig, use_container_width=True)

total_cost = price_per_panel * len(test_dates)

if program_name != "Ultimate Program":
    total_cost = price_per_panel * len(test_dates)
    st.markdown(f"<h3 style='text-align: center; color: {colors['text']};'>💰 Uproft customer pays: ${total_cost:.2f} for {duration_months} months ({len(test_dates)} tests)</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: {colors['text']};'>🧰 Price per panel: {price_per_panel})</h3>", unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FDF5E6;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    plan = programs[program_name][test_frequency][payment_plan]
    duration_months = plan.get('duration_months')
    st.markdown(f"<h3 style='text-align: center; color: {colors['text']};'>💰 Customer pays: ${price_per_panel:.2f} every month for {duration_months} months </h3>", unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FDF5E6;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    

if st.checkbox(":green[Show Test Schedule Data]"):
    df = pd.DataFrame({
        'Test Date': test_dates,
        'Cost': [price_per_panel] * len(test_dates)
    })
    df_display = df.copy()
    df_display['Test Date'] = pd.to_datetime(df_display['Test Date']).dt.strftime('%Y-%m-%d')
    if program_name == 'Ultimate Program':
        df_display['Test Detail'] = test_details[:len(test_dates)]
    else:
        df_display['Test Detail'] = ""
    st.dataframe(df_display.reset_index(drop=True))