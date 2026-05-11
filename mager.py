student = {}

while True:
    print("\n -------STUDENT MANMENT SYSTEM-------")
    
    print("1. Add Student")
    print("2. View Students")
    print("3. check result")
    print("4. Exit")
    
    choice = input("ENTER YOUR CHOICE:")
    
    if choice == '1':
        name = input("enter student name")
        marks = int(input("enter marks:"))
        student[name] = marks
        print(f"{name} Successfully Added!")
        
    elif choice == 2:
        if not student:
            print("No students found.")
        else :
            for name ,marks in student.items():
                print(f"Name: {name}, Marks: {marks}")
                
    elif choice == 3:
        name = input("enter student name")
        
        if name in student:
            marks = student[name]
            
            if marks >= 40:
                print(f"{name} has passed with marks: {marks}")
             
            else:
                print("FAIL")   
        else:
            print("Student not Found PLEASE enter valid student")       