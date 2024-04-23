from ncbi_qa import fetch_data, extract_question

def display_theme_selection(themes):
    """Display the theme selection menu."""
    print("Select a theme by entering the number:")
    for i, theme in enumerate(themes, start=1):
        print(f"{i}. {theme}")
    theme_choice = int(input("Enter your choice: ")) - 1
    return theme_choice

def get_user_choice():
    """Get the user's choice for next action."""
    print("\nWhat would you like to do next?")
    print("1. Get another question on the same theme")
    print("2. Change theme")
    print("3. Quit")
    return input("Enter your choice (1, 2, or 3): ")

def main(api_key):
    themes = [
        "COVID-19",
        "diabetes",
        "heart disease",
        "cancer",
        "Alzheimer's disease",
        "vaccination",
        "genetics",
        "nutrition",
        "mental health",
        "exercise"
    ]
    while True:
        theme_choice = display_theme_selection(themes)
        if theme_choice < 0 or theme_choice >= len(themes):
            print("Invalid choice. Exiting.")
            return

        theme = themes[theme_choice]
        while True:
            data = fetch_data(theme, api_key)
            question, correct_answer = extract_question(data, api_key)
            if not correct_answer:
                print(question)
                continue

            print("\nQuestion: ", question)
            user_answer = input("Your answer: ")
            print("Correct answer: ", correct_answer)
            print("Your answer was: " + ("correct" if user_answer.lower() == correct_answer.lower() else "incorrect"))

            user_choice = get_user_choice()
            if user_choice == '1':
                continue
            elif user_choice == '2':
                break
            elif user_choice == '3':
                print("Thank you for using the application. Goodbye!")
                return


if __name__ == "__main__":
    api_key = "755d036499c17656e4f731fdc4b1749e7c08"  # Replace with your actual API key
    main(api_key)