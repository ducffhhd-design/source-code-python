# -*- coding: utf-8 -*-
"""
CHUONG TRINH QUAN LY THANH VIEN VA THU HOI PHI CAU LAC BO
Python 3.10+
Du lieu duoc luu trong thanh_vien.txt va lich_su_dong_phi.txt.
"""

from datetime import datetime
from pathlib import Path
import csv
THANH_VIEN_FILE = Path("thanhvien.txt")
LICH_SU_FILE = Path("lichsudongphi.txt")

# Muc hoi phi mau theo ky (co the thay doi theo quy dinh cua CLB)
MUC_HOI_PHI = {
    "Thuong": 200000,
    "Tich cuc": 150000,
    "Danh du": 0,
}
TRANG_THAI_LOAI = ("Thuong", "Tich cuc", "Danh du")


def nhap_chuoi(thong_bao, bat_buoc=True):
    while True:
        gia_tri = input(thong_bao).strip()
        if bat_buoc and not gia_tri:
            print("Du lieu khong duoc de trong.")
            continue
        return gia_tri


def nhap_ngay(thong_bao, bat_buoc=True, mac_dinh=""):
    while True:
        gia_tri = input(thong_bao).strip()
        if not gia_tri and not bat_buoc:
            return mac_dinh
        try:
            datetime.strptime(gia_tri, "%Y-%m-%d")
            return gia_tri
        except ValueError:
            print("Ngay khong hop le. Vui long nhap theo dinh dang YYYY-MM-DD.")


def nhap_so_dien_thoai(thong_bao="So dien thoai: "):
    while True:
        sdt = input(thong_bao).strip()
        if sdt and sdt.isdigit() and 9 <= len(sdt) <= 11:
            return sdt
        print("So dien thoai phai gom 9-11 chu so va khong duoc de trong.")


def tim_theo_ma(danh_sach, ma_tv):
    for tv in danh_sach:
        if tv["ma_tv"].casefold() == ma_tv.casefold():
            return tv
    return None


def nhap_loai_thanh_vien(loai_hien_tai=None):
    print("Loai thanh vien:")
    for i, loai in enumerate(TRANG_THAI_LOAI, start=1):
        print(f"{i}. {loai} (hoi phi/ky: {MUC_HOI_PHI[loai]:,} VND)")
    while True:
        gia_tri = input(
            f"Chon loai (1-{len(TRANG_THAI_LOAI)})"
            + (f" [Enter giu {loai_hien_tai}]" if loai_hien_tai else "")
            + ": "
        ).strip()
        if not gia_tri and loai_hien_tai:
            return loai_hien_tai
        try:
            index = int(gia_tri)
            if 1 <= index <= len(TRANG_THAI_LOAI):
                return TRANG_THAI_LOAI[index - 1]
        except ValueError:
            pass
        print("Lua chon khong hop le.")


def tao_thanh_vien(danh_sach):
    print("\n--- THEM THANH VIEN ---")
    while True:
        ma_tv = nhap_chuoi("Ma thanh vien: ")
        if tim_theo_ma(danh_sach, ma_tv):
            print("Ma thanh vien da ton tai. Hay nhap ma khac.")
        else:
            break

    ho_ten = nhap_chuoi("Ho va ten: ")
    ngay_sinh = nhap_ngay("Ngay sinh (YYYY-MM-DD): ")
    gioi_tinh = nhap_chuoi("Gioi tinh: ")
    so_dien_thoai = nhap_so_dien_thoai()
    ngay_gia_nhap = nhap_ngay("Ngay gia nhap (YYYY-MM-DD): ")
    loai = nhap_loai_thanh_vien()

    tv = {
        "ma_tv": ma_tv,
        "ho_ten": ho_ten,
        "ngay_sinh": ngay_sinh,
        "gioi_tinh": gioi_tinh,
        "so_dien_thoai": so_dien_thoai,
        "ngay_gia_nhap": ngay_gia_nhap,
        "loai_thanh_vien": loai,
    }
    danh_sach.append(tv)
    print("Them thanh vien thanh cong.")


