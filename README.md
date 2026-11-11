# California Housing — Model as a Service (Flask + Docker)

บริการทำนายราคาบ้านกลางของ California ด้วย RandomForest ห่อด้วย Flask และรันใน Docker

## โครงสร้างไฟล์

```
demo_flask_service/
├─ app.py             # Flask server (/, /health, /predict)
├─ train_model.py     # เทรนโมเดลแล้วเซฟเป็น model/model.pkl
├─ requirements.txt   # dependencies
├─ Dockerfile
├─ templates/main.html
└─ model/             # สร้างอัตโนมัติเมื่อเทรน
```

## วิธี Build และ Run ด้วย Docker

```powershell
docker build -t ds-ml-service .
docker run --rm -p 5000:5000 ds-ml-service
```

- หน้าเว็บ: http://127.0.0.1:5000/
- เช็คสถานะ: http://127.0.0.1:5000/health

ถ้าพอร์ต 5000 ถูกใช้อยู่ ให้เปลี่ยนเป็น `-p 8080:5000`

## วิธีรันโดยไม่ใช้ Docker (ทดสอบก่อน)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python train_model.py
python app.py
```

## ทดสอบ API

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/predict" -Method POST -Body '{"features":[8.3,25.0,6.0,1.0,1200,3.0,34.2,-118.3]}' -ContentType "application/json"
```

ผลลัพธ์ที่คาดไว้: `{"prediction": 4.03...}` (ประมาณ $403,000)

## Screenshots

(ใส่ภาพหน้าเว็บที่ทำนายสำเร็จไว้ที่นี่)
