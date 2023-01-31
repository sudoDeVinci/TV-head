# parsing funtions to make argument passing to each script easier.
def parseStringtoInt(integer:str) -> int:
    try:
        out = int(integer)
    except ValueError:
        return False
    return out