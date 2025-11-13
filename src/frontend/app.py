import streamlit as st
from datetime import datetime, timedelta
from services import AppointmentService
from models import Animal, Owner, AppointmentCreate, AnimalType, AppointmentStatus
import requests
import re

# Page configuration
st.set_page_config(
    page_title="🐾 Pet Clinic",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# Custom CSS for a nicer look
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4ECDC4;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .pet-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #4ECDC4;
    }
    .status-scheduled {
        background-color: #FFE66D;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-weight: bold;
    }
    .status-confirmed {
        background-color: #4ECDC4;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-weight: bold;
        color: white;
    }
    .status-completed {
        background-color: #95E1D3;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-weight: bold;
    }
    .status-cancelled {
        background-color: #FF6B6B;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-weight: bold;
        color: white;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #f0f2f6;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .welcome-text {
        text-align: center;
        font-size: 1.2rem;
        color: #4ECDC4;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize service
@st.cache_resource
def get_appointment_service():
    return AppointmentService(base_url="http://localhost:8001")

def validate_email(email):
    """Simple email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def login_page():
    """Display login page"""
    st.markdown('<h1 class="main-header">🐾 Welcome to Pet Clinic 🐾</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("### 🔐 Please Sign In")
        st.markdown("Enter your email to access the Pet Clinic portal")
        
        with st.form("login_form"):
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
            submitted = st.form_submit_button("🐾 Enter Clinic", use_container_width=True)
            
            if submitted:
                if not email:
                    st.error("⚠️ Please enter your email address")
                elif not validate_email(email):
                    st.error("⚠️ Please enter a valid email address")
                else:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.success(f"✅ Welcome back, {email}!")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.info("💡 **Tip**: Any valid email format will work! This is a demo login.")
        
        # Fun examples
        with st.expander("🎭 Need inspiration? Try these:"):
            st.code("drsmith@petclinic.com")
            st.code("vettech@animalcare.com")
            st.code("petlover@example.com")

# Check if user is logged in
if not st.session_state.logged_in:
    login_page()
    st.stop()

# Main app (only shown when logged in)
appointment_service = get_appointment_service()

# Header
st.markdown('<h1 class="main-header">🐾 Welcome to Pet Clinic 🐾</h1>', unsafe_allow_html=True)
st.markdown("### Your trusted partner in pet care")

# Sidebar navigation
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio(
    "Choose a page:",
    ["🏠 Home", "📅 Book Appointment", "📋 View Appointments", "🔍 Search Appointment"]
)

# Animal type emoji mapping
animal_emoji = {
    "dog": "🐕",
    "cat": "🐈",
    "bird": "🐦",
    "rabbit": "🐰",
    "hamster": "🐹",
    "other": "🐾"
}

# Status color mapping
def get_status_class(status: str) -> str:
    return f'status-{status.lower()}'

# Home Page
if page == "🏠 Home":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🏥 **Professional Care**\nExpert veterinarians at your service")
    
    with col2:
        st.success("⏰ **Flexible Hours**\nBook appointments that fit your schedule")
    
    with col3:
        st.warning("💝 **Pet Friendly**\nWe treat your pets like family")
    
    st.markdown('<p class="sub-header">📊 Quick Stats</p>', unsafe_allow_html=True)
    
    try:
        appointments = appointment_service.list_appointments()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Appointments", len(appointments))
        
        with col2:
            scheduled = len([a for a in appointments if a.status == AppointmentStatus.SCHEDULED])
            st.metric("Scheduled", scheduled)
        
        with col3:
            confirmed = len([a for a in appointments if a.status == AppointmentStatus.CONFIRMED])
            st.metric("Confirmed", confirmed)
        
        with col4:
            completed = len([a for a in appointments if a.status == AppointmentStatus.COMPLETED])
            st.metric("Completed", completed)
        
        # Recent appointments
        st.markdown('<p class="sub-header">🕒 Recent Appointments</p>', unsafe_allow_html=True)
        
        if appointments:
            recent = sorted(appointments, key=lambda x: x.created_at, reverse=True)[:5]
            for apt in recent:
                emoji = animal_emoji.get(apt.animal.type.value, "🐾")
                with st.container():
                    col1, col2, col3 = st.columns([2, 3, 1])
                    with col1:
                        st.write(f"{emoji} **{apt.animal.name}** ({apt.animal.type.value.title()})")
                    with col2:
                        st.write(f"👤 {apt.owner.name} • 📅 {apt.appointment_date.strftime('%B %d, %Y at %I:%M %p')}")
                    with col3:
                        st.markdown(f'<span class="{get_status_class(apt.status.value)}">{apt.status.value.upper()}</span>', unsafe_allow_html=True)
                    st.divider()
        else:
            st.info("No appointments yet. Book your first appointment!")
            
    except requests.exceptions.RequestException as e:
        st.error("⚠️ Unable to connect to the appointment service. Please make sure the API is running on http://localhost:8001")

# Book Appointment Page
elif page == "📅 Book Appointment":
    st.markdown('<p class="sub-header">📅 Book a New Appointment</p>', unsafe_allow_html=True)
    
    with st.form("appointment_form"):
        st.write("### 🐾 Pet Information")
        col1, col2 = st.columns(2)
        
        with col1:
            pet_name = st.text_input("Pet Name *", placeholder="e.g., Fluffy")
            pet_type = st.selectbox("Pet Type *", options=[t.value for t in AnimalType])
        
        with col2:
            pet_breed = st.text_input("Breed", placeholder="e.g., Golden Retriever")
            pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=1)
        
        st.write("### 👤 Owner Information")
        col1, col2 = st.columns(2)
        
        with col1:
            owner_name = st.text_input("Full Name *", placeholder="e.g., John Smith")
            owner_email = st.text_input("Email *", placeholder="e.g., john@example.com")
        
        with col2:
            owner_phone = st.text_input("Phone Number *", placeholder="e.g., (555) 123-4567")
        
        st.write("### 📋 Appointment Details")
        col1, col2 = st.columns(2)
        
        with col1:
            appointment_date = st.date_input(
                "Appointment Date *",
                min_value=datetime.now().date(),
                value=datetime.now().date() + timedelta(days=1)
            )
        
        with col2:
            appointment_time = st.time_input("Appointment Time *", value=datetime.now().replace(hour=10, minute=0).time())
        
        reason = st.text_input("Reason for Visit *", placeholder="e.g., Annual checkup, vaccination")
        notes = st.text_area("Additional Notes (Optional)", placeholder="Any special requirements or concerns...")
        
        submitted = st.form_submit_button("🎯 Book Appointment", use_container_width=True)
        
        if submitted:
            if not all([pet_name, pet_type, owner_name, owner_email, owner_phone, reason]):
                st.error("⚠️ Please fill in all required fields marked with *")
            else:
                try:
                    # Create models
                    animal = Animal(
                        name=pet_name,
                        type=AnimalType(pet_type),
                        breed=pet_breed if pet_breed else None,
                        age=pet_age if pet_age > 0 else None
                    )
                    
                    owner = Owner(
                        name=owner_name,
                        email=owner_email,
                        phone=owner_phone
                    )
                    
                    appointment_datetime = datetime.combine(appointment_date, appointment_time)
                    
                    appointment_data = AppointmentCreate(
                        animal=animal,
                        owner=owner,
                        appointment_date=appointment_datetime,
                        reason=reason,
                        notes=notes if notes else None
                    )
                    
                    # Create appointment
                    created_appointment = appointment_service.create_appointment(appointment_data)
                    
                    st.success(f"✅ Appointment successfully booked! Appointment ID: {created_appointment.id}")
                    st.balloons()
                    
                    # Display confirmation
                    st.info(f"""
                    **Appointment Confirmation**
                    
                    🐾 Pet: {created_appointment.animal.name} ({created_appointment.animal.type.value.title()})
                    
                    👤 Owner: {created_appointment.owner.name}
                    
                    📅 Date & Time: {created_appointment.appointment_date.strftime('%B %d, %Y at %I:%M %p')}
                    
                    📋 Reason: {created_appointment.reason}
                    
                    📧 Confirmation email sent to: {created_appointment.owner.email}
                    """)
                    
                except requests.exceptions.RequestException as e:
                    st.error(f"⚠️ Unable to book appointment. Please make sure the API is running. Error: {str(e)}")
                except Exception as e:
                    st.error(f"⚠️ An error occurred: {str(e)}")

# View Appointments Page
elif page == "📋 View Appointments":
    st.markdown('<p class="sub-header">📋 All Appointments</p>', unsafe_allow_html=True)
    
    # Filter options
    col1, col2 = st.columns([1, 3])
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            options=["All"] + [s.value.title() for s in AppointmentStatus]
        )
    
    try:
        # Get appointments
        if status_filter == "All":
            appointments = appointment_service.list_appointments()
        else:
            status = AppointmentStatus(status_filter.lower())
            appointments = appointment_service.list_appointments(status)
        
        st.write(f"**Found {len(appointments)} appointment(s)**")
        
        if appointments:
            # Sort by appointment date
            appointments_sorted = sorted(appointments, key=lambda x: x.appointment_date, reverse=True)
            
            for apt in appointments_sorted:
                emoji = animal_emoji.get(apt.animal.type.value, "🐾")
                
                with st.expander(f"{emoji} {apt.animal.name} - {apt.appointment_date.strftime('%B %d, %Y at %I:%M %p')} - {apt.status.value.upper()}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("#### 🐾 Pet Details")
                        st.write(f"**Name:** {apt.animal.name}")
                        st.write(f"**Type:** {apt.animal.type.value.title()}")
                        if apt.animal.breed:
                            st.write(f"**Breed:** {apt.animal.breed}")
                        if apt.animal.age:
                            st.write(f"**Age:** {apt.animal.age} years")
                        
                        st.write("#### 👤 Owner Details")
                        st.write(f"**Name:** {apt.owner.name}")
                        st.write(f"**Email:** {apt.owner.email}")
                        st.write(f"**Phone:** {apt.owner.phone}")
                    
                    with col2:
                        st.write("#### 📋 Appointment Details")
                        st.write(f"**ID:** {apt.id}")
                        st.write(f"**Date & Time:** {apt.appointment_date.strftime('%B %d, %Y at %I:%M %p')}")
                        st.write(f"**Reason:** {apt.reason}")
                        if apt.notes:
                            st.write(f"**Notes:** {apt.notes}")
                        st.write(f"**Status:** {apt.status.value.upper()}")
                        st.write(f"**Created:** {apt.created_at.strftime('%B %d, %Y at %I:%M %p')}")
                    
                    # Action buttons
                    st.write("---")
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        if st.button("✅ Confirm", key=f"confirm_{apt.id}"):
                            try:
                                appointment_service.update_appointment_status(apt.id, AppointmentStatus.CONFIRMED)
                                st.success("Appointment confirmed!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                    
                    with col2:
                        if st.button("✔️ Complete", key=f"complete_{apt.id}"):
                            try:
                                appointment_service.update_appointment_status(apt.id, AppointmentStatus.COMPLETED)
                                st.success("Appointment completed!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                    
                    with col3:
                        if st.button("📅 Reschedule", key=f"reschedule_{apt.id}"):
                            try:
                                appointment_service.update_appointment_status(apt.id, AppointmentStatus.SCHEDULED)
                                st.success("Appointment rescheduled!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                    
                    with col4:
                        if st.button("❌ Cancel", key=f"cancel_{apt.id}", type="primary"):
                            try:
                                appointment_service.cancel_appointment(apt.id)
                                st.success("Appointment cancelled!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
        else:
            st.info("No appointments found with the selected filter.")
    
    except requests.exceptions.RequestException as e:
        st.error("⚠️ Unable to connect to the appointment service. Please make sure the API is running on http://localhost:8001")

# Search Appointment Page
elif page == "🔍 Search Appointment":
    st.markdown('<p class="sub-header">🔍 Search for an Appointment</p>', unsafe_allow_html=True)
    
    appointment_id = st.text_input("Enter Appointment ID", placeholder="e.g., abc123...")
    
    if st.button("🔎 Search", use_container_width=True):
        if not appointment_id:
            st.warning("Please enter an appointment ID")
        else:
            try:
                apt = appointment_service.get_appointment(appointment_id)
                
                st.success("✅ Appointment Found!")
                
                emoji = animal_emoji.get(apt.animal.type.value, "🐾")
                
                st.markdown(f"### {emoji} Appointment Details")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("#### 🐾 Pet Information")
                    st.write(f"**Name:** {apt.animal.name}")
                    st.write(f"**Type:** {apt.animal.type.value.title()}")
                    if apt.animal.breed:
                        st.write(f"**Breed:** {apt.animal.breed}")
                    if apt.animal.age:
                        st.write(f"**Age:** {apt.animal.age} years")
                    
                    st.write("#### 👤 Owner Information")
                    st.write(f"**Name:** {apt.owner.name}")
                    st.write(f"**Email:** {apt.owner.email}")
                    st.write(f"**Phone:** {apt.owner.phone}")
                
                with col2:
                    st.write("#### 📋 Appointment Information")
                    st.write(f"**ID:** {apt.id}")
                    st.write(f"**Date & Time:** {apt.appointment_date.strftime('%B %d, %Y at %I:%M %p')}")
                    st.write(f"**Reason:** {apt.reason}")
                    if apt.notes:
                        st.write(f"**Notes:** {apt.notes}")
                    st.markdown(f'**Status:** <span class="{get_status_class(apt.status.value)}">{apt.status.value.upper()}</span>', unsafe_allow_html=True)
                    st.write(f"**Created:** {apt.created_at.strftime('%B %d, %Y at %I:%M %p')}")
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    st.error("❌ Appointment not found. Please check the ID and try again.")
                else:
                    st.error(f"⚠️ An error occurred: {str(e)}")
            except requests.exceptions.RequestException as e:
                st.error("⚠️ Unable to connect to the appointment service. Please make sure the API is running on http://localhost:8001")

# Footer
st.sidebar.markdown("---")
st.sidebar.success(f"👤 Logged in as:\n\n**{st.session_state.user_email}**")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("""
    **🐾 Pet Clinic**
    
    Your trusted partner in pet care
    
    📞 Contact: (555) 123-4567
    
    📧 Email: info@petclinic.com
    
    🌐 www.petclinic.com
""")
