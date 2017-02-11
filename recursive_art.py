"""
ComputationalArt by Seungin Lyu
Creates artistic image with randomized functions created by recursion!

"""

import doctest
import random
import math
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context).
        The function computes depth between min_depth and max_depth.
        Random function at (depth > 1) chosen from building_blocks list.
        Random function at (depth == 1) chosen from base list.
        -----------------------------------------------------------
        Definition of each function in building_blocks (depth > 1):
        1) avg(a, b) = 0.5 * (a + b), requires two children a,b
        2) prod(a, b) = a * b, requires two children a,b
        3) cos_pi = cos(pi * a), requires single child a
        4) sin_pi = sin(pi * a), requires single child a
        5) cos_pi_squared = cos(pi**2 * a), requires single child a
        6) sin_pi_squared = sin(pi**2 * a), requires single child a
        -----------------------------------------------------------
        Definition of base case (depth = 1)
        1) x(a,b) = x, has no children
        2) y(a,b) = y, has no children

        It chooses one function from the building_blocks list from
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    building_blocks = ["avg", "prod", "cos_pi", "sin_pi",
                       "cos_pi_squared", "sin_pi_squared"]  # 2 addtional func.
    ran_range = len(building_blocks) - 1
    # computes a new random depth min_depth <= depth <= max_depth
    depth = random.randint(min_depth, max_depth)
    random_function = []
    if(depth == 1):
        base = ["x", "y"]  # depth 1 can either have x or y.
        random_function.append(base[random.randint(0, len(base)-1)])
        return random_function  # returns either ['x'] or ['y']
    else:
        # compute the random function at current depth
        random_function.append(building_blocks[random.randint(0, ran_range)])
        # check if the computed random function requires two children
        if(random_function[-1] in ["avg", "prod"]):
            child_1 = build_random_function(depth-1, depth-1)
            child_2 = build_random_function(depth-1, depth-1)
            # append both child_1 and child_2 to random_function
            random_function.append(child_1)
            random_function.append(child_2)
        else:
            child = build_random_function(depth-1, depth-1)
            random_function.append(child)
    return random_function


def evaluate_random_function(f, x, y):
    """ Evaluate the random nested function f with inputs x,y using recursion
        Representation of the function f :
        -----------------------------------
        1) avg(a, b) = 0.5 * (a + b)
        2) prod(a, b) = a * b
        3) cos_pi = cos(pi * a)
        4) sin_pi = sin(pi * a)
        5) cos_pi_squared = cos(pi**2 * a)
        6) sin_pi_squared = sin(pi**2 * a)
        7) x(a,b) = x
        8) y(a,b) = y
        -----------------------------------
        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"], -0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"], 0.1, 0.02)
        0.02
        >>> evaluate_random_function(['cos_pi', ['sin_pi', ['y']]], 0, 0)
        1.0
        >>> evaluate_random_function(["prod",["sin_pi",["x"]],["cos_pi",["x"]]],0 , 0)
        0.0
    """
    if f == ['x']:
        return x
    elif f == ['y']:
        return y
    elif f == ['avg']:
        return 0.5 * (x + y)
    elif f == ['prod']:
        return x * y
    elif f == ['cos_pi']:
        return math.cos(math.pi * x)
    elif f == ['sin_pi']:
        return math.sin(math.pi * x)
    elif f == ['cos_pi_squared']:
        return math.cos(math.pi**2 * x)
    elif f == ['sin_pi_squared']:
        return math.sin(math.pi**2 * x)
    else:
        requires_two_children = ['avg', 'prod']
        if([f[0]]) in requires_two_children:
            new_x = evaluate_random_function(f[1], x, y)
            new_y = evaluate_random_function(f[2], x, y)
            return evaluate_random_function([f[0]], new_x, new_y)
        else:
            new_x = evaluate_random_function(f[1], x, y)
            return evaluate_random_function([f[0]], new_x, y)


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
        >>> remap_interval(0, 0, 255, -1, 1)
        -1.0
        >>> remap_interval(255, 0, 255, -1, 1)
        1.0
    """
    input_range = input_interval_start - input_interval_end
    output_range = output_interval_start - output_interval_end
    scalar = (output_range / input_range)
    new_val = output_interval_start + scalar * (val - input_interval_start)
    return new_val


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """

    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel
    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    doctest.testmod()
    # Create some computational art!
    generate_art("myart.png")
