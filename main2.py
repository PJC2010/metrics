from datetime import datetime, timedelta


# Helper function to calculate Proportion of Days Covered (PDC)
def calculate_pdc(covered_days, measurement_period_start, measurement_period_end):
    total_days_in_period = (measurement_period_end - measurement_period_start).days + 1
    covered_days_in_period = sum(1 for day in covered_days if measurement_period_start <= day <= measurement_period_end)
    return covered_days_in_period / total_days_in_period if total_days_in_period else 0


def calculate_adherence_metrics(medication_fills, measurement_end_date):
    medication_fills = sorted(medication_fills, key=lambda x: x['fill_date'])
    covered_days = set()
    immediate_covered_days = set()
    first_fill_date = medication_fills[0]['fill_date']

    for fill in medication_fills:
        fill_date = fill['fill_date']
        day_supply = fill['day_supply']
        next_fill_date = fill_date + timedelta(days=day_supply)

        for i in range(day_supply):
            covered_days.add(fill_date + timedelta(days=i))
            if fill == medication_fills[-1]:  # For immediate metrics, only consider the last fill
                immediate_covered_days.add(fill_date + timedelta(days=i))

    # Calculate cumulative metrics
    cumulative_next_fill_date = max(covered_days) + timedelta(days=1) if covered_days else None
    cumulative_pdc = calculate_pdc(covered_days, first_fill_date, measurement_end_date)

    # Calculate immediate metrics
    immediate_next_fill_date = max(immediate_covered_days) + timedelta(days=1) if immediate_covered_days else None
    immediate_pdc = calculate_pdc(immediate_covered_days, first_fill_date, measurement_end_date)

    # Today's date to check if medication is past due
    today = datetime.now()

    metrics = {
        "LASTFILLEDDATEMEDICATION": medication_fills[-1]['fill_date'].strftime("%m-%d-%Y"),
        "IMMEDIATENEXTFILLDATE": immediate_next_fill_date.strftime("%m-%d-%Y") if immediate_next_fill_date else 'N/A',
        "CUMULATIVENEXTFILLDATE": cumulative_next_fill_date.strftime(
            "%m-%d-%Y") if cumulative_next_fill_date else 'N/A',
        "IMMEDIATEDAYSMISSEDNBR": (
                    medication_fills[-1] - immediate_next_fill_date).days if immediate_next_fill_date and today > immediate_next_fill_date else 0,
        "CUMULATIVEDAYSMISSEDNBR": (
                    today - cumulative_next_fill_date).days if cumulative_next_fill_date and today > cumulative_next_fill_date else 0,
        "IMMEDIATEPDCNBR": immediate_pdc,
        "CUMULATIVEPDCNBR": cumulative_pdc,
        # ... Other metrics calculations
    }

    return metrics


# Example usage
medication_fills = [
    {'fill_date': datetime.strptime("01-20-2023", "%m-%d-%Y"), 'day_supply': 90},
    {'fill_date': datetime.strptime("04-20-2023", "%m-%d-%Y"), 'day_supply': 90},
    {'fill_date': datetime.strptime("05-31-2023", "%m-%d-%Y"), 'day_supply': 90},
    {'fill_date': datetime.strptime("07-17-2023", "%m-%d-%Y"), 'day_supply': 90},
    {'fill_date': datetime.strptime("08-24-2023", "%m-%d-%Y"), 'day_supply': 90},
    {'fill_date': datetime.strptime("10-18-2023", "%m-%d-%Y"), 'day_supply': 90},
    # ... add more fills if necessary
]

measurement_end_date = datetime.strptime("12-31-2023", "%m-%d-%Y")

adherence_metrics = calculate_adherence_metrics(medication_fills, measurement_end_date)

# Print the metrics
for metric, value in adherence_metrics.items():
    print(f"{metric}: {value if value is not None else 'N/A'}")
