# Imports, tkinter: for GUI, random: for shuffling, PriorityQueue: for A* search, msgbox: for displaying dialog boxes, sqlite3: for databases, bcrypt: for hashing passwords

import random
import sqlite3
import tkinter as tk
import tkinter.messagebox as msgbox
from queue import PriorityQueue

import bcrypt

### Maze class instantiated: Lines 19, 518, 442
### UserAuthentication class instantiated: Lines 38, 275
### MazeApplication class instantiated: Line 574
### Maze generation algorithms (Recursive Backtracker and Prim's): Lines 532, 549
### Pathfinding algorithm: Lines 322-362
### Database creation: Lines 49-68
### Maze generation and rendering: Lines 18-35
### Main execution block: Line 572
# Maze class for maze generation and rendering


class Maze:

    # Initialises maze dimensions and creates a grid with default wall/unvisited cells

    def __init__(self, height, width):

        self.height = height

        self.width = width

        self.maze = [[0] * width for _ in range(height)]

    # Generates maze using Prim's algorithm

    def generate(self):

        self.maze = prims_algorithm(self.height, self.width)

    # Renders maze on canvas, black for walls, white for paths

    def render(self, canvas):

        for i in range(self.height):

            for j in range(self.width):

                color = "black" if self.maze[i][j] == 0 else "white"

                canvas.create_rectangle(
                    j * 10, i * 10, (j + 1) * 10, (i + 1) * 10, fill=color
                )


# User authentication class for login and database management


