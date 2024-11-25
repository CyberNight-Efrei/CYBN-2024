from copy import deepcopy

import anvil
from anvil import Block, OldBlock, region

import debug
from symbols import *

"""
Je te préviens, toi qui lis ce script. C'est possiblement le pire code que tu liras de ta vie. Ce script ferait peur
à des dévs Valve qui travaillent sur le vieux Source. Que dis-je, il ferait peur aux dévs GTA V.
En fait ce script, c'est le résultat de 3 semaines de boulot sans structure, sans logique, avec pleins de tentatives,
encore, et encore, et encore... C'est au moins 2 profs mobilisés pour essayer d'expliquer une méthode pour
parser (PARSER!!!) un circuit logique à mettre dans z3 (s/o à l'idée de faire des réseaux neuronaux pour comprendre
le circuit lol).

Ce code c'est une insulte à Alan Turing, à John von Neumann, à Claude Shannon, à George Boole, à Charles Babbage,
à Ada Lovelace, à Grace Hopper, à Dennis Ritchie, à Ken Thompson, à Linus Torvalds, à Richard Stallman,
et peut-être même un peu à ma mère qui j'espère n'aura jamais le déplaisir d'avoir à faire à ce mur de non-sens.
C'est presque aussi abyssal que le format .psd (projet Photoshop), ou que le site random d'une préfecture française.

Franchement on dirait que j'exagère mais vraiment je pense chaque mot que j'écris et y a eu 0% d'IA ou d'alcool
là-dedans. Je me **devais** de faire ce disclaimer. Je sais même pas comment l'agent du FBI qui me surveille a
pu laisser passer ça. En fait ça devrait servir en tant qu'étude de cas pour voir tout ce qu'il ne faut pas faire
non seulement en programmation, mais en résolution de problèmes en général.

Je ferais un parallèle à La Divine Comédie de Dante, notamment au fait que ce script soit comparable à l'Enfer (plus
tu avances, plus tu te rends compte que c'est la merde), mais ce serait évidemment une injure à Dante Alighieri.

Je ferai donc plutôt un parallèle à ce moment dans Mother 3 où toute la team mange des champignons random sur une île et
se retrouve à voir des hallucinations. C'est un peu ça, ce script. C'est un trip. Un trip de 3 semaines.
En parlant de Mother 3, j'pense que même Lucas aurait du mal à comprendre ce script. Et pourtant il comprend les
animaux, cette tête de neuill. Même le mal qui réside en Giygas ou Porky n'arrive pas à la cheville de ce script.

Aux gars, aux filles, respectez vos yeux, partez tant qu'il est encore temps.


















Non...? Bon, je te souhaite bonne chance, et si tu as des questions, n'hésite pas à me contacter. Je suis là pour t'aider...
Maybe.
"""


CIRCUIT_LAYER = 4
CIRCUIT_SIZE = (8, 7)

ELEMENTS = {
    98: "gNAND",
    35: "gNOT",
    99: "gXOR", # bloc MINECRAFT de la porte XOR
    55: "redstone",
    0xFF: "NAND",
    0xFE: "NOT",
    0xFD: "OR",
    0xFC: "XOR",
}

MatElement = Gate | Wire | Entry | OldBlock | Block | int

def print_2d_array(arr):
    for row in arr:
        print(*row, sep="\t")

def mat_of_chunk(ch):
    res = []
    for Z in range(16):
        col = []
        for X in range(16):
            block = ch.get_block(X, CIRCUIT_LAYER, Z)
            col.append(block)
        res.append(col)
    return res

# def fill_circuit():
#     chunks = []
#     for Z in (-2, -1, 0, 1, 2, 3, 4):
#         for X in (-2, -1, 0, 1, 2, 3, 4, 5):
#             try:
#                 ch = region.get_chunk(X, Z)
#             except:
#                 try:
#                     ch = region_1.get_chunk(X, Z)
#                 except:
#                     print(f"FUCK chunk {X},{Z}")
#                     exit(-1)
#             chunks.append(mat_of_chunk(ch))
#
#     # Aggregate the chunks into a single 2D array
#     res = []
#     for Z in range(3):
#         row = chunks[Z * 5], chunks[Z*5 + 1], chunks[Z*5 + 2], chunks[Z*5 + 3], chunks[Z*5 + 4]
#         for i in range(16):
#             res.append(row[0][i] + row[1][i] + row[2][i] + row[3][i] + row[4][i])
#
#     return res


