import subprocess
import os
import shutil
import sys

def run_command(cmd):
    print(f"Выполняю: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Ошибка: {result.stderr}")
    return result.returncode

def main():
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name=TextSupportHelper',
        '--clean',
        'main.py'
    ]

    result = run_command(' '.join(cmd))
    
    if result == 0:
        print("\n✅ Сборка завершена успешно!")
        print(f"Файл: {os.path.abspath('dist/TextSupportHelper.exe')}")
    else:
        print("\n❌ Ошибка сборки!")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()