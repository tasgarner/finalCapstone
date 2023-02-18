# importing module
import datetime

# defining function to register user
def reg_user():
    added_user = (input("Enter the username you'd like to add: "))
    new_user = False
    with open('user.txt', 'r') as user_file:
        lines = user_file.readlines()
        for line in lines:
            # checking that the user isn't already in database
            if line.find(added_user) != -1:
                print("Error: username already exists. Please enter a different username.")
                new_user = True
                break
            # if user doesn't exist, create user and passwork
            if new_user == False:
                added_user_password = (input("Enter the password for this user: "))
                new_password = False

                while new_password == False:   
                    password_confirm = input("Please retype your password to confirm: ")

                    if added_user_password == password_confirm:
                        new_password = True
                        return "User saved!"
                    
                    # making sure that the user enters the password twice to confirm
                    else:
                        print("Passwords do not match. Try again.")

                # appending to user.txt file
                with open ('user.txt', 'a')as user_file:
                    user_file.write(f"\n{added_user}, {added_user_password}")

# defining function to add task
def add_task():
        # opening task file and allowing user to append
        task_file = open("tasks.txt", "a+")
        username = input("Enter the username of the assignee: ")
        
        # getting task information from user
        added_task_title = input("Enter the title of the task: ")
        added_task_description = input("Give a description of the task:\n")
        task_due_date = input("Enter the due date [in format dd-mm-yyyy]:\n")
        task_status = input("Has the task been completed? [Yes or No]: ") 
        
        # writing the information to the file
        task_file.write(f"\n{username}, {added_task_title}, {added_task_description}, {task_due_date}, {task_status}")
        task_file.close()

# defining function to view all tasks
def view_all():
    task_file = open("tasks.txt", "r")

    # stripping and splitting the lines for formatting purposes
    for line in task_file:
        task_file_content = line.strip().split(",")

        # using indexing to print the correct information in a clear format
        print(f"""
        Task username:          {task_file_content[0]}
        Task tile:              {task_file_content[1]}
        Task description:       {task_file_content[2]}
        Task due date:          {task_file_content[3]}
        Task completion:        {task_file_content[4]}
        """)

# defining function to view mine and make changes
def view_mine():
    # asking user to confirm the username of the tasks they would like to be checked
    with open("tasks.txt", "r") as task_file:
        username = input("What user's tasks are you looking for?:")
        lines = task_file.readlines()

        # finding the relevant task information in file
        tasks = []
        for line in lines:
            task_file_content = line.strip().split(",")
            if line.find(username) != -1: 
                tasks.append({
                    'username': task_file_content[0],
                    'title': task_file_content[1],
                    'description': task_file_content[2],
                    'due_date': task_file_content[3],
                    'completion': task_file_content[4]
                })

        # printing error message if user has no assigned tasks
        if len(tasks) == 0:
            print("No tasks found for the specified user.")
            return
        
        for i, task in enumerate(tasks):
            print(f"{i}: {task['title']}")
        
        task_index = int(input("Enter the number of the task you want to view (-1 to return to main menu): "))
        if task_index == -1:
            return
        
        # getting task information and printing it in user friendly way
        task = tasks[task_index]
        print(f"""
        Task username:          {task['username']}
        Task tile:              {task['title']}
        Task description:       {task['description']}
        Task due date:          {task['due_date']}
        Task completion:        {task['completion']}
        """)

        # giving user the option to edit status of the task
        choice = input("What would you like to do (mark complete/edit)? ")
        if choice.lower() == 'mark complete':
            completion = input("Mark task as complete (yes/no)? ")
            if completion.lower() == 'yes':
                task['completion'] = 'yes'
            elif completion.lower() == 'no':
                task['completion'] = 'no'
            else:
                print("Invalid input. Task completion not updated.")
        elif choice.lower() == 'edit':
            
            # allow user to edit task username or due date
            task['username'] = input("Update username: ")
            task['due_date'] = input("Update due date: ")
        else:
            print("Invalid input. No changes made to task.")

