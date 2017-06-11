# ######################
# Some useful utilities.
# ######################


import json, os, pickle

def listPrettyPrint(l, n):
    """Prints a list l on n columns to improve readability"""
    if(n == 5):
        for a,b,c,d,e in zip(l[::5],l[1::5],l[2::5],l[3::5],l[4::5]):
            print('{:<22}{:<22}{:<22}{:<22}{:<}'.format(a,b,c,d,e))
    if(n == 4):
        for a,b,c,d in zip(l[::4],l[1::4],l[2::4],l[3::4]):
            print('{:<30}{:<30}{:<30}{:<}'.format(a,b,c,d))
    if(n == 3):
        for a,b,c in zip(l[::3],l[1::3],l[2::3]):
            print('{:<30}{:<30}{:<}'.format(a,b,c))
    if(n == 2):
        for a,b in zip(l[::2],l[1::2]):
            print('{:<40}{:<}'.format(a,b))
    if(len(l)%n != 0): #print remaining
        for i in range(len(l)%n):
            print(l[-(len(l)%n):][i], end='\t')

def save_json(objects, path):
    """
    Save a list of objects as JSON (.txt).
    """

    # Remove the file if it exists
    if os.path.exists(path):
        os.remove(path)
    for obj in objects:
        # 'a' stands for 'append' to the end of the file
        # '+' to create the file if it doesn't exist
        with open(path, 'a+') as f:
            f.write(json.dumps(obj))
            f.write('\n')


def load_json(path):
    """
    Read a JSON from a text file. Expect a list of objects.
    """

    with open(path) as f:
        lines = f.readlines()
    return [json.loads(s) for s in lines]


def save_pkl(obj, path):
    """
    Save an object to path.
    """
    with open(path, 'wb') as f:
        pickle.dump(obj, f)


def load_pkl(path):
    """
    Load a pickle from path.
    """
    with open(path, 'rb') as f:
        return pickle.load(f)
