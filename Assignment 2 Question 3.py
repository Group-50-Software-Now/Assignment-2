import turtle

"""
This program uses Python Turtle graphics to draw a polygon.
Each side of the polygon is drawn using a recursive pattern,
which creates an inward triangular design.

The user can control:
- Number of sides
- Length of each side
- Depth of recursion
"""


def draw_edge(t, length, depth):
    """
    Draws one side (edge) of the shape using recursion.

    Parameters:
    t      : turtle object used for drawing
    length : length of the current edge
    depth  : recursion depth (controls how detailed the pattern is)

    Why recursion is used:
    The same drawing pattern needs to repeat on smaller and smaller
    parts of the line. Recursion makes this easier and cleaner
    than using loops.
    """

    # Base case:
    # If depth becomes 0, we stop calling the function again.
    # This is very important, otherwise the program would run forever.
    if depth == 0:
        t.forward(length)
        return
 
    # The line is divided into three equal parts.
    # This keeps the shape balanced and visually consistent.
    part = length / 3

    # Draw the first straight section
    draw_edge(t, part, depth - 1)

    # Turn right to start creating the inward triangle
    t.right(60)
    draw_edge(t, part, depth - 1)

    # Turn left more sharply to form the peak of the triangle
    t.left(120)
    draw_edge(t, part, depth - 1)

    # Turn back to restore the original direction
    t.right(60)

    # Draw the final section to complete one full edge
    draw_edge(t, part, depth - 1)


def draw_polygon(t, sides, length, depth):
    """
    Draws a regular polygon using the recursive edge function.

    Parameters:
    t      : turtle object
    sides  : number of sides of the polygon
    length : length of each side
    depth  : recursion depth for each edge

    Why this function exists:
    It separates the idea of "drawing an edge" from
    "drawing the full polygon", which makes the code
    easier to understand and reuse.
    """

    # A regular polygon needs equal angles so it closes properly
    angle = 360 / sides

    # Draw each side and rotate the turtle after each edge
    for _ in range(sides):
        draw_edge(t, length, depth)
        t.right(angle)


# User Input (with validation) 

"""
Input validation is used so the program does not crash
if the user types something invalid.

Using while True allows the program to keep asking
until correct input is provided.
"""

while True:
    try:
        sides = int(input("Enter the number of sides (3 or more): "))
        if sides < 3:
            print("A polygon needs at least 3 sides.")
            continue
        break
    except ValueError:
        print("Please enter a whole number.")

while True:
    try:
        length = float(input("Enter the side length (positive number): "))
        if length <= 0:
            print("The length must be greater than zero.")
            continue
        break
    except ValueError:
        print("Please enter a valid number.")

while True:
    try:
        depth = int(input("Enter the recursion depth (0 or more): "))
        if depth < 0:
            print("Depth cannot be negative.")
            continue
        break
    except ValueError:
        print("Please enter a whole number.")


# Turtle Setup 

"""
This section prepares the Turtle drawing environment.
Keeping setup code separate makes the program easier
to read and modify later.
"""

# Create the drawing window
screen = turtle.Screen()
screen.bgcolor("white")  # Plain background makes the pattern clearer

# Create the turtle
t = turtle.Turtle()
t.speed(0)       # Fastest speed so recursion finishes quicker
t.hideturtle()   # Hide the turtle so only the drawing is visible

# Move turtle slightly so the drawing stays centred on screen
t.penup()
t.goto(-length / 2, length / 3)
t.pendown()

# Start drawing the polygon using the recursive pattern
draw_polygon(t, sides, length, depth)

# Keep the window open until the user closes it
turtle.done()

