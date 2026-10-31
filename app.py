
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

VAT_RATE = Decimal("0.20")
TWELVE = Decimal("12")
TWENTY_FOUR = Decimal("24")
PENNY = Decimal("0.01")


# ============================================================
# CALCULATION FUNCTIONS
# ============================================================

def money(value):
    """Round to two decimal places."""
    return value.quantize(PENNY, rounding=ROUND_HALF_UP)


def format_gbp(value):
    """Format a number as GBP."""
    return f"£{money(value):,.2f}"


def parse_amount(value):
    """Safely parse a GBP amount entered as text."""
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
        raise ValueError("Please enter a valid non-negative amount.")


def calculate_offer(ex_vat):
    """Calculate the offered amount including VAT."""
    return money(ex_vat * (Decimal("1") + VAT_RATE))


def calculate_customer(ex_vat, inc_vat):
    """
    Calculate the missing customer amount.

    If both are provided, the including-VAT amount
    takes priority for savings calculations.
    """

    if ex_vat is None and inc_vat is None:
        return None, None, None

    if ex_vat is not None and inc_vat is not None:
        return ex_vat, inc_vat, "both"

    if ex_vat is not None:
        calculated_inc = calculate_offer(ex_vat)
        return ex_vat, calculated_inc, "excl"

    calculated_ex = money(
        inc_vat / (Decimal("1") + VAT_RATE)
    )

    return calculated_ex, inc_vat, "incl"


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f5f7fb;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main heading */

