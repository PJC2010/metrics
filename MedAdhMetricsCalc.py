from datetime import datetime, timedelta

# Medication fill data provided
medication_fills = [
    {'fill_date': datetime.strptime("01/20/2023", "%m/%d/%Y"), 'day_supply': 90},
    {'fill_date': datetime.strptime("04/20/2023", "%m/%d/%Y"), 'day_supply': 90},
    {'fill_date': datetime.strptime("05/31/2023", "%m/%d/%Y"), 'day_supply': 90},
    {'fill_date': datetime.strptime("07/17/2023", "%m/%d/%Y"), 'day_supply': 90},
    {'fill_date': datetime.strptime("08/24/2023", "%m/%d/%Y"), 'day_supply': 90},
    {'fill_date': datetime.strptime("10/18/2023", "%m/%d/%Y"), 'day_supply': 90},
]

# Calculate metrics as of this date
as_of_date = datetime.strptime("12/31/2023", "%m/%d/%Y")

# Initialize covered days set for cumulative metrics
covered_days = set()

# Calculate covered days for each fill
for fill in medication_fills:
    start_date = fill['fill_date']
    for day in range(fill['day_supply']):
        covered_days.add(start_date + timedelta(days=day))

# Get the last fill date
last_fill_date = medication_fills[-1]['fill_date']

# Calculate the measurement period
measurement_period_start = medication_fills[0]['fill_date']
measurement_period = (as_of_date - measurement_period_start).days + 1

# Calculate IMMEDIATENEXTFILLDATE and CUMULATIVENEXTFILLDATE
immediate_next_fill_date = last_fill_date + timedelta(days=90)
cumulative_next_fill_date = max(covered_days) + timedelta(days=1)

# IMMEDIATEDAYSMISSEDNBR and CUMULATIVEDAYSMISSEDNBR
immediate_days_missed_nbr = (as_of_date - immediate_next_fill_date).days if as_of_date > immediate_next_fill_date else 0
cumulative_days_missed_nbr = (as_of_date - cumulative_next_fill_date).days if as_of_date > cumulative_next_fill_date else 0

# IMMEDIATEDAYSPASTDUENBR and CUMULATIVEDAYSPASTDUENBR
immediate_days_past_due_nbr = immediate_days_missed_nbr
cumulative_days_past_due_nbr = cumulative_days_missed_nbr

# Calculate PDC (Proportion of Days Covered)
immediate_pdc_nbr = len(covered_days) / measurement_period
cumulative_pdc_nbr = immediate_pdc_nbr

# Calculate Adherence Days Needed (ADR)
immediate_adr_nbr = max(0, int(measurement_period * 0.8) - len(covered_days))
cumulative_adr_nbr = immediate_adr_nbr

# Calculate LASTIMPACTABLEDATE
immediate_last_impactable_date = last_fill_date + timedelta(days=90 + immediate_adr_nbr)
cumulative_last_impactable_date = immediate_last_impactable_date

# Print the metrics
print(f"LASTFILLEDDATEMEDICATION: {last_fill_date.strftime('%m/%d/%Y')}")
print(f"IMMEDIATENEXTFILLDATE: {immediate_next_fill_date.strftime('%m/%d/%Y')}")
print(f"CUMULATIVENEXTFILLDATE: {cumulative_next_fill_date.strftime('%m/%d/%Y')}")
print(f"IMMEDIATEDAYSMISSEDNBR: {immediate_days_missed_nbr}")
print(f"CUMULATIVEDAYSMISSEDNBR: {cumulative_days_missed_nbr}")
print(f"IMMEDIATEDAYSPASTDUENBR: {immediate_days_past_due_nbr}")
print(f"CUMULATIVEDAYSPASTDUENBR: {cumulative_days_past_due_nbr}")
print(f"IMMEDIATEDAYSTOADHERENTNBR: {immediate_adr_nbr}")
print(f"CUMULATIVEDAYSTOADHERENTNBR: {cumulative_adr_nbr}")
print(f"IMMEDIATEPDCNBR: {immediate_pdc_nbr:.2f}")
print(f"CUMULATIVEPDCNBR: {cumulative_pdc_nbr:.2f}")
print(f"IMMEDIATEADRNBR: {immediate_adr_nbr}")
print(f"CUMULATIVEADRNBR: {cumulative_adr_nbr}")
print(f"IMMEDIATELASTIMPACTABLEDATE: {immediate_last_impactable_date.strftime('%m/%d/%Y')}")
print(f"CUMULATIVELASTIMPACTABLEDATE: {cumulative_last_impactable_date.strftime('%m/%d/%Y')}")
