from tvlib._config import *

"""
Getting variable sized led screens for testing on https://wokwi.com
Generating Json file for LED screen, resolution from upload/res.txt
"""


def get_res() -> Tuple[int, int]:
    """
    Get the resolution of the display from the config file.
    """
    res = []
    with open('upload/res.txt', 'r', encoding = 'utf-8') as r:
        res = [int(line.rstrip('\n')) for line in r]
    return tuple(res)


def get_json(width: int, height: int) -> str:
    """
    Build the json required to display example config for LEDS on Wokwi.
    """
    init_top = 115
    init_left = -90

    type = "\"type\": \"wokwi-neopixel\""
    attrs = ", \"attrs\": {}"

    number = 0
    display = []
    max = width*height
    display_connections = []
    for row in range(height):
        for col in range(width):
            led_string = "{ " + type + ", \"id\": \"rgb" + str(number+1) + "\", \"top\": " + str(init_top+(row*30)) + ", \"left\": " + str(init_left+(col*30))+ attrs +" }"
            display.append(led_string)
            if number != max+1:
                led_voltage_string = "[ \"rgb" + str(number+1) + ":VDD\", \"rgb" + str(number+2) + ":VSS\", \"green\", [ \"h0\" ] ]"
                led_data_string = "[ \"rgb" + str(number+1) + ":DOUT\", \"rgb" + str(number+2) + ":DIN\", \"green\", [ \"h0\" ] ]"
                display_connections.append(led_voltage_string)
                display_connections.append(led_data_string)
            number+=1


    headerstring = """{
    \"version\": 1,
    \"author\": \"Anonymous maker\",
    \"editor\": \"wokwi\",
    \"parts\": [
        {
        \"type\": \"wokwi-esp32-devkit-v1\",
        \"id\": \"esp\",
        \"top\": -49.99,
        \"left\": -500.07,
        \"attrs\": { \"env\": \"micropython-20220618-v1.19.1\" }
        },\n""" + str(",\n".join(display)) + "\n],\n"

    connections = """\"connections\": [\n
    [ \"esp:TX0\", \"$serialMonitor:RX\", \"\", [] ],
    [ \"esp:RX0\", \"$serialMonitor:TX\", \"\", [] ],
    [ \"esp:3V3\", \"rgb1:VSS\", \"green\", [ \"v0\" ] ],
    [ \"esp:D13\", \"rgb1:DIN\", \"green\", [ \"h0\" ] ],
    """ + str(",\n".join(display_connections)) + "\n],\n"

    dependencies = """\"dependencies\": {} \n}"""
    return f"{headerstring}{connections}{dependencies}"

def save(savepath: str = "diagram.json", data = "{}") -> None:
    write_json(savepath, data)
