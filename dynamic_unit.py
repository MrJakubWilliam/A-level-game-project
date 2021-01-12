# Importing libraries __________________________________________________________________________________________________
from screeninfo import get_monitors
# ______________________________________________________________________________________________________________________

# Working out the value of u____________________________________________________________________________________________

# Finding out the resolution of the primary monitor_____________________________________________________________________

screen_resolution = None
for monitor in get_monitors():
    monitor = str(monitor)
    monitor_details = list(monitor[8:len(monitor)-1])

    counter = 0
    for i in monitor_details:
        if i is "+":
            break
        counter += 1

    monitor_details = ''.join(monitor_details)

    if monitor_details[len(monitor_details)-4:] == "+0+0":
        screen_resolution = monitor_details[:len(monitor_details)-4]

screen_resolution = list(screen_resolution)

counter = 0
for i in screen_resolution:
    if i == "x":
        break
    counter += 1

screen_width = "".join(screen_resolution[:counter])
screen_width = int(screen_width)
# screen_width = 540

# ______________________________________________________________________________________________________________________

u = screen_width/1920

# ______________________________________________________________________________________________________________________