def generate_reports():
    # initialize the task counters
    total_tasks = 0
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0

    # open tasks.txt in read mode
    with open("tasks.txt", "r") as tasks_file:
        # read each line in tasks.txt
        for line in tasks_file:
            # split the line into a list of words
            words = line.split()

            # increment the total tasks counter
            total_tasks += 1

            # checking if the task is completed or not
            if words[-1] == "no":
                uncompleted_tasks += 1
            else:
                completed_tasks += 1

    # calculate the percentage of tasks that are incomplete and the percentage of tasks that are overdue
    incomplete_percent = (uncompleted_tasks / total_tasks) * 100
    overdue_percent = (overdue_tasks / total_tasks) * 100

    # open task_overview.txt in write mode
    with open("task_overview.txt", "w") as task_file:
        # build the task overview string using string formatting
        task_overview = (
            "Total tasks: {}\n"
            "Completed tasks: {}\n"
            "Uncompleted tasks: {}\n"
            "Overdue tasks: {}\n"
            "Incomplete tasks: {:.2f}%\n"
            "Overdue tasks: {:.2f}%\n"
        ).format(total_tasks, completed_tasks, uncompleted_tasks, overdue_tasks, incomplete_percent, overdue_percent)

        # write the task overview to task_overview.txt
        task_file.write(task_overview)

    # ===== user_overview.txt =====
    tasks = []
    with open("tasks.txt", "r") as tasks_file:
        for line in tasks_file:
            tasks.append(line.strip().split(","))

    # initialize counters for number of users and tasks
    num_users = 0
    num_tasks = len(tasks)
    user_tasks = {}

    # process data
    for task in tasks:
        user = task[0]
        if user not in user_tasks:
            user_tasks[user] = {"total": 0, "completed": 0, "overdue": 0}
        user_tasks[user]["total"] += 1
        if task[3] == "yes":
            user_tasks[user]["completed"] += 1
        elif task[1] < datetime.datetime.now().strftime("%d-%m-%Y"):
            user_tasks[user]["overdue"] += 1

    with open("user.txt", "r") as users_file:
        for line in users_file:
            num_users += 1

    # write report to file
    with open("user_overview.txt", "w") as report_file:
        report_file.write("Number of users: " + str(num_users) + "\n")
        report_file.write("Number of tasks: " + str(num_tasks) + "\n")
        for user, data in user_tasks.items():
            report_string = """
            Total tasks: {}
            Percentage of total tasks: {:.2f}%
            Percentage of tasks completed: {:.2f}%
            Percentage of tasks not completed: {:.2f}%
            Percentage of tasks overdue: {:.2f}%\n"""
            report_file.write(report_string.format(user, data["total"] / num_tasks * 100, data["completed"] / data["total"] * 100, (data["total"] - data["completed"]) / data["total"] * 100, data["overdue"] / data["total"] * 100))
 

def display_stats():
    num_of_tasks = 0
    num_of_users = 0
                
         # taking the number of lines in the 2 txt files to present the stats for tasks and users
    with open("tasks.txt", "r") as task_file:
        num_of_tasks = len(task_file.readlines())
        print (f"Total number of tasks: {num_of_tasks}")

    with open("user.txt", "r") as username_in_file:
        num_of_users = len(username_in_file.readlines())
        print (f"Total number of users: {num_of_users}")

def error_message():
    print("Error: please choose from the options above.")

#==========Login Section=============
# creating an empty dictionary
users = {}

#opening and reading user.txt file for valid usernames & splitting the line into usernames & passwords
with open ('user.txt', 'r', encoding='utf-8') as username_in_file:
    for line in username_in_file:
        username_in_file, password_in_file = line.split(", ")
        users[username_in_file.strip()] = password_in_file.strip()

# allowing user input for login, printing a response message
username = input("Please enter your username: ")
while username not in users:
    print("Error: Incorrect username.")
    username = input("Please enter your username: ")
if username in users:
            print("Valid username!")

# repeating the above for the password entry
with open('user.txt', 'r', encoding='utf-8') as password_in_file:
     for line in password_in_file:
        username_in_file, password_in_file = line.split(", ")
        users[password_in_file.strip()] = username_in_file.strip()

user_password = input("Please enter your password: ")
while user_password not in users:
     print("Error: Incorrect password.")
     user_password = input("Please enter a valid password: ")
if user_password in users:
    valid_password = print("Correct password!")


while True:
    if username == "admin":
        # providing admin with personalised options
        admin_menu = input("""Please choose from the options below:
        r - register a new user
        a - add a task
        va - view all tasks
        vm - view my tasks
        gr - generate reports
        ds - display statistics
        e - exit
        """)

        if admin_menu == "r":
            reg_user()
        elif admin_menu == "a":
            add_task()
        elif admin_menu == "va":
            view_all()
        elif admin_menu == "vm":
            view_mine()
        elif admin_menu == "gr":
            print("Reports generated")
            generate_reports()
        elif admin_menu == "ds":
            display_stats()
        elif admin_menu == "e":
            print("Closing program")
            exit()
        else:
            error_message()
    
    elif username != "admin":
        # providing non-admin users with limited options
        menu = input("""Please choose from the options below:
        a - add a task
        va - view all tasks
        vm - view my tasks
        e - exit
        """)

        if menu == "a":
            add_task()
        elif menu == "va":
            view_all()
        elif menu == "vm":
            view_mine()
        elif menu == "e":
            print("Closing program")
            exit()
        else:
            error_message()