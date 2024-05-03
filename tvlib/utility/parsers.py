# parsing funtions to make argument passing to each script easier.
def parseStringtoInt(integer: str) -> int|bool:
    try:
        out = int(integer)
        return out
    except ValueError:
        return False

def getIntInput(prompt: str) -> int:
    while True:
        try:
            out = input(f">> {prompt}: ")
            out = int(out)
            if out < 0:
                print(f"\nPlease provide a positive integer.\n")
                continue
            return out
        except ValueError as e:
            print(f"\n{out} is not as integer.\n")