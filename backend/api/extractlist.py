import json

# Ruta del archivo JSON
json_file_path = 'users.json'

# Leer el archivo JSON y extraer los nombres de usuario
with open(json_file_path, 'r', encoding='utf-8') as file:
    users = json.load(file)

# Utilizar una lista y un conjunto para almacenar los nombres de usuario y eliminar duplicados
user_logins_list = []
seen_logins = set()

for user in users:
    login = user['login']
    if login not in seen_logins:
        user_logins_list.append(login)
        seen_logins.add(login)

# Ruta del archivo de texto donde se guardará la lista de nombres de usuario
text_file_path = 'user_logins.txt'

# Guardar la lista en el archivo de texto
with open(text_file_path, 'w', encoding='utf-8') as file:
    for login in user_logins_list:
        file.write(f"{login}\n")

print(f"Lista de nombres de usuario guardada en {text_file_path}")
