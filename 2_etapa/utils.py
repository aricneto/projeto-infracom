def pretty_print(msg, gutter="|", roof="-", floor="-"):
    msg = gutter + " " + msg + " " + gutter
    print(len(msg) * roof)
    print(msg)
    print(len(msg) * floor)