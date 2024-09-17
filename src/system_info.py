# system_info.py

import platform
import psutil
import subprocess
import GPUtil

# Получение информации об ОС
def get_os_info():
    system = platform.system()
    release = platform.release()

    if system == "Windows":
        try:
            # Получаем точную версию Windows с помощью команды systeminfo
            output = subprocess.check_output("systeminfo", shell=True).decode()
            for line in output.split("\n"):
                if "OS Name" in line:
                    os_name = line.split(":")[1].strip()
                if "OS Version" in line:
                    os_version = line.split(":")[1].strip()
            return f"OS Name: {os_name} {os_version}"
        except Exception as e:
            return f"OS Name: {system} {release} (detailed version not available)"
    else:
        return f"OS Name: {system} {release}"

# Получение информации о процессоре
def get_processor_info():
    cpu_info = platform.processor()
    cpu_freq = psutil.cpu_freq()
    return f"{cpu_info} @ {cpu_freq.current} MHz, {psutil.cpu_count(logical=False)} Core(s), {psutil.cpu_count(logical=True)} Logical Processor(s)"

# Получение производителя материнской платы
def get_baseboard_manufacturer():
    try:
        result = subprocess.check_output("wmic baseboard get Manufacturer", shell=True).decode().split("\n")[1].strip()
        return result if result else "N/A"
    except Exception as e:
        return str(e)

# Получение информации о системе
def get_system_info():
    system_info = {
        "System Type": platform.machine(),
        "Processor": get_processor_info(),
        "BaseBoard Manufacturer": get_baseboard_manufacturer(),
        "Installed Physical Memory (RAM)": f"{round(psutil.virtual_memory().total / (1024**3))} GB"
    }
    return system_info

# Получение информации о GPU
def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append({
            "GPU Name": gpu.name,
            "GPU Load": f"{gpu.load * 100} %",
            "GPU Total Memory": f"{gpu.memoryTotal} MB",
            "GPU Temperature": f"{gpu.temperature} °C",
            "GPU Free Memory": f"{gpu.memoryFree} MB"
        })
    return gpu_info

# Главная функция для получения всей информации о конфигурации сервера
def get_server_configuration():
    config = {
        "OS Information": get_os_info(),
        "System Information": get_system_info(),
        "GPU Information": get_gpu_info()
    }
    return config


# Функция для загрузки инструкции
def get_usage_instructions():
    instructions = """
    ...

    1. Для успешного использования сервера необходимо ввести кодовое слово.

    2. Выберите нейронную модель из списка [.pth] или [.cbm].

    3. Загрузите соответсвующий файл формата CSV с данными для анализа под выбранный тип модели.

    4. Для моделей типа [.pth] установите диапазон ячеек для обработки. Если нужно обработать все записи, введите 0 и -1.

    5. Для моделей типа [.pth] после обработки можно сохранить результаты в итоговый файл.

    Эта система позволяет быстро и точно анализировать данные, используя выбранную модель BERT или CatBoost, и получать результаты в удобном формате.
    """
    return instructions
