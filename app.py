import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Carbon Choices",
    page_icon="🌿",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg,
        #FFE8D6 0%,
        #F8E7E8 50%,
        #E8E1FA 100%
    ) !important;
}

.stApp h1,
.stApp h2,
.stApp h3,
.stApp p,
.stApp label {
    color: #493B50 !important;
}

.stApp li,
.stApp li p,
.stApp [data-testid="stMarkdownContainer"] {
    color: #493B50 !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stSidebar"] {
    background: #F8E7E8 !important;
}


/* ===== SIDEBAR DESIGN ===== */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg, #FFF0F5 0%, #F0E9FF 100%
    ) !important;
}

/* Sidebar headings */
[data-testid="stSidebar"] h3 {
    color: #7C3AED !important;
    font-size: 22px !important;
    font-weight: 900 !important;
    letter-spacing: 0.7px;
    margin-top: 18px !important;
    margin-bottom: 20px !important;
}

/* Navigation item spacing */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 14px !important;
}

/* Navigation text */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid #E3D6F5;
    border-radius: 13px;
    padding: 12px 14px !important;
    margin-bottom: 4px;
}

/* Bigger, bold menu text */
[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    color: #493B50 !important;
    font-size: 17px !important;
    font-weight: 750 !important;
}

/* Sidebar dividers */
[data-testid="stSidebar"] hr {
    border-color: #D9C7F2 !important;
    margin-top: 22px !important;
    margin-bottom: 22px !important;
}

/* Brand and supporting text */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    line-height: 1.9 !important;
}

.feature-card {
    background: #FFFFFF !important;
    border: 1px solid #E8D8E9;
    border-radius: 20px;
    box-shadow: 0 8px 0 #DCCFE5,
                0 14px 24px rgba(73, 59, 80, 0.12);
}

.stApp .stButton button {
    background: #E8E1FA !important;
    color: #493B50 !important;
    border: 1px solid #C8BCE8 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
}

/* White text for download button */
.stApp [data-testid="stDownloadButton"] button {
    background-color: #8B5CF6 !important;
    color: #FFFFFF !important;
    border: none !important;
}

.stApp [data-testid="stDownloadButton"] button p,
.stApp [data-testid="stDownloadButton"] button span {
    color: #FFFFFF !important;
}


[data-testid="stToolbar"] {
    opacity: 1 !important;
    visibility: visible !important;
}

[data-testid="stToolbar"] button,
[data-testid="stToolbar"] a {
    color: #263238 !important;
}

