def runcmd(args, input=None, acceptable_return_codes=[0]):
    """
    Split args into a list, run this command, and return its output.
    Raise RuntimeError if the command does not return 0.
    @note: This function will not work if args contains pipes |
    @param input: If this exists, it will be fed as stdin
    """
    import subprocess
#    print args
    import string
    if input == None: stdin = None
    else: stdin = subprocess.PIPE
    proc = subprocess.Popen(string.split(args), stdout=subprocess.PIPE, stdin=stdin)
#    proc = subprocess.Popen(string.split(args), stdout=subprocess.PIPE)
    output = proc.communicate(input=input)[0]
    if proc.returncode not in acceptable_return_codes:
        import exceptions
        raise exceptions.RuntimeError("Return code = %d (not in acceptable_return_codes=%s)" % (proc.returncode, acceptable_return_codes))
    return output

def homedir():
    import os
    return os.environ["HOME"]
def utilsdir():
    import os
    return os.environ["UTILS"]

def sign(i, assertions=True):
    """
    + or - 1
    @precondition: i != 0
    """
    if assertions:
        assert i != 0
    else:
        if i == 0: return 0

    return +1 if i > 0 else -1

def unique_elements_list_intersection(list1,list2):
    """
    Return the unique elements that are in both list1 and list2
    (repeated elements in listi will not be duplicated in the result).
    This should run in O(n1+n2) where n1=|list1|, n2=|list2|.
    """
    return list(set.intersection(set(list1),set(list2)))