.main-header {
    background: linear-gradient(120deg, #152b4a, #244e79);
    padding: 30px 34px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.main-header h1 {
    color: white;
    font-size: 30px;
    font-weight: 800;
    margin: 0 0 7px 0;
}

.main-header p {
    color: #d6e3f2;
    font-size: 14px;
    margin: 0;
}

/* Section headings */

.section-title {
    font-size: 19px;
    font-weight: 800;
    color: #172b46;
    margin-top: 12px;
    margin-bottom: 3px;
}

.section-description {
    font-size: 13px;
    color: #748197;
    margin-bottom: 15px;
}

/* Input labels */

div[data-testid="stTextInput"] label {
    font-size: 13px;
    font-weight: 600;
    color: #33445c;
}

div[data-testid="stTextInput"] input {
    border-radius: 9px;
    border: 1px solid #d8e0eb;
    background: white;
    min-height: 45px;
    font-size: 16px;
    font-weight: 600;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #3678c9;
    box-shadow: 0 0 0 1px #3678c9;
}

/* Calculated amount cards */

.calculated-card {
    background: #eaf2ff;
    border: 1px solid #d6e5fa;
    padding: 15px 18px;
    border-radius: 11px;
    margin-top: 8px;
    margin-bottom: 15px;
}

.calculated-label {
    color: #506985;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 5px;
}

.calculated-value {
    color: #174b86;
    font-size: 25px;
    font-weight: 800;
}

/* Results */

.results-heading {
    font-size: 20px;
    font-weight: 800;
    color: #172b46;
    margin-top: 20px;
    margin-bottom: 14px;
}

.metric-card {
    background: white;
    border: 1px solid #e3e9f1;
    border-radius: 14px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 2px 8px rgba(20, 40, 70, 0.035);
}

.metric-label {
    color: #78869a;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 10px;
}

.metric-value {
    color: #16865b;
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.metric-value.negative {
    color: #d05b49;
}

.metric-value.neutral {
    color: #344b68;
}

.metric-note {
    color: #8b97a8;
    font-size: 11px;
    margin-top: 7px;
}

/* Information */

.info-note {
    background: #eef3f9;
    border-radius: 10px;
    padding: 13px 16px;
    color: #52657d;
    font-size: 12px;
    margin-top: 15px;
}

/* Footer */

.footer {
    text-align: center;
    color: #9aa5b5;
    font-size: 11px;
    margin-top: 35px;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="main-header">
    <h1>💷 Monthly Savings Calculator</h1>
    <p>Calculate customer savings instantly. Enter the offered price
    and the customer's current monthly payment.</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SECTION 1 — AGENT OFFER
# ============================================================

st.markdown(
    '<div class="section-title">01 &nbsp; Your offer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Enter the monthly amount offered by the agent. '
    'VAT is automatically added at 20%.'
    '</div>',
    unsafe_allow_html=True
)

offer_col, offer_result_col = st.columns([1.15, 1])

with offer_col:

    offer_input = st.text_input(
        "Offered monthly amount (Excl. VAT)",
        placeholder="e.g. 50.00",
        key="offer_ex",
        help="Enter the agent's offered monthly price excluding VAT."
    )

with offer_result_col:

    try:
        offer_ex = parse_amount(offer_input)
        offer_error = None
    except ValueError as e:
        offer_ex = None
        offer_error = str(e)

    if offer_error:
        st.error(offer_error)

    elif offer_ex is not None:

        offer_inc = calculate_offer(offer_ex)

        st.markdown(f"""
        <div class="calculated-card">
            <div class="calculated-label">
                OFFERED MONTHLY AMOUNT INCLUDING 20% VAT
            </div>
            <div class="calculated-value">
                {format_gbp(offer_inc)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="calculated-card">
            <div class="calculated-label">
                OFFERED MONTHLY AMOUNT INCLUDING 20% VAT
            </div>
            <div class="calculated-value">£0.00</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# SECTION 2 — CUSTOMER CURRENT PRICE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">02 &nbsp; Customer current price</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Enter whichever amount is available. You can enter both '
    'if the customer has provided both figures.'
    '</div>',
    unsafe_allow_html=True
)

customer_col1, customer_col2 = st.columns(2)

with customer_col1:

    customer_ex_input = st.text_input(
        "Current monthly amount (Excl. VAT)",
        placeholder="e.g. 65.00",
        key="customer_ex",
        help="Optional. Enter the customer's current price excluding VAT."
    )

with customer_col2:

    customer_inc_input = st.text_input(
        "Current monthly amount (Incl. VAT)",
        placeholder="e.g. 78.00",
        key="customer_inc",
        help="Optional. Enter the actual amount the customer pays including VAT."
    )


# ============================================================
# CUSTOMER PRICE CALCULATION
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

else:

    customer_ex, customer_inc, customer_source = calculate_customer(
        customer_ex_input_value,
        customer_inc_input_value
    )


# Display calculated customer values

if customer_source is not None:

    st.markdown("**Calculated customer amounts**")

    result_col1, result_col2 = st.columns(2)

    with result_col1:

        st.markdown(f"""
        <div class="calculated-card">
            <div class="calculated-label">
                MONTHLY AMOUNT EXCLUDING VAT
            </div>
            <div class="calculated-value">
                {format_gbp(customer_ex)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with result_col2:

        st.markdown(f"""
        <div class="calculated-card">
            <div class="calculated-label">
                MONTHLY AMOUNT INCLUDING VAT
            </div>
            <div class="calculated-value">
                {format_gbp(customer_inc)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    if customer_source == "both":

        st.caption(
            "Both amounts were provided. The including-VAT figure "
            "is used as the customer's actual payment for savings."
        )

    elif customer_source == "excl":

        st.caption(
            "Including-VAT amount automatically calculated at 20%."
        )

    elif customer_source == "incl":

        st.caption(
            "Excluding-VAT amount automatically calculated at 20%."
        )


# ============================================================
# SECTION 3 — SAVINGS CALCULATION
# ============================================================

st.divider()

st.markdown(
    '<div class="results-heading">03 &nbsp; Customer savings</div>',
    unsafe_allow_html=True
)

if customer_error or offer_error:

    st.warning(
        "Please correct the invalid amount before calculating savings."
    )

elif offer_ex is None:

    st.info(
        "Enter the agent's offered monthly amount to get started."
    )

elif customer_source is None:

    st.info(
        "Enter the customer's current amount (including VAT, "
        "excluding VAT, or both) to calculate savings."
    )

else:

    # Monthly difference: positive = saving, negative = additional cost

    monthly_difference = money(customer_inc - offer_inc)

    yearly_difference = money(monthly_difference * TWELVE)

    two_year_difference = money(monthly_difference * TWENTY_FOUR)

    # Determine result labels and colours

    if monthly_difference > 0:

        status = "Customer saves"

        monthly_label = "Monthly savings"
        yearly_label = "1-year savings"
        two_year_label = "2-year savings"

        value_class = "metric-value"

    elif monthly_difference < 0:

        status = "Offer costs more"

        monthly_label = "Additional monthly cost"
        yearly_label = "Additional cost over 1 year"
        two_year_label = "Additional cost over 2 years"

        value_class = "metric-value negative"

    else:

        status = "No price difference"

        monthly_label = "Monthly difference"
        yearly_label = "1-year difference"
        two_year_label = "2-year difference"

        value_class = "metric-value neutral"

    st.markdown(
        f'<div class="info-note">'
        f'<b>{status}</b> &nbsp;|&nbsp; '
        f'Current monthly payment: {format_gbp(customer_inc)} '
        f'&nbsp;|&nbsp; '
        f'New monthly payment: {format_gbp(offer_inc)}'
        f'</div>',
        unsafe_allow_html=True
    )

    # Display three savings cards

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{monthly_label}</div>
            <div class="{value_class}">
                {format_gbp(abs(monthly_difference))}
            </div>
            <div class="metric-note">Per month</div>
        </div>
        """, unsafe_allow_html=True)

    with metric_col2:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{yearly_label}</div>
            <div class="{value_class}">
                {format_gbp(abs(yearly_difference))}
            </div>
            <div class="metric-note">12 months</div>
        </div>
        """, unsafe_allow_html=True)

    with metric_col3:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{two_year_label}</div>
            <div class="{value_class}">
                {format_gbp(abs(two_year_difference))}
            </div>
            <div class="metric-note">24 months</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    Monthly Savings Calculator &nbsp;•&nbsp;
    VAT calculated at a flat rate of 20% &nbsp;•&nbsp;
    All amounts in GBP (£)
</div>
""", unsafe_allow_html=True)
