palabra= "que_sucede"
lista=palabra.split("_")
print(lista)
total=""
if len(palabra) > 1:
    for i in palabra:
        total+=str("\"i\" ")

print(total, type(total))