</style>
""", unsafe_allow_html=True)


# ===== SIDEBAR NAVIGATION =====
with st.sidebar:
    st.markdown("""
        <div style="padding: 15px 0 25px 0;">
            <div style="font-size: 48px;"></div>
            <div style="font-size: 30px; font-weight: 900;
                        line-height: 1.5; color: #7C3AED;">
                Carbon Choices
            </div>
            <div style="font-size: 16px; font-weight: 700;
                        margin-top: 8px; color: #493B50;">
                MAKE EVERY CHOICE COUNT
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### YOUR WORKSPACE")

    page = st.radio(
        "Navigation",
        [
            " Overview",
            " My Footprint",
            " Top 3 Actions",
            " What-If Simulator",
            " Download Report"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("""
        <div style="padding: 16px 10px;
                    background: #E8E1FA; border-radius: 14px;">
            <div style="font-size: 17px; font-weight: 800;
                        color: #493B50;">
                🌍 YOUR IMPACT MATTERS
            </div>
            <div style="font-size: 15px; line-height: 1.8;
                        margin-top: 8px; color: #493B50;">
                Small changes today, a greener tomorrow.
            </div>
        </div>
    """, unsafe_allow_html=True)



# ===== SESSION STATE =====

# ===== SESSION STATE =====
defaults = {
    "started": False,
    "calculated": False,
    "travel_distance": 10.0,
    "transport_mode": "Car",
    "electricity": 100.0,
    "diet": "Vegetarian",
    "shopping_frequency": "Rarely",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ===== EMISSION CALCULATIONS =====
food_emissions = {
    "Vegetarian": 500,
    "Mostly vegetarian": 800,
    "Mixed diet": 1200,
    "Mostly non-vegetarian": 1600
}

shopping_emissions = {
    "Rarely": 100,
    "Once or twice a month": 250,
    "Weekly": 500,
    "Several times a week": 800
}

recommendations = {
    "Transport": [
        ("🚲", "Choose greener travel",
         "Walk, cycle, or use public transport for short trips."),
        ("🚗", "Share your ride",
         "Carpool with friends or colleagues whenever possible."),
        ("🗓️", "Plan your journeys",
         "Combine errands into one trip to reduce unnecessary travel.")
    ],
    "Electricity": [
        ("💡", "Switch to LED bulbs",
         "Use energy-efficient LED lighting at home."),
        ("🔌", "Avoid standby power",
         "Switch off appliances when not in use."),
        ("❄️", "Use AC wisely",
         "Choose a comfortable temperature and keep filters clean.")
    ],
    "Food": [
        ("🥗", "Try more plant-based meals",
         "Include beans, lentils, vegetables, and other plant-based foods."),
        ("🍽️", "Reduce food waste",
         "Plan meals and finish the food you take."),
        ("🥦", "Plan your groceries",
         "Buy only what you need and use fresh food before it spoils.")
    ],
    "Shopping": [
        ("🛍️", "Buy mindfully",
         "Pause before purchases and buy only what you need."),
        ("♻️", "Reuse and repair",
         "Repair, reuse, or donate items instead of replacing them."),
        ("👕", "Choose durable products",
         "Prefer long-lasting products over frequent replacements.")
    ]
}


# ===== OVERVIEW PAGE =====
if page.strip() == "Overview":

    st.title("🌿 Carbon Choices")
    st.subheader("Know what actually matters.")
    st.write(
        "Understand your carbon footprint, discover what contributes "
        "most to it, and find practical ways to reduce your impact."
    )

    # ===== WELCOME SCREEN =====
    if not st.session_state.started:

        if st.button("🌱 Get Started", type="primary"):
            st.session_state.started = True
            st.rerun()

    # ===== LIFESTYLE QUESTIONNAIRE =====
    if st.session_state.started and not st.session_state.calculated:

        st.subheader("🌱 Tell Us About Your Lifestyle")
        st.write("Enter your daily lifestyle information below.")

        with st.form("lifestyle_form"):

            travel_distance = st.number_input(
                "Daily travel distance (km)",
                min_value=0.0,
                max_value=500.0,
                value=10.0,
                step=1.0,
                key="travel_distance"
            )

            transport_mode = st.selectbox(
                "Main mode of transport",
                [
                    "Car",
                    "Bike/Scooter",
                    "Bus",
                    "Train/Metro",
                    "Electric Vehicle",
                    "Walking/Cycling"
                ],
                key="transport_mode"
            )

            electricity = st.number_input(
                "Monthly electricity consumption (kWh)",
                min_value=0.0,
                max_value=10000.0,
                value=100.0,
                step=10.0,
                key="electricity"
            )

            diet = st.selectbox(
                "Your diet",
                [
                    "Vegetarian",
                    "Mostly vegetarian",
                    "Mixed diet",
                    "Mostly non-vegetarian"
                ],
                key="diet"
            )

            shopping_frequency = st.selectbox(
                "How often do you shop?",
                [
                    "Rarely",
                    "Once or twice a month",
                    "Weekly",
                    "Several times a week"
                ],
                key="shopping_frequency"
            )

            submitted = st.form_submit_button(
                "Calculate My Footprint",
                type="primary"
            )

        if submitted:
            st.session_state.calculated = True
            st.rerun()

    # ===== RESULTS =====
    if st.session_state.calculated:

        st.success("Your footprint has been calculated!")

        travel_distance = st.session_state.travel_distance
        electricity = st.session_state.electricity
        diet = st.session_state.diet
        shopping_frequency = st.session_state.shopping_frequency

        transport_emissions = travel_distance * 0.21 * 365
        electricity_emissions = electricity * 0.70 * 12
        food_value = food_emissions[diet]
        shopping_value = shopping_emissions[shopping_frequency]

        emissions_data = {
            "Transport": transport_emissions,
            "Electricity": electricity_emissions,
            "Food": food_value,
            "Shopping": shopping_value
        }

        total_emissions = sum(emissions_data.values())
        biggest_source = max(emissions_data, key=emissions_data.get)

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Annual Carbon Footprint",
                f"{total_emissions:,.0f} kg CO₂e"
            )

        with col2:
            st.metric("Biggest Emission Source", biggest_source)

        st.subheader("Your Carbon Snapshot")
        st.bar_chart(emissions_data)

        st.info(
            f"Your biggest estimated emission source is **{biggest_source}**. "
            "Explore the other pages to find ways to reduce it."
        )

        st.markdown("### 🌱 Your Next Steps")
        st.write("1. Check your biggest emission source.")
        st.write("2. Explore your Top 3 Actions.")
        st.write("3. Test a habit change in the What-If Simulator.")

    # ===== START OVER =====
    if st.session_state.started:
        if st.button("🔄 Start Over"):
            st.session_state.started = False
            st.session_state.calculated = False
            st.rerun()


# ===== DATA FOR ALL RESULTS PAGES =====
if page.strip() != "Overview":

    if not st.session_state.calculated:
        st.title("🌿 Carbon Choices")
        st.info("First, go to Overview and complete your lifestyle questionnaire.")

    else:
        travel_distance = st.session_state.travel_distance
        electricity = st.session_state.electricity
        diet = st.session_state.diet
        shopping_frequency = st.session_state.shopping_frequency

        transport_emissions = travel_distance * 0.21 * 365
        electricity_emissions = electricity * 0.70 * 12
        food_value = food_emissions[diet]
        shopping_value = shopping_emissions[shopping_frequency]

        emissions_data = {
            "Transport": transport_emissions,
            "Electricity": electricity_emissions,
            "Food": food_value,
            "Shopping": shopping_value
        }

        total_emissions = sum(emissions_data.values())
        biggest_source = max(emissions_data, key=emissions_data.get)


        # ===== MY FOOTPRINT =====
        if page.strip() == "My Footprint":

            st.title("🌍 My Carbon Footprint")
            st.write("Understand where your estimated emissions come from.")

            st.metric(
                "Annual Carbon Footprint",
                f"{total_emissions:,.0f} kg CO₂e/year"
            )

            st.subheader("Emissions by Category")
            st.bar_chart(emissions_data)

            st.caption(
                "These are simplified estimates, not a precise measurement "
                "of your actual carbon footprint."
            )


        # ===== TOP 3 ACTIONS =====
        elif page.strip() == "Top 3 Actions":

            st.title("🎯 Your Top 3 Actions")
            st.write(
                f"Your biggest estimated emission source is **{biggest_source}**."
            )
            st.write("Start with these practical actions:")

            actions = recommendations[biggest_source]
            columns = st.columns(3)

            for i, (emoji, title, description) in enumerate(actions):
                with columns[i]:
                    st.markdown(f"### {emoji}")
                    st.markdown(f"**{title}**")
                    st.write(description)

            st.caption(
                "Actual emission savings depend on your habits and circumstances."
            )


        # ===== WHAT-IF SIMULATOR =====
        elif page.strip() == "What-If Simulator":

            st.title("🔮 What-If Simulator")
            st.write(
                "What if you reduced your daily travel distance? "
                "Move the slider to explore the estimated change."
            )

            new_travel_distance = st.slider(
                "New daily travel distance (km)",
                min_value=0.0,
                max_value=100.0,
                value=min(float(travel_distance), 100.0),
                step=1.0
            )

            new_transport_emissions = new_travel_distance * 0.21 * 365

            new_total_emissions = (
                new_transport_emissions
                + electricity_emissions
                + food_value
                + shopping_value
            )

            reduction = total_emissions - new_total_emissions

            reduction_percentage = (
                (reduction / total_emissions) * 100
                if total_emissions > 0 else 0
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Original Footprint",
                    f"{total_emissions:,.0f} kg CO₂e/year"
                )

            with col2:
                st.metric(
                    "What-If Footprint",
                    f"{new_total_emissions:,.0f} kg CO₂e/year",
                    delta=f"{-reduction:,.0f} kg CO₂e/year"
                )

            if reduction > 0:
                st.success(
                    f"🌱 Estimated reduction: {reduction:,.0f} kg CO₂e/year "
                    f"({reduction_percentage:.1f}%)"
                )
            elif reduction < 0:
                st.warning(
                    f"Your estimated footprint increases by "
                    f"{abs(reduction):,.0f} kg CO₂e/year."
                )
            else:
                st.info("Your estimated footprint remains unchanged.")


        # ===== DOWNLOAD REPORT =====
        elif page.strip() == "Download Report":

            st.title("📥 Download Your Carbon Report")
            st.write("Your estimated annual emissions, category by category.")

            report_df = pd.DataFrame({
                "Category": list(emissions_data.keys()),
                "Annual Emissions (kg CO2e)": list(emissions_data.values())
            })

            st.dataframe(report_df, use_container_width=True)

            st.download_button(
                label="📄 Download My Carbon Report",
                data=report_df.to_csv(index=False),
                file_name="carbon_footprint_report.csv",
                mime="text/csv"
            )


