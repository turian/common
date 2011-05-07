
def pids(processname, entireline=True):
    """
    Find the pid(s) of a running process, returned as a list.
    Code from: http://www.echarcha.com/forum/archive/index.php/t-26378.html

    enterline means search the entire 'ps ax' line, not just the command.
    """
    import os
    import signal

    pids = []
    for line in os.popen('ps xa'):
        fields  = line.split()
        pid     = fields[0]
        process = fields[4]

        if entireline: searchstr = line
        else: searchstr = process

#        if searchstr.find(processname) > 0:
        if searchstr.find(processname) >= 0:
#            print line
            pids.append(int(pid))
    return pids

if __name__ == "__main__":
    print pids("firefox")
