# Maze Solver

- Report: [`maze-solver.pdf`](./maze-solver.pdf).
- Code: [`maze-solver.py`](./maze-solver.py).

## Features

- Login screen allows users to enter credentials and toggle password visibility.
- Users can register with a unique username and password, triggering a confirmation message upon successful registration.
- Admin console accessible with predefined credentials for managing users, including deletion and bulk deletion.
- Post-login, users access a maze generation menu to create mazes with adjustable dimensions.
- Maze generation includes options for perfect and random mazes, with save and regenerate functionalities.
- "My mazes" menu displays saved mazes with options to delete individual mazes or all saved mazes.
- Maze creation and saved mazes menus feature "quit" buttons for exiting the program.
- Admin panel and saved mazes menu include scrollbars for navigating overflow content.
- Usernames and passwords must adhere to specific length and character criteria, with error messages for invalid inputs.
- Functionality includes regenerating saved mazes to their original state and re-displaying their paths.

## Running locally

1. Clone this repository.
2. Create a virtual python environment by running `python -m venv venv`.
3. Run `source venv/bin/activate`.
4. Install bcrypt via `pip install bcrypt`.
5. Run `python maze-program/index.py`.

Admin credentials

- username: `admin123`.
- password: `admin123`.

## Screenshots

![image](https://github.com/user-attachments/assets/fa7d5df4-fcef-4b8e-bc7b-4329c196c67b)
![image](https://github.com/user-attachments/assets/30386071-5df4-49d3-8636-4466bb9a3431)
![image](https://github.com/user-attachments/assets/ab79efc6-ca63-44d3-a089-89d75225f52e)
