with open("datos.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        print(linea.strip())