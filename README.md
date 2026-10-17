# PC Donanım İzleyici

Python ile bilgisayarınızın CPU, GPU ve RAM durumunu izlemenizi sağlayan basit bir script.

## Özellikler
- CPU kullanım yüzdesi
- CPU sıcaklığı (Windows/WMI üzerinden)
- RAM kullanım miktarı ve yüzdesi
- GPU (Ekran kartı) kullanım yüzdesi, sıcaklığı ve VRAM kullanımı

## Kurulum

1. Python'u yükleyin (https://www.python.org)
2. Bu klasördeki terminali açın ve gerekli kütüphaneleri kurun:

```bash
pip install -r requirements.txt
```

3. Scripti çalıştırın:

```bash
python monitor.py
```

## Önemli Notlar

- **CPU Sıcaklığı:** Sadece Windows'ta çalışır ve donanımınızın WMI sensörüne bağlıdır. Bazı sistemlerde CPU sıcaklığı okunamayabilir. Bu durumda [OpenHardwareMonitor](https://openhardwaremonitor.org/) kurulu olduğundan emin olun.
- **GPU:** `GPUtil` genellikle NVIDIA kartlarıyla çalışır (nvidia-smi gerekir). AMD/Intel ekran kartları için destek sınırlıdır.
- Çıkmak için `Ctrl+C` tuşlarına basın.

## Çıktı Örneği

```
==================================================
 PC DONANIM DURUMU
==================================================
[CPU] Kullanım: %12.5
[CPU] Sıcaklık: 55.0°C
[RAM] Kullanım: %45.2 | 8.1 GB / 16.0 GB | Boş: 8.8 GB
[GPU 0] NVIDIA GeForce RTX 3060: Kullanım %15.0 | Sıcaklık 62°C | VRAM %20.0 (1228MB / 6144MB)
==================================================
```