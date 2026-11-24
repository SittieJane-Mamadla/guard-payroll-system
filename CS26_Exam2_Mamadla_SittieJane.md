# CS 26 Exam 2 – Technical Documentation

**Student:** Sittie Jane Mamadla

**Program:** Security Guard Attendance and Salary System (Guard Management and Payroll)

**Status of project:** Work in progress. This report documents what is implemented now and what is planned.
---

## A. Program Title and Overview

**Program name:** Security Guard Attendance and Salary System (console menu program)

**Intended users:** A security agency administrator or payroll clerk who needs to keep a list of guards, record each guard's shifts, and produce a payroll report.

**Main purpose:** The program stores guard details (name, post, hourly rate), records shifts (date, time in, time out), checks that the input is valid, calculates the hours worked and the pay for each shift, and exports a payroll report as a text file.

The current version runs in the terminal (`python main.py`) and saves data in plain text files. The final version is planned to use a database and a Tkinter graphical interface (see Section D).

---

## B. Problem Description

Security agencies track guard attendance and salary by hand or in notebooks. This causes mistakes: wrong hour counts, missing shifts, and slow payroll computation. The program is needed to record the data once, validate it, and compute the pay automatically and consistently.

### Inputs

- Guard details: name, post, hourly rate
- Shift details: guard ID, date (`YYYY-MM-DD`), time in (`HH:MM`), time out (`HH:MM`)
- Menu choices typed by the user

### Processing

- Validate all input (empty values, commas, wrong formats, impossible times, unknown guard ID)
- Generate the next guard ID
- Convert times to decimal hours and compute hours worked: `time out - time in`
- Compute pay: `hours × hourly rate`
- Add up total shifts, total hours, and total pay

### Outputs

- Tables of guards and shifts shown on screen
- Messages such as `Guard saved.` or `Error: ...`
- A payroll report file, `payroll_report.txt`

---

## C. Program Objectives

The project has five objectives. The status column shows how far each one has progressed.

| # | Objective | Status |
|---|---|---|
| 1 | Store guard details (name, post, hourly rate) in a database. | **Partly done.** |
| 2 | Record and validate each guard's shift date, time in, and time out. | **Done**  |
| 3 | Calculate hours worked, separating regular and overtime hours. | **Partly done.** |
| 4 | Compute each guard's gross pay, deductions, and net pay. | **Partly done.** |
| 5 | Display payslips and a payroll summary in a graphical interface. | **Planned.** |

---

## D. Program Requirements and Features

### Implemented features

- Menu-driven program with a loop (`while True`)
- Add a guard with validation, and automatic ID numbering
- View all guards in an aligned table
- Add a shift with validation (guard exists, date format, time format, time out later than time in)
- View all shifts
- Export a payroll report with per-shift hours and pay, and totals
- Sample data is added automatically on the first run
- Data persists between runs (stored in text files)

### Planned enhancements

- Replace text files with a database (guards and shifts tables)
- Regular and overtime hours (for example, first 8 hours regular)
- Deductions stored in a dictionary, and net pay
- Tkinter interface with a payslip view and payroll summary table

### Assumptions and limitations

- A shift cannot cross midnight (time out must be later than time in).
- Names and posts cannot contain commas, because commas separate the fields in the text files.
- The date check only tests the format and that the month is 1–12 and the day is 1–31. It does not check the number of days in each month (see Section J, Debugging).
- There is no edit or delete function yet.

---

## E. Program Structure and Modules

```
project_folder/
├── Main.py            (menu and user interaction)
├── payroll.py         (validation and calculations)
├── storage.py         (reading and writing files)
├── guards.txt         (created automatically: guard records)
├── shifts.txt         (created automatically: shift records)
└── payroll_report.txt (created when the report is exported)
```

| File | Purpose |
|---|---|
| `Main.py` | Shows the menu, asks the user for input, and calls the other modules. |
| `payroll.py` | Checks input and does calculations. It never reads or writes files. |
| `storage.py` | Does all file reading and writing. |

**How the modules work together:** `Main.py` starts with `import storage` and `import payroll`, then calls functions such as `payroll.validate_guard()` and `storage.save_guard()`. `Main.py` is the only file that talks to the user, `payroll.py` decides what is valid and computes results, and `storage.py` is the only file that touches the disk. Because of this separation, `storage.py` can later be replaced by a database module with the same function names without changing the other two files.

```python
import storage
import payroll
```

---

## F. Data Structures

### List
A list holds all the guards loaded from the file. It is the right choice because the number of guards grows and the program needs to loop through them in order.

```python
guards = []                 # in storage.load_guards()
...
guards.append(guard)
```

