
def validate_guard(name, post, rate_text):
    # Checks the guard details and returns a tuple: (name, post, rate)
    name = name.strip()
    post = post.strip()

    if name == "":
        raise ValueError("Name is required.")

    # Commas are not allowed because the text file uses commas to separate data.
    if "," in name or "," in post:
        raise ValueError("Name and post must not contain commas.")

    try:
        rate = float(rate_text)
    except ValueError:
        raise ValueError("Hourly rate must be a number.")

    if rate <= 0:
        raise ValueError("Hourly rate must be greater than 0.")

    return (name, post, rate)


def next_guard_id(guards):
    # The new ID is one more than the biggest ID in the list.
    biggest = 0
    for guard in guards:
        if guard["guard_id"] > biggest:
            biggest = guard["guard_id"]
    return biggest + 1


def find_guard(guards, guard_id):
    # Returns the guard (dictionary) with this ID, or None if there is none.
    for guard in guards:
        if guard["guard_id"] == guard_id:
            return guard
    return None


def time_to_hours(text):
    # Changes a time like "08:30" into hours like 8.5
    if len(text) != 5 or text[2] != ":":
        raise ValueError("Time must be in HH:MM format, like 08:30.")

    try:
        hour = int(text[:2])
        minute = int(text[3:])
    except ValueError:
        raise ValueError("Time must be in HH:MM format, like 08:30.")

    if hour > 23 or minute > 59:
        raise ValueError("Time must be between 00:00 and 23:59.")

    return hour + minute / 60


def check_date(text):
    # Checks that the date looks like YYYY-MM-DD, like 2026-11-03
    if len(text) != 10 or text[4] != "-" or text[7] != "-":
        raise ValueError("Date must be in YYYY-MM-DD format, like 2026-11-03.")

    try:
        year = int(text[:4])
        month = int(text[5:7])
        day = int(text[8:])
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format, like 2026-11-03.")

    if month < 1 or month > 12 or day < 1 or day > 31:
        raise ValueError("Month must be 1-12 and day must be 1-31.")


def calculate_hours(time_in, time_out):
    # Returns the hours worked in one shift.
    start = time_to_hours(time_in)
    end = time_to_hours(time_out)

    if end <= start:
        raise ValueError("Time out must be later than time in.")

    return end - start


def calculate_pay(hours, rate):
    return hours * rate


def validate_shift(guards, guard_id_text, shift_date, time_in, time_out):
    # Checks all the shift inputs and returns a tuple:
    # (guard_id, date, time_in, time_out)
    shift_date = shift_date.strip()
    time_in = time_in.strip()
    time_out = time_out.strip()

    try:
        guard_id = int(guard_id_text)
    except ValueError:
        raise ValueError("Guard ID must be a whole number.")

    if find_guard(guards, guard_id) is None:
        raise ValueError("Guard ID does not exist.")

    check_date(shift_date)
    calculate_hours(time_in, time_out)  # stops with an error if the times are wrong

    return (guard_id, shift_date, time_in, time_out)


def build_report_lines(guards, shifts):
    # Builds the payroll report as a list of text lines.
    lines = []
    lines.append("PAYROLL REPORT")
    lines.append("-" * 70)
    lines.append(f"{'Guard':<20}{'Date':<12}{'In':<7}{'Out':<7}{'Hours':>7}{'Pay':>12}")
    lines.append("-" * 70)

    total_hours = 0
    total_pay = 0

    for guard_id, shift_date, time_in, time_out in shifts:
        guard = find_guard(guards, guard_id)

        if guard is None:
            lines.append(f"Skipped a shift with unknown guard ID {guard_id}")
        else:
            try:
                hours = calculate_hours(time_in, time_out)
                pay = calculate_pay(hours, guard["rate"])
                total_hours = total_hours + hours
                total_pay = total_pay + pay
                lines.append(f"{guard['name']:<20}{shift_date:<12}{time_in:<7}{time_out:<7}{hours:>7.1f}{pay:>12.2f}")
            except ValueError:
                lines.append(f"Skipped an invalid shift for {guard['name']} on {shift_date}")

    lines.append("-" * 70)
    lines.append(f"Total shifts: {len(shifts)}")
    lines.append(f"Total hours: {total_hours:.1f}")
    lines.append(f"Total pay: {total_pay:.2f}")

    return lines
