import turtle


def draw_edge(t, length, depth):
    """
    This function draws one side of the shape.
    Recursion is used because the same pattern needs to repeat
    on smaller and smaller parts of the line.
    """

    # This condition is necessary to stop the recursion,
    # otherwise the function would keep calling itself forever.
    if depth == 0:
        t.forward(length)
        return

    # Dividing the line into three parts helps keep the shape balanced
    # and makes the recursive pattern look even on all sides.
    part = length / 3

    # Draw the first section before making any turns
    draw_edge(t, part, depth - 1)

    # These turns create an inward triangular shape.
    # The angles are chosen so the turtle ends up facing
    # the correct direction again after the indentation.
    t.right(60)
    draw_edge(t, part, depth - 1)

    t.left(120)
    draw_edge(t, part, depth - 1)

    t.right(60)

    # Drawing the final section completes one full edge
    # while keeping the overall direction unchanged.
    draw_edge(t, part, depth - 1)


def draw_polygon(t, sides, length, depth):
    """
    This function draws a regular polygon.
    Each side uses the same recursive edge so the pattern
    stays consistent around the shape.
    """

    # A regular polygon needs equal turns so it closes properly.
    angle = 360 / sides

    for _ in range(sides):
        draw_edge(t, length, depth)
        t.right(angle)


# User Input (with validation) 

# Input validation is added so the program does not crash
# if the user enters something invalid by mistake.

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

# A plain background makes it easier to see the pattern clearly.
screen = turtle.Screen()
screen.bgcolor("white")

t = turtle.Turtle()
t.speed(0)       # Using the fastest speed helps recursion finish quicker
t.hideturtle()   # Hiding the turtle makes the final design look cleaner

# Moving the turtle slightly helps keep the drawing centred on the screen,
# especially when larger shapes or deeper recursion is used.
t.penup()
t.goto(-length / 2, length / 3)
t.pendown()

# Start drawing the polygon with the recursive pattern
draw_polygon(t, sides, length, depth)

turtle.done()


    