class UserAuthentication:

    # Sets up GUI elements and database for user authentication

    def __init__(self, root, on_login_success):

        self.root = root

        self.on_login_success = on_login_success

        self.signup_window = None

        self.error_window = None

        self.create_user_database()

        self.create_database()

        self.show_login_form()

    # Creates user table in SQLite database

    @staticmethod
    def create_user_database():

        conn = sqlite3.connect("mazes.db")

        c = conn.cursor()

        c.execute(
            """CREATE TABLE IF NOT EXISTS users

                    (username TEXT PRIMARY KEY, password_hash TEXT)"""
        )

        conn.commit()

        conn.close()

    # Creates mazes table in SQLite database

    @staticmethod
    def create_database():

        conn = sqlite3.connect("mazes.db")

        c = conn.cursor()

        c.execute(
            """CREATE TABLE IF NOT EXISTS mazes

                    (id INTEGER PRIMARY KEY, height INTEGER, width INTEGER,

                    maze_type TEXT, maze_data TEXT, saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
        )

        conn.commit()

        conn.close()

    # Hashes password using bcrypt

    @staticmethod
    def hash_password(password):

        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Clears all widgets from root

    def clear_root(self):

        for widget in self.root.winfo_children():

            widget.destroy()

    # Compares user password with hashed password

    def check_password(self, hashed_password, user_password):

        return bcrypt.checkpw(user_password.encode("utf-8"), hashed_password)

    # Displays login form in root widget

    def show_login_form(self):

        self.clear_root()

        tk.Label(self.root, text="Username").pack()

        self.username_entry = tk.Entry(self.root)

        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()

        self.password_entry = tk.Entry(self.root, show="*")

        self.password_entry.pack()

        self.show_password_button = tk.Button(
            self.root, text="Show Password", command=self.toggle_password_visibility
        )

        self.show_password_button.pack()

        tk.Button(self.root, text="Log In", command=self.login).pack()

        tk.Button(self.root, text="Sign Up", command=self.show_signup_form).pack()

    # Handles user login with admin check, password validation, and database interaction

    def login(self):

        username = self.username_entry.get()

        password = self.password_entry.get()

        if username == "admin123" and password == "admin123":

            self.show_admin_window()

            return

        conn = sqlite3.connect("mazes.db")

        c = conn.cursor()

        c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))

        result = c.fetchone()

        if result and self.check_password(result[0], password):

            self.on_login_success()

        else:

            msgbox.showerror("Login Failed", "Invalid username or password")

        conn.close()

    # Toggles the visibility of the password in the login form

    def toggle_password_visibility(self):

        if self.password_entry.cget("show") == "*":

            self.password_entry.config(show="")

            self.show_password_button.config(text="Hide Password")

        else:

            self.password_entry.config(show="*")

            self.show_password_button.config(text="Show Password")

    # Toggles the visibility of the password in the signup form

    def toggle_signup_password_visibility(self):

        if self.new_password_entry.cget("show") == "*":

            self.new_password_entry.config(show="")

            self.show_signup_password_button.config(text="Hide Password")

        else:

            self.new_password_entry.config(show="*")

            self.show_signup_password_button.config(text="Show Password")

    # Sets up and displays the signup form with username and password fields

    def show_signup_form(self):

        if self.signup_window and self.signup_window.winfo_exists():

            return

        self.signup_window = tk.Toplevel(self.root)

        self.signup_window.title("Sign Up")

        tk.Label(self.signup_window, text="Username").pack()

        self.new_username_entry = tk.Entry(self.signup_window)

        self.new_username_entry.pack()

        tk.Label(self.signup_window, text="Password").pack()

        self.new_password_entry = tk.Entry(self.signup_window, show="*")

        self.new_password_entry.pack()

        self.show_signup_password_button = tk.Button(
            self.signup_window,
            text="Show Password",
            command=self.toggle_signup_password_visibility,
        )

        self.show_signup_password_button.pack()

        tk.Button(self.signup_window, text="Sign Up", command=self.signup).pack()

        self.signup_window.protocol("WM_DELETE_WINDOW", self.on_signup_window_close)

    # Closes the signup window

    def on_signup_window_close(self):

        self.signup_window.destroy()

        self.signup_window = None

    # Manages admin window creation, user display, and admin actions

    def show_admin_window(self):

        if hasattr(self, "admin_window") and self.admin_window.winfo_exists():

            for widget in self.admin_window.winfo_children():

                widget.destroy()

        else:

            self.admin_window = tk.Toplevel(self.root)

            self.admin_window.title("Admin Panel")

        scrollable_frame = tk.Frame(self.admin_window)

        scrollable_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(scrollable_frame)

        scrollbar = tk.Scrollbar(
            scrollable_frame, orient="vertical", command=canvas.yview
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner_frame = tk.Frame(canvas)

        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        conn = sqlite3.connect("mazes.db")

        c = conn.cursor()

        c.execute("SELECT username FROM users WHERE username != 'admin123'")

        users = c.fetchall()

        for user in users:

            username = user[0]

            user_frame = tk.Frame(inner_frame)

            user_label = tk.Label(user_frame, text=username)

            user_label.pack(side=tk.LEFT)

            delete_button = tk.Button(
                user_frame,
                text="Delete",
                command=lambda u=username: self.delete_user(u),
            )

            delete_button.pack(side=tk.LEFT)

            user_frame.pack()

        inner_frame.update_idletasks()

        canvas.config(scrollregion=canvas.bbox("all"))

        tk.Button(
            self.admin_window, text="Delete All Users", command=self.delete_all_users
        ).pack()

        tk.Button(
            self.admin_window, text="Quit", command=self.admin_window.destroy
        ).pack()

    # Deletes all non-admin users after confirmation, updates admin window

    def delete_all_users(self):

        conn = sqlite3.connect("mazes.db")

        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM users WHERE username != 'admin123'")

        count = c.fetchone()[0]

        if count == 0:

            msgbox.showinfo("Delete All Users", "There are no users to delete.")

        else:

            response = msgbox.askyesno(
                "Confirm", "Are you sure you want to delete all users?"
            )

            if response:

                c.execute("DELETE FROM users WHERE username != 'admin123'")

                conn.commit()

        conn.close()

        self.show_admin_window()

    # Deletes a specific user and refreshes admin window

    def delete_user(self, username):

        conn = sqlite3.connect("mazes.db")

        c = conn.cursor()

        c.execute("DELETE FROM users WHERE username = ?", (username,))

        conn.commit()

        conn.close()

        self.show_admin_window()

    # Handles new user registration with username uniqueness and reserved username check

    def signup(self):

        new_username = self.new_username_entry.get()

        new_password = self.new_password_entry.get()

        if not self.validate_credentials(new_username, new_password):

            return

        hashed_password = UserAuthentication.hash_password(new_password)

        if new_username == "admin123":

            msgbox.showerror(
                "Signup Failed", "This username is reserved and cannot be used."
            )

            return

        try:

            conn = sqlite3.connect("mazes.db")

            c = conn.cursor()

            c.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (new_username, hashed_password),
            )

            conn.commit()

            msgbox.showinfo("Signup Successful", "Account created successfully")

            self.signup_window.destroy()

        except sqlite3.IntegrityError:

            msgbox.showerror("Signup Failed", "Username already exists")

        finally:

            conn.close()

    # Validates the input string based on length and allowed characters

    def is_valid_input(self, input_string):

        if not (3 <= len(input_string) <= 16):

            return False

        return all(char.isalnum() or char in "-_" for char in input_string)

    # Shows a custom error dialog with the given message

    def show_error_dialog(self, message):

        if self.error_window and self.error_window.winfo_exists():

            self.error_window.destroy()

        self.error_window = tk.Toplevel(self.root)

        self.error_window.title("Error")

        tk.Label(self.error_window, text=message).pack(padx=10, pady=10)

        tk.Button(self.error_window, text="OK", command=self.error_window.destroy).pack(
            pady=(0, 10)
        )

    # Validates both username and password

    def validate_credentials(self, username, password):

        valid_username = self.is_valid_input(username)

        valid_password = self.is_valid_input(password)

        error_message = "Invalid input:\n"

        if not valid_username or not valid_password:

            if not all(char.isalnum() or char in "-_" for char in username):

                error_message += (
                    "- Username can only contain a-z, A-Z, 0-9, -, and _.\n"
                )

            if not all(char.isalnum() or char in "-_" for char in password):

                error_message += (
                    "- Password can only contain a-z, A-Z, 0-9, -, and _.\n"
                )

            if not (3 <= len(username) <= 16):

                error_message += "- Username must be 3 to 16 characters long.\n"

            if not (3 <= len(password) <= 16):

                error_message += "- Password must be 3 to 16 characters long."

            self.show_error_dialog(error_message)

            return False

        return True


# Manages maze creation, user interactions, pathfinding, and GUI for the maze program


class MazeApplication:

    # Sets up the main application window and user authentication

    def __init__(self, root):

        self.root = root

        self.root.title("Maze Program")

        self.user_auth = UserAuthentication(root, self.on_login_success)

        self.maze_type = "Perfect"

    # Displays main menu upon successful login

    def on_login_success(self):

        self.main_menu()

    # Deletes a specific maze by ID and refreshes maze list

    def delete_maze(self, maze_id):

        conn = sqlite3.connect("mazes.db")

        c = conn.cursor()

        c.execute("DELETE FROM mazes WHERE id = ?", (maze_id,))

        conn.commit()

        conn.close()

        self.my_mazes()

    # Deletes all mazes after user confirmation, updates maze list

    def delete_all_mazes(self):

        conn = sqlite3.connect("mazes.db")

        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM mazes")

        count = c.fetchone()[0]

        if count == 0:

            msgbox.showinfo("Delete All", "There are no mazes to delete.")

        else:

            response = msgbox.askyesno(
                "Confirm", "Are you sure you want to delete all mazes?"
            )

            if response:

                conn = sqlite3.connect("mazes.db")

                c = conn.cursor()

                c.execute("DELETE FROM mazes")

                conn.commit()

                conn.close()

                self.my_mazes()

    # Saves current maze state to the database

    def save_current_maze(self):

        conn = sqlite3.connect("mazes.db")

        c = conn.cursor()

        maze_str = ",".join([" ".join(map(str, row)) for row in self.maze.maze])

        c.execute(
            "INSERT INTO mazes (height, width, maze_type, maze_data) VALUES (?, ?, ?, ?)",
            (self.current_height, self.current_width, self.current_maze_type, maze_str),
        )

        conn.commit()

        conn.close()

        msgbox.showinfo("Success", "Successfully saved the maze")

    # A* search algorithm for pathfinding in maze

    @staticmethod
    def a_star_search(maze, start, end):

        def heuristic(a, b):

            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def get_neighbors(pos):

            neighbors = []

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:

                x, y = pos[0] + dx, pos[1] + dy

                if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 1:

                    neighbors.append((x, y))

            return neighbors

        frontier = PriorityQueue()

        frontier.put((0, start))

        came_from = {}

        cost_so_far = {}

        came_from[start] = None

        cost_so_far[start] = 0

        while not frontier.empty():

            current = frontier.get()[1]

            if current == end:

                break

            for next in get_neighbors(current):

                new_cost = cost_so_far[current] + 1

                if next not in cost_so_far or new_cost < cost_so_far[next]:

                    cost_so_far[next] = new_cost

                    priority = new_cost + heuristic(end, next)

                    frontier.put((priority, next))

                    came_from[next] = current

        current = end

        path = []

        while current != start:

            if current not in came_from:

                return None

            path.append(current)

            current = came_from[current]

        path.append(start)

        path.reverse()

        return path

    # Finds and displays a path in the maze using A* search

    def find_path(self, height, width):

        start = (0, 0)

        end = (height - 1, width - 1)

        path = MazeApplication.a_star_search(self.maze.maze, start, end)

        if path is not None:

            self.show_path(path)

        else:

            print("No path found!")

    # Visually represents a found path on the maze

    def show_path(self, path):

        if path:

            for x, y in path:

                self.canvas.create_rectangle(
                    y * 10, x * 10, (y + 1) * 10, (x + 1) * 10, fill="blue"
                )

            self.canvas.update()

        else:

            print("No path to show.")

    # Updates the maze type (Perfect/Non-Perfect)

    def update_maze_type(self, maze_type):

        self.maze_type = maze_type

    # Sets application window size based on maze dimensions

    def set_window_size(self, width, height):

        canvas_width = width * 10

        canvas_height = height * 10

        self.root.geometry(f"{canvas_width}x{canvas_height + 50}")

    # Clears all widgets from the root window

    def clear_root(self):

        for widget in self.root.winfo_children():

            widget.destroy()

    # Displays the main menu with options for maze creation and viewing

    def main_menu(self):

        self.clear_root()

        self.root.geometry("300x200")

        tk.Button(self.root, text="Make Maze", command=self.make_maze_menu).pack()

        tk.Button(self.root, text="My Mazes", command=self.my_mazes).pack()

        self.add_quit_button()

    # Randomizes maze dimensions and generates the maze

    def randomize_and_generate(self):

        self.height_slider.set(random.randint(15, 76))

        self.width_slider.set(random.randint(15, 76))

        self.generate_maze(
            self.height_slider.get(), self.width_slider.get(), self.maze_type
        )

    # Displays the maze generation menu with dimension controls and maze type selection

    def make_maze_menu(self):

        self.clear_root()

        self.root.geometry("300x400")

        tk.Label(self.root, text="Maze Height:").pack()

        self.height_slider = tk.Scale(
            self.root, from_=15, to=75, orient="horizontal", label="15 to 75 cells"
        )

        self.height_slider.pack()

        tk.Label(self.root, text="Maze Width:").pack()

        self.width_slider = tk.Scale(
            self.root, from_=15, to=75, orient="horizontal", label="15 to 75 cells"
        )

        self.width_slider.pack()

        maze_type = tk.StringVar(self.root)

        maze_type.set(self.maze_type)

        tk.OptionMenu(
            self.root,
            maze_type,
            "Perfect",
            "Non-Perfect",
            command=self.update_maze_type,
        ).pack()

        tk.Button(
            self.root, text="Randomize", command=self.randomize_and_generate
        ).pack()

        tk.Button(
            self.root,
            text="Generate Maze",
            command=lambda: self.generate_maze(
                int(self.height_slider.get()),
                int(self.width_slider.get()),
                maze_type.get(),
            ),
        ).pack()

        self.add_go_back_button()

        self.add_quit_button()

    # Updates window size based on the maze dimensions

    def update_size(self, event=None):

        self.set_window_size(
            int(self.width_slider.get()), int(self.height_slider.get())
        )

    # Regenerates and displays a saved maze from the database

    def regenerate_saved_maze(self, maze_id):

        conn = sqlite3.connect("mazes.db")

        c = conn.cursor()

        c.execute("SELECT height, width, maze_data FROM mazes WHERE id = ?", (maze_id,))

        height, width, maze_str = c.fetchone()

        conn.close()

        maze_array = [list(map(int, row.split())) for row in maze_str.split(",")]

        self.maze = Maze(height, width)

        self.maze.maze = maze_array

        self.display_maze(height, width)

    # Displays saved mazes with options for regeneration and deletion

    def my_mazes(self):

        self.clear_root()

        self.add_go_back_button()

        self.add_quit_button()

        tk.Button(self.root, text="Delete All", command=self.delete_all_mazes).pack()

        conn = sqlite3.connect("mazes.db")

        c = conn.cursor()

        c.execute("SELECT id, height, width, saved_at FROM mazes")

        saved_mazes = c.fetchall()

        conn.close()

        scrollable_frame = tk.Frame(self.root)

        scrollable_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(scrollable_frame)

        scrollbar = tk.Scrollbar(
            scrollable_frame, orient="vertical", command=canvas.yview
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner_frame = tk.Frame(canvas)

        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        for maze in saved_mazes:

            maze_id, height, width, saved_at = maze

            maze_frame = tk.Frame(inner_frame)

            tk.Label(
                maze_frame,
                text=f"Maze ID: {maze_id}, Size: {height}x{width}, Saved: {saved_at}",
            ).pack(side=tk.LEFT)

            tk.Button(
                maze_frame,
                text="Generate",
                command=lambda m_id=maze_id: self.regenerate_saved_maze(m_id),
            ).pack(side=tk.LEFT)

            tk.Button(
                maze_frame,
                text="Delete",
                command=lambda m_id=maze_id: self.delete_maze(m_id),
            ).pack(side=tk.LEFT)

            maze_frame.pack()

        inner_frame.update_idletasks()

        canvas.config(scrollregion=canvas.bbox("all"))

    # Returns to the main menu

    def go_back(self):

        self.main_menu()

    # Adds a 'Go Back' button specific to the maze generation interface

    def add_go_back_button_generate_maze(self, button_frame):

        tk.Button(button_frame, text="Go Back", command=self.make_maze_menu).pack(
            side=tk.BOTTOM
        )

    # Quits the application

    def quit_app(self):

        self.root.quit()

    # Adds a 'Go Back' button

    def add_go_back_button(self):

        tk.Button(self.root, text="Go Back", command=self.go_back).pack()

    # Adds a 'Quit' button

    def add_quit_button(self):

        tk.Button(self.root, text="Quit", command=self.quit_app).pack()

    # Displays the maze with interaction options

    def display_maze(self, height, width):

        self.clear_root()

        canvas_width, canvas_height = width * 10, height * 10

        canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height)

        self.canvas = canvas

        canvas.pack(side=tk.TOP)

        self.maze.render(canvas)

        button_frame = tk.Frame(self.root)

        button_frame.pack(after=canvas)

        tk.Button(button_frame, text="Save", command=self.save_current_maze).pack(
            side=tk.LEFT
        )

        tk.Button(button_frame, text="Quit", command=self.quit_app).pack(side=tk.LEFT)

        tk.Button(
            button_frame,
            text="Regenerate Maze",
            command=lambda: self.generate_maze(
                self.current_height, self.current_width, self.current_maze_type
            ),
        ).pack(side=tk.LEFT)

        tk.Button(
            button_frame,
            text="Find Path",
            command=lambda: self.find_path(height, width),
        ).pack(side=tk.LEFT)

        self.add_go_back_button_generate_maze(button_frame)

    # Generates a new maze based on dimensions and type

    def generate_maze(self, height, width, maze_type):

        self.current_height, self.current_width, self.current_maze_type = (
            height,
            width,
            maze_type,
        )

        valid_maze, maze_generation_attempts = False, 0

        while not valid_maze and maze_generation_attempts < 250:

            maze_generation_attempts += 1

            self.maze = Maze(height, width)

            self.maze.maze = (
                recursive_backtracker(height, width)
                if maze_type == "Perfect"
                else prims_algorithm(height, width)
            )

            if self.a_star_search(self.maze.maze, (0, 0), (height - 1, width - 1)):

                valid_maze = True

            else:

                print(
                    f"Maze generation attempt {maze_generation_attempts} failed. No path found."
                )

        if valid_maze:

            self.display_maze(height, width)

        else:

            msgbox.showwarning(
                "Maze Generation Failed",
                "Unable to generate a solvable maze. Please try different dimensions or regenerate.",
            )

            print("Could not generate a valid maze. Please try again.")

            self.make_maze_menu()


# Recursive backtracker algorithm for maze generation


def recursive_backtracker(height, width):

    def carve_passage_from(cx, cy, grid):

        directions = [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]

        random.shuffle(directions)

        for nx, ny in directions:

            if 0 <= nx < height and 0 <= ny < width and grid[nx][ny] == 0:

                if (
                    0 <= nx + (nx - cx) < height
                    and 0 <= ny + (ny - cy) < width
                    and grid[nx + (nx - cx)][ny + (ny - cy)] == 0
                ):

                    grid[nx][ny] = 1

                    grid[nx + (nx - cx)][ny + (ny - cy)] = 1

                    carve_passage_from(nx + (nx - cx), ny + (ny - cy), grid)

    maze = [[0] * width for _ in range(height)]

    start_x, start_y = random.randint(0, height - 1), random.randint(0, width - 1)

    maze[start_x][start_y] = 1

    carve_passage_from(start_x, start_y, maze)

    return maze


# Prim's algorithm for maze generation


def prims_algorithm(height, width):

    local_maze = [[0] * width for _ in range(height)]

    visited = set()

    walls = set()

    start = (0, 0)

    visited.add(start)

    local_maze[start[0]][start[1]] = 1

    walls.update({(0, 1), (1, 0)})

    while walls:

        wall = random.choice(list(walls))

        x, y = wall

        neighbors = [
            (nx, ny)
            for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            if (nx, ny) in visited
        ]

        if len(neighbors) == 1:

            nx, ny = neighbors[0]

            local_maze[x][y] = 1

            visited.add((x, y))

            for dx, dy in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:

                if 0 <= dx < height and 0 <= dy < width and (dx, dy) not in visited:

                    walls.add((dx, dy))

        walls.remove(wall)

    return local_maze


# Main execution block

if __name__ == "__main__":

    root = tk.Tk()

    app = MazeApplication(root)

    root.mainloop()
