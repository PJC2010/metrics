from datetime import datetime, timedelta


# Function to parse date
def parse_date(date_str):
    return datetime.strptime(date_str, "%m-%d-%Y")


# Function to calculate the measurement period
def get_measurement_period(last_fill_date):
    end_date = datetime(2023, 12, 31)
    return (end_date - last_fill_date).days


# Function to calculate PDC
def get_pdc(covered_days, measurement_period):
    return len(covered_days) / measurement_period if measurement_period > 0 else 0


# Function to calculate adherence
def get_adherence(pdc, measurement_period, pdc_threshold=0.8):
    days_needed = measurement_period * pdc_threshold
    days_covered = pdc * measurement_period
    if days_covered >= days_needed:
        return 0  # Already above threshold
    else:
        return days_needed - days_covered


# Function to calculate cumulative metrics
def calculate_cumulative_metrics(prescriptions):
    covered_days = set()
    last_fill_date = None

    for prescription in sorted(prescriptions, key=lambda x: x['fill_date']):
        start_date = prescription['fill_date']
        end_date = start_date + timedelta(days=prescription['day_supply'])
        last_fill_date = max(last_fill_date, end_date) if last_fill_date else end_date

        # Add each day of coverage to the set
        for single_date in (start_date + timedelta(n) for n in range(prescription['day_supply'])):
            covered_days.add(single_date)

    measurement_period = get_measurement_period(last_fill_date)
    pdc = get_pdc(covered_days, measurement_period)
    adr = get_adherence(pdc, measurement_period)

    return pdc, adr, last_fill_date, covered_days, measurement_period


# Main function to process input and display output
def main():
    prescriptions = []
    while True:
        # Collect user input for fill dates and day supplies
        last_fill_date_str = input("Enter the last filled date (MM-DD-YYYY) or 'done' to finish: ")
        if last_fill_date_str.lower() == 'done':
            break
        day_supply = int(input("Enter the day supply number: "))

        # Add the prescription to the list
        prescriptions.append({
            'fill_date': parse_date(last_fill_date_str),
            'day_supply': day_supply
        })

    # Calculate cumulative metrics
    cumulative_pdc, cumulative_adr, last_fill_date, covered_days, measurement_period = calculate_cumulative_metrics(
        prescriptions)

    # Calculate immediate metrics based on the last fill
    immediate_pdc = cumulative_pdc
    immediate_adr = cumulative_adr
    immediate_last_fill_date = last_fill_date

    # Display results
    print(f"\nMetrics for the medication:")
    print(f"Measurement Period: {measurement_period} days")
    print(f"Last Fill Date: {immediate_last_fill_date.strftime('%m-%d-%Y')}")
    print(f"Next Expected Fill Date: {(immediate_last_fill_date + timedelta(days=1)).strftime('%m-%d-%Y')}")
    print(f"Immediate PDC: {immediate_pdc:.2%}")
    print(f"Immediate ADR: {int(immediate_adr)} days")
    print(f"Cumulative PDC: {cumulative_pdc:.2%}")
    print(f"Cumulative ADR: {int(cumulative_adr)} days")


if __name__ == "__main__":
    main()

