import os
import re
import requests
import urllib3

# Отключаем предупреждения SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_subdomains_hackertarget(domain):
    """Собирает поддомены через стабильное API HackerTarget."""
    print(f"[*] Запуск OSINT-разведки для домена: {domain}")
    print("[*] Посылаем запрос к HackerTarget (работает мгновенно)...")

    # Используем бесплатный эндпоинт HackerTarget для поиска хостов
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)

        # Если сервис временно перегружен или лимит исчерпан
        if "error" in response.text.lower():
            print(f"[-] Ошибка сервиса: {response.text.strip()}")
            return set()

        if response.status_code != 200:
            print(f"[-] Ошибка сети. Код ответа сервера: {response.status_code}")
            return set()

        subdomains = set()

        # HackerTarget возвращает данные в формате: поддомен,IP-адрес (каждый с новой строки)
        lines = response.text.strip().split("\n")

        for line in lines:
            if "," in line:
                # Отделяем имя поддомена от IP-адреса
                sub_name = line.split(",")[0].strip().lower()

                # Проверяем валидность
                if sub_name.endswith(domain) and sub_name != domain:
                    subdomains.add(sub_name)

        return subdomains

    except Exception as e:
        print(f"[-] Произошла ошибка при запросе: {e}")

    return set()


def save_results(domain, subdomains):
    """Сохраняет найденные поддомены в текстовый файл."""
    if not subdomains:
        print("[-] Поддомены не найдены. Попробуйте другой домен.")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = f"{domain}_subdomains.txt"
    full_path = os.path.join(script_dir, filename)

    sorted_subs = sorted(list(subdomains))

    with open(full_path, "w", encoding="utf-8") as f:
        for sub in sorted_subs:
            f.write(sub + "\n")

    print("\n" + "=" * 50)
    print(f"[+] УСПЕХ! Найдено уникальных поддоменов: {len(sorted_subs)}")
    print(f"[+] Результаты сохранены в файл: {full_path}")
    print("=" * 50 + "\n")

    print("Список обнаруженных поддоменов:")
    for sub in sorted_subs:
        print(f"  - {sub}")


if __name__ == "__main__":
    target_domain = input(
        "Введите целевой домен (например, google.com): "
    ).strip()

    if target_domain:
        found_subs = get_subdomains_hackertarget(target_domain)
        save_results(target_domain, found_subs)
    else:
        print("[-] Вы не ввели домен.")
