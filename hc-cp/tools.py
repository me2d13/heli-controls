
def range_map(x, in_min, in_max, out_min, out_max):
    #return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    val = (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    if val > out_max:
        return out_max
    return val
