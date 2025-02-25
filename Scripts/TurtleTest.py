import serial
import re
import turtle
import math

# Set serial port
ser = serial.Serial('COM10', 115200, 
                    timeout=1, # 1 second timeout
                    # dsrdtr=False,  # Deactivates DTR to avoid reset
                    rtscts=False   # Deactivates RTS to avoid problems with GPIO 0
                    )

# Extract distance values from the structure they come with when printing in serial
pattern = re.compile(r"an(\d):([\d.]+)m")

# Define limits for the Turtle graph
xmin, xmax = -1, 2
ymin, ymax = -1, 2

# Set Turtle plane
screen = turtle.Screen()
screen.setworldcoordinates(xmin, ymin, xmax, ymax)
screen.tracer(0)  # Desactivar actualización automática para mejor rendimiento

# Define anchors' positions
anchors = {
    "an0": (0, 0),  # Anchor 0 
    "an1": (1, 0),  # Anchor 1
    "an2": (0.5, 0.86)  # Anchor 2
}

# Draw anchors in Turtle screen
turtle.speed(0)
turtle.penup()
for key, (x, y) in anchors.items():
    turtle.goto(x, y)
    turtle.dot(10, "red")  # Anchors en rojo
    turtle.write(key, align="center", font=("Arial", 12, "bold"))

# Crear el marcador del tag
tag = turtle.Turtle()
tag.shape("circle")
tag.color("blue")
tag.penup()
tag.goto(0, 0)  # Iniciar en el origen

last_readings = {"an0": None, "an1": None, "an2": None}

def trilateration(d0, d1, d2):
    """Calcula la posición del tag usando trilateración"""
    x0, y0 = anchors["an0"]
    x1, y1 = anchors["an1"]
    x2, y2 = anchors["an2"]

    # Fórmulas de trilateración
    A = 2 * (x1 - x0)
    B = 2 * (y1 - y0)
    C = d0**2 - d1**2 - x0**2 + x1**2 - y0**2 + y1**2

    D = 2 * (x2 - x0)
    E = 2 * (y2 - y0)
    F = d0**2 - d2**2 - x0**2 + x2**2 - y0**2 + y2**2

    # Resolver el sistema de ecuaciones
    denom = A * E - B * D
    if abs(denom) < 1e-6:
        return None  # Evita división por cero si no hay solución

    x = (C * E - F * B) / denom
    y = (A * F - D * C) / denom
    return x, y

distances = {"an0": None, "an1": None, "an2": None}
def actualizar_posicion():
    """Lee datos del serial, calcula la posición y actualiza la pantalla"""
    # global distances

    if ser.in_waiting:
        line = ser.readline().decode().strip()
        match = pattern.findall(line)

        if match:
            anchor_id = f"an{match[0][0]}"
            distance = float(match[0][1])
            distances[anchor_id] = distance
            print("Length_dis: ", len(distances))
            print("dis: ", distances)

            # Cuando tengamos las 3 distancias, procesamos
            if all(distances.values()):
                pos = trilateration(distances["an0"], distances["an1"], distances["an2"])
                if pos:
                    tag.goto(pos)
                    screen.update()  # Refrescar la pantalla

    screen.ontimer(actualizar_posicion, 100)  # Llamar a la función cada 100 ms

# Iniciar la actualización continua
actualizar_posicion()
screen.mainloop()