def hien_thi_danh_sach(danh_sach):
    print("\n--- DANH SACH THANH VIEN ---")
    if not danh_sach:
        print("Danh sach trong.")
        return
    headers = ["Ma TV", "Ho va ten", "Ngay sinh", "Gioi tinh", "SDT",
               "Ngay gia nhap", "Loai TV", "Phi/ky"]
    rows = []
    for tv in danh_sach:
        rows.append([
            tv["ma_tv"], tv["ho_ten"], tv["ngay_sinh"], tv["gioi_tinh"],
            tv["so_dien_thoai"], tv["ngay_gia_nhap"], tv["loai_thanh_vien"],
            f'{MUC_HOI_PHI[tv["loai_thanh_vien"]]:,}'
        ])
    widths = [max(len(str(row[i])) for row in [headers] + rows) for i in range(len(headers))]
    print(" | ".join(headers[i].ljust(widths[i]) for i in range(len(headers))))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(" | ".join(str(row[i]).ljust(widths[i]) for i in range(len(headers))))


def cap_nhat_thanh_vien(danh_sach):
    print("\n--- CAP NHAT THANH VIEN ---")
    ma_tv = nhap_chuoi("Nhap ma thanh vien can cap nhat: ")
    tv = tim_theo_ma(danh_sach, ma_tv)
    if not tv:
        print("Khong tim thay thanh vien.")
        return
    print("Nhan Enter neu muon giu nguyen gia tri hien tai.")
    cac_truong = [
        ("ho_ten", "Ho va ten"),
        ("ngay_sinh", "Ngay sinh"),
        ("gioi_tinh", "Gioi tinh"),
    ]
    for key, nhan in cac_truong:
        moi = input(f"{nhan} [{tv[key]}]: ").strip()
        if moi:
            if key == "ngay_sinh":
                try:
                    datetime.strptime(moi, "%Y-%m-%d")
                except ValueError:
                    print("Ngay khong hop le, giu nguyen gia tri cu.")
                    continue
            tv[key] = moi

    moi_sdt = input(f"So dien thoai [{tv['so_dien_thoai']}]: ").strip()
    if moi_sdt:
        if moi_sdt.isdigit() and 9 <= len(moi_sdt) <= 11:
            tv["so_dien_thoai"] = moi_sdt
        else:
            print("So dien thoai khong hop le, giu nguyen gia tri cu.")

    moi_ngay = input(f"Ngay gia nhap [{tv['ngay_gia_nhap']}]: ").strip()
    if moi_ngay:
        try:
            datetime.strptime(moi_ngay, "%Y-%m-%d")
            tv["ngay_gia_nhap"] = moi_ngay
        except ValueError:
            print("Ngay khong hop le, giu nguyen gia tri cu.")

    tv["loai_thanh_vien"] = nhap_loai_thanh_vien(tv["loai_thanh_vien"])
    print("Cap nhat thanh cong.")


def xoa_thanh_vien(danh_sach):
    print("\n--- XOA THANH VIEN ---")
    ma_tv = nhap_chuoi("Nhap ma thanh vien can xoa: ")
    tv = tim_theo_ma(danh_sach, ma_tv)
    if not tv:
        print("Khong tim thay thanh vien.")
        return
    xac_nhan = input(f"Xoa {tv['ho_ten']} ({tv['ma_tv']})? (y/n): ").strip().lower()
    if xac_nhan == "y":
        danh_sach.remove(tv)
        print("Da xoa thanh vien. Lich su thu phi cu van duoc giu trong file.")
    else:
        print("Da huy thao tac.")


def tim_kiem_thanh_vien(danh_sach):
    print("\n--- TIM KIEM ---")
    print("1. Ma thanh vien\n2. Ho ten\n3. So dien thoai\n4. Loai thanh vien")
    lua_chon = input("Lua chon: ").strip()
    truong = {"1": "ma_tv", "2": "ho_ten", "3": "so_dien_thoai", "4": "loai_thanh_vien"}
    if lua_chon not in truong:
        print("Lua chon khong hop le.")
        return
    tu_khoa = nhap_chuoi("Nhap tu khoa: ").casefold()
    ket_qua = [tv for tv in danh_sach if tu_khoa in tv[truong[lua_chon]].casefold()]
    hien_thi_danh_sach(ket_qua)


