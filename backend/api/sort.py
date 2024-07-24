def read_levels(file_path):
    login_levels = []
    with open(file_path, 'r') as file:
        for line in file:
            if "Login: " in line and "Nivel: " in line:
                login = line.split("Login: ")[1].split(",")[0]
                level_str = line.split("Nivel: ")[1].strip()
                try:
                    level = float(level_str)
                    login_levels.append((login, level))
                except ValueError:
                    print(f"Invalid level value for login '{login}': {level_str}")
    return login_levels

def write_sorted_levels(sorted_levels, output_file):
    with open(output_file, 'w') as file:
        for rank, (login, level) in enumerate(sorted_levels, start=1):
            file.write(f"{rank}. {login}: {level}\n")
            print(f"{rank}. {login}: {level}")

def main():
    input_file = 'levels.txt'
    output_file = 'sorted_levels.txt'

    login_levels = read_levels(input_file)
    sorted_levels = sorted(login_levels, key=lambda item: item[1], reverse=True)
    write_sorted_levels(sorted_levels, output_file)

    print(f"Lista de niveles guardada en {output_file}")

if __name__ == "__main__":
    main()
