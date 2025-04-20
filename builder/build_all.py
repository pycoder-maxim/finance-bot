import os
import platform
import subprocess

def run_build_script():
    # Определение операционной системы
    operating_system = platform.system()

    # Определение имени скрипта сборки в зависимости от операционной системы
    if operating_system == 'Windows':
        build_script = 'build_all.cmd'
    else:
        build_script = 'build_all.sh'

    # Проверка существования скрипта
    if not os.path.exists(build_script):
        print(f"Скрипт {build_script} не найден.")
        return

    # Запуск скрипта
    if operating_system == 'Windows':
        subprocess.run(build_script, shell=True)
    else:
        subprocess.run(['bash', build_script])

if __name__ == "__main__":
    run_build_script()