The report is also built as a list of text lines (`lines = []` in `build_report_lines`), which is later written to the file line by line.

### Tuple
A shift is stored as a tuple: `(guard_id, date, time_in, time_out)`. A tuple fits because a recorded shift has a fixed set of four values that should not be changed accidentally. Functions also return tuples, such as `validate_guard`, which returns `(name, post, rate)`.

```python
sample_shifts = [
    (1, "2026-11-03", "08:00", "16:00"),
]
```

### Dictionary
Each guard is a dictionary because the details have names (keys), which are easier to read than positions.

```python
guard = {
    "guard_id": 1,
    "name": "Juan Dela Cruz",
    "post": "Main Gate",
    "rate": 100.0,
}
```

---

## G. Functions

### `payroll.py`

| Function | Parameters | Returns | Purpose |
|---|---|---|---|
| `validate_guard` | `name, post, rate_text` | tuple `(name, post, rate)` | Cleans and validates guard input; raises `ValueError` if invalid. |
| `next_guard_id` | `guards` | int | Returns the biggest existing ID plus one. |
| `find_guard` | `guards, guard_id` | dictionary or `None` | Finds a guard by ID. |
| `time_to_hours` | `text` | float | Converts `"08:30"` to `8.5`; validates the format. |
| `check_date` | `text` | nothing | Raises `ValueError` if the date format is wrong. |
| `calculate_hours` | `time_in, time_out` | float | Hours worked in one shift; error if out is not later than in. |
| `calculate_pay` | `hours, rate` | float | `hours * rate`. |
| `validate_shift` | `guards, guard_id_text, shift_date, time_in, time_out` | tuple `(guard_id, date, time_in, time_out)` | Validates all shift input. |
| `build_report_lines` | `guards, shifts` | list of strings | Builds the payroll report text and totals. |

### `storage.py`

| Function | Parameters | Returns | Purpose |
|---|---|---|---|
| `load_guards` | none | list of dictionaries | Reads `guards.txt`. |
| `load_shifts` | none | list of tuples | Reads `shifts.txt`. |
| `save_guard` | `guard` | nothing | Appends one guard to `guards.txt`. |
| `save_shift` | `shift` | nothing | Appends one shift to `shifts.txt`. |
| `add_sample_data` | none | nothing | Adds starter data if both files are empty or missing. |
| `write_report` | `lines` | nothing | Writes the report to `payroll_report.txt`. |

### Code excerpt 1: converting time to hours

```python
def time_to_hours(text):
    if len(text) != 5 or text[2] != ":":
        raise ValueError("Time must be in HH:MM format, like 08:30.")
    hour = int(text[:2])
    minute = int(text[3:])
    if hour > 23 or minute > 59:
        raise ValueError("Time must be between 00:00 and 23:59.")
    return hour + minute / 60
```

The function first checks the shape of the text (5 characters with a colon in the middle). It then slices the hour (`text[:2]`) and minute (`text[3:]`), rejects impossible values, and returns decimal hours so that `08:30` becomes `8.5`. This makes subtraction and multiplication by the rate simple.

### Code excerpt 2: generating the next guard ID

```python
def next_guard_id(guards):
    biggest = 0
    for guard in guards:
        if guard["guard_id"] > biggest:
            biggest = guard["guard_id"]
    return biggest + 1
```

The loop keeps the largest ID seen so far. The new guard gets that value plus one, so IDs stay unique. With an empty list, the first ID is 1.

### Code excerpt 3: formatting the output with f-strings

The tables on screen and in the report are aligned using f-string format specifiers (in `view_guards_menu()` in `Main.py`):

```python
print(f"{g['guard_id']:<6}{g['name']:<20}{g['post']:<15}{g['rate']:>8.2f}")
```

Inside each `{ }`, the part after the colon controls how the value is shown:

| Specifier | Meaning | Example in the program |
|---|---|---|
| `:<6` | left-align in a space 6 characters wide | guard ID, name, post |
| `:>8` | right-align in a space 8 characters wide | rate column |
| `.2f` | show a decimal number with 2 digits after the point | `100.0` is shown as `100.00` |

Because every row uses the same widths, the columns line up. The report uses the same idea (`:>7.1f` for hours and `:>12.2f` for pay).

---

## H. File Handling

| File | Format | Mode used | Used by |
|---|---|---|---|
| `guards.txt` | CSV-like text: `id,name,post,rate` | `"r"` to read, `"a"` to append | `load_guards`, `save_guard` |
| `shifts.txt` | `guard_id,date,time_in,time_out` | `"r"` to read, `"a"` to append | `load_shifts`, `save_shift` |
| `payroll_report.txt` | Formatted plain text | `"w"` to write | `write_report` |

