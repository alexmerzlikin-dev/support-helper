import keyboard
import time
import sys
import os
import json

CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Файл конфигурации {CONFIG_FILE} не найден!")
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    if "bindings" not in config:
        raise ValueError("В конфиге отсутствует секция 'bindings'")
    
    if "settings" not in config:
        config["settings"] = {}
    
    settings = config["settings"]
    defaults = {
        "send_enter": False,
        "delay_before": 0.1,
        "delay_after": 0.05,
        "reload_hotkey": "ctrl+shift+r"
    }
    
    for key, default_value in defaults.items():
        if key not in settings:
            settings[key] = default_value
    
    return config

def send_text(text, settings):
    delay_before = settings.get("delay_before", 0.1)
    delay_after = settings.get("delay_after", 0.05)
    send_enter = settings.get("send_enter", True)
    
    if delay_before > 0:
        time.sleep(delay_before)
    
    keyboard.write(text)
    
    if send_enter and not text.endswith('\n'):
        if delay_after > 0:
            time.sleep(delay_after)
        keyboard.press_and_release('enter')

def edit_config():
    try:
        import subprocess
        import platform
        
        if platform.system() == "Windows":
            os.startfile(CONFIG_FILE)
        elif platform.system() == "Darwin":
            subprocess.call(["open", CONFIG_FILE])
        else:
            subprocess.call(["xdg-open", CONFIG_FILE])
    except:
        print(f"Файл конфигурации: {os.path.abspath(CONFIG_FILE)}")

class ConfigManager:
    def __init__(self):
        self.config = None
        self.settings = None
        self.bindings = None
    
    def load(self):
        self.config = load_config()
        self.settings = self.config.get("settings", {})
        self.bindings = self.config.get("bindings", {})
    
    def register_hotkeys(self):
        keyboard.unhook_all()
        
        for key, text in self.bindings.items():
            keyboard.add_hotkey(key, lambda t=text: send_text(t, self.settings))
        
        reload_key = self.settings.get("reload_hotkey", "ctrl+shift+r")
        keyboard.add_hotkey(reload_key, self.reload_config)
        keyboard.add_hotkey("ctrl+shift+e", edit_config)
    
    def reload_config(self):
        print("\n" + "=" * 50)
        print("Перезагрузка конфигурации...")
        
        try:
            self.load()
            self.register_hotkeys()
            print(f"Загружено {len(self.bindings)} биндов")
        except Exception as e:
            print(f"Ошибка: {e}")
        
        print("=" * 50 + "\n")

def main():
    print("=" * 50)
    print("Помощник для поддержки")
    print("=" * 50)
    
    if not os.path.exists(CONFIG_FILE):
        print(f"ОШИБКА: Файл {CONFIG_FILE} не найден!")
        print(f"Создайте {CONFIG_FILE} с обязательной секцией 'bindings'")
        sys.exit(1)
    
    config_manager = ConfigManager()
    
    try:
        config_manager.load()
    except Exception as e:
        print(f"ОШИБКА загрузки конфигурации: {e}")
        sys.exit(1)

    if not config_manager.bindings:
        print("ОШИБКА: В конфигурации нет биндов")
        sys.exit(1)
    
    config_manager.register_hotkeys()
    
    print(f"\nЗагружено {len(config_manager.bindings)} горячих клавиш")
    print(f"\nСписок биндов:\n")
    
    for i, (key, text) in enumerate(config_manager.bindings.items(), 1):
        display_text = text.replace('\n', '\\n')
        if len(display_text) > 60:
            display_text = display_text[:57] + "..."
        print(f"{i:2}. {key:25} -> {display_text}")
    
    print("\n" + "=" * 50)
    print("Программа активна")
    reload_key = config_manager.settings.get("reload_hotkey", "ctrl+shift+r")
    print(f"{reload_key} - перезагрузить конфиг")
    print("ctrl+shift+e - редактировать конфиг")
    print("Ctrl+C - выход")
    print("=" * 50 + "\n")

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nЗавершено")
    finally:
        keyboard.unhook_all()

if __name__ == "__main__":
    main()