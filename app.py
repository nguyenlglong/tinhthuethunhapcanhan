import streamlit as st
st.image("logo.jpg.jpg")
# ==========================
# TIÊU ĐỀ
# ==========================
st.title("💰 Ứng dụng tính thuế thu nhập cá nhân_Đề tài 1_Nguyễn Lê Gia Long")
st.write("Tính thuế TNCN từ lương Gross theo quy định hiện hành.")

# ==========================
# NHẬP DỮ LIỆU
# ==========================
gross_salary = st.number_input(
    "Nhập lương Gross (triệu đồng/tháng)",
    min_value=0.0,
    value=20.0,
    step=0.5
)

dependents = st.number_input(
    "Nhập số người phụ thuộc",
    min_value=0,
    value=0,
    step=1
)

# ==========================
# HÀM TÍNH THUẾ TNCN
# ==========================
def calculate_tax(taxable_income):
    tax = 0

    brackets = [
        (5, 0.05),
        (10, 0.10),
        (18, 0.15),
        (32, 0.20),
        (52, 0.25),
        (80, 0.30),
        (float("inf"), 0.35)
    ]

    lower_limit = 0

    for upper_limit, rate in brackets:
        if taxable_income > lower_limit:
            taxable_part = min(taxable_income, upper_limit) - lower_limit
            tax += taxable_part * rate
            lower_limit = upper_limit
        else:
            break

    return tax

# ==========================
# NÚT TÍNH TOÁN
# ==========================
if st.button("Tính thuế TNCN"):

    # Bảo hiểm người lao động đóng
    bhxh = gross_salary * 0.08   # 8%
    bhyt = gross_salary * 0.015  # 1.5%
    bhtn = gross_salary * 0.01   # 1%

    total_insurance = bhxh + bhyt + bhtn

    # Giảm trừ gia cảnh
    personal_deduction = 11.0
    dependent_deduction = dependents * 4.4

    # Thu nhập tính thuế
    taxable_income = (
        gross_salary
        - total_insurance
        - personal_deduction
        - dependent_deduction
    )

    taxable_income = max(0, taxable_income)

    # Thuế TNCN
    personal_income_tax = calculate_tax(taxable_income)

    # Lương thực nhận
    net_salary = (
        gross_salary
        - total_insurance
        - personal_income_tax
    )

    # ==========================
    # HIỂN THỊ KẾT QUẢ
    # ==========================
    st.success("Kết quả tính toán")

    st.subheader("📋 Chi tiết")

    st.write(f"BHXH (8%): **{bhxh:,.2f} triệu đồng**")
    st.write(f"BHYT (1.5%): **{bhyt:,.2f} triệu đồng**")
    st.write(f"BHTN (1%): **{bhtn:,.2f} triệu đồng**")

    st.write(f"Tổng bảo hiểm: **{total_insurance:,.2f} triệu đồng**")

    st.write(
        f"Giảm trừ bản thân: **{personal_deduction:,.2f} triệu đồng**"
    )

    st.write(
        f"Giảm trừ người phụ thuộc: **{dependent_deduction:,.2f} triệu đồng**"
    )

    st.write(
        f"Thu nhập tính thuế: **{taxable_income:,.2f} triệu đồng**"
    )

    st.write(
        f"Thuế TNCN phải nộp: **{personal_income_tax:,.2f} triệu đồng**"
    )

    st.success(
        f"💵 Lương NET thực nhận: {net_salary:,.2f} triệu đồng/tháng"
    )
