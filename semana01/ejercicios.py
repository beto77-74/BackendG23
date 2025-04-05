# print('Hola Mundo')

# saludo = 'Hola Mundo2'
# print(saludo)

# nombre = input('Ingrese tu nombre:')
# print('Hola: {}' .format(nombre))

# valor = ((3+2)/(2*5))**2
# print(valor)

# horas = input('ingrese las horas trabajadas: ')
# costo = input('ingrese el costo x hora: ')
# paga = int(horas) * int(costo)
# print('Le corresponde {} de paga' .format(paga) )

# numero = float(input('ingrese el numero: '))
# calculo = (numero*(numero+1))/2
# print(calculo)

# peso = float(input('Ingrese su peso (en kg): '))
# estatura = float(input('Ingrese su estatura (en metros): '))

# calculo = round(peso / (estatura**2),2)
# print(calculo)

# dividendo = float(input('Ingrese el dividendo: '))
# divisor = float(input('Ingrese el divisor: '))

# cociente = int(dividendo / divisor)
# residuo = int(dividendo % divisor)

# print('Dividendo: ' + format(dividendo))
# print('Divisor: ' + format(divisor))
# print('Cociente: ' + format(cociente))
# print('Residuo: ' + format(residuo))


# cantidad = float(input('Ingrese la cantidad a invertir: '))
# interes = float(input('Ingrese el interes anual (Ej: 10,20...): '))
# anno = float(input('Ingrese el numero de años: '))

# capitalObt = round((cantidad * ((interes/100+1)**anno)),2)
# print('El capital Obtenido es: ' + format(capitalObt))

# def saludo():
#     print('hola amiga...')

# saludo()

# def saludo(nombre):
#     print('Hola ' + nombre)

# saludo('Carlos')

# def email(direccion):
#     if '@' in direccion:
#         print('Email valido')
#     else:
#         print('Email no valido')

# email('ss')


def sumar_numeros():
    suma = 0
    while True:
        try:
            numero = int(input("Ingresa un número (0 para terminar): "))
            if numero == 0:
                break
            suma += numero
        except ValueError:
            print("Por favor, ingresa un número válido.")
    return suma

resultado = sumar_numeros()
print(f"La suma de los números ingresados es: {resultado}")