def load_region(region_cache, region_x, region_z):
    """Loads a region file from cache or disk as needed."""
    if (region_x, region_z) not in region_cache:
        try:
            region_file_path = f"test-mca/r.{region_x}.{region_z}.mca"
            region_cache[(region_x, region_z)] = anvil.Region.from_file(region_file_path)
        except FileNotFoundError:
            print(f"Error: Region file {region_file_path} not found.")
            region_cache[(region_x, region_z)] = None
    return region_cache[(region_x, region_z)]

def get_chunk(region, chunk_x, chunk_z):
    """Fetches the specified chunk from a region."""
    try:
        return region.get_chunk(chunk_x, chunk_z)
    except:
        print(f"Error: Chunk ({chunk_x}, {chunk_z}) not found in region.")
        return None

def fill_circuit(start_x, start_z, width, height, y_level):
    """
    Creates a grid representing a slice of the specified area at the given y_level.
    """
    region_cache = {}  # Cache to store loaded regions
    grid = []  # Resulting 2D grid for the slice view at y_level

    from math import floor

    # Traverse the specified area
    for z in range(start_z, start_z + height):
        row = []
        for x in range(start_x, start_x + width):
            # Determine the region and chunk coordinates
            chunk_x, chunk_z = floor(x / 16), floor(z / 16)
            region_x, region_z = floor(chunk_x / 32), floor(chunk_z / 32)

            # Load the region file if not already loaded
            region = load_region(region_cache, region_x, region_z)
            if region is None:
                row.append(None)  # Indicate missing data for this cell
                continue

            # Fetch the chunk
            chunk = get_chunk(region, chunk_x, chunk_z)
            if chunk is None:
                row.append(None)  # Indicate missing data for this cell
                continue

            # Fetch the block at the specified y_level
            try:
                block = chunk.get_block(x % 16, y_level, z % 16)  # Use local coordinates within the chunk
                row.append(block)  # Add the block ID to the row
            except IndexError:
                # If the y_level is out of bounds, add None to indicate missing data
                row.append(None)

        grid.append(row)  # Add the row to the grid

    return grid

def fill_circuit_beta():
    chunk = region.get_chunk(0, 0)
    res = []
    for Z in range(1, 6):
        col = []
        for X in range(1, 9):
            block = chunk.get_block(X, CIRCUIT_LAYER, Z)
            col.append(block)
        res.append(col)
    return res

def place_gates(arr):
    print("Placing gates on:")
    start = deepcopy(arr)
    print_2d_array(debug.make_suitable_for_print(start))

    for Z in range(len(arr)):
        for X in range(len(arr[Z])):
            match arr[Z][X].id:
                case 57:
                    for off_z in range(3):
                        for off_x in range(2):
                            arr[Z + off_z][X + off_x].id = 0

                    arr[Z][X].id = 55
                    arr[Z + 1][X].id = 0xFF # NAND
                    arr[Z + 2][X].id = 55

                    arr[Z + 1][X + 1].id = 55
                case 41:
                    arr[Z][X].id = 0xFE # NOT
                    arr[Z][X + 1].id = 55
                case 133:
                    for off_z in range(3):
                        for off_x in range(5):
                            arr[Z + off_z][X + off_x].id = 0

                    arr[Z][X].id = 55
                    arr[Z + 1][X].id = 0xFC # XOR
                    arr[Z + 1][X + 1].id = 55
                    arr[Z + 1][X + 2].id = 55
                    arr[Z + 1][X + 3].id = 55
                    arr[Z + 1][X + 4].id = 55
                    arr[Z + 2][X].id = 55
                case 0xFC|0xFD|0xFE|0xFF:
                    pass
                case _:
                    if is_junction(arr, Z, X):
                        arr[Z][X].id = 0xFD # OR
    print("\t\t"+"v"*12)
    print_2d_array(debug.make_suitable_for_print(arr))
    return arr

def find_entries(arr):
    entries = []
    for Z in range(len(arr)):
        for X in range(len(arr[Z])):
            if arr[Z][X].id == 69:
                entries.append((Z, X))
    return entries

def get(arr, Z, X) -> MatElement | None:
    if Z < 0 or X < 0: return None
    try:
        return arr[Z][X]
    except IndexError:
        return None


