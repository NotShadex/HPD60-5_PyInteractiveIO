import pyvisa
import argparse
import f


rm = pyvisa.ResourceManager()
a_gpibs = rm.list_resources()
print("Devices found:", a_gpibs)
inst = [None] * len(a_gpibs)
for i, gpib in enumerate(a_gpibs):
    dev = f.check(gpib)
    if dev == "Power Supply":
        inst = rm.open_resource(gpib)
    else:
        inst = rm.open_resource(gpib)

parser = argparse.ArgumentParser()
switch = False
# Change this string if you want to test it for your instrument (will probably not work since HPD60-5 uses some really weird commands gl I guess)
if dev == "Power Supply":
    inst.write("ISET 5")
    parser.add_argument("-info", help="provides info about the instrument", action="store_true")
    parser.add_argument("-vset", help="sets voltage in volts", type=float)
    parser.add_argument("-iset", help="sets current in amps", type=float)
    parser.add_argument("-q", help="use advanced query/status commands", type=str)
    parser.add_argument("-p", help="use programming/calibration commands", type=str, nargs=2)
    switch = True
else:
    print(f'This program was made specifically for HPD 60-5 and might not work for your instrument')
    print(f'If you want to change it please look at the code itself')
args = parser.parse_args()

if switch:

    if args.info:
        print("====================================================================================")
        print("Name:", f.cut(inst.query("ID?").split()))
        print("Voltage:", f.cut(inst.query("VSET?").split()))
        print("Current:", f.cut(inst.query("ISET?").split()))
        print("Soft Voltage Limit:", f.cut(inst.query("VMAX?").split()))
        print("Soft Current Limit:", f.cut(inst.query("IMAX?").split()))
        print("Foldback Protection:", f.cut(inst.query("FOLD?").split()))
        print("Output:", f.cut(inst.query("OUT?").split()))
        print("Hold:", f.cut(inst.query("HOLD?").split(" ")), end="")
        print("Unmask:", f.cut(inst.query("UNMASK?").split(" ")), end="")
        print("Service Request Capability:", f.cut(inst.query("SRQ?").split()))
        print("AUXA:", f.cut(inst.query("AUXA?").split()))
        print("AUXB:", f.cut(inst.query("AUXB?").split()))
        print("OVP Trip Voltage:", f.cut(inst.query("OVSET?").split()))
        print("Delay:", f.cut(inst.query("DLY?").split()))
        print("Local Mode:", f.cut(inst.query("LOC?").split()))
        print("====================================================================================", end="")

    elif args.vset:

        inst.write(f'VSET {args.vset}')
        print("Voltage set to:", f.cut(inst.query("VSET?").split()), end="")

    elif args.iset:

        inst.write(f'ISET {args.iset}')
        print("Current set to:", f.cut(inst.query("ISET?").split()))

    elif args.q:

        print(inst.query(args.q))

    elif args.p:

        tmp = f.to_list(args.p)
        print(inst.query(tmp))
