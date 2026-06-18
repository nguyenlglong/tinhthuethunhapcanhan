import streamlit as st

# Tiêu đề ứng dụng
st.title("💰 Ứng dụng tính thuế thu nhập cá nhân_Đề tài 1_Nguyễn Lê Gia Long")

# Nhập dữ liệu
thu_nhap = st.number_input(
    "Nhập thu nhập tính thuế hàng tháng (triệu đồng)",
    min_value=0.0,
    value=20.0
)

# Hàm tính thuế TNCN theo biểu lũy tiến từng phần
def tinh_thue_tncn(tn):
    thue = 0

    bac_thue = [
        (5, 0.05),
        (10, 0.10),
        (18, 0.15),
        (32, 0.20),
        (52, 0.25),
        (80, 0.30),
        (float("inf"), 0.35)
    ]

    muc_duoi = 0

    for muc_tren, ty_le in bac_thue:
        if tn > muc_duoi:
            phan_chiu_thue = min(tn, muc_tren) - muc_duoi
            thue += phan_chiu_thue * ty_le
            muc_duoi = muc_tren
        else:
            break

    return thue

# Nút tính toán
if st.button("Tính thuế"):

    thue = tinh_thue_tncn(thu_nhap)
    thu_nhap_sau_thue = thu_nhap - thue

    st.success("Kết quả tính toán")

    st.write(
        f"📌 Thuế thu nhập cá nhân phải nộp: **{thue:,.2f} triệu đồng**"
    )

    st.write(
        f"📌 Thu nhập sau thuế: **{thu_nhap_sau_thue:,.2f} triệu đồng**"
    )