**Example line in `guards.txt`:** `1,Juan Dela Cruz,Main Gate,100.0`

**Modes:** Append mode (`"a"`) adds to the end and keeps old data. It also creates the file if it does not exist, which is why `guards.txt` and `shifts.txt` appear automatically. Write mode (`"w"`) replaces the old report each time it is exported.

**Role of `with open(...)`:** It closes the file automatically when the block ends, even if an error occurs.

```python
with open(GUARDS_FILE, "a") as file:
    file.write(line)
```

**Absent file:** `load_guards()` and `load_shifts()` catch `FileNotFoundError` and return an empty list, so the program works on the first run.

**Malformed lines:** A line that does not have exactly 4 comma-separated parts, or whose ID or rate cannot be converted by `int()`/`float()`, is skipped and a message `Skipped bad line...` is printed. The program does not crash.

**Persistence:** Records persist between runs because they are saved in text files. In testing, a guard and a shift added in one run were still listed when the program was started again.

---

## I. Error Handling

### Expected errors (input validation)
These are caused by the user's input and are expected. The functions in `payroll.py` detect them and `raise ValueError` with a clear message. The menu functions in `Main.py` catch them with `try/except ValueError` and show the message, so the program continues instead of stopping.

```python
try:
    name, post, rate = payroll.validate_guard(name, post, rate_text)
    ...
    storage.save_guard(guard)
    print("Guard saved.")
except ValueError as error:
    print("Error:", error)
```

| Situation | Where handled |
|---|---|
| Empty name, comma in name/post, rate not a number, rate ≤ 0 | `validate_guard` |
| Guard ID not a number, or guard does not exist | `validate_shift` |
| Wrong date format or month/day out of range | `check_date` |
| Wrong time format, hour/minute out of range, time out not later than time in | `time_to_hours`, `calculate_hours` |
| `guards.txt` / `shifts.txt` missing | `except FileNotFoundError` in `load_*` |
| Corrupted line in a data file | `except ValueError` in `load_*` |
| Shift in the file with an unknown guard or invalid times | `build_report_lines` writes a "Skipped" line |

### Unexpected programming errors
Only `ValueError` and `FileNotFoundError` are caught. Other errors (a typing mistake or a bug) are not hidden by a general `except`, so they would show a Python traceback that helps in debugging. This keeps expected input mistakes separate from real bugs.

---

## J. Testing, Debugging, and Results

All tests below were run on the actual program code. Tests T1–T11 call the functions directly, and T12–T13 run the whole program through the menu.

### Test table

| ID | Scenario | Input | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| T1 | Normal: valid guard | `validate_guard("Ana Cruz", "Lobby", "105")` | `("Ana Cruz", "Lobby", 105.0)` | `('Ana Cruz', 'Lobby', 105.0)` | Pass |
| T2 | Normal: hours and pay of a shift | `calculate_hours("08:00","16:00")`, then `calculate_pay(8.0, 100.0)` | `8.0` hours, `800.0` pay | `8.0` and `800.0` | Pass |
| T3 | Boundary: longest possible shift in one day | `calculate_hours("00:00","23:59")` | about `23.98` | `23.983333333333334` | Pass |
| T4 | Boundary: time out equals time in | `calculate_hours("08:00","08:00")` | `ValueError` | `Time out must be later than time in.` | Pass |
| T5 | Invalid: comma in name | `validate_guard("Cruz, Ana","Lobby","105")` | `ValueError` | `Name and post must not contain commas.` | Pass |
| T6 | Invalid: rate not a number / zero | rate `"abc"` and rate `"0"` | `ValueError` for each | `Hourly rate must be a number.` and `Hourly rate must be greater than 0.` | Pass |
| T7 | Invalid: bad time format / impossible time | `"8:00"` and `"25:00"` | `ValueError` for each | `Time must be in HH:MM format, like 08:30.` and `Time must be between 00:00 and 23:59.` | Pass |
| T8 | Invalid: guard ID does not exist / not a number | IDs `"9"` and `"abc"` | `ValueError` for each | `Guard ID does not exist.` and `Guard ID must be a whole number.` | Pass |
| T9 | Invalid: wrong date format / month 13 | `"11-03-2026"` and `"2026-13-01"` | `ValueError` for each | `Date must be in YYYY-MM-DD format...` and `Month must be 1-12 and day must be 1-31.` | Pass |
| T10 | Failure: data files do not exist | `load_guards()` and `load_shifts()` with no files | empty lists, no crash | `[]` and `[]` | Pass |
| T11 | Failure: malformed lines in `guards.txt` | file with one good line, `bad line`, and `abc,B,y,50` | only the good line is loaded; bad lines reported | 1 guard loaded; printed `Skipped bad line in guards file:` for both bad lines | Pass |
| T12 | Normal: first-run sample data, run twice | call `add_sample_data()` two times | 4 guards and 4 shifts, not duplicated | 4 guards and 4 shifts both times | Pass |
| T13 | Normal: full program flow and persistence | Menu: add guard `Mark Tan, Gate 2, 120`; add shift for guard 5 on `2026-11-06` 08:00–17:00; view shifts; export; exit. Then run again and choose "View all guards". | Guard and shift saved; report exported; data still present on the second run | Files `guards.txt` and `shifts.txt` had the new records; `Payroll report saved to payroll_report.txt` was shown; second run listed the guards | Pass |
| T14 | Normal: payroll report on sample data | `build_report_lines()` with the 4 sample guards and 4 sample shifts | total hours 34.0, total pay 3380.00 | `Total hours: 34.0`, `Total pay: 3380.00` | Pass |
| T15 | Boundary: impossible calendar date | `validate_shift(guards,"1","2026-02-31","08:00","16:00")` | `ValueError` (February has no 31st) | **Accepted**: returned `(1, '2026-02-31', '08:00', '16:00')` | **Fail** |

