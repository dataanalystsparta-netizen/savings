
import streamlit as st
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Monthly Savings Calculator",
    page_icon="💷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

VAT = Decimal("1.20")
PENNY = Decimal("0.01")


# ============================================================
# CALCULATIONS
# ============================================================

def money(value):
    return value.quantize(PENNY, rounding=ROUND_HALF_UP)


def gbp(value):
    return f"£{money(value):,.2f}"


def parse_amount(value):
    if not value or not value.strip():
        return None

    cleaned = value.strip().replace("£", "").replace(",", "").replace(" ", "")

    try:
        amount = Decimal(cleaned)

        if not amount.is_finite() or amount < 0:
            raise ValueError

        return money(amount)

    except (InvalidOperation, ValueError):
        raise ValueError("Enter a valid non-negative amount.")


def calculate_customer(ex, inc):
    if ex is None and inc is None:
        return None, None, None

    if ex is not None and inc is not None:
        return ex, inc, "both"

    if ex is not None:
        return ex, money(ex * VAT), "excl"

    return money(inc / VAT), inc, "incl"


# ============================================================
# STYLING
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #f4f6fa;
    font-family: 'DM Sans', sans-serif;
}

/* Compact page */

.block-container {
    max-width: 1050px;
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    padding-left: 2rem;
    padding-right: 2rem;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.55rem;
}

/* FIX: INPUT TEXT VISIBILITY */

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
.stTextInput input {
    color: #172b46 !important;
    -webkit-text-fill-color: #172b46 !important;
    background-color: #ffffff !important;
    caret-color: #174b86 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    height: 42px !important;
    opacity: 1 !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #9aa5b5 !important;
    -webkit-text-fill-color: #9aa5b5 !important;
    opacity: 1 !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #3678c9 !important;
    box-shadow: 0 0 0 1px #3678c9 !important;
}

div[data-testid="stTextInput"] label {
    color: #33445c !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    margin-bottom: 2px !important;
}

/* Header */

