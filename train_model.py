from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib, os

# 1) โหลดข้อมูล: X = 8 ฟีเจอร์ของบ้าน, y = ราคากลาง (หน่วย $100,000)
data = fetch_california_housing(as_frame=False)
X, y = data.data, data.target

# 2) แบ่งข้อมูล 80% เทรน / 20% ทดสอบ (random_state ทำให้ผลซ้ำได้)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

# 3) เทรน RandomForest 100 ต้น
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(Xtr, ytr)

# 4) เซฟโมเดลเป็นไฟล์ เพื่อให้ app.py โหลดไปใช้ทำนายได้
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/model.pkl")
print("บันทึกโมเดลเรียบร้อยที่ model/model.pkl")
