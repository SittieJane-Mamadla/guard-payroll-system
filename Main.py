# main.py
# The menu of the Guard Management and Payroll program.
# To run it:  python main.py
import storage
import payroll


def add_guard_menu():
    name = input("Name: ")
    post = input("Post: ")
    rate_text = input("Hourly rate: ")

    try:
        name, post, rate = payroll.validate_guard(name, post, rate_text)
        guards = storage.load_guards()
        guard = {
            "guard_id": payroll.next_guard_id(guards),
            "name": name,
            "post": post,
            "rate": rate,
        }
        storage.save_guard(guard)
        print("Guard saved.")
    except ValueError as error:
        print("Error:", error)


def view_guards_menu():
    print(f"{'ID':<6}{'Name':<20}{'Post':<15}{'Rate':>8}")
    print("-" * 49)
    for g in storage.load_guards():
        print(f"{g['guard_id']:<6}{g['name']:<20}{g['post']:<15}{g['rate']:>8.2f}")


def add_shift_menu():
    guard_id_text = input("Guard ID: ")
    shift_date = input("Date (YYYY-MM-DD): ")
    time_in = input("Time in (HH:MM): ")
    time_out = input("Time out (HH:MM): ")

    try:
        guards = storage.load_guards()
        shift = payroll.validate_shift(guards, guard_id_text, shift_date, time_in, time_out)
        storage.save_shift(shift)
        print("Shift saved.")
    except ValueError as error:
        print("Error:", error)


def view_shifts_menu():
    print(f"{'No.':<6}{'Guard':<8}{'Date':<14}{'In':<8}{'Out':<8}")
    print("-" * 44)
    number = 1
    for guard_id, shift_date, time_in, time_out in storage.load_shifts():
        print(f"{number:<6}{guard_id:<8}{shift_date:<14}{time_in:<8}{time_out:<8}")
        number = number + 1


def export_report_menu():
    guards = storage.load_guards()
    shifts = storage.load_shifts()
    lines = payroll.build_report_lines(guards, shifts)
    storage.write_report(lines)
    print("Payroll report saved to", storage.REPORT_FILE)


storage.add_sample_data()

while True:
    print("\n--- GUARD MANAGEMENT ---")
    print("1. Add guard")
    print("2. View all guards")
    print("3. Add shift")
    print("4. View all shifts")
    print("5. Export payroll report")
    print("6. Exit")
    choice = input("Choose: ")

    if choice == "1":
        add_guard_menu()
    elif choice == "2":
        view_guards_menu()
    elif choice == "3":
        add_shift_menu()
    elif choice == "4":
        view_shifts_menu()
    elif choice == "5":
        export_report_menu()
    elif choice == "6":
        break
    else:
        print("Invalid choice.")