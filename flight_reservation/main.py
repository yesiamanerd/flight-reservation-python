# Add the project root directory to sys.path
import os
import sys
from models.auth import CLIAuthenticator
from controllers.user_controller import UserController
from controllers.flight_controller import FlightController
from controllers.reservation_controller import ReservationController
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Task 2, 5, 9: Import modules here


# Task 2, 6, 10, 18: Redefine the main() function
def main():
    auth = CLIAuthenticator()  # Initialize the command-line interface authenticator
    user_controller = UserController() # Initialize the user controller

    # Let the user log in
    while (user_controller.current_user==None):
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            user_controller.login()   # Attempt to log in
        elif choice == "2":
            if (user_controller.signup()):    # Attempt to sign up;
                if(user_controller.login()):  # if successful, proceed to log in
                    break

        elif choice == "3":
            return
        else:
            print("Invalid choice, try again.")

    # If login is successful, proceed with reservations
    if user_controller.current_user:
        flight_controller = FlightController()
        reservation_controller = ReservationController()

        while True:
            # Display reservation options
            # print("1. Search/Reserve Flights")
            # print("2. View Reservations")
            # print("3. Cancel Reservation")
            # print("4. Add Flight (admin only)")
            # print("5. Cancel Flight (admin only)")
            # print("6. Exit")
            # choice = input("Enter your choice: ")

            # after successful login, you have `user` with user.roles
            options = [
                ("Search/Reserve Flights", reservation_controller.search_flights),
                ("View Reservations", reservation_controller.view_reservations),
                ("Cancel Reservation", reservation_controller.cancel_reservation),
            ]

            print("USER: ", user_controller.current_user)
            # only admins get these
            if "admin" in user_controller.current_user.roles:
                options += [
                    ("Add Flight", flight_controller.add_flight),
                    ("Cancel Flight", flight_controller.delete_flight),
                ]

            options.append(("Exit", lambda *_: exit(0)))

            # display
            for i, (label, _) in enumerate(options, start=1):
                print(f"{i}. {label}")

            # prompt
            choice = input("Enter your choice: ")
            try:
                idx = int(choice) - 1
                _, action = options[idx]
                action(user_controller.current_user)  # or pass whatever args it expects
            except (ValueError, IndexError):
                print("❌ Invalid choice, please try again.")

            # if choice == "1":
            #     reservation_controller.search_flights(user_controller.current_user)
            # elif choice == "2":
            #     reservation_controller.view_reservations(user_controller.current_user)
            # elif choice == "3":
            #     reservation_controller.cancel_reservation(user_controller.current_user)
            # elif choice == "4":
            #     flight_controller.add_flight()
            # elif choice == "5":
            #     flight_controller.cancel_flight(user_controller.current_user)
            # elif choice == "6":
            #     break   # Exit the reservation system
            # else:
            #     print("Invalid choice, try again.")   # Handle invalid input
    return


if __name__ == "__main__":
    main()
