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
    },
    'Ultimate Program': {
        'Every 6 weeks': {
            '6-month plan': {
                'price_per_panel': 99,
                'period_weeks': 6,  # 6 weeks interval
                'duration_months': 6,
                'tests_included': 4
            },
            '12-month plan': {
                'price_per_panel': 85,
                'period_weeks': 6,  # 6 weeks interval
                'duration_months': 12,
                'tests_included': 8
            },
        }
    }
}

panels_ultimate = {
    1  : "Thyroid+ (including Core Health)",
    2  :  "Hormones",
    3  :  "Metabolic (including Core Health)",
    4  : "Mineral Panel"
}

program_name = "Ultimate Program"
test_frequency = "Every 6 weeks"
payment_plan = "6-month plan"
plan = programs[program_name][test_frequency][payment_plan]

print(plan.get("duration_months"))