def get_next(Z, X, direction):
    global circuit, visit, debug_counter # :-)
    pass
    if isinstance(get(circuit, Z, X), OR):
        # Keep track of the junctions
        if explorable_neighbors(circuit, Z, X) > 1:
            # todo: append or insert?
            visit.append((Z, X))
            # visit.insert(0, (Z, X))

        # Go forward (not to the right, **forward**) IF there is no Wire (and if there is actual stuff to be visited),
        # else that means we already visited it
        if not isinstance(get(circuit, Z + direction[0], X + direction[1]), Wire) and get(circuit, Z + direction[0], X + direction[1]) != 0:
            if isinstance(get(circuit, Z + direction[0], X + direction[1]), OR):
                if not matching_dir(direction) in get(circuit, Z + direction[0], X + direction[1]).visited:
                    return Z + direction[0], X + direction[1], direction
                direction = (0, 1)
            else:
                return Z + direction[0], X + direction[1], direction
        if direction == (0, 1):
            if not isinstance(get(circuit, Z + 1, X), Wire) and get(circuit, Z + 1, X) != 0:
                # At this point, the tested block is not a Wire, and is not 0. It could be a gate or a 55 (wire block)
                if isinstance(get(circuit, Z + 1, X), OR):
                    if not matching_dir((1, 0)) in get(circuit, Z + 1, X).visited:
                        return Z + 1, X, (1, 0)
                else:
                    return Z + 1, X, (1, 0)

            if not isinstance(get(circuit, Z - 1, X), Wire) and get(circuit, Z - 1, X) != 0:
                if isinstance(get(circuit, Z - 1, X), OR):
                    if not matching_dir((-1, 0)) in get(circuit, Z - 1, X).visited:
                        return Z - 1, X, (-1, 0)
                else:
                    return Z - 1, X, (-1, 0)
            return -1, 0, (0, 1)
            # raise ValueError("No next block found :(")
        else:
            if not isinstance(get(circuit, Z, X + 1), Wire) and get(circuit, Z, X + 1) != 0:
                return Z, X + 1, (0, 1)
            if not isinstance(get(circuit, Z - 1, X), Wire) and get(circuit, Z - 1, X) != 0:
                return Z - 1, X, (-1, 0)
            if not isinstance(get(circuit, Z + 1, X), Wire) and get(circuit, Z + 1, X) != 0:
                return Z + 1, X, (1, 0)

            return -1, 0, (0, 1)

    # Check to the right, then to the direction vector
    if get(circuit, Z, X + 1) != 0:
        return Z, X + 1, (0, 1)
    if get(circuit, Z + direction[0], X + direction[1]) != 0:
        return Z + direction[0], X + direction[1], direction
    if direction == (0, 1):
        if get(circuit, Z + 1, X) is not None and get(circuit, Z + 1, X) != 0:
            return Z + 1, X, (1, 0)
        if get(circuit, Z - 1, X):
            return Z - 1, X, (-1, 0)

    debug.print_and_highlight(debug.make_suitable_for_print(circuit), Z, X)
    raise ValueError("No next block found :(")

def is_gate(element: Gate | Wire | Entry) -> bool:
    return isinstance(element, Gate)
def is_gate_id(ID: int) -> bool:
    return ID >= 0xFA

def is_wire(element: MatElement) -> bool:
    return isinstance(element, Wire)

def is_junction(arr, Z, X) -> bool:
    neighbors = [get(arr, Z + 1, X), get(arr, Z - 1, X), get(arr, Z, X + 1), get(arr, Z, X - 1)]
    return sum(n != 0 and n is not None for n in neighbors) >= 3 and (get(arr, Z, X) == 55 or get(arr, Z, X) == 0xFD) # OR gate
assert is_junction([[0, 55, 0],
                    [55,55,55],
                    [0, 55, 0]], 1, 1) == True
assert is_junction([[0, 55, 0],
                    [55,55, 0],
                    [0, 55, 0]], 1, 1) == True

def explorable_neighbors(arr, Z, X):
    res = [get(arr, Z + 1, X), get(arr, Z - 1, X), get(arr, Z, X + 1)]
    for n in res:
        if isinstance(n, OR):
            if matching_dir((n.z - Z, n.x - X)) in n.visited:
                res.remove(n)
    return len([n for n in res if n != 0 and n is not None and not isinstance(n, Wire)])

def del_column(arr, col):
    for row in range(len(arr)):
        arr[row].pop(col)
    return arr

def make_gate(gate_type: str, expr) -> Gate:
    match gate_type:
        case "NAND":
            return NAND(expr)
        case "NOT":
            return NOT(expr)
        case "OR" | "redstone":
            return OR(expr)
        case "XOR":
            return XOR(expr)
        case _:
            raise ValueError(f"Unknown gate type: {gate_type}")



