import paramiko # type: ignore
import time

def get_bandit_password(level, current_password):
    host = 'bandit.labs.overthewire.org'
    port = 2220
    username = f'bandit{level}'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try: 
        print(f"[*] Подключаемся к {username}... с паролем: {current_password}")
        client.connect(hostname=host, port=port, username=username, password=current_password, timeout=10)

        if level == 0:
            command = 'cat readme'
        elif level == 1:
            command = 'cat ./-'
        elif level == 2:
            command = 'cat ./"--spaces in this filename--"'
        elif level == 3:
            command = 'cat ~/inhere/...Hiding-From-You'
        else:
            command = 'ls -la'

        stdin, stdout, stderr = client.exec_command(command)

        output = stdout.read().decode().strip()
        client.close()

        if output:
            lines = [line.strip() for line in output.splitlines() if line.strip()]
            if lines:
                found = lines[-1].split()[-1]
                print(f"[DEBUG] Очищенный пароль: {found}")
                return found
        
        return None
    
    except Exception as e:
        print(f"[!] Ошибка на уровне {level}: {e}")
        return None

start_level = 0
current_pass = 'bandit0'
filename = "passwords.txt"

with open(filename, "w", encoding='utf-8') as f:
    f.write("=== Найденные пароли Bandit ===\n")

for lvl in range(start_level, 4):
    found_pass = get_bandit_password(lvl, current_pass)

    if found_pass:
        print(f"[+] Поздравляем! Уровень {lvl} пройден. Для уровня {lvl+1} используем: '{found_pass}' (длина: {len(found_pass)})")
        current_pass = found_pass
        with open(filename, "a", encoding='utf-8') as f:
            f.write(f"bandit{lvl+1}: {found_pass}\n")

    else:
        print(f"[!] Не удалось получить пароль на уровне {lvl}") 
        break

print(f"\n[!] Все пароли сохранены в файл {filename}")