def sap_xep_thanh_vien(danh_sach):
    print("\n--- SAP XEP ---")
    print("1. Ho ten\n2. Hoi phi\n3. Ngay gia nhap")
    lua_chon = input("Tieu chi: ").strip()
    if lua_chon not in ("1", "2", "3"):
        print("Lua chon khong hop le.")
        return
    print("1. Tang dan\n2. Giam dan")
    chieu = input("Chon chieu: ").strip()
    if chieu not in ("1", "2"):
        print("Lua chon khong hop le.")
        return
    khoa = {
        "1": lambda tv: tv["ho_ten"].casefold(),
        "2": lambda tv: MUC_HOI_PHI[tv["loai_thanh_vien"]],
        "3": lambda tv: tv["ngay_gia_nhap"],
    }[lua_chon]
    danh_sach.sort(key=khoa, reverse=(chieu == "2"))
    print("Da sap xep.")
    hien_thi_danh_sach(danh_sach)


def doc_lich_su():
    lich_su = []
    if not LICH_SU_FILE.exists():
        return lich_su
    try:
        with LICH_SU_FILE.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, delimiter="|")
            for dong in reader:
                if dong.get("ma_tv") and dong.get("ky"):
                    lich_su.append(dong)
    except (OSError, csv.Error) as e:
        print(f"Loi doc lich su: {e}")
    return lich_su


def thu_hoi_phi(danh_sach):
    print("\n--- THU HOI PHI ---")
    ma_tv = nhap_chuoi("Ma thanh vien: ")
    tv = tim_theo_ma(danh_sach, ma_tv)
    if not tv:
        print("Thanh vien khong ton tai.")
        return
    ky = nhap_chuoi("Ky dong phi (YYYY-MM, vi du 2026-10): ")
    try:
        datetime.strptime(ky, "%Y-%m")
    except ValueError:
        print("Ky khong hop le. Hay dung dinh dang YYYY-MM.")
        return

    lich_su = doc_lich_su()
    for dong in lich_su:
        if dong.get("ma_tv", "").casefold() == tv["ma_tv"].casefold() and dong.get("ky") == ky:
            print("Thanh vien nay da duoc ghi nhan dong phi ky nay.")
            return

    so_tien = MUC_HOI_PHI[tv["loai_thanh_vien"]]
    print(f"Thanh vien: {tv['ho_ten']} | Loai: {tv['loai_thanh_vien']}")
    print(f"So tien can thu: {so_tien:,} VND")
    xac_nhan = input("Xac nhan da nhan tien? (y/n): ").strip().lower()
    if xac_nhan != "y":
        print("Chua ghi nhan thu phi.")
        return

    thoi_diem = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_moi = not LICH_SU_FILE.exists() or LICH_SU_FILE.stat().st_size == 0
    try:
        with LICH_SU_FILE.open("a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["ma_tv", "ho_ten", "ky", "so_tien", "thoi_diem"],
                delimiter="|"
            )
            if file_moi:
                writer.writeheader()
            writer.writerow({
                "ma_tv": tv["ma_tv"], "ho_ten": tv["ho_ten"], "ky": ky,
                "so_tien": so_tien, "thoi_diem": thoi_diem
            })
        print("Da ghi nhan thu phi thanh cong.")
    except OSError as e:
        print(f"Khong the ghi lich su: {e}")


def xem_lich_su_dong_phi():
    print("\n--- LICH SU DONG HOI PHI ---")
    lich_su = doc_lich_su()
    if not lich_su:
        print("Chua co lich su dong phi.")
        return
    for dong in lich_su:
        print(
            f"Ma: {dong.get('ma_tv')} | Ten: {dong.get('ho_ten')} | "
            f"Ky: {dong.get('ky')} | So tien: {int(dong.get('so_tien', 0)):,} VND | "
            f"Thoi diem: {dong.get('thoi_diem')}"
        )


