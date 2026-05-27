from __future__ import annotations
import json
import os
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any
from datetime import datetime

DATA_FILE = "students.json"

# --------------------------- Domain Model ---------------------------

@dataclass
class Student:
    student_id: str
    name: str
    age: int
    grade: str         #"A", "B+", "9th", etc.
    email: str
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat(timespec="seconds") + "Z")
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat(timespec="seconds") + "Z")

    def update_timestamp(self) -> None:
        self.updated_at = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Student":
        return Student(
            student_id=str(d["student_id"]),
            name=str(d["name"]),
            age=int(d["age"]),
            grade=str(d["grade"]),
            email=str(d["email"]),
            created_at=d.get("created_at") or datetime.utcnow().isoformat(timespec="seconds") + "Z",
            updated_at=d.get("updated_at") or datetime.utcnow().isoformat(timespec="seconds") + "Z",
        )

# --------------------------- Storage Layer ---------------------------

class StudentRepository:
    def __init__(self, path: str = DATA_FILE) -> None:
        self.path = path
        self._ensure_file()

    def _ensure_file(self) -> None:
        if not os.path.exists(self.path):
            self._save_all([])

    def _load_all(self) -> List[Student]:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Student.from_dict(x) for x in data]
        except (json.JSONDecodeError, FileNotFoundError):
            # Recover from a corrupted/missing file by resetting
            self._save_all([])
            return []
        except Exception as e:
            print(f"Error loading data: {e}")
            return []

    def _save_all(self, students: List[Student]) -> None:
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([asdict(s) for s in students], f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")

    # CRUD
    def add(self, student: Student) -> bool:
        students = self._load_all()
        if any(s.student_id == student.student_id for s in students):
            return False
        students.append(student)
        self._save_all(students)
        return True

    def get(self, student_id: str) -> Optional[Student]:
        students = self._load_all()
        for s in students:
            if s.student_id == student_id:
                return s
        return None

    def update(self, student_id: str, **fields) -> bool:
        students = self._load_all()
        updated = False
        for i, s in enumerate(students):
            if s.student_id == student_id:
                # Update allowed fields
                if "name" in fields and fields["name"] is not None:
                    s.name = fields["name"]
                if "age" in fields and fields["age"] is not None:
                    s.age = int(fields["age"])
                if "grade" in fields and fields["grade"] is not None:
                    s.grade = fields["grade"]
                if "email" in fields and fields["email"] is not None:
                    s.email = fields["email"]
                s.update_timestamp()
                students[i] = s
                updated = True
                break
        if updated:
            self._save_all(students)
        return updated

    def delete(self, student_id: str) -> bool:
        students = self._load_all()
        new_students = [s for s in students if s.student_id != student_id]
        if len(new_students) == len(students):
            return False
        self._save_all(new_students)
        return True

    def all(self) -> List[Student]:
        return self._load_all()

# --------------------------- Validation ---------------------------

def validate_student_id(sid: str) -> str:
    sid = sid.strip()
    if not sid:
        raise ValueError("Student ID cannot be empty.")
    if len(sid) > 20:
        raise ValueError("Student ID is too long (max 20).")
    if any(ch.isspace() for ch in sid):
        raise ValueError("Student ID cannot contain whitespace.")
    return sid

def validate_name(name: str) -> str:
    name = " ".join(name.split())
    if not name:
        raise ValueError("Name cannot be empty.")
    if len(name) > 60:
        raise ValueError("Name is too long (max 60).")
    return name

def validate_age(age_str: str) -> int:
    try:
        age = int(age_str)
    except ValueError:
        raise ValueError("Age must be an integer.")
    if not (3 <= age <= 120):
        raise ValueError("Age must be between 3 and 120.")
    return age

def validate_grade(grade: str) -> str:
    grade = grade.strip()
    if not grade:
        raise ValueError("Grade cannot be empty.")
    if len(grade) > 15:
        raise ValueError("Grade is too long (max 15).")
    return grade

def validate_email(email: str) -> str:
    email = email.strip()
    if not email or "@" not in email or email.startswith("@") or email.endswith("@"):
        raise ValueError("Email must be a valid address (e.g., user@example.com).")
    if len(email) > 80:
        raise ValueError("Email is too long (max 80).")
    return email

# --------------------------- Presentation Utils ---------------------------

def print_table(rows: List[Dict[str, Any]], headers: List[str]) -> None:
    if not rows:
        print("(no records)")
        return
    # Column widths
    widths = {h: max(len(h), max(len(str(r.get(h, ""))) for r in rows)) for h in headers}
    sep = "+-" + "-+-".join("-" * widths[h] for h in headers) + "-+"

    def fmt_row(r: Dict[str, Any]) -> str:
        return "| " + " | ".join(str(r.get(h, "")).ljust(widths[h]) for h in headers) + " |"

    print(sep)
    print("| " + " | ".join(h.ljust(widths[h]) for h in headers) + " |")
    print(sep)
    for r in rows:
        print(fmt_row(r))
    print(sep)

def student_to_row(s: Student) -> Dict[str, Any]:
    return {
        "ID": s.student_id,
        "Name": s.name,
        "Age": s.age,
        "Grade": s.grade,
        "Email": s.email,
        "Updated": s.updated_at,
    }

# --------------------------- Application Services ---------------------------

class StudentService:
    def __init__(self, repo: StudentRepository) -> None:
        self.repo = repo

    def create_student(self, student_id: str, name: str, age: str, grade: str, email: str) -> str:
        sid = validate_student_id(student_id)
        nm = validate_name(name)
        ag = validate_age(age)
        gr = validate_grade(grade)
        em = validate_email(email)
        s = Student(student_id=sid, name=nm, age=ag, grade=gr, email=em)
        ok = self.repo.add(s)
        if not ok:
            return f"Error: Student with ID '{sid}' already exists."
        return f"Student '{sid}' created."

    def update_student(self, student_id: str, name: Optional[str], age: Optional[str],
                       grade: Optional[str], email: Optional[str]) -> str:
        sid = validate_student_id(student_id)
        fields: Dict[str, Any] = {}
        if name is not None and name != "":
            fields["name"] = validate_name(name)
        if age is not None and age != "":
            fields["age"] = validate_age(age)
        if grade is not None and grade != "":
            fields["grade"] = validate_grade(grade)
        if email is not None and email != "":
            fields["email"] = validate_email(email)
        if not fields:
            return "Nothing to update."
        ok = self.repo.update(sid, **fields)
        return "Updated." if ok else f"Error: Student '{sid}' not found."

    def delete_student(self, student_id: str) -> str:
        sid = validate_student_id(student_id)
        ok = self.repo.delete(sid)
        return "Deleted." if ok else f"Error: Student '{sid}' not found."

    def get_student(self, student_id: str) -> Optional[Student]:
        sid = validate_student_id(student_id)
        return self.repo.get(sid)

    def list_students(self, sort_by: str = "student_id", descending: bool = False,
                      grade_filter: Optional[str] = None) -> List[Student]:
        studs = self.repo.all()
        if grade_filter:
            studs = [s for s in studs if s.grade.lower() == grade_filter.lower()]
        key_map = {
            "student_id": lambda s: s.student_id,
            "name": lambda s: s.name.lower(),
            "age": lambda s: s.age,
            "grade": lambda s: s.grade.lower(),
            "email": lambda s: s.email.lower(),
            "updated": lambda s: s.updated_at,
        }
        key_fn = key_map.get(sort_by, key_map["student_id"])
        studs.sort(key=key_fn, reverse=descending)
        return studs

    def search(self, query: str) -> List[Student]:
        q = query.strip().lower()
        if not q:
            return []
        studs = self.repo.all()
        return [
            s for s in studs
            if q in s.student_id.lower()
            or q in s.name.lower()
            or q in s.grade.lower()
            or q in s.email.lower()
        ]

# --------------------------- Console UI ---------------------------

def prompt(msg: str) -> str:
    return input(msg).strip()

def menu() -> None:
    repo = StudentRepository()
    svc = StudentService(repo)

    actions = {
        "1": "Add student",
        "2": "Update student",
        "3": "Delete student",
        "4": "View student by ID",
        "5": "List students",
        "6": "Search students",
        "0": "Exit",
    }

    while True:
        print("\nStudent Management System")
        for k in sorted(actions.keys()):
            print(f" {k}. {actions[k]}")

        choice = prompt("Select an option: ")
        try:
            if choice == "1":
                print("\nAdd Student")
                sid = prompt("ID: ")
                name = prompt("Name: ")
                age = prompt("Age: ")
                grade = prompt("Grade: ")
                email = prompt("Email: ")
                try:
                    msg = svc.create_student(sid, name, age, grade, email)
                    print(msg)
                except ValueError as ve:
                    print(f"Validation error: {ve}")

            elif choice == "2":
                print("\nUpdate Student")
                sid = prompt("ID to update: ")
                # Empty input means keep unchanged
                name = prompt("New Name (leave blank to keep): ")
                age = prompt("New Age (leave blank to keep): ")
                grade = prompt("New Grade (leave blank to keep): ")
                email = prompt("New Email (leave blank to keep): ")
                # Convert blanks to None so validator can skip
                name = name if name != "" else None
                age = age if age != "" else None
                grade = grade if grade != "" else None
                email = email if email != "" else None
                try:
                    msg = svc.update_student(sid, name, age, grade, email)
                    print(msg)
                except ValueError as ve:
                    print(f"Validation error: {ve}")

            elif choice == "3":
                print("\nDelete Student")
                sid = prompt("ID to delete: ")
                try:
                    print(svc.delete_student(sid))
                except ValueError as ve:
                    print(f"Validation error: {ve}")

            elif choice == "4":
                print("\nView Student")
                sid = prompt("ID: ")
                try:
                    s = svc.get_student(sid)
                    if s:
                        print_table([student_to_row(s)], ["ID", "Name", "Age", "Grade", "Email", "Updated"])
                    else:
                        print(f"No student found with ID '{sid}'.")
                except ValueError as ve:
                    print(f"Validation error: {ve}")

            elif choice == "5":
                print("\nList Students")
                sort_by = prompt("Sort by (student_id, name, age, grade, email, updated) [student_id]: ") or "student_id"
                order = prompt("Order (asc/desc) [asc]: ") or "asc"
                descending = order.lower().startswith("d")
                gf = prompt("Filter by grade (leave blank for all): ").strip() or None
                studs = svc.list_students(sort_by=sort_by, descending=descending, grade_filter=gf)
                rows = [student_to_row(s) for s in studs]
                print_table(rows, ["ID", "Name", "Age", "Grade", "Email", "Updated"])

            elif choice == "6":
                print("\nSearch Students")
                q = prompt("Enter search query (matches ID/Name/Grade/Email): ")
                studs = svc.search(q)
                rows = [student_to_row(s) for s in studs]
                print_table(rows, ["ID", "Name", "Age", "Grade", "Email", "Updated"])

            elif choice == "0":
                print("Goodbye.")
                return
            else:
                print("Invalid choice. Please enter a valid option.")
        except KeyboardInterrupt:
            print("\nInterrupted. Returning to menu...")
        except Exception as e:
            print(f"Unexpected error: {e}")

# --------------------------- Entry Point ---------------------------

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nExiting.")
