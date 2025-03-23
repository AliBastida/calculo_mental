import tkinter as tk
import random

# Variables globales
score = 0
time_remaining = 30.0  # Tiempo inicial en segundos
dt = 0.1               # Intervalo de actualización (segundos)
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
    label_problema.config(text=problema)
    entry_respuesta.delete(0, tk.END)

def verificar_respuesta(event=None):
    """
    Verifica si la respuesta ingresada es correcta.
    Si es correcta, aumenta el puntaje y genera un nuevo problema.
    """
    global score
    try:
        respuesta_usuario = float(entry_respuesta.get())
    except ValueError:
        entry_respuesta.delete(0, tk.END)
        return
    if abs(respuesta_usuario - current_answer) < 1e-5:
        score += 1
        label_score.config(text=f"Aciertos: {score}")
        nueva_pregunta()
    else:
        entry_respuesta.delete(0, tk.END)

def actualizar_temporizador():
    """
    Actualiza el temporizador. El decremento depende del número de aciertos,
    acelerando el paso del tiempo conforme se acumulan respuestas correctas.
    """
    global time_remaining
    if time_remaining > 0:
        decremento = dt * (1 + score * speed_factor)
        time_remaining -= decremento
        label_tiempo.config(text=f"Tiempo restante: {time_remaining:.1f} s")
        root.after(int(dt * 1000), actualizar_temporizador)
    else:
        label_problema.config(text="¡Tiempo terminado!")
        entry_respuesta.config(state="disabled")
        boton_verificar.config(state="disabled")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Juego de Cálculo Divertido")
root.configure(bg="lightblue")  # Fondo de color claro

# Instrucciones de bienvenida
label_instrucciones = tk.Label(root, 
                               text="¡Bienvenido!\nResuelve las operaciones lo más rápido que puedas.",
                               font=("Comic Sans MS", 16, "bold"), 
                               bg="lightblue", 
                               wraplength=400, 
                               justify="center")
label_instrucciones.pack(pady=10)

# Etiqueta para mostrar el problema matemático
label_problema = tk.Label(root, text="", font=("Comic Sans MS", 24, "bold"), bg="lightblue")
label_problema.pack(pady=20)

# Entrada para que el usuario ingrese la respuesta
entry_respuesta = tk.Entry(root, font=("Comic Sans MS", 20), justify="center")
entry_respuesta.pack(pady=10)
entry_respuesta.bind("<Return>", verificar_respuesta)

# Botón para verificar la respuesta
boton_verificar = tk.Button(root, text="Verificar", command=verificar_respuesta,
                            font=("Comic Sans MS", 16, "bold"), bg="yellow", fg="black")
boton_verificar.pack(pady=10)

# Etiqueta para mostrar los aciertos
label_score = tk.Label(root, text="Aciertos: 0", font=("Comic Sans MS", 16), bg="lightblue")
label_score.pack(pady=5)

# Etiqueta para mostrar el tiempo restante
label_tiempo = tk.Label(root, text=f"Tiempo restante: {time_remaining:.1f} s", font=("Comic Sans MS", 16), bg="lightblue")
label_tiempo.pack(pady=5)

# Inicia el juego con la primera pregunta y el temporizador
nueva_pregunta()
actualizar_temporizador()

root.mainloop()

