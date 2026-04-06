import json
from datetime import date
guild_habits = {
    "fitness": [
        "Walk 30 minutes",
        "Go to the gym",
        "Stretch",
        "Do 20 squats"
    ],
    "health": [
        "Drink water",
        "Eat vegetables",
        "Avoid sugary drinks",
        "Prepare a healthy meal"
    ],
    "education": [
        "Study Python",
        "Read 10 pages",
        "Practice German",
        "Write notes"
    ]
}


def add_user(users: dict, name: str, age: int, gender: str, goal: str):
    users[name] = {
        "age": age,
        "goal": goal,
        "gender": gender,
        "xp": 0,
        "habits": []
    }


def print_profile(users: dict, name: str):
    if name not in users:
        print(f"User {name} not found")
        return

    profile = users[name]
    print(f"--- Profile: {name} ---")
    print(f"Age: {profile['age']}")
    print(f"Gender: {profile['gender']}")
    print(f"Main Goal: {profile['goal']}")
    print(f"XP: {profile['xp']}")
    print(f"Active Habits: {len(profile['habits'])}")


def choose_guild():
    print("Choose your guild:")
    print("1. Fitness")
    print("2. Health")
    print("3. Education")
    print("4. Exit")

    while True:
        choice = input("Enter guild number: ")

        if choice == "1":
            return "fitness"
        elif choice == "2":
            return "health"
        elif choice == "3":
            return "education"
        elif choice == "4":
            return None
        else:
            print("Invalid choice, please try again.")


def show_guild_habits(guild: str):
    print(f"Available habits for {guild.capitalize()} Guild:")

    habits = guild_habits[guild]
    for index, habit in enumerate(habits, start=1):
        print(f"{index}. {habit}")


def choose_habit_from_guild(guild: str):
    habits = guild_habits[guild]

    while True:
        show_guild_habits(guild)
        choice = input("Choose a habit number (or type 'exit'): ")

        if choice.lower() == "exit":
            return None

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(habits):
                return habits[choice - 1]

        print(
            f"Please enter a number between 1 and {len(habits)}, or type 'exit'.")


def add_habit(users: dict, name: str, habit_name: str, guild: str):
    if name not in users:
        print(f"User {name} not found")
        return

    habits = users[name]["habits"]
    today = str(date.today())
    for habit in habits:
        if habit["name"].lower() == habit_name.lower():
            if habit.get("last_completed") == today:
                print(f"You already completed '{habit_name}' today!")
                return
            habit["streak"] += 1
            habit["xp"] += 10
            habit["last_completed"] = today

            users[name]["xp"] += 10

            level = get_habit_level(habit["guild"], habit["xp"])

            print(f"Updated! {habit_name} streak is now {habit['streak']}")
            print(f"{habit_name} gained 10 XP and is now at level: {level}")
            print(f"You gained 10 XP! Total XP: {users[name]['xp']}")
            return

    new_habit = {
        "name": habit_name,
        "guild": guild,
        "streak": 1,
        "xp": 10, "last_completed": str(date.today())
    }

    habits.append(new_habit)
    users[name]["xp"] += 10

    level = get_habit_level(new_habit["guild"], new_habit["xp"])

    print(f"New habit added: {habit_name} (streak: 1)")
    print(f"{habit_name} gained 10 XP and starts at level: {level}")
    print(f"You gained 10 XP! Total XP: {users[name]['xp']}")


def get_habit_level(guild: str, habit_xp: int):

    ranks = {
        "fitness": [(120, "Master"), (70, "Warrior"), (30, "Explorer")],
        "health": [(120, "Master"), (70, "Cultivator"), (30, "Guardian")],
        "education": [(120, "Master"), (70, "Scholar"), (30, "Sage")]
    }

    if guild not in ranks:
        return "Unknown"

    for xp_needed, title in ranks[guild]:
        if habit_xp >= xp_needed:
            return title

    return "Apprentice"


def show_all_habits(users: dict, name: str):
    if name not in users:
        print(f"User {name} not found")
        return

    habit_list = users[name]["habits"]
    print(f"Habits for {name}:")

    for habit in habit_list:
        level = get_habit_level(habit["guild"], habit["xp"])
        print(
            f"* {habit['name']} | Guild: {habit['guild']} | "
            f"Streak: {habit['streak']} | Habit XP: {habit['xp']} | Rank: {level}"
        )


def save_data(users: dict):
    with open("user_data.json", "w") as file:
        json.dump(users, file, indent=4)

    print("Data saved successfully!")


def load_data():
    try:
        with open("user_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("No previous data found. Starting fresh.")
        return {}


def main():
    users = load_data()

    user_name = input("Enter your name: ").lower()

    if user_name.lower() in users:
        print("Welcome back!")
    else:
        while True:
            try:
                user_age = int(input("Enter your age: "))
                break
            except ValueError:
                print("Please enter your age in numbers")

        general_gender = ["Female", "Male", "Other"]
        print("Choose your gender: ")
        for index, gender in enumerate(general_gender, start=1):
            print(f"{index}.{gender}")
        while True:
            choice = input("Enter the number: ")
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(general_gender):
                    user_gender = general_gender[choice-1]
                    break
                else:
                    print("Invalid choice, please try again.")
        user_goal = input("What is your main goal? ")

        add_user(users, user_name, user_age, user_gender, user_goal)

    print_profile(users, user_name)

    while True:
        print("\nChoose a guild, or type 'exit' to finish.")
        selected_guild = choose_guild()
        if selected_guild is None:
            break
        chosen_habit = choose_habit_from_guild(selected_guild)

        if chosen_habit is None:
            continue

        add_habit(users, user_name, chosen_habit, selected_guild)

        stop = input("Do you want to add another habit? (yes/no): ").lower()
        if stop == "no":
            break

    show_all_habits(users, user_name)
    print(f"Final XP: {users[user_name]['xp']}")
    save_data(users)


if __name__ == "__main__":
    main()