def thong_ke(danh_sach):
    print("\n--- THONG KE ---")
    lich_su = doc_lich_su()
    da_dong_ma = {dong.get("ma_tv", "").casefold() for dong in lich_su}
    tong = len(danh_sach)
    da_dong = sum(1 for tv in danh_sach if tv["ma_tv"].casefold() in da_dong_ma)
    tong_thu = sum(int(dong.get("so_tien", 0)) for dong in lich_su)
    print(f"Tong so thanh vien: {tong}")
    print(f"So thanh vien da tung dong phi: {da_dong}")
    print(f"So thanh vien chua tung dong phi: {tong - da_dong}")
    print(f"Tong hoi phi da thu (tat ca cac ky): {tong_thu:,} VND")
    print("So thanh vien theo tung loai:")
    for loai in TRANG_THAI_LOAI:
        so_luong = sum(1 for tv in danh_sach if tv["loai_thanh_vien"] == loai)
        print(f"- {loai}: {so_luong}")


def luu_du_lieu(danh_sach):
    truong = ["ma_tv", "ho_ten", "ngay_sinh", "gioi_tinh", "so_dien_thoai",
              "ngay_gia_nhap", "loai_thanh_vien"]
    try:
        with THANH_VIEN_FILE.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=truong, delimiter="|")
            writer.writeheader()
            writer.writerows(danh_sach)
        print(f"Da luu {len(danh_sach)} thanh vien vao {THANH_VIEN_FILE}.")
    except OSError as e:
        print(f"Loi khi luu du lieu: {e}")


def doc_du_lieu():
    danh_sach = []
    if not THANH_VIEN_FILE.exists():
        print(f"Chua co file {THANH_VIEN_FILE}; se bat dau voi danh sach rong.")
        return danh_sach
    try:
        with THANH_VIEN_FILE.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, delimiter="|")
            for dong in reader:
                if not dong.get("ma_tv") or not dong.get("ho_ten"):
                    continue
                loai = dong.get("loai_thanh_vien", "Thuong")
                if loai not in MUC_HOI_PHI:
                    loai = "Thuong"
                tv = {
                    "ma_tv": dong["ma_tv"],
                    "ho_ten": dong["ho_ten"],
                    "ngay_sinh": dong.get("ngay_sinh", ""),
                    "gioi_tinh": dong.get("gioi_tinh", ""),
                    "so_dien_thoai": dong.get("so_dien_thoai", ""),
                    "ngay_gia_nhap": dong.get("ngay_gia_nhap", ""),
                    "loai_thanh_vien": loai,
                }
                if not tim_theo_ma(danh_sach, tv["ma_tv"]):
                    danh_sach.append(tv)
        print(f"Da doc {len(danh_sach)} thanh vien tu file.")
    except (OSError, csv.Error) as e:
        print(f"Loi khi doc du lieu: {e}")
    return danh_sach


def hien_thi_menu():
    print("""
========================================
         QUAN LY CAU LAC BO
========================================
1. Them thanh vien
2. Hien thi danh sach
3. Cap nhat thanh vien
4. Xoa thanh vien
5. Tim kiem thanh vien
6. Sap xep thanh vien
7. Thu hoi phi
8. Thong ke
9. Luu du lieu
10. Doc du lieu
11. Xem lich su dong hoi phi
0. Thoat
========================================""")


def main():
    danh_sach = doc_du_lieu()
    while True:
        hien_thi_menu()
        lua_chon = input("Lua chon: ").strip()
        if lua_chon == "1":
            tao_thanh_vien(danh_sach)
        elif lua_chon == "2":
            hien_thi_danh_sach(danh_sach)
        elif lua_chon == "3":
            cap_nhat_thanh_vien(danh_sach)
        elif lua_chon == "4":
            xoa_thanh_vien(danh_sach)
        elif lua_chon == "5":
            tim_kiem_thanh_vien(danh_sach)
        elif lua_chon == "6":
            sap_xep_thanh_vien(danh_sach)
        elif lua_chon == "7":
            thu_hoi_phi(danh_sach)
        elif lua_chon == "8":
            thong_ke(danh_sach)
        elif lua_chon == "9":
            luu_du_lieu(danh_sach)
        elif lua_chon == "10":
            danh_sach = doc_du_lieu()
        elif lua_chon == "11":
            xem_lich_su_dong_phi()
        elif lua_chon == "0":
            luu_du_lieu(danh_sach)
            print("Da luu du lieu. Tam biet!")
            break
        else:
            print("Lua chon khong hop le. Vui long chon lai.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nChuong trinh da duoc dung boi nguoi dung.")
