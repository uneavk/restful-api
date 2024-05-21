import json
import requests

BASE_URL = "http://127.0.0.1:1103/api/exams"
def liner():
    print('~'*40)
def print_error(e):
    print(f"An error occurred while making the request: {e}")

def get_exam(exam_id=None):
    try:
        if not exam_id :
            url = f"{BASE_URL}"
            res = requests.get(url)
            res.raise_for_status()
            print('Get exams:')
            print(res.json())
            liner()
        else:
            url = f"{BASE_URL}/{exam_id}"
            res = requests.get(url)
            if res.status_code == 404:
                print(f'Get exam {exam_id}')
                print(f"Exam {exam_id} not found")
                liner()
            else:
                res.raise_for_status()
                print('Get exam')
                print(res.json())
                liner()
    except requests.exceptions.RequestException as e:
        print_error(e)

def post_exam(subject_id, date, location, examiner):
    try:
        data = {
            "subject_id": subject_id,
            "date": date,
            "location": location,
            "examiner": examiner
        }
        headers = {
            "Content-Type": "application/json"
        }
        res = requests.post(BASE_URL, data=json.dumps(data), headers=headers)
        res.raise_for_status()
        print('Post exam')
        print(res.json())
        liner()
    except requests.exceptions.RequestException as e:
        print('Post exam')
        print_error(e)
        liner()

def put_exam(exam_id, subject_id=None, date=None, location=None, examiner=None):
    try:
        url = f"{BASE_URL}/{exam_id}"
        data = {}
        if subject_id:
            data["subject_id"] = subject_id
        if date:
            data["date"] = date
        if location:
            data["location"] = location
        if examiner:
            data["examiner"] = examiner
        headers = {
            "Content-Type": "application/json"
        }
        res = requests.put(url, data=json.dumps(data), headers=headers)
        if res.status_code == 404:
            print(f"Exam {exam_id} not found")
        elif res.status_code == 400:
            print(res.json()["message"])
            liner()
        else:
            res.raise_for_status()
            print(f'Put exam {exam_id}')
            print(res.json())
            liner()
    except requests.exceptions.RequestException as e:
        print(f'Put exam {exam_id}')
        print_error(e)
        liner()


def delete_exam(exam_id):
    try:
        url = f"{BASE_URL}/{exam_id}"
        res = requests.delete(url)

        if res.status_code == 404:
            print('Delete exam')
            print(f"Exam {exam_id} not found")
        else:
            res.raise_for_status()
            print(f'Delete exam {exam_id}')
            print(f"Exam {exam_id} deleted")

    except requests.exceptions.RequestException as e:
        print('Delete exam')
        print_error(e)

    liner()


def print_menu():
    print("1. Get exams")
    print("2. Get exam by ID")
    print("3. Post exam")
    print("4. Put exam")
    print("5. Delete exam")
    print("0. Exit")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice (0-6): ")

        if choice == "0":
            print("Exiting the program. Goodbye!")
            break
        elif choice == "1":
            get_exam()
        elif choice == "2":
            exam_id = input("Enter exam ID: ")
            get_exam(exam_id)
        elif choice == "3":
            subject_id = input("Enter subject ID: ")
            date = input("Enter date: ")
            location = input("Enter location: ")
            examiner = input("Enter examiner: ")
            post_exam(subject_id, date, location, examiner)
        elif choice == "4":
            exam_id = input("Enter exam ID: ")
            subject_id = input("Enter new subject ID(press enter if you don't want to change) : ")
            date = input("Enter new date(press enter if you don't want to change) : ")
            location = input("Enter new location (press enter if you don't want to change): ")
            examiner = input("Enter new examiner(press enter if you don't want to change): ")
            put_exam(exam_id, subject_id=subject_id or None,
                                  date=date or None, location=location or None, examiner=examiner or None)
        elif choice == "5":
            exam_id = input("Enter exam ID: ")
            delete_exam(exam_id)
        else:
            print("Invalid choice. Please enter a number between 0 and 6.")

main()
