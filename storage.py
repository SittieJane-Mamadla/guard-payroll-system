# storage.py
# This module does all the reading and writing of files.
# Later, when we learn databases, we can replace this module
# with a database module that has the same function names.

GUARDS_FILE = "guards.txt"
SHIFTS_FILE = "shifts.txt"
REPORT_FILE = "payroll_report.txt"


def load_guards():
    # Reads guards.txt and returns a list of dictionaries.
    # Each line in the file looks like: 1,Juan Dela Cruz,Main Gate,100.0
    guards = []

    try:
        with open(GUARDS_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(",")

                if len(parts) != 4:
                    print("Skipped bad line in guards file:", line.strip())
                else:
                    try:
                        guard = {
                            "guard_id": int(parts[0]),
                            "name": parts[1],
                            "post": parts[2],
                            "rate": float(parts[3]),
                        }
                        guards.append(guard)
                    except ValueError:
                        print("Skipped bad line in guards file:", line.strip())
    except FileNotFoundError:
        # No file yet, so there are no guards. Return the empty list.
        pass

    return guards


def load_shifts():
    # Reads shifts.txt and returns a list of tuples.
    # Each line looks like: 1,2026-11-03,08:00,16:00
    shifts = []

    try:
        with open(SHIFTS_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(",")

                if len(parts) != 4:
                    print("Skipped bad line in shifts file:", line.strip())
                else:
                    try:
                        shift = (int(parts[0]), parts[1], parts[2], parts[3])
                        shifts.append(shift)
                    except ValueError:
                        print("Skipped bad line in shifts file:", line.strip())
    except FileNotFoundError:
        pass

    return shifts


def save_guard(guard):
    # Adds one guard (a dictionary) to the end of guards.txt
    # Mode "a" means append: old data is kept.
    line = f"{guard['guard_id']},{guard['name']},{guard['post']},{guard['rate']}\n"
    with open(GUARDS_FILE, "a") as file:
        file.write(line)


def save_shift(shift):
    # Adds one shift (a tuple) to the end of shifts.txt
    line = f"{shift[0]},{shift[1]},{shift[2]},{shift[3]}\n"
    with open(SHIFTS_FILE, "a") as file:
        file.write(line)


def add_sample_data():
    # Adds starter data only if there are no guards and no shifts yet.
    if len(load_guards()) > 0 or len(load_shifts()) > 0:
        return

    sample_guards = [
        {"guard_id": 1, "name": "Juan Dela Cruz", "post": "Main Gate", "rate": 100.0},
        {"guard_id": 2, "name": "Maria Santos", "post": "Lobby", "rate": 110.0},
        {"guard_id": 3, "name": "Pedro Reyes", "post": "Parking Area", "rate": 95.0},
        {"guard_id": 4, "name": "Ana Lopez", "post": "Back Gate", "rate": 105.0},
    ]
    for guard in sample_guards:
        save_guard(guard)

    sample_shifts = [
        (1, "2026-11-03", "08:00", "16:00"),
        (1, "2026-11-04", "08:00", "18:00"),
        (2, "2026-11-03", "08:00", "12:00"),
        (3, "2026-11-05", "06:00", "18:00"),
    ]
    for shift in sample_shifts:
        save_shift(shift)


def write_report(lines):
    # Writes a list of text lines to the report file.
    # Mode "w" means write: the old report is replaced.
    with open(REPORT_FILE, "w") as file:
        for line in lines:
            file.write(line + "\n")