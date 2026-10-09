from flask import Flask, render_template, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "quan_ly_sinh_vien")
)

@app.route("/")
def trang_chu():
    return render_template("index.html")


@app.route("/api/sinhvien")
def danh_sach_sinh_vien():
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sinh_vien")

    danh_sach = cursor.fetchall()

    cursor.close()

    return danh_sach

@app.route("/api/sinhvien", methods=["POST"])
def them_sinh_vien():
    data = request.get_json()

    maSV = data["maSV"].strip()
    hoTen = data["hoTen"].strip()
    lop = data["lop"].strip()

    cursor = db.cursor()

    sql = """
        INSERT INTO sinh_vien (maSV, hoTen, lop)
        VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(sql, (maSV, hoTen, lop))
        db.commit()

        return {"message": "Thêm sinh viên thành công"}

    except mysql.connector.Error:
        return {"message": "Mã sinh viên đã tồn tại! Vui lòng nhập mã khác."}

    finally:
        cursor.close()


@app.route("/api/sinhvien/<maSV>", methods=["DELETE"])
def xoa_sinh_vien(maSV):
    cursor = db.cursor()

    sql = "DELETE FROM sinh_vien WHERE maSV = %s"

    cursor.execute(sql, (maSV,))

    db.commit()

    cursor.close()

    return {"message": "Xóa sinh viên thành công"}

@app.route("/api/sinhvien/<maSV>", methods=["PUT"])
def sua_sinh_vien(maSV):
    data = request.get_json()

    hoTen = data["hoTen"]
    lop = data["lop"]

    cursor = db.cursor()

    sql = """
        UPDATE sinh_vien
        SET hoTen = %s, lop = %s
        WHERE maSV = %s
    """

    cursor.execute(sql, (hoTen, lop, maSV))

    db.commit()

    cursor.close()

    return {"message": "Cập nhật sinh viên thành công"}

if __name__ == "__main__":
    app.run(debug=True)