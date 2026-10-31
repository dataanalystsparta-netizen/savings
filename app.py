
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
# CALCULATION FUNCTIONS
# ============================================================

def money(value):
    return value.quantize(PENNY, rounding=ROUND_HALF_UP)


def gbp(value):
    return f"£{money(value):,.2f}"


def parse_amount(value):
    """Safely convert entered amounts into GBP Decimal values."""

    if not value or not value.strip():
        return None

    cleaned = (
        value.strip()
        .replace("£", "")
        .replace(",", "")
        .replace(" ", "")
    )

    try:
        amount = Decimal(cleaned)

        if not amount.is_finite() or amount < 0:
            raise ValueError

        return money(amount)

    except (InvalidOperation, ValueError):
        raise ValueError("Enter a valid non-negative amount.")


def calculate_amounts(ex, inc):
    """
    Calculate missing VAT amount.

    If both are provided:
    - Keep both actual entered values.
    - Use including-VAT amount for savings.
    - Flag any discrepancy against 20% VAT.
    """

    if ex is None and inc is None:
        return None, None, None, False

    if ex is not None and inc is not None:

        expected_inc = money(ex * VAT)

        discrepancy = expected_inc != inc

        return ex, inc, "both", discrepancy

    if ex is not None:

        calculated_inc = money(ex * VAT)

        return ex, calculated_inc, "excl", False

    calculated_ex = money(inc / VAT)

    return calculated_ex, inc, "incl", False


def savings_class(value):
    if value > 0:
        return "metric-value"

    elif value < 0:
        return "metric-value negative"

    return "metric-value neutral"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #f4f6fa;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1050px;
    padding-top: 4rem !important;
    padding-bottom: 1rem !important;
    padding-left: 2rem;
    padding-right: 2rem;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.55rem;
}

/* INPUT VISIBILITY */

div[data-testid="stTextInput"] input {
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

/* HEADER */

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

/* MODE SELECTOR */

div[role="radiogroup"] {
    gap: 12px;
}

div[role="radiogroup"] label {
    background: white;
    border: 1px solid #dce4ef;
    border-radius: 8px;
    padding: 7px 16px;
    font-weight: 700;
    color: #263e5a !important;
}

div[role="radiogroup"] label p {
    color: #263e5a !important;
    font-size: 13px;
}

div[role="radiogroup"] label:has(input:checked) {
    background: #e7f0ff;
    border-color: #397dc0;
}

/* SECTION HEADINGS */

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

/* CALCULATED CARDS */

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

/* AMOUNT CARDS */

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

/* SAVINGS */

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
    padding: 13px 12px;
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
    font-size: 23px;
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

/* STATUS */

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

/* FOOTER */

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
# CALCULATION PERIOD
# ============================================================

st.markdown(
    '<div class="section-heading">Calculation Period</div>',
    unsafe_allow_html=True
)

mode = st.radio(
    "Select calculation period",
    ["Monthly", "Quarterly (3 months)"],
    horizontal=True,
    label_visibility="collapsed",
    key="calculation_mode"
)

is_quarterly = mode == "Quarterly (3 months)"

period_key = "quarterly" if is_quarterly else "monthly"
period_name = "Quarterly" if is_quarterly else "Monthly"

st.caption(
    "All entered amounts represent a 3-month period."
    if is_quarterly
    else "All entered amounts represent a 1-month period."
)


# ============================================================
# 01 — AGENT OFFER
# ============================================================

st.markdown(
    '<div class="section-heading">01 &nbsp; Agent Offer</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="section-sub">'
    f'Enter either or both offered {period_name.lower()} amounts.'
    f'</div>',
    unsafe_allow_html=True
)

offer_col1, offer_col2 = st.columns(2)

with offer_col1:

    offer_ex_input = st.text_input(
        f"Offered {period_name.lower()} amount (Excl. VAT)",
        placeholder="e.g. 50.00",
        key=f"offer_ex_{period_key}"
    )

with offer_col2:

    offer_inc_input = st.text_input(
        f"Offered {period_name.lower()} amount (Incl. VAT)",
        placeholder="e.g. 60.00",
        key=f"offer_inc_{period_key}"
    )


# ============================================================
# AGENT OFFER CALCULATION
# ============================================================

try:

    offer_ex_input_value = parse_amount(offer_ex_input)
    offer_inc_input_value = parse_amount(offer_inc_input)

    offer_error = None

except ValueError as e:

    offer_ex_input_value = None
    offer_inc_input_value = None
    offer_error = str(e)


if offer_error:

    st.error(offer_error)

    offer_ex = None
    offer_inc = None
    offer_source = None
    offer_discrepancy = False

else:

    offer_ex, offer_inc, offer_source, offer_discrepancy = (
        calculate_amounts(
            offer_ex_input_value,
            offer_inc_input_value
        )
    )


# ============================================================
# DISPLAY OFFERED AMOUNTS
# ============================================================

if offer_source is not None:

    display_offer1, display_offer2 = st.columns(2)

    with display_offer1:

        st.markdown(f"""
        <div class="customer-card">
            <div class="customer-label">
                OFFERED {period_name.upper()} AMOUNT EXCLUDING VAT
            </div>
            <div class="customer-value">{gbp(offer_ex)}</div>
        </div>
        """, unsafe_allow_html=True)

    with display_offer2:

        st.markdown(f"""
        <div class="calculated-card" style="margin-top:0;">
            <div class="calculated-label">
                OFFERED {period_name.upper()} AMOUNT INCLUDING VAT
            </div>
            <div class="calculated-value">{gbp(offer_inc)}</div>
        </div>
        """, unsafe_allow_html=True)

    if offer_source != "both":

        st.caption(
            "Missing amount automatically calculated using 20% VAT."
        )

    if offer_discrepancy:

        st.warning(
            "Offered amounts do not reconcile at 20% VAT. "
            "The including-VAT amount will be used for savings calculations."
        )


# ============================================================
# 02 — CUSTOMER CURRENT PRICE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-heading">02 &nbsp; Customer Current Price</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="section-sub">'
    f'Enter either or both current {period_name.lower()} amounts.'
    f'</div>',
    unsafe_allow_html=True
)

