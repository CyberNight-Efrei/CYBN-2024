import ctypes
import re

from anvil import Block, OldBlock

# Do not @ me

SPACES = 3

def print_and_highlight(arr, Z, X):
    for i, row in enumerate(arr):
        for j, el in enumerate(row):
            if i == Z and j == X:
                print(f"\033[1;31;40m{el:0{SPACES}}\033[0m", end=" "*SPACES)
            else:
                el = str(el) if el != 0 else " "*SPACES
                print(f"{el:0{SPACES}}", end=" "*SPACES)
        print()

def make_suitable_for_print(arr):
    res = []
    for Z, row in enumerate(arr):
        r = []
        for X, el in enumerate(row):
            if type(el) == int:
                r.append(el)
            elif isinstance(el, Block) or isinstance(el, OldBlock):
                r.append(el.id)
            else:
                r.append(el.__class__.__name__[:SPACES])

        res.append(r)
    return res

def show(Z, X):
    from parse_blocks import circuit
    print_and_highlight(make_suitable_for_print(circuit), Z, X)

def get_obj(ID):
    # UNSAFE!!!
    return ctypes.cast(ID, ctypes.py_object).value

def show_by_id(ID):
    # VERY UNSAFE!!!
    obj = get_obj(ID)
    show(obj.z, obj.x)

def check(exp: str, exprs):

    m = re.search("[0-9]{13}", exp)
    while m is not None:
        show_by_id(int(m.group()))
        exp = exp.replace(m.group(), check(exprs[int(m.group())], exprs))
        m = re.search("[0-9]{13}", exp)
    return exp


def resolve_references(data):
    unresolved = set(data.keys())
    def settle(d):
        # move only all resolved values to the top
        r = {k: v for k, v in d.items() if re.search(r"[0-9]{13}", v) is None}
        u = {k: v for k, v in d.items() if re.search(r"[0-9]{13}", v) is not None}
        return {**r, **u}


    while len(unresolved) > 0:
        data = settle(data)
        keys, values = list(data.keys()), list(data.values())
        for key, value in zip(keys, values):
            matches = list(re.finditer(r"[0-9]{13}", value))
            for match in matches:
                match = int(match.group(0))
                # is match before current key?
                if (keys.index(match) < keys.index(key) and match not in unresolved) or re.search(r"[0-9]{13}", data[match]) is None:
                    data[key] = data[key].replace(str(match), data[match])
                    # print(data[key].replace(str(match), data[match]))
            if re.search(r"[0-9]{13}", data[key]) is None and key in unresolved:
                unresolved.remove(key)
                break
    return data
