from exercises.lip_exercise import LipExercise
from exercises.tongue_exercise import TongueExercise
from exercises.jaw_exercise import JawExercise

def main():
    print("Choose an exercise:")
    print("1. Lip Exercise")
    print("2. Tongue Exercise")
    print("3. Jaw Exercise")
    choice = input("Enter your choice: ")

    if choice == '1':
        LipExercise().run()
    elif choice == '2':
        TongueExercise().run()
    elif choice == '3':
        JawExercise().run()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()