async function themSinhVien() {
    let maSV = document.getElementById("maSV").value.trim();
    let hoTen = document.getElementById("hoTen").value.trim();
    let lop = document.getElementById("lop").value.trim();

    if (maSV === "" || hoTen === "" || lop === "") {
        alert("Vui lòng nhập đầy đủ thông tin!");
        return;
    }

    // Nếu đang sửa sinh viên
    if (maSVDangSua !== null) {

        let response = await fetch("/api/sinhvien/" + maSVDangSua, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                hoTen: hoTen,
                lop: lop
            })
        });

        let ketQua = await response.json();

        alert(ketQua.message);

        maSVDangSua = null;
        document.getElementById("nutThemSua").innerText = "Thêm sinh viên";
        document.getElementById("maSV").disabled = false;

    } else {

        // Nếu đang thêm sinh viên
        let response = await fetch("/api/sinhvien", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                maSV: maSV,
                hoTen: hoTen,
                lop: lop
            })
        });

        let ketQua = await response.json();

        alert(ketQua.message);
    }

    document.getElementById("maSV").value = "";
    document.getElementById("hoTen").value = "";
    document.getElementById("lop").value = "";

    hienThiSinhVien();
}

async function xoaSinhVien(nut) {
    let dong = nut.parentElement.parentElement;

    let maSV = dong.cells[0].innerText.trim();

    let xacNhan = confirm("Bạn có chắc muốn xóa sinh viên này không?");

    if (!xacNhan) {
        return;
    }

    let response = await fetch("/api/sinhvien/" + maSV, {
        method: "DELETE"
    });

    let ketQua = await response.json();

    alert(ketQua.message);

    hienThiSinhVien();
}


let maSVDangSua = null;

function suaSinhVien(nut) {
    let dong = nut.parentElement.parentElement;

    let maSV = dong.cells[0].innerText;
    let hoTen = dong.cells[1].innerText;
    let lop = dong.cells[2].innerText;

    maSVDangSua = maSV;

    document.getElementById("maSV").value = maSV;
    document.getElementById("hoTen").value = hoTen;
    document.getElementById("lop").value = lop;
    document.getElementById("nutThemSua").innerText = "Cập nhật sinh viên";
    document.getElementById("maSV").disabled = true;
}

async function hienThiSinhVien() {
    let response = await fetch("/api/sinhvien");

    let danhSach = await response.json();

    let bang = document.querySelector("tbody");

    bang.innerHTML = "";

    danhSach.forEach(function(sinhVien) {
        let dong = bang.insertRow();

        dong.insertCell(0).innerText = sinhVien.maSV;
        dong.insertCell(1).innerText = sinhVien.hoTen;
        dong.insertCell(2).innerText = sinhVien.lop;

        let oThaoTac = dong.insertCell(3);

        oThaoTac.innerHTML = `
            <button onclick="suaSinhVien(this)">Sửa</button>
            <button onclick="xoaSinhVien(this)">Xóa</button>
        `;
    });
}

hienThiSinhVien();
function timKiemSinhVien() {
    let tuKhoa = document.getElementById("oTimKiem").value.toLowerCase();

    let cacDong = document.querySelectorAll("tbody tr");

    cacDong.forEach(function(dong) {
    let maSV = dong.cells[0].innerText.toLowerCase();
    let hoTen = dong.cells[1].innerText.toLowerCase();
    let lop = dong.cells[2].innerText.toLowerCase();

    if (
    maSV.includes(tuKhoa) ||
    hoTen.includes(tuKhoa) ||
    lop.includes(tuKhoa)
) {
            dong.style.display = "";
        } else {
            dong.style.display = "none";
        }
    });
}
