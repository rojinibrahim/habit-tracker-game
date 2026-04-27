import json
from datetime import date, timedelta
import sys
faction_habits = {
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


def add_user(users: dict, user_key: str, display_name: str, age: int, gender: str):
    users[user_key] = {
        "name": display_name,
        "age": age,
        "gender": gender,
        "xp": 0,
        "habits": []
    }


def print_profile(users: dict, user_key: str):
    if user_key not in users:
        print(f"User {user_key} not found")
        return

    profile = users[user_key]
    print(f"--- Profile: {profile['name']} ---")
    print(f"Age: {profile['age']}")
    print(f"Gender: {profile['gender']}")
    print(f"XP: {profile['xp']}")
    print(f"Active Habits: {len(profile['habits'])}\n")


def choose_faction():
    print("Choose your faction:")
    print("1. Fitness")
    print("2. Health")
    print("3. Education")
    print("4. Exit")

    while True:
        choice = input("Enter faction number: ")

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


def show_faction_habits(faction: str):
    print(f"Available habits for {faction.capitalize()} Faction:")

    habits = faction_habits[faction]
    for index, habit in enumerate(habits, start=1):
        print(f"{index}. {habit}")


def choose_habit_from_faction(faction: str):
    habits = faction_habits[faction]

    while True:
        show_faction_habits(faction)
        choice = input("Choose a habit number (or type 'exit'): ")

        if choice.lower() == "exit":
            return None

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(habits):
                return habits[choice - 1]

        print(
            f"Please enter a number between 1 and {len(habits)}, or type 'exit'.")


def add_habit(users: dict, user_key: str, habit_name: str, faction: str):
    if user_key not in users:
        print(f"User not found")
        return

    habits = users[user_key]["habits"]
    today = str(date.today())
    last = habit.get("last_completed")
    yesterday = str(date.today() - timedelta(days=1))
    for habit in habits:
        if habit["name"].lower() == habit_name.lower():
            if last == today:
                print(f"You already completed '{habit_name}' today!")
                return
            elif last == yesterday:
                habit["streak"] += 1
                habit["xp"] += 10
                habit["last_completed"] = today
            else:
                habit["streak"] = 1
                print(f"Streak reset! You missed a day. Starting fresh at 1.")
            users[user_key]["xp"] += 10

            level = get_habit_level(habit["faction"], habit["xp"])

            print(f"Updated! {habit_name} streak is now {habit['streak']}")
            print(f"{habit_name} gained 10 XP and is now at level: {level}")
            print(f"You gained 10 XP! Total XP: {users[user_key]['xp']}")
            return

    new_habit = {
        "name": habit_name,
        "faction": faction,
        "streak": 1,
        "xp": 10, "last_completed": str(date.today())
    }

    habits.append(new_habit)
    users[user_key]["xp"] += 10

    level = get_habit_level(new_habit["faction"], new_habit["xp"])

    print(f"New habit added: {habit_name} (streak: 1)")
    print(f"{habit_name} gained 10 XP and starts at level: {level}")
    print(f"You gained 10 XP! Total XP: {users[user_key]['xp']}")


def get_habit_level(faction: str, habit_xp: int):

    level_titles = {
        "fitness": [(120, "Master"), (70, "Warrior"), (30, "Explorer")],
        "health": [(120, "Master"), (70, "Cultivator"), (30, "Guardian")],
        "education": [(120, "Master"), (70, "Scholar"), (30, "Sage")]
    }

    if faction not in level_titles:
        return "Unknown"

    for xp_needed, title in level_titles[faction]:
        if habit_xp >= xp_needed:
            return title

    return "Apprentice"


def show_all_habits(users: dict, user_key: str):
    if user_key not in users:
        print(f"User not found")
        return
    profile = users[user_key]
    habit_list = profile["habits"]
    print(f"Habits for {profile['name']}:")

    for habit in habit_list:
        level = get_habit_level(habit["faction"], habit["xp"])
        print(
            f"* {habit['name']} | Faction: {habit['faction']} | "
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


def greet_returning_user(users: dict, user_key: str):
    print(f"Welcome back, {users[user_key]['name']}!")
    print("Your return brings hope to Aethelgard in our battle against the Lord of Nightmares.")


def ask_age() -> int:
    while True:
        try:
            return int(input("Enter your age: "))
        except ValueError:
            print("Please enter your age in numbers")


def ask_gender() -> str:
    general_gender = ["Female", "Male", "Other"]
    print("Choose your gender: ")
    for index, gender in enumerate(general_gender, start=1):
        print(f"{index}.{gender}")
    while True:
        choice = input("Enter the number: ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(general_gender):
                return general_gender[choice - 1]
            else:
                print("Invalid choice, please try again.")


def register_new_user(users: dict, user_key: str, display_name: str):
    print("Welcome to Aethelgard, young wanderer. My name is Honora, and I am the guide for wanderers like yourself.")
    print(
        f"Hello, {display_name}. As you can see, our world, Aethelgard, lies in ruins.")
    print("The Lord of Nightmares came with his army and invaded our land.")
    print("They destroyed our beautiful home and brought darkness upon us.")
    print(
        f"Now, dear {display_name}, with your help, we can defeat the Lord of Nightmares and bring peace back to our world.")

    approve = input("Will you help us in our mission? (y/n): ").lower()

    if approve == "y":
        print("We are truly grateful to hear that.")
        print("All you must do is choose a habit you wish to bring into your life.")
        print("With each passing day that you remain faithful to it, you strike a blow against the Lord of Nightmares.")
        print("Do not worry—you are not alone on this journey.")
        print("The faction you choose will stand beside you and support you.")
    else:
        print("That is disappointing to hear, but we respect your choice. May your path still be peaceful.")
        sys.exit()

    user_age = ask_age()
    user_gender = ask_gender()
    add_user(users, user_key, display_name, user_age, user_gender)


def habit_selection_loop(users: dict, user_key: str):
    while True:
        print("\nChoose a faction, or type 'exit' to finish.")
        selected_faction = choose_faction()
        if selected_faction is None:
            break
        chosen_habit = choose_habit_from_faction(selected_faction)
        if chosen_habit is None:
            continue
        add_habit(users, user_key, chosen_habit, selected_faction)
        stop = input("Do you want to add another habit? (yes/no): ").lower()
        if stop == "no":
            break


def main():
    users = load_data()
    display_name = input("May I know your name? ").strip()
    user_key = display_name.lower()

    if user_key in users:
        greet_returning_user(users, user_key)
    else:
        register_new_user(users, user_key, display_name)

    print_profile(users, user_key)
    habit_selection_loop(users, user_key)
    show_all_habits(users, user_key)
    print(f"Final XP: {users[user_key]['xp']}")
    save_data(users)


if __name__ == "__main__":
    main()
