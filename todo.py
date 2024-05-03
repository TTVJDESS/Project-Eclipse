import os
import pickle
import hashlib
from colorama import init, Fore, Style
from datetime import datetime
init(autoreset=True)  # Initialize colorama

# Define colors
COLOR_TITLE = Fore.CYAN
COLOR_MENU = Fore.GREEN
COLOR_ERROR = Fore.RED
COLOR_SUCCESS = Fore.MAGENTA

# Data storage filenames
USER_DATA_FILE = "user_data.pkl"

# Function to clear the console screen
def clear_screen():
    # Clear screen command based on OS
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display the to-do list
def show_list(todo_list):
    clear_screen()
    print(COLOR_TITLE + "Your To-Do List:")
    if not todo_list:
        print("  No tasks.")
    else:
        for index, task_info in enumerate(todo_list, start=1):
            category, task, deadline, priority = task_info
            if deadline:
                formatted_deadline = deadline.strftime("%Y-%m-%d %H:%M")
                print(f"  {index}. [{category}] {task} - Deadline: {formatted_deadline} - Priority: {priority}")
            else:
                print(f"  {index}. [{category}] {task} - Priority: {priority}")

# Function to hash a password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to register a new user
def register_user():
    clear_screen()
    print(COLOR_TITLE + "User Registration")

    username = input(COLOR_MENU + "Enter your desired username: ")
    password = input(COLOR_MENU + "Enter your password: ")

    with open(USER_DATA_FILE, 'rb') as f:
        user_data = pickle.load(f)

    if username in user_data:
        print(COLOR_ERROR + "Username already exists. Please choose another username.")
        return

    hashed_password = hash_password(password)
    user_data[username] = {'password': hashed_password, 'tasks': []}

    with open(USER_DATA_FILE, 'wb') as f:
        pickle.dump(user_data, f)

    print(COLOR_SUCCESS + "User registered successfully. You can now log in.")

# Function to authenticate a user
def authenticate_user():
    clear_screen()
    print(COLOR_TITLE + "User Login")

    username = input(COLOR_MENU + "Enter your username: ")
    password = input(COLOR_MENU + "Enter your password: ")

    with open(USER_DATA_FILE, 'rb') as f:
        user_data = pickle.load(f)

    if username not in user_data or user_data[username]['password'] != hash_password(password):
        print(COLOR_ERROR + "Invalid username or password. Please try again.")
        return None

    print(COLOR_SUCCESS + "Login successful. Welcome, " + username + "!")
    return username

# Function to add a task for the authenticated user
def add_task(username):
    clear_screen()
    print(COLOR_TITLE + f"Add Task for {username}")

    with open(USER_DATA_FILE, 'rb') as f:
        user_data = pickle.load(f)

    task = input(COLOR_MENU + "Enter task to add: ")
    category = input(COLOR_MENU + "Enter category for the task: ")
    deadline_str = input(COLOR_MENU + "Enter deadline for the task (YYYY-MM-DD HH:MM) or leave blank: ")
    priority = input(COLOR_MENU + "Enter priority for the task (high, medium, low): ").lower()

    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print(COLOR_ERROR + "Invalid deadline format. Please use YYYY-MM-DD HH:MM.")
            return
    else:
        deadline = None

    user_data[username]['tasks'].append((category, task, deadline, priority))

    with open(USER_DATA_FILE, 'wb') as f:
        pickle.dump(user_data, f)

    print(COLOR_SUCCESS + f"Task '{task}' added to your to-do list under category '{category}' with priority '{priority}'.")
    show_list(user_data[username]['tasks'])

# Function to sort tasks by deadline
def sort_tasks_by_deadline(username):
    with open(USER_DATA_FILE, 'rb') as f:
        user_data = pickle.load(f)

    user_tasks = user_data[username]['tasks']
    sorted_tasks = sorted(user_tasks, key=lambda x: x[2] if x[2] else datetime.max)  # Sort by deadline

    clear_screen()
    print(COLOR_TITLE + "Tasks sorted by Deadline:")
    show_list(sorted_tasks)

# Function to sort tasks by category
def sort_tasks_by_category(username):
    with open(USER_DATA_FILE, 'rb') as f:
        user_data = pickle.load(f)

    user_tasks = user_data[username]['tasks']
    sorted_tasks = sorted(user_tasks, key=lambda x: x[0])  # Sort by category

    clear_screen()
    print(COLOR_TITLE + "Tasks sorted by Category:")
    show_list(sorted_tasks)

# Function to sort tasks by task name
def sort_tasks_by_name(username):
    with open(USER_DATA_FILE, 'rb') as f:
        user_data = pickle.load(f)

    user_tasks = user_data[username]['tasks']
    sorted_tasks = sorted(user_tasks, key=lambda x: x[1].lower())  # Sort by task name

    clear_screen()
    print(COLOR_TITLE + "Tasks sorted by Task Name:")
    show_list(sorted_tasks)

# Main function to run the to-do list application
def main():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'wb') as f:
            pickle.dump({}, f)

    print(COLOR_TITLE + "Welcome to the To-Do List Application!")

    while True:
        print("\nChoose an option:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        try:
            choice = int(input(COLOR_MENU + "Enter your choice (1-3): "))
            if choice == 1:
                register_user()
            elif choice == 2:
                username = authenticate_user()
                if username:
                    while True:
                        print("\nChoose an option:")
                        print("1. Add Task")
                        print("2. Sort Tasks")
                        print("3. Show To-Do List")
                        print("4. Logout")

                        try:
                            user_choice = int(input(COLOR_MENU + "Enter your choice (1-4): "))
                            if user_choice == 1:
                                add_task(username)
                            elif user_choice == 2:
                                while True:
                                    print("\nSort Tasks by:")
                                    print("1. Deadline")
                                    print("2. Category")
                                    print("3. Task Name")
                                    print("4. Back to Main Menu")

                                    try:
                                        sort_choice = int(input(COLOR_MENU + "Enter your sort choice (1-4): "))
                                        if sort_choice == 1:
                                            sort_tasks_by_deadline(username)
                                        elif sort_choice == 2:
                                            sort_tasks_by_category(username)
                                        elif sort_choice == 3:
                                            sort_tasks_by_name(username)
                                        elif sort_choice == 4:
                                            break
                                        else:
                                            print(COLOR_ERROR + "Invalid choice. Please choose a number from 1 to 4.")
                                    except ValueError:
                                        print(COLOR_ERROR + "Invalid input. Please enter a valid choice.")
                            elif user_choice == 3:
                                with open(USER_DATA_FILE, 'rb') as f:
                                    user_data = pickle.load(f)
                                show_list(user_data[username]['tasks'])
                            elif user_choice == 4:
                                clear_screen()
                                print(COLOR_TITLE + "Logging out. Goodbye, " + username + "!")
                                break
                            else:
                                print(COLOR_ERROR + "Invalid choice. Please choose a number from 1 to 4.")
                        except ValueError:
                            print(COLOR_ERROR + "Invalid input. Please enter a valid choice.")
            elif choice == 3:
                clear_screen()
                print(COLOR_TITLE + "Exiting program. Goodbye!")
                break
            else:
                print(COLOR_ERROR + "Invalid choice. Please choose a number from 1 to 3.")
        except ValueError:
            print(COLOR_ERROR + "Invalid input. Please enter a valid choice.")

if __name__ == "__main__":
    main()
