<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Juego de Cálculo Divertido</title>
    <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
    <script defer src="https://pyscript.net/latest/pyscript.js"></script>
    <style>
        body {
            background-color: lightblue;
            font-family: "Comic Sans MS", cursive, sans-serif;
            text-align: center;
            padding: 20px;
        }
        #game-container {
            max-width: 600px;
            margin: auto;
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }
        #problem {
            font-size: 2em;
            margin: 20px;
        }
        #score, #timer {
            font-size: 1.5em;
            margin: 10px;
        }
        #answer {
            font-size: 1.5em;
            padding: 5px;
            width: 100px;
            text-align: center;
        }
        #verify-button {
            font-size: 1.5em;
            padding: 5px 10px;
            background-color: yellow;
            border: none;
            cursor: pointer;
        }
        #instructions {
            font-size: 1.2em;
            margin-bottom: 20px;
        }
        #message {
            font-size: 1.5em;
            margin-top: 20px;
            color: red;
        }
    </style>
</head>
<body>
    <div id="game-container">
        <div id="instructions">
            ¡Bienvenido! Resuelve las operaciones lo más rápido que puedas.
        </div>
        <div id="problem">Cargando...</div>
        <input type="number" id="answer" placeholder="Respuesta" />
        <br><br>
        <button id="verify-button">Verificar</button>
        <div id="score">Aciertos: 0</div>
        <div id="timer">Tiempo restante: 30.0 s</div>
        <div id="message"></div>
    </div>

    <py-script>
import random
from js import document, setTimeout

# Variables globales
score = 0
time_remaining = 30.0  # Tiempo inicial en segundos
dt = 0.1               # Intervalo de actualización en segundos
speed_factor = 0.05    # Factor de aceleración por cada acierto
current_answer = None  # Almacena la respuesta correcta del problema actual

def generar_problema():
    """
    Genera un problema matemático aleatorio (suma, resta, multiplicación o división)
    y retorna una tupla con la cadena del problema y la respuesta correcta.
    Para división se asegura que el resultado sea entero.
    """
    operacion = random.choice(["+", "-", "*", "/"])
    if operacion == "+":
        a = random.randint(0, 20)
        b = random.randint(0, 20)
        resultado = a + b
    elif operacion == "-":
        a = random.randint(0, 20)
        b = random.randint(0, a)  # Evita resultados negativos
        resultado = a - b
    elif operacion == "*":
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        resultado = a * b
    elif operacion == "/":
        b = random.randint(1, 10)
        resultado = random.randint(0, 10)
        a = b * resultado  # Asegura división exacta
    problema = f"{a} {operacion} {b} = ?"
    return problema, resultado

def nueva_pregunta():
    """
    Genera un nuevo problema y actualiza la interfaz.
    """
    global current_answer
    problema, resultado = generar_problema()
    current_answer = resultado
    document.getElementById("problem").innerHTML = problema
    document.getElementById("answer").value = ""

def verificar_respuesta(event=None):
    """
    Verifica si la respuesta ingresada es correcta.
    Si es correcta, aumenta el puntaje y genera un nuevo problema.
    """
    global score
    try:
        respuesta_usuario = float(document.getElementById("answer").value)
    except:
        document.getElementById("answer").value = ""
        return
    if abs(respuesta_usuario - current_answer) < 1e-5:
        score += 1
        document.getElementById("score").innerHTML = f"Aciertos: {score}"
        nueva_pregunta()
    else:
        document.getElementById("answer").value = ""

def actualizar_temporizador():
    """
    Actualiza el temporizador y acelera el paso del tiempo conforme se acumulan aciertos.
    """
    global time_remaining
    if time_remaining > 0:
        decremento = dt * (1 + score * speed_factor)
        time_remaining -= decremento
        if time_remaining < 0:
            time_remaining = 0
        document.getElementById("timer").innerHTML = f"Tiempo restante: {time_remaining:.1f} s"
        setTimeout(actualizar_temporizador, int(dt * 1000))
    else:
        document.getElementById("message").innerHTML = "¡Tiempo terminado!"
        document.getElementById("answer").disabled = True
        document.getElementById("verify-button").disabled = True

def on_keydown(event):
    """
    Manejador para el evento keydown que verifica si se presionó Enter.
    """
    if event.key == "Enter":
        event.preventDefault()  # Evita acciones por defecto
        verificar_respuesta()

# Inicialización
nueva_pregunta()
actualizar_temporizador()

# Eventos para el botón y la tecla Enter
document.getElementById("verify-button").addEventListener("click", verificar_respuesta)
document.getElementById("answer").addEventListener("keydown", on_keydown)
    </py-script>
</body>
</html>

