"""
PC Donanım İzleme Scripti
-------------------------
Bu script şu bilgileri gösterir:
- CPU kullanımı ve sıcaklığı
- RAM kullanımı
- Ekran kartı (GPU) kullanımı, sıcaklığı ve VRAM kullanımı

Gereken kurulumlar:
    pip install psutil GPUtil wmi

Notlar:
- CPU sıcaklığı ölçümü sadece Windows'ta WMI üzerinden çalışır ve
  donanımınızın sensörünü temsil eden bir WMI sınıfına bağlıdır.
  Bazı sistemlerde CPU sıcaklığı "Ölçülemiyor" olarak gözükür.
  Bu durumda OpenHardwareMonitor gibi bir program kurulu olmalı ve
  WMI arayüzü etkinleştirilmelidir.
- GPU ölçümleri NVIDIA kartlarda GPUtil (nvidia-smi) üzerinden çalışır.
  AMD/Intel ekran kartları için sınırlı destek vardır.
"""

import time
import platform
import sys

try:
    import psutil
except ImportError:
    print("psutil bulunamadı. Kurulum için: pip install psutil")
    sys.exit(1)

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False


def get_cpu_temperature():
    """Windows'ta WMI üzerinden CPU sıcaklığını döndürür (Celcius)."""
    if platform.system() != "Windows":
        return None
    if not WMI_AVAILABLE:
        return None
    try:
        c = wmi.WMI(namespace="root\\wmi")
        thermal_sensors = c.MSAcpi_ThermalZoneTemperature()
        temperatures = []
        for sensor in thermal_sensors:
            try:
                # CurrentTemperature: 0.1 Kelvin cinsinden
                kelvin = sensor.CurrentTemperature / 10.0
                celsius = kelvin - 273.15
                temperatures.append(round(celsius, 1))
            except Exception:
                continue
        return temperatures
    except Exception:
        return None


def get_gpu_info():
    """GPU kullanımı, sıcaklığı ve VRAM bilgilerini döndürür."""
    if not GPU_AVAILABLE:
        return []
    try:
        gpus = GPUtil.getGPUs()
        result = []
        for g in gpus:
            result.append({
                "id": g.id,
                "name": g.name,
                "load_percent": round(g.load * 100, 1),
                "temperature_c": g.temperature,
                "memory_used_mb": g.memoryUsed,
                "memory_total_mb": g.memoryTotal,
                "memory_percent": round(g.memoryUtil * 100, 1),
            })
        return result
    except Exception:
        return []


def get_ram_info():
    """RAM kullanım bilgilerini döndürür."""
    ram = psutil.virtual_memory()
    return {
        "total_gb": round(ram.total / (1024 ** 3), 2),
        "used_gb": round(ram.used / (1024 ** 3), 2),
        "available_gb": round(ram.available / (1024 ** 3), 2),
        "percent": ram.percent,
    }


def print_status():
    """Anlık donanım durumunu ekrana yazdırır."""
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_temps = get_cpu_temperature()

    # RAM
    ram = get_ram_info()

    # GPU
    gpus = get_gpu_info()

    print("\n" + "=" * 50)
    print(" PC DONANIM DURUMU")
    print("=" * 50)

    print(f"[CPU] Kullanım: %{cpu_percent}")
    if cpu_temps:
        temp_str = " | ".join([f"{t}°C" for t in cpu_temps])
        print(f"[CPU] Sıcaklık: {temp_str}")
    else:
        print("[CPU] Sıcaklık: Ölçülemiyor (WMI sensörü yok veya erişilemiyor)")

    print(
        f"[RAM] Kullanım: %{ram['percent']} | "
        f"{ram['used_gb']} GB / {ram['total_gb']} GB | "
        f"Boş: {ram['available_gb']} GB"
    )

    if gpus:
        for g in gpus:
            print(
                f"[GPU {g['id']}] {g['name']}: "
                f"Kullanım %{g['load_percent']} | "
                f"Sıcaklık {g['temperature_c']}°C | "
                f"VRAM %{g['memory_percent']} "
                f"({g['memory_used_mb']}MB / {g['memory_total_mb']}MB)"
            )
    else:
        print("[GPU] Bilgi: Ölçülemiyor (GPUtil kurulu değil veya GPU bulunamadı)")

    print("=" * 50)


def main():
    print("PC Donanım İzleyici başlatılıyor... (Çıkmak için Ctrl+C)")
    try:
        while True:
            print_status()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nİzleme durduruldu.")


if __name__ == "__main__":
    main()