circuit: list[list[MatElement]] = place_gates(fill_circuit(0, 0, 125, 97, CIRCUIT_LAYER))
circuit = del_column(circuit, 0)
debug_counter = 0
if __name__ == "__main__":

    print("Following inputs, with starting point 69...")

    # a list of elements to be visited
    visit: list[tuple[int, int]] = find_entries(circuit)
    for coord in visit:
        circuit[coord[0]][coord[1]] = Entry(*coord)


    THE_EXIT = Exit()
    z, x = 0, 0
    try:
        while not THE_EXIT.completed:
            prevZ, prevX = 0, 0
            dir_vec = (0, 1)
            curr_expr = None
            # element is either a gate or an entrypoint
            print_2d_array(debug.make_suitable_for_print(circuit))
            print("=====================================")
            while len(visit) > 0:
                last_actions = []
                # sort by x so that we always go to the leftmost element
                visit.sort(key=lambda coordinates: coordinates[1])
                start_coords = visit[0]
                curr_expr = circuit[start_coords[0]][start_coords[1]]
                dir_vec = (0, 1)
                z, x, dir_vec = get_next(*start_coords, dir_vec)
                if z == -1:
                    visit.pop(0)
                    continue
                prevZ, prevX = start_coords
                if isinstance(circuit[prevZ][prevX], OR):
                    circuit[prevZ][prevX].visit_branch(matching_dir((prevZ - z, prevX - x)))
                error = False
                while True and not error:
                    debug_counter += 1
                    pass
                    # print()
                    # print_and_highlight(make_suitable_for_print(circuit), z, x)
                    if is_junction(circuit, z, x): # Junction (=OR gate) found
                        circuit[z][x] = make_gate("OR", curr_expr) # OR doesn't have a specific ID in our matrix
                        circuit[z][x].z = z
                        circuit[z][x].x = x
                        circuit[z][x].add_input(curr_expr, prevZ, prevX)
                        visit.append((z, x))
                        break
                    elif get(circuit, z, x) == 123:
                        THE_EXIT.completed = True
                        THE_EXIT.z = z
                        THE_EXIT.x = x
                        THE_EXIT.expr = curr_expr
                        break
                    elif is_gate(circuit[z][x]): # Existing gate found
                        circuit[z][x].add_input(curr_expr, prevZ, prevX)
                        visit.append((z, x))
                        break
                    elif is_wire(circuit[z][x]): # Existing wire found
                        # TODO
                        # note post cybn: or not :)
                        break
                    elif circuit[z][x].id == 55:
                        circuit[z][x] = Wire(curr_expr)
                        circuit[z][x].z = z
                        circuit[z][x].x = x
                        last_actions.append((z, x, 55))
                    elif is_gate_id(circuit[z][x].id): # New gate found
                        circuit[z][x] = make_gate(ELEMENTS[circuit[z][x].id], curr_expr)
                        circuit[z][x].z = z
                        circuit[z][x].x = x
                        circuit[z][x].add_input(curr_expr, prevZ, prevX)
                        visit.append((z, x))
                        break
                    # Normally unreachable
                    elif isinstance(circuit[z][x], Entry):
                        raise ValueError("Fuck. Entrypoint reached")
                    prevZ, prevX = z, x
                    try:
                        z, x, dir_vec = get_next(z, x, dir_vec)
                    except ValueError:
                        for undo_z, undo_x, set_to in last_actions[::-1]:
                            circuit[undo_z][undo_x] = set_to
                            print(f"Rolled back z={z}, x={x} to {set_to} ({type(set_to)})")
                        visit.append(visit[0])
                        error = True
                        break
                # À CHANGER ICI, ON NE GERE PAS LES OU!!!
                # Really?
                visit.pop(0)

    except Exception as e:
        debug.print_and_highlight(debug.make_suitable_for_print(circuit), z, x)
        print("DAMN DANIEL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(e)

    print("Visit: ", visit)
    print(f"Exited at debug_counter={debug_counter}")

    exprs = {}

    for obj in ALL_OBJECTS:
        exprs[id(obj)] = obj.resolve()
        if isinstance(obj, XOR) and len(obj.inputs) < 2:
            debug.print_and_highlight(debug.make_suitable_for_print(circuit), obj.z, obj.x)
            raise ValueError(f"XOR gate with less than 2 inputs at z={obj.z}, x={obj.x}")

    keys = list(exprs.keys())

    import json
    exprs = debug.resolve_references(exprs)
    final = list(exprs.values())[-1]

    exprs["final"] = final
    with open("exprs.json", "w") as f:
        json.dump(exprs, f, indent=2)
    print("Done :)")