Manual check of T14: Juan 8 h × 100 = 800, Juan 10 h × 100 = 1000, Maria 4 h × 110 = 440, Pedro 12 h × 95 = 1140. Total pay = 3380 and total hours = 34, which matches the program output.

### Debugging observation

**Defect found (T15):** While testing boundary dates, the program accepted `2026-02-31`. The cause is in `check_date()`: it only checks `day < 1 or day > 31` for every month, so it does not know how many days each month has. The variable `year` is also calculated but never used.

```python
if month < 1 or month > 12 or day < 1 or day > 31:
    raise ValueError("Month must be 1-12 and day must be 1-31.")
```

**Planned correction (not yet implemented in my current code):** use Python's `datetime` module to validate the date, for example by calling `datetime.strptime(text, "%Y-%m-%d")` inside a `try` and converting the resulting `ValueError` into the program's own error message. **How I will verify it:** re-run T15 and expect `ValueError`, then re-run T9 and a normal date such as `2026-11-03` to confirm that valid dates are still accepted.

**Other observation:** In the payroll report, `Total shifts` uses `len(shifts)`, which counts every shift in the file, including shifts that were skipped (unknown guard or invalid times). So this number can be larger than the number of rows printed. This is documented as a limitation for now.

**Another observation during development:** `guards.txt`, `shifts.txt`, and `payroll_report.txt` are not created by separate code; they are created by the `open()` calls in `storage.py` (modes `"a"` and `"w"` create a missing file). The VS Code explorer may not show a new file until it is refreshed.

---

## K. Conclusion

**What the program achieves:** The current version lets the user add guards and shifts, validates the input with specific error messages, calculates hours and pay for each shift, and exports a payroll report. It uses lists, tuples, and dictionaries, is divided into three modules with clear roles, saves data in files that persist between runs, and handles expected errors without crashing.

**Limitations:** It is a console program using text files. There is no overtime, deductions, or net pay yet. Shifts cannot cross midnight, and the date check allows impossible dates such as February 31.

**Possible improvements:**
1. Replace `storage.py` with a database module (guards and shifts tables) and add the Tkinter interface with payslips and a payroll summary.
2. Add regular/overtime hours and a deductions dictionary to compute gross pay and net pay, and fix the date validation using `datetime`.

---

## L. References

- Python documentation: built-in functions `open()`, `int()`, `float()`, and exceptions (`ValueError`, `FileNotFoundError`), https://docs.python.org/3/
- Python documentation: `datetime.strptime` (for the planned date fix), https://docs.python.org/3/library/datetime.html
- GeeksforGeeks, "File Handling in Python", https://www.geeksforgeeks.org/python/file-handling-python/ (studied to understand `open()`, file modes, the `with` statement, and `FileNotFoundError`, used in Section H).
- Towards Data Science, "Formatting strings and numbers in python", https://towardsdatascience.com/formatting-strings-and-numbers-in-python-16a326a5d5b3/ (studied to understand f-string alignment with `:<` and `:>` and decimal places with `.2f`, used in Section G, Code excerpt 3).
- AI assistance: I used Claude (Anthropic) as a learning aid for this project. It explained my code line by line, pointed out mistakes and weak points in my program (for example, the date check that accepts impossible dates), guided me toward the solutions, and gave examples such as sample test cases and code excerpts. It also helped me organize and format this Markdown report. I studied the explanations, ran the program myself, and reviewed the report so that I understand the code and results written here.
