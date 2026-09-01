import csv
import matplotlib.pyplot as plt

# Function to convert 100 scale mark to GPA
def convert_to_gpa(mark):
    return round((mark / 100) * 4.0, 2)

# Function to generate student ID using slicing
def generate_id(first_name, last_name, roll_no):
    return first_name[:3].upper() + last_name[:2].upper() + str(roll_no)

# Insertion sort to rank students based on average GPA
def insertion_sort(students):
    for i in range(1, len(students)):
        key = students[i]
        j = i - 1
        while j >= 0 and students[j]['avg_gpa'] < key['avg_gpa']:
            students[j + 1] = students[j]
            j -= 1
        students[j + 1] = key
    return students

# Read data from CSV file
def read_student_data(filename):
    students = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['Name']
                first, last = name.split()[0], name.split()[1]
                roll = row['Roll']
                subjects = {
                    "Python": int(row['Python']),
                    "Maths": int(row['Maths']),
                    "DBMS": int(row['DBMS'])
                }
                gpa_subjects = {sub: convert_to_gpa(mark) for sub, mark in subjects.items()}
                avg_gpa = round(sum(gpa_subjects.values()) / len(gpa_subjects), 2)
                student_id = generate_id(first, last, roll)
                students.append({
                    "id": student_id,
                    "name": name,
                    "subjects": gpa_subjects,
                    "avg_gpa": avg_gpa
                })
    except FileNotFoundError:
        print("Error: CSV file not found")
    except Exception as e:
        print("Error while reading file:", e)
    return students

# Write report card for each student
def write_report_cards(students):
    for s in students:
        try:
            filename = f"{s['id']}_report.txt"
            with open(filename, 'w') as f:
                f.write(f"Report Card\n")
                f.write(f"Student ID: {s['id']}\n")
                f.write(f"Name: {s['name']}\n")
                f.write("Subjects and GPA:\n")
                for sub, gpa in s['subjects'].items():
                    f.write(f"  {sub}: {gpa}\n")
                f.write(f"Average GPA: {s['avg_gpa']}\n")
        except Exception as e:
            print("Error writing report for", s['name'], ":", e)

# Plot class average
def plot_class_average(students):
    names = [s['name'] for s in students]
    gpas = [s['avg_gpa'] for s in students]
    plt.bar(names, gpas, color='skyblue')
    plt.xlabel('Students')
    plt.ylabel('Average GPA')
    plt.title('Class Performance Overview')
    plt.savefig('class_average.png')
    plt.show()

# Main execution
if __name__ == "__main__":
    data = read_student_data("students.csv")
    if data:
        ranked_students = insertion_sort(data)
        print("Ranked Students:")
        for idx, s in enumerate(ranked_students, start=1):
            print(f"{idx}. {s['name']} (ID: {s['id']}) - GPA: {s['avg_gpa']}")
        write_report_cards(ranked_students)
        plot_class_average(ranked_students)
    else:
        print("No student data available.")