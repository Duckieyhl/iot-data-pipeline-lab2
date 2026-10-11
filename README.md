# IoT Data Pipeline - Lab 2

**Sinh viên thực hiện:** Nguyễn Anh Đức  
**Mã sinh viên:** B23DCCN176  
**Lớp / Ngành:** Hệ thống Thông tin - Học viện Công nghệ Bưu chính Viễn thông (PTIT)

---

## 📌 Giới thiệu
Dự án xây dựng luồng xử lý dữ liệu IoT thời gian thực (Real-time IoT Data Pipeline):  
**ESP32 (Wokwi) ➔ MQTT Broker (`test.mosquitto.org`) ➔ Python Collector ➔ InfluxDB Cloud ➔ Grafana Cloud**

---

## 🛠️ Yêu cầu môi trường
- Python 3.9+
- Trình duyệt web (Chạy Wokwi Simulator, InfluxDB Cloud v3, Grafana Cloud)

---

## 🚀 Hướng dẫn chạy hệ thống

### Bước 1: Khởi chạy Wokwi Simulator
1. Mở sơ đồ Wokwi với file `firmware/main.ino` và `config/diagram.json`.
2. Bấm nút **Play** (tam giác xanh) để khởi chạy mô phỏng.
3. Quan sát Serial Monitor báo `WiFi connected` và `publish=OK`.

### Bước 2: Cài đặt thư viện Python
Mở Terminal tại thư mục `collector/` và cài đặt dependencies:
```bash
pip install paho-mqtt influxdb-client