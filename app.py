
from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import IntegrityError
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

app = Flask(__name__)


def ket_noi_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "4000")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "test"),
        ssl_ca=certifi.where(),
        ssl_verify_cert=True,
        ssl_verify_identity=True,
        connection_timeout=15
    )


@app.route("/")
def trang_chu():
    return render_template("index.html")


@app.route("/api/sinhvien")
def danh_sach_sinh_vien():
    db = ket_noi_db()
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sinh_vien")
        danh_sach = cursor.fetchall()
        cursor.close()
        return danh_sach
    finally:
        db.close()


@app.route("/api/sinhvien", methods=["POST"])
def them_sinh_vien():
    data = request.get_json()

    maSV = data["maSV"].strip()
    hoTen = data["hoTen"].strip()
    lop = data["lop"].strip()

    db = ket_noi_db()
    cursor = db.cursor()

    sql = """
        INSERT INTO sinh_vien (maSV, hoTen, lop)
        VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(sql, (maSV, hoTen, lop))
        db.commit()
        return {"message": "Thêm sinh viên thành công"}
    except IntegrityError:
        db.rollback()
        return {
            "message": "Mã sinh viên đã tồn tại! Vui lòng nhập mã khác."
        }, 409
    finally:
        cursor.close()
        db.close()


@app.route("/api/sinhvien/<maSV>", methods=["DELETE"])
def xoa_sinh_vien(maSV):
    db = ket_noi_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM sinh_vien WHERE maSV = %s",
            (maSV,)
        )
        db.commit()
        cursor.close()
        return {"message": "Xóa sinh viên thành công"}
    finally:
        db.close()


@app.route("/api/sinhvien/<maSV>", methods=["PUT"])
def sua_sinh_vien(maSV):
    data = request.get_json()

    hoTen = data["hoTen"].strip()
    lop = data["lop"].strip()

    db = ket_noi_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            """
            UPDATE sinh_vien
            SET hoTen = %s, lop = %s
            WHERE maSV = %s
            """,
            (hoTen, lop, maSV)
        )
        db.commit()
        cursor.close()
        return {"message": "Cập nhật sinh viên thành công"}
    finally:
        db.close()


if __name__ == "__main__":
    app.run(debug=True)