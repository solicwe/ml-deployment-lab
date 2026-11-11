# California Housing — Model as a Service (Flask + Docker)

บริการทำนายราคาบ้านกลาง (median house value) ของ California ด้วยโมเดล RandomForest
ห่อเป็นเว็บแอปด้วย Flask และรันใน Docker container ด้วย Gunicorn

## โครงสร้างโปรเจค

```
ml-deployment-lab/
├─ app.py              # Flask server: /, /health, /predict
├─ train_model.py      # เทรนโมเดลแล้วเซฟเป็น model/model.pkl
├─ requirements.txt    # ไลบรารีที่ใช้ (ระบุเวอร์ชัน)
├─ Dockerfile          # สูตรสร้าง Docker image
├─ templates/
│  └─ main.html        # หน้าเว็บกรอกค่าและแสดงผลทำนาย
├─ model/              # สร้างอัตโนมัติเมื่อเทรน (ไม่ push ขึ้น GitHub)
└─ screenshots/        # ภาพประกอบการทดสอบ
```

## วิธี Build และ Run ด้วย Docker

ต้องติดตั้งและเปิด Docker Desktop ก่อน จากนั้นรันในโฟลเดอร์โปรเจค:

```powershell
docker build -t ds-ml-service .
docker run --rm -p 5000:5000 ds-ml-service
```

- ตอน `docker build` ระบบจะติดตั้งไลบรารีและเทรนโมเดลไว้ใน image (ต้องต่ออินเทอร์เน็ตเพื่อโหลดข้อมูล)
- เปิดเบราว์เซอร์ที่ http://127.0.0.1:5000/ เพื่อใช้หน้าเว็บ
- ตรวจสถานะที่ http://127.0.0.1:5000/health
- ถ้าพอร์ต 5000 ถูกใช้อยู่ ให้เปลี่ยนเป็น `-p 8080:5000` แล้วเข้าที่พอร์ต 8080

## วิธีรันโดยไม่ใช้ Docker (ทดสอบในเครื่อง)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python train_model.py
python app.py
```

หมายเหตุ: Gunicorn ใช้บน Windows โดยตรงไม่ได้ วิธีนี้จึงใช้ Flask development server แทน

## API

| Method | Path | คำอธิบาย |
|---|---|---|
| GET | `/` | หน้าเว็บสำหรับกรอกค่า |
| GET | `/health` | เช็คสถานะ และแสดงรายชื่อฟีเจอร์ |
| POST | `/predict` | รับ JSON แล้วตอบค่าทำนาย |

ลำดับฟีเจอร์ที่ต้องส่ง (8 ค่า):
`MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude`

ตัวอย่างเรียกด้วย PowerShell:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:5000/predict" -Method POST -Body '{"features":[8.3,25.0,6.0,1.0,1200,3.0,34.2,-118.3]}' -ContentType "application/json"
```

ผลลัพธ์: `{"prediction":4.029...}` หมายถึงประมาณ $403,000 (หน่วยของโมเดลคือ $100,000)

ถ้าส่งจำนวนฟีเจอร์ไม่ครบ 8 ค่า จะได้ HTTP 400 พร้อมข้อความ error

## ภาพผลการทดสอบ

### โครงสร้างไฟล์โปรเจค
![โครงสร้างไฟล์](screenshots/Structure.jpg)

### Docker image ที่สร้างสำเร็จ
![docker images](screenshots/Docker-images.jpg)

### รัน container สำเร็จ (Listening at 0.0.0.0:5000)
![docker run](screenshots/Docker-run.jpg)

### หน้าเว็บทำนายผล
![หน้าเว็บ](screenshots/Web-predict.jpg)

### ทดสอบ API ผ่าน PowerShell
![ทดสอบ API](screenshots/API-test.jpg)
