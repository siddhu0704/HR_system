import mysql.connector
import datetime

try:
    mysqldb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hrsystem"
    )
    cur = mysqldb.cursor()
except mysql.connector.Error as err:
    print(f"Database connection error: {err}")
    exit()

def create_employee():
    try:
        name = input("Enter employee name: ").strip()
        department = input("Enter department: ").strip()
        designation = input("Enter designation: ").strip()
        join_date = input("Enter join date (YYYY-MM-DD): ").strip()
        salary = float(input("Enter salary: "))
        datetime.datetime.strptime(join_date, "%Y-%m-%d")
        sql = "INSERT INTO employee (Name, Department, Designation, Join_date, Salary) VALUES (%s,%s,%s,%s,%s)"
        cur.execute(sql, (name, department, designation, join_date, salary))
        mysqldb.commit()
        print("Employee created successfully.")
    except Exception as e:
        print(f"Error: {e}")

def mark_attendance():
    try:
        emp_id = int(input("Enter employee ID: "))
        cur.execute("SELECT * FROM employee WHERE emp_id = %s", (emp_id,))
        if not cur.fetchone():
            print("Employee does not exist.")
            return
        status = input("Enter status (Present / Absent / Leave): ").capitalize()
        if status not in ["Present", "Absent", "Leave"]:
            print("Invalid status.")
            return
        att_date = input("Enter date (YYYY-MM-DD): ")
        datetime.datetime.strptime(att_date, "%Y-%m-%d")
        sql = "INSERT INTO attendance (emp_id, status, att_date) VALUES (%s,%s,%s)"
        cur.execute(sql, (emp_id, status, att_date))
        mysqldb.commit()
        print("Attendance recorded successfully.")
    except Exception as e:
        print(f"Error: {e}")

def view_attendance():
    try:
        emp_id = int(input("Enter employee ID to view attendance: "))
        cur.execute("SELECT Name FROM employee WHERE emp_id = %s", (emp_id,))
        result = cur.fetchone()
        if not result:
            print("Employee does not exist.")
            return
        emp_name = result[0]
        cur.execute("SELECT att_date, status FROM attendance WHERE emp_id = %s", (emp_id,))
        records = cur.fetchall()
        if records:
            print(f"Attendance for {emp_name}:")
            for date, status in records:
                print(f"{date} : {status}")
        else:
            print("No attendance records found.")
    except Exception as e:
        print(f"Error: {e}")

def apply_leave():
    try:
        emp_id = int(input("Enter employee ID: "))
        cur.execute("SELECT * FROM employee WHERE emp_id = %s", (emp_id,))
        if not cur.fetchone():
            print("Employee does not exist.")
            return
        leave_date = input("Enter leave date (YYYY-MM-DD): ")
        reason = input("Enter reason for leave: ").strip()
        datetime.datetime.strptime(leave_date, "%Y-%m-%d")
        sql = "INSERT INTO apply_for_leave (emp_id, leave_date, reason) VALUES (%s,%s,%s)"
        cur.execute(sql, (emp_id, leave_date, reason))
        mysqldb.commit()
        print("Leave applied successfully.")
    except Exception as e:
        print(f"Error: {e}")

def process_leave():
    try:
        leave_id = int(input("Enter leave request ID: "))
        decision = input("Approve or Reject: ").capitalize()
        if decision not in ["Approved", "Rejected"]:
            print("Invalid input. Must be 'Approved' or 'Rejected'.")
            return
        cur.execute("SELECT * FROM apply_for_leave WHERE leave_id = %s", (leave_id,))
        if not cur.fetchone():
            print("Leave request not found.")
            return
        cur.execute("UPDATE apply_for_leave SET status = %s WHERE leave_id = %s", (decision, leave_id))
        mysqldb.commit()
        print(f"Leave request ID {leave_id} updated to '{decision}'.")
    except Exception as e:
        print(f"Error: {e}")

def record_salary():
    try:
        emp_id = int(input("Enter employee ID: "))
        cur.execute("SELECT * FROM employee WHERE emp_id = %s", (emp_id,))
        if not cur.fetchone():
            print("Employee does not exist.")
            return
        pay_date = input("Enter payment date (YYYY-MM-DD): ")
        amount = float(input("Enter amount: "))
        datetime.datetime.strptime(pay_date, "%Y-%m-%d")
        sql = "INSERT INTO salary_payments (emp_id, pay_date, amount) VALUES (%s,%s,%s)"
        cur.execute(sql, (emp_id, pay_date, amount))
        mysqldb.commit()
        print("Salary payment recorded successfully.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        print("""
Select an option:
1. Create Employee
2. Mark Attendance
3. View Attendance
4. Apply for Leave
5. Approve/Reject Leave
6. Record Salary Payment
7. Exit
""")
        choice = input("Enter your choice (1-7): ")
        if choice == "1":
            create_employee()
        elif choice == "2":
            mark_attendance()
        elif choice == "3":
            view_attendance()
        elif choice == "4":
            apply_leave()
        elif choice == "5":
            process_leave()
        elif choice == "6":
            record_salary()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Enter 1-7.")

    cur.close()
    mysqldb.close()

if __name__ == "__main__":
    main()
