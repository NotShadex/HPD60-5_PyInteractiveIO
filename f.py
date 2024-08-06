def cut(string):
    string.pop(0)
    x = " ".join(string)
    return x


def to_list(arg):
    new = arg[0]+" "+arg[1]
    return new


def check(device):
    if "HPD60-5" in device:
        return "Power Supply"
    elif "GPIB0::5::INSTR" in device:
        return "Power Supply"
    else:
        return "Unknown device"