customer_col1, customer_col2 = st.columns(2)

with customer_col1:

    customer_ex_input = st.text_input(
        f"Current {period_name.lower()} amount (Excl. VAT)",
        placeholder="e.g. 65.00",
        key=f"customer_ex_{period_key}"
    )

with customer_col2:

    customer_inc_input = st.text_input(
        f"Current {period_name.lower()} amount (Incl. VAT)",
        placeholder="e.g. 78.00",
        key=f"customer_inc_{period_key}"
    )


# ============================================================
# CUSTOMER CALCULATION
# ============================================================

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
    customer_discrepancy = False

else:

    customer_ex, customer_inc, customer_source, customer_discrepancy = (
        calculate_amounts(
            customer_ex_input_value,
            customer_inc_input_value
        )
    )


# ============================================================
# DISPLAY CUSTOMER AMOUNTS
# ============================================================

if customer_source is not None:

    display_customer1, display_customer2 = st.columns(2)

    with display_customer1:

        st.markdown(f"""
        <div class="customer-card">
            <div class="customer-label">
                CURRENT {period_name.upper()} AMOUNT EXCLUDING VAT
            </div>
            <div class="customer-value">{gbp(customer_ex)}</div>
        </div>
        """, unsafe_allow_html=True)

    with display_customer2:

        st.markdown(f"""
        <div class="customer-card">
            <div class="customer-label">
                CURRENT {period_name.upper()} AMOUNT INCLUDING VAT
            </div>
            <div class="customer-value">{gbp(customer_inc)}</div>
        </div>
        """, unsafe_allow_html=True)

    if customer_source != "both":

        st.caption(
            "Missing amount automatically calculated using 20% VAT."
        )

    if customer_discrepancy:

        st.warning(
            "Customer amounts do not reconcile at 20% VAT. "
            "The including-VAT amount will be used for savings calculations."
        )


# ============================================================
# 03 — SAVINGS CALCULATIONS
# ============================================================

st.divider()

st.markdown(
    '<div class="results-heading">03 &nbsp; Customer Savings</div>',
    unsafe_allow_html=True
)


if offer_error or customer_error:

    st.warning("Please correct the invalid amount.")

elif offer_source is None:

    st.info("Enter at least one offered amount to get started.")

elif customer_source is None:

    st.info(
        "Enter at least one customer current amount to calculate savings."
    )

else:

    # Difference for selected input period.
    # Positive = savings.
    # Negative = additional cost.

    period_difference = money(customer_inc - offer_inc)

    if is_quarterly:

        monthly_difference = money(
            period_difference / Decimal("3")
        )

        quarter_difference = period_difference

        yearly_difference = money(
            period_difference * Decimal("4")
        )

        two_year_difference = money(
            period_difference * Decimal("8")
        )

    else:

        monthly_difference = period_difference

        quarter_difference = money(
            period_difference * Decimal("3")
        )

        yearly_difference = money(
            period_difference * Decimal("12")
        )

        two_year_difference = money(
            period_difference * Decimal("24")
        )


    # Status and labels

    if period_difference > 0:

        status = "✓ Customer saves money with this offer"
        status_class = ""

        labels = [
            "1 MONTH SAVINGS",
            "1 QUARTER SAVINGS",
            "1 YEAR SAVINGS",
            "2 YEARS SAVINGS"
        ]

        value_class = "metric-value"

    elif period_difference < 0:

        status = "⚠ The new offer costs the customer more"
        status_class = "negative"

        labels = [
            "1 MONTH ADDITIONAL COST",
            "1 QUARTER ADDITIONAL COST",
            "1 YEAR ADDITIONAL COST",
            "2 YEARS ADDITIONAL COST"
        ]

        value_class = "metric-value negative"

    else:

        status = "The customer pays exactly the same"
        status_class = "neutral"

        labels = [
            "1 MONTH DIFFERENCE",
            "1 QUARTER DIFFERENCE",
            "1 YEAR DIFFERENCE",
            "2 YEARS DIFFERENCE"
        ]

        value_class = "metric-value neutral"


    st.markdown(f"""
    <div class="status {status_class}">
        {status}
    </div>
    """, unsafe_allow_html=True)


    # Four savings cards

    metric_cols = st.columns(4)

    values = [
        monthly_difference,
        quarter_difference,
        yearly_difference,
        two_year_difference
    ]

    periods = [
        "Per month",
        "3 months",
        "12 months",
        "24 months"
    ]

    for col, label, value, period in zip(
        metric_cols, labels, values, periods
    ):

        with col:

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="{value_class}">
                    {gbp(abs(value))}
                </div>
                <div class="metric-note">{period}</div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown(f"""
<div class="footer">
    Savings Calculator &nbsp;·&nbsp;
    {period_name} Mode &nbsp;·&nbsp;
    Flat VAT: 20% &nbsp;·&nbsp; GBP (£)
</div>
""", unsafe_allow_html=True)
