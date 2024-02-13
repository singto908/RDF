import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk  
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

np.random.seed(42)  # ตั้งค่า seed เพื่อให้ผลลัพธ์มีความสอดคล้องกัน
n_samples = 100
age = np.random.randint(15, 50, n_samples)
gender = np.random.choice(['Male', 'Female'], n_samples)
weight = np.random.randint(40, 100, n_samples)
height = np.random.randint(140, 200, n_samples)
shoe_size = np.random.randint(5, 13, n_samples)

data = pd.DataFrame({
    'Age': age,
    'Gender': gender,
    'Weight': weight,
    'Height': height,
    'Shoe Size': shoe_size
})

def open_csv():
    global random_forest  # ประกาศตัวแปร global เพื่อใช้งานในทั้งโปรแกรม
    file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path, encoding='cp1252')
        update_treeview(df)
        
        # สร้างโมเดล Random Forest
        X_train = data.drop('Gender', axis=1)
        y_train = data['Gender']
        random_forest = RandomForestClassifier(n_estimators=100, random_state=42)
        random_forest.fit(X_train, y_train)


def update_treeview(data):
    for item in tree.get_children():
        tree.delete(item)

    for index, row in data.iterrows():
        tree.insert("", "end", values=row.tolist())

    result_entry.delete(0, tk.END)
    result_entry.insert(0, ', '.join(map(str, data.iloc[0].tolist())))

def open_image():
    file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        img = Image.open(file_path)
        img = img.resize((600, 500), resample=Image.ANTIALIAS)
        new_image = ImageTk.PhotoImage(img)
        image_label.config(image=new_image)
        image_label.image = new_image

def predict_gender():
    try:
        age = float(entry_age.get())
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        shoe_size = float(entry_shoe_size.get())

        input_data = np.array([[age, weight, height, shoe_size]])
        
        # ทำนายเพศโดยใช้โมเดล Random Forest
        prediction = random_forest.predict(input_data)
        
        result_entry.delete(0, tk.END)
        result_entry.insert(0, 'Male' if prediction == 'Male' else 'Female')
    except ValueError:
        result_entry.delete(0, tk.END)
        result_entry.insert(0, 'Please enter valid data')

# สร้างหน้าต่าง GUI
root = tk.Tk()
root.title("My GUI")

# สร้าง Treeview สำหรับแสดงตาราง
tree = ttk.Treeview(root, columns=(1, 2, 3, 4, 5), show="headings", height=10)

image_label = tk.Label(root)
image_label.grid(row=0, column=2, padx=10, pady=10)

# กำหนดขนาดของคอลัมน์
tree.column(1, width=80)
tree.column(2, width=80)
tree.column(3, width=80)
tree.column(4, width=80)
tree.column(5, width=80)

# กำหนดชื่อคอลัมน์
tree.heading(1, text="เพศ")
tree.heading(2, text="อายุ")
tree.heading(3, text="น้ำหนัก")
tree.heading(4, text="ส่วนสูง")
tree.heading(5, text="เบอร์รองเท้า")

# แสดง Treeview
tree.grid(row=0, column=1, padx=10, pady=10)

# สร้างปุ่มกด (เปิดไฟล์ CSV)
open_csv_button = tk.Button(root, text="Open CSV", command=open_csv)
open_csv_button.place(x=10, y=250)

# สร้างปุ่มกด (เปิดไฟล์รูปภาพ)
open_image_button = tk.Button(root, text="Open Image", command=open_image)
open_image_button.place(x=10, y=290)

# สร้างช่องใส่ข้อมูล 3 ช่อง พร้อมข้อความกำกับ
label_age = tk.Label(root, text="age:")
label_age.place(x=150, y=255)
entry_age = tk.Entry(root)
entry_age.place(x=200, y=255)

label_weight = tk.Label(root, text="weight:")
label_weight.place(x=150, y=294)
entry_weight = tk.Entry(root)
entry_weight.place(x=200, y=294)

label_height = tk.Label(root, text="height :")
label_height.place(x=150, y=333)
entry_height = tk.Entry(root)
entry_height.place(x=200, y=333)

label_shoe_size = tk.Label(root, text="shoe :")
label_shoe_size.place(x=150, y=372)
entry_shoe_size = tk.Entry(root)
entry_shoe_size.place(x=200, y=372)

# สร้างปุ่มกด (พื้นหลังสีเขียว)
predict_button = tk.Button(root, text="ทำนายเพศ", bg="green", fg="white", command=predict_gender)
predict_button.place(x=200, y=410)

# Label แสดงผลลัพธ์
label_result = tk.Label(root, text="ผลลัพธ์:")
label_result.place(x=150, y=450)
result_entry = tk.Entry(root)
result_entry.place(x=200, y=450)

# กำหนดขนาดหน้าจอและแสดง GUI
root.geometry("600x500+420+220")
root.mainloop()
