# ----- IMPORTAR BIBLIOTECAS -----
import os
import time #funciones relacionadas con el tiempo


# ----- INICIO DEL JUEGO / SELECCION DE FICHA -----

def inicio_juego():
    print("**** BIENVENIDO ****")

    while True: #se repetira indefinidamente hasta que usamos break para salir cuando el usuario haya seleccionado una ficha valida
        ficha = input("Seleccione su ficha: X / O\n").upper().strip() #covertir letras a mayusculas y sin espacios

        if ficha == "X":
            humano = "X"
            ordenador = "O"
            break
        elif ficha == "O":
            humano = "O"
            ordenador = "X"
            break
        else:
            print("Por favor, introduce X u O.")
    return humano, ordenador


# ----- CREACION DEL TABLERO -----

def tablero(matriz):
    print("\nTRES EN RAYA\n")
    print("     |     |     ")
    print("  {}  |  {}  |  {}".format(
        matriz[0], matriz[1], matriz[2]))
    print(" 1   | 2   | 3")
    print("-----------------")
    print("     |     |     ")
    print("  {}  |  {}  |  {}".format(
        matriz[3], matriz[4], matriz[5]))
    print(" 4   | 5   | 6")
    print("-----------------")
    print("     |     |     ")
    print("  {}  |  {}  |  {}".format(
        matriz[6], matriz[7], matriz[8]))
    print(" 7   | 8   | 9")
    print()


# ----- COMPROBAR LAS REGLAS DEL JUEGO -----

def obtener_ganador(matriz): #La funcion recibe el tablero y define todas las combinaciones posibles para ganar en total son 8
    combinaciones = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in combinaciones:
        if (matriz[a] == matriz[b] == matriz[c] #comprueba que las 3 casillas tengan exactamente el mismo valor
                and matriz[a] != " "): #comprueba que la primera casilla no este vacia
            return matriz[a] # si se cumplen ambas condiciones devuelve la ficha ganadora, que será X u O

    return None #Si ninguna combinacion es ganadora la funcion termina con


def victoria(matriz):
    return obtener_ganador(matriz) is not None #Si expresion es verdadera (True) y no hay ganador, devuelve None, es falsa (False)


def empate(matriz): #solo hay empate cuando nadie ha ganado y el tablero esta lleno
    return not victoria(matriz) and " " not in matriz 


# ----- MOVIMIENTO DEL JUGADOR HUMANO -----

def movimiento_jugador(matriz, humano): #Recibe los parametros de la matriz y la ficha que le corresponde al jugador, "X" u "O".
    while True:  #Repetir hasta recibir una jugada valida
        try:
            casilla = int(input("Seleccione una casilla (1-9): "))
        except ValueError:
            print("Debes introducir un numero del 1 al 9.")
            continue
        if casilla < 1 or casilla > 9: #validar el rango de la casilla tiene que ser entre 1 y 9
            print("La casilla debe estar entre 1 y 9.")
        elif matriz[casilla - 1] != " ": # Si ese elemento no es " ", significa que ya tiene una ficha y no se puede ocupar otra vez.
            print("Esa casilla ya esta ocupada.")
        else:
            matriz[casilla - 1] = humano #Colocar la ficha
            break


# ----- ALGORITMO MINIMAX -----

def minimax(matriz, turno, humano, ordenador, profundidad=0):#Recibe 5 parametros

    # Caso terminal alguien ha ganado
    ganador = obtener_ganador(matriz)

    if ganador == ordenador:
        return 10 - profundidad #Si el ganador es la computadora, devuelve una puntuacion Positiva

    if ganador == humano:
        return profundidad - 10 #Si el ganador es el humano, devuelve una puntuacion Negativa

    # Caso de terminar en empate
    if " " not in matriz:
        return 0

    # Si juega el ordenador busca maximizar la puntuacion
    if turno == ordenador:
        mejor_puntuacion = float("-inf")#buscamos la puntuación mas ALTA asi que comenzamos con infinito positivo

        for i in range(9):
            if matriz[i] == " ":
                # Simular la jugada del ordenador
                matriz[i] = ordenador
                puntuacion = minimax(
                    matriz, humano, humano, ordenador, #Recursividad: Le pide a otra ejecucion de MINIMAX que investiga que sucederia despues de realizar ese movimiento
                    profundidad + 1
                )

                # Deshacer el movimiento simulado
                matriz[i] = " "

                mejor_puntuacion = max(
                    mejor_puntuacion, puntuacion
                )

        return mejor_puntuacion

    # Si juega el humano, busca minimizar la puntuacion
    else:
        mejor_puntuacion = float("inf") #buscamos la puntuación mas BAJA asi que comenzamos con infinito positivo

        for i in range(9):
            if matriz[i] == " ":
                # Simular el movimiento del humano
                matriz[i] = humano

                puntuacion = minimax(
                    matriz, ordenador, humano, ordenador,
                    profundidad + 1
                )

                # Deshacer el movimiento simulado
                matriz[i] = " "

                mejor_puntuacion = min( #estamos simulando el turno del humano, y MINIMAX supone que el humano elegira la respuesta que produzca la puntuacion mas baja para la computadora
                    mejor_puntuacion, puntuacion
                )

        return mejor_puntuacion


# ----- MOVIMIENTO DEL ORDENADOR CON MINIMAX -----

def movimiento_ordenador(matriz, humano, ordenador):
    mejor_puntuacion = float("-inf")
    mejor_casilla = None

    for i in range(9):
        if matriz[i] == " ":
            # Probar una posible jugada
            matriz[i] = ordenador

            puntuacion = minimax(
                matriz, humano, humano, ordenador, 1
            )

            # Deshacer la jugada para probar otra
            matriz[i] = " "

            # Conservar la mejor jugada encontrada
            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_casilla = i

    if mejor_casilla is not None: #Realizar la jugada definitiva coloca su ficha
        matriz[mejor_casilla] = ordenador


# ----- DESARROLLO DE LA PARTIDA -----

while True:
    matriz = [" "] * 9 #Empiezan vacia la matriz

    os.system("cls" if os.name == "nt" else "clear")

    humano, ordenador = inicio_juego()

    # El jugador humano comienza la partida
    turno = humano
    resultado = None

    while resultado is None: #Si resultado es None, significa que todavia no hay un resultado final
        os.system("cls" if os.name == "nt" else "clear")
        tablero(matriz)

        if turno == humano:
            print("Tu turno:", humano)
            movimiento_jugador(matriz, humano) #Se llama a la funcion que solicita la casilla al usuario y valida su movimiento

        else:
            print("El ordenador esta pensando...")
            time.sleep(0.5)
            movimiento_ordenador(matriz, humano, ordenador) #Coloca la ficha en la casilla que considera mejor

        # Comprobar el resultado despues de cada movimiento
        ganador = obtener_ganador(matriz)

        if ganador is not None:
            resultado = ganador
        elif " " not in matriz:
            resultado = "EMPATE"
        else:
            # Cambiar el turno de humano a ordenador y viciversa
            if turno == humano:
                turno = ordenador
            else:
                turno = humano

    # Mostrar el tablero final
    os.system("cls" if os.name == "nt" else "clear") #limpiar la pantalla de la consola
    tablero(matriz)

    if resultado == humano:
        print("Felicidades, has ganado.")
    elif resultado == ordenador:
        print("El ordenador ha ganado.")
    else:
        print("La partida termino en empate.")

    respuesta = input("\nDeseas jugar otra partida? (Si/No): ").upper()

    if respuesta != "Si":
        print("Gracias por jugar.")
        break