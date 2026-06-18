import streamlit as st
import pandas as pd

# ======================
# CẤU HÌNH
# ======================
st.set_page_config(
    page_title="Tính Thuế TNCN",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Ứng dụng tính Thuế Thu Nhập Cá Nhân")

# ======================
# NHẬP DỮ LIỆU
# ======================

gross_salary = st.number_input(
    "Lương Gross (VNĐ/tháng)",
    min_value=0,
    value=30000000,
    step=1000000
)

insurance_salary = st.number_input(
    "Lương làm căn cứ đóng bảo hiểm (VNĐ)",
    min_value=0,
    value=gross_salary,
    step=1000000
)

dependents = st.number_input(
    "Số người phụ thuộc",
    min_value=0,
    value=0,
    step=1
)

resident_type = st.selectbox(
    "Loại lao động",
    ["Cư trú", "Không cư trú"]
)

region = st.selectbox(
    "Vùng lương tối thiểu",
    ["Vùng I", "Vùng II", "Vùng III", "Vùng IV"]
)

# ======================
# LƯƠNG TỐI THIỂU VÙNG
# ======================

region_salary = {
    "Vùng I": 4960000,
    "Vùng II": 4410000,
    "Vùng III": 3860000,
    "Vùng IV": 3450000
}

minimum_salary = region_salary[region]

# ======================
# HẰNG SỐ
# ======================

PERSONAL_DEDUCTION = 15_500_000
DEPENDENT_DEDUCTION = 6_200_000

# Trần BHXH/BHYT (có thể thay đổi theo quy định mới)
BHXH_BHYT_CAP = 46_800_000

# ======================
# HÀM TÍNH BẢO HIỂM
# ======================

def calculate_insurance(base_salary):

    bhtn_cap = minimum_salary * 20

    bhxh_base = min(base_salary, BHXH_BHYT_CAP)
    bhyt_base = min(base_salary, BHXH_BHYT_CAP)
    bhtn_base = min(base_salary, bhtn_cap)

    bhxh = bhxh_base * 0.08
    bhyt = bhyt_base * 0.015
    bhtn = bhtn_base * 0.01

    return bhxh, bhyt, bhtn

# ======================
# HÀM TÍNH THUẾ LŨY TIẾN
# ======================

def calculate_progressive_tax(income):

    brackets = [
        (10_000_000, 0.05),
        (30_000_000, 0.10),
        (60_000_000, 0.20),
        (100_000_000, 0.30),
        (float("inf"), 0.35)
    ]

    tax = 0
    lower = 0

    detail_rows = []

    for idx, (upper, rate) in enumerate(brackets, start=1):

        if income <= lower:
            break

        taxable_part = min(income, upper) - lower

        tax_amount = taxable_part * rate

        tax += tax_amount

        detail_rows.append({
            "Bậc thuế": idx,
            "Thu nhập chịu thuế": round(taxable_part),
            "Thuế suất": f"{rate*100:.0f}%",
            "Thuế phải nộp": round(tax_amount)
        })

        lower = upper

    return tax, detail_rows

# ======================
# NÚT TÍNH TOÁN
# ======================

if st.button("Tính thuế"):

    # ------------------
    # BẢO HIỂM
    # ------------------

    bhxh, bhyt, bhtn = calculate_insurance(
        insurance_salary
    )

    insurance_total = bhxh + bhyt + bhtn

    # ------------------
    # THU NHẬP TÍNH THUẾ
    # ------------------

    if resident_type == "Cư trú":

        taxable_income = (
            gross_salary
            - insurance_total
            - PERSONAL_DEDUCTION
            - dependents * DEPENDENT_DEDUCTION
        )

        taxable_income = max(0, taxable_income)

        tax, detail_rows = calculate_progressive_tax(
            taxable_income
        )

    else:

        taxable_income = (
            gross_salary
            - insurance_total
        )

        taxable_income = max(0, taxable_income)

        tax = taxable_income * 0.20

        detail_rows = [{
            "Bậc thuế": "-",
            "Thu nhập chịu thuế": round(taxable_income),
            "Thuế suất": "20%",
            "Thuế phải nộp": round(tax)
        }]

    # ------------------
    # LƯƠNG NET
    # ------------------

    net_salary = (
        gross_salary
        - insurance_total
        - tax
    )

    # ==================
    # KẾT QUẢ
    # ==================

    st.success("Kết quả tính toán")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📋 Chi tiết")

        st.write(
            f"BHXH: {bhxh:,.0f} VNĐ"
        )

        st.write(
            f"BHYT: {bhyt:,.0f} VNĐ"
        )

        st.write(
            f"BHTN: {bhtn:,.0f} VNĐ"
        )

        st.write(
            f"Tổng bảo hiểm: {insurance_total:,.0f} VNĐ"
        )

        st.write(
            f"Thu nhập tính thuế: {taxable_income:,.0f} VNĐ"
        )

        st.write(
            f"Thuế TNCN: {tax:,.0f} VNĐ"
        )

    with col2:

        st.metric(
            "💵 Lương NET thực nhận",
            f"{net_salary:,.0f} VNĐ"
        )

    # ==================
    # BẢNG CHI TIẾT THUẾ
    # ==================

    st.subheader("📊 Chi tiết các bậc thuế")

    df_tax = pd.DataFrame(detail_rows)

    st.dataframe(
        df_tax,
        use_container_width=True
    )

    # ==================
    # BIỂU ĐỒ
    # ==================

    st.subheader("📈 Gross → Insurance → Tax → Net")

    chart_df = pd.DataFrame({
        "Khoản mục": [
            "Gross",
            "Bảo hiểm",
            "Thuế TNCN",
            "Net"
        ],
        "Số tiền": [
            gross_salary,
            insurance_total,
            tax,
            net_salary
        ]
    })

    st.bar_chart(
        chart_df.set_index("Khoản mục")
    )
