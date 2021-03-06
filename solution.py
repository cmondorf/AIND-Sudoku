assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values



def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    unit_dict = {}
    i = 0
    for unit in unitlist:
        twin_list = []
        purge_list = []
        for box in unit:
            if len(values[box]) == 2:
                # how to find if this value repeats in the unit?
                for box_2 in unit:
                    if box == box_2:
                        pass
                    else:
                        if values[box_2] == values[box]:
                            twin_list = [box, box_2]
                            purge_list = [values[box]]
                            unit_dict[i] = [twin_list, purge_list]
        i += 1
    # necessary information extracted
    # now to update board
    i = 0 # reset counter
    for unit in unitlist:
        if i not in unit_dict:
            i += 1
            pass
        else:
            for box in unit:
                if box in unit_dict[i][0]:
                    pass
                else:
                    if len(values[box]) > 1 and (unit_dict[i][1][0] or unit_dict[i][1][1] in values[box]):
                        container = list(values[box])

                        if unit_dict[i][1][0][0] in container:
                            container.remove(unit_dict[i][1][0][0])
                        if unit_dict[i][1][0][1] in container:
                            container.remove(unit_dict[i][1][0][1])
                        assign_value(values, box, ''.join(container))
            i += 1
    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B] # source: courseware lesson 5.4

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [['A1','B2','C3','D4','E5','F6','G7','H8','I9'],['A9','B8','C7','D6','E5','F4','G3','H2', 'I1']]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# currently units is a dictionary with a list of boxes in the units each square belongs to
# add unit for diagonals
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
# make sure peers are updated to include diagonal peers

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """

    # all other fn get values as input, and so presumeably update with the assign fn above.
    #print('grid_values')
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cross(rows, cols)
    sudoku_dict = {}
    i = 0
    for i in range(len(grid)):
        # identify empties and enter string of digits if empty
        if grid[i] == ".":
            sudoku_dict[boxes[i]] = '123456789'
            #values = assign_value(values, boxes[i], '123456789')
        else:
            sudoku_dict[boxes[i]] = grid[i]
            #values = assign_value(values, boxes[i], grid[i])
    return sudoku_dict




def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # print(values) # values here is type None
    pass

def eliminate(values):
    # if a box's peers have a value, then the box can't containt them either
    # flipside of this is that if a box has a value, all peers cannot have that value

    # iterate over all values
    # for key in values:
    #     if len(values[key])==1:
    #     # if box has only one value, move on
    #         pass
    #     else:
    #     # if box has more than one value, look through all peers and eliminate those values
    #         value_list = '123456789'
    #
    #         # there is an error in when the assignment is happening here.
    #
    #         for peer in peers[key]:
    #             if len(values[peer]) == 1:
    #                 if values[peer] in value_list:
    #                     value_list = list(value_list)
    #                     value_list.remove(values[peer])
    #                     value_list = ''.join(value_list)
    #                     assign_value(values, key, value_list)
    # return values

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values




def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values




def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy

        values = eliminate(values)
        values = naked_twins(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #convert string to dictionary
    values = grid_values(grid)


    values = reduce_puzzle(values)
    values = search(values)
    return values




if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
