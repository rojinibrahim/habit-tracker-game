import json
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


def add_user(users: dict, name: str, age: int, gender: str, goal: str, guild: str):
    users[name] = {
        "age": age,
        "goal": goal,
        "gender": gender,
        "guild": guild,
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
    print(f"Guild: {profile['guild']}")
    print(f"XP: {profile['xp']}")
    print(f"Active Habits: {len(profile['habits'])}")


def choose_guild():
    print("Choose your guild:")
    print("1. Fitness")
    print("2. Health")
    print("3. Education")

    while True:
        choice = input("Enter guild number: ")

        if choice == "1":
            return "fitness"
        elif choice == "2":
            return "health"
        elif choice == "3":
            return "education"
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

        print("Invalid choice, please try again.")


def add_habit(users: dict, name: str, habit_name: str):
    if name not in users:
        print(f"User {name} not found")
        return

    habits = users[name]["habits"]

    for habit in habits:
        if habit["name"].lower() == habit_name.lower():
            habit["streak"] += 1
            users[name]["xp"] += 10
            print(f"Updated! {habit_name} streak is now {habit['streak']}")
            print(f"You gained 10 XP! Total XP: {users[name]['xp']}")
            return

    new_habit = {"name": habit_name, "streak": 1}
    habits.append(new_habit)
    users[name]["xp"] += 10
    print(f"New habit added: {habit_name} (streak: 1)")
    print(f"You gained 10 XP! Total XP: {users[name]['xp']}")


def show_all_habits(users: dict, name: str):
    if name not in users:
        print(f"User {name} not found")
        return

    habit_list = users[name]["habits"]
    print(f"Habits for {name}:")
    for habit in habit_list:
        print(f"* {habit['name']} (Current streak: {habit['streak']})")


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

    user_name = input("Enter your name: ")

    if user_name in users:
        print("Welcome back!")
        user_guild = users[user_name]["guild"]
    else:
        user_age = int(input("Enter your age: "))
        user_gender = input("Enter your gender: ")
        user_goal = input("What is your main goal? ")

        user_guild = choose_guild()

        add_user(users, user_name, user_age,
                 user_gender, user_goal, user_guild)

    print_profile(users, user_name)

    while True:
        chosen_habit = choose_habit_from_guild(user_guild)

        if chosen_habit is None:
            break

        add_habit(users, user_name, chosen_habit)

    show_all_habits(users, user_name)
    print(f"Final XP: {users[user_name]['xp']}")
    save_data(users)


if __name__ == "__main__":
    main()