.main-header {
    background: linear-gradient(115deg, #152b4a, #285582);
    padding: 19px 25px;
    border-radius: 13px;
    color: white;
    margin-bottom: 12px;
}

.main-header h1 {
    color: white !important;
    font-size: 25px;
    font-weight: 800;
    margin: 0;
    padding: 0;
}

.main-header p {
    color: #d7e5f4;
    font-size: 12px;
    margin: 3px 0 0 0;
}

/* Sections */

.section-heading {
    color: #172b46;
    font-size: 17px;
    font-weight: 800;
    margin: 5px 0 0 0;
}

.section-sub {
    color: #77869a;
    font-size: 12px;
    margin: 0 0 5px 0;
}

/* Calculated values */

.calculated-card {
    background: #eaf2ff;
    border: 1px solid #d7e5f8;
    border-radius: 9px;
    padding: 9px 13px;
    margin-top: 24px;
    min-height: 65px;
}

.calculated-label {
    color: #526984;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.3px;
}

.calculated-value {
    color: #174b86;
    font-size: 21px;
    font-weight: 800;
    margin-top: 2px;
}

/* Customer calculated values */

.customer-card {
    background: white;
    border: 1px solid #e0e7f0;
    border-radius: 9px;
    padding: 9px 13px;
}

.customer-label {
    color: #77869a;
    font-size: 10px;
    font-weight: 700;
}

.customer-value {
    color: #174b86;
    font-size: 19px;
    font-weight: 800;
}

/* Savings results */

.results-heading {
    color: #172b46;
    font-size: 18px;
    font-weight: 800;
    margin: 4px 0 8px 0;
}

.metric-card {
    background: white;
    border: 1px solid #e0e7f0;
    border-radius: 11px;
    padding: 13px 15px;
    min-height: 92px;
    box-shadow: 0 2px 5px rgba(20,40,70,0.025);
}

.metric-label {
    color: #77869a;
    font-size: 11px;
    font-weight: 700;
}

.metric-value {
    color: #13865a;
    font-size: 24px;
    font-weight: 800;
    margin-top: 4px;
}

.metric-value.negative {
    color: #d05245;
}

.metric-value.neutral {
    color: #344b68;
}

.metric-note {
    color: #98a3b1;
    font-size: 10px;
}

/* Status */

.status {
    padding: 9px 13px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    margin: 5px 0 9px 0;
    background: #e9f6ef;
    color: #16754e;
}

.status.negative {
    background: #fff0ed;
    color: #bc493d;
}

.status.neutral {
    background: #edf1f6;
    color: #52647b;
}

/* Dividers and footer */

hr {
    margin: 10px 0 !important;
    border-color: #e1e7ef !important;
}

.footer {
    color: #9aa5b5;
    text-align: center;
    font-size: 10px;
    margin-top: 14px;
}

div[data-testid="stAlert"] {
    padding: 8px 12px;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="main-header">
    <h1>💷 Monthly Savings Calculator</h1>
    <p>Instantly calculate customer savings · VAT at 20% · GBP (£)</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# 01 — AGENT OFFER
# ============================================================

st.markdown(
    '<div class="section-heading">01 &nbsp; Agent Offer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-sub">Enter the offered monthly price excluding VAT.</div>',
    unsafe_allow_html=True
)

offer_col, offer_result_col = st.columns([1, 1])

with offer_col:
    offer_input = st.text_input(
        "Offered monthly amount (Excl. VAT)",
        placeholder="e.g. 50.00",
        key="offer_ex"
    )

try:
    offer_ex = parse_amount(offer_input)
    offer_error = None
except ValueError as e:
    offer_ex = None
    offer_error = str(e)

if offer_error:
    st.error(offer_error)
    offer_inc = None
else:
    offer_inc = money(offer_ex * VAT) if offer_ex is not None else None

with offer_result_col:
    value = gbp(offer_inc) if offer_inc is not None else "—"

    st.markdown(f"""
    <div class="calculated-card">
        <div class="calculated-label">OFFERED MONTHLY AMOUNT INCLUDING 20% VAT</div>
        <div class="calculated-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 02 — CUSTOMER CURRENT PRICE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-heading">02 &nbsp; Customer Current Price</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-sub">Enter either or both amounts. The missing amount will be calculated automatically.</div>',
    unsafe_allow_html=True
)

cust_col1, cust_col2 = st.columns(2)

with cust_col1:
    customer_ex_input = st.text_input(
        "Current monthly amount (Excl. VAT)",
        placeholder="e.g. 65.00",
        key="customer_ex"
    )

with cust_col2:
    customer_inc_input = st.text_input(
        "Current monthly amount (Incl. VAT)",
        placeholder="e.g. 78.00",
        key="customer_inc"
    )

try:
    customer_ex_input_value = parse_amount(customer_ex_input)
    customer_inc_input_value = parse_amount(customer_inc_input)
    customer_error = None
except ValueError as e:
    customer_ex_input_value = None
    customer_inc_input_value = None
    customer_error = str(e)

if customer_error:
    st.error(customer_error)
    customer_ex = None
    customer_inc = None
    customer_source = None
else:
    customer_ex, customer_inc, customer_source = calculate_customer(
        customer_ex_input_value,
        customer_inc_input_value
    )


# Display customer calculated figures

if customer_source is not None:

    display_col1, display_col2 = st.columns(2)

    with display_col1:
        st.markdown(f"""
        <div class="customer-card">
            <div class="customer-label">CURRENT AMOUNT EXCLUDING VAT</div>
            <div class="customer-value">{gbp(customer_ex)}</div>
        </div>
        """, unsafe_allow_html=True)

    with display_col2:
        st.markdown(f"""
        <div class="customer-card">
            <div class="customer-label">CURRENT AMOUNT INCLUDING VAT</div>
            <div class="customer-value">{gbp(customer_inc)}</div>
        </div>
        """, unsafe_allow_html=True)

    if customer_source == "both":
        st.caption("Both figures entered. Including-VAT amount used for savings.")
    else:
        st.caption("Missing amount automatically calculated using 20% VAT.")


# ============================================================
# 03 — SAVINGS RESULTS
# ============================================================

st.divider()

st.markdown(
    '<div class="results-heading">03 &nbsp; Customer Savings</div>',
    unsafe_allow_html=True
)

if offer_error or customer_error:

    st.warning("Please correct the invalid amount.")

elif offer_ex is None:

    st.info("Enter the agent's offered amount to get started.")

elif customer_source is None:

    st.info("Enter the customer's current monthly amount to calculate savings.")

else:

    monthly = money(customer_inc - offer_inc)
    yearly = money(monthly * Decimal("12"))
    two_year = money(monthly * Decimal("24"))

    if monthly > 0:
        status = "✓ Customer saves money with this offer"
        status_class = ""
        labels = [
            "MONTHLY SAVINGS",
            "1-YEAR SAVINGS",
            "2-YEAR SAVINGS"
        ]
        value_class = "metric-value"

    elif monthly < 0:
        status = "⚠ The new offer costs the customer more"
        status_class = "negative"
        labels = [
            "ADDITIONAL MONTHLY COST",
            "ADDITIONAL COST · 1 YEAR",
            "ADDITIONAL COST · 2 YEARS"
        ]
        value_class = "metric-value negative"

    else:
        status = "The customer pays exactly the same"
        status_class = "neutral"
        labels = [
            "MONTHLY DIFFERENCE",
            "1-YEAR DIFFERENCE",
            "2-YEAR DIFFERENCE"
        ]
        value_class = "metric-value neutral"

    st.markdown(f"""
    <div class="status {status_class}">{status}</div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)

    values = [monthly, yearly, two_year]
    periods = ["Per month", "12 months", "24 months"]

    for col, label, value, period in zip(cols, labels, values, periods):

        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="{value_class}">{gbp(abs(value))}</div>
                <div class="metric-note">{period}</div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    Monthly Savings Calculator &nbsp;·&nbsp; Flat VAT rate: 20% &nbsp;·&nbsp; All amounts in GBP
</div>
""", unsafe_allow_html=True)
