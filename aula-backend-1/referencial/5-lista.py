numeros = [1, 2, 3, 4, 5]

print("Lista de números:", numeros)

print("Primeiro elemento:", numeros[0])  # Primeiro elemento
print("Último elemento:", numeros[-1])  # Último elemento

numeros.append(6)
print("Lista após adicionar 6:", numeros)

numeros.remove(3)
print("Lista após remover o número 3:", numeros)

print("Elementos da lista:")
for numero in numeros:
    print(numero)

if 2 in numeros:
    print("O número 2 está na lista.")
else:
    print("O número 2 não está na lista.")
