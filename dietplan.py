def calculate_bmr(weight, height, age, gender):
    """
    Calculate the Basal Metabolic Rate (BMR) using the Mifflin-St Jeor Equation.
    """
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Invalid gender. Please enter 'male' or 'female'.")
    return bmr

def suggest_diet_plan(weight, height, age, gender, diet_type, goal):
    """
    Suggest a diet plan based on the user's body weight, height, age, gender, diet preference, and fitness goal.
    """
    bmr = calculate_bmr(weight, height, age, gender)

    if goal == 'bulking':
        caloric_intake = bmr * 1.2  # 20% surplus for bulking
    elif goal == 'dieting':
        caloric_intake = bmr * 0.8  # 20% deficit for dieting
    else:
        raise ValueError("Invalid goal. Please enter 'bulking' or 'dieting'.")

    if diet_type == 'vegetarian':
        diet_plan = {
            'Breakfast': 'Oatmeal with fruits and nuts',
            'Lunch': 'Quinoa salad with vegetables and chickpeas',
            'Dinner': 'Lentil soup with mixed vegetables',
            'Snacks': 'Greek yogurt with honey and berries'
        }
    elif diet_type == 'non-vegetarian':
        diet_plan = {
            'Breakfast': 'Egg white omelette with spinach and tomatoes',
            'Lunch': 'Grilled chicken breast with steamed vegetables',
            'Dinner': 'Salmon fillet with quinoa and asparagus',
            'Snacks': 'Cottage cheese with pineapple'
        }
    else:
        raise ValueError("Invalid diet type. Please enter 'vegetarian' or 'non-vegetarian'.")

    # Print the diet plan
    print("\nYour Suggested Diet Plan:")
    print(f"Caloric Intake: {caloric_intake:.2f} calories/day")
    for meal, suggestion in diet_plan.items():
        print(f"{meal}: {suggestion}")

def main():
    print("Welcome to the Diet Plan Suggestion Program!")

    # Input data from user
    weight = float(input("Enter your weight in kg: "))
    height = float(input("Enter your height in cm: "))
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (male/female): ").strip().lower()
    diet_type = input("Enter your diet preference (vegetarian/non-vegetarian): ").strip().lower()
    goal = input("Enter your fitness goal (bulking/dieting): ").strip().lower()

    try:
        suggest_diet_plan(weight, height, age, gender, diet_type, goal)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
