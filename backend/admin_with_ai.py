import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import bcrypt
import requests


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Orchestration - Admin",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# MONGODB CONNECTION
# =========================================================

MONGO_URL = "mongodb+srv://Manju123:Manju123@cluster0.q2agwan.mongodb.net/?appName=Cluster0"
#API_URL = "http://127.0.0.1:8000"
API_URL = "https://mproject-knzg.onrender.com"

try:
    client = MongoClient(
        MONGO_URL,
        serverSelectionTimeoutMS=2000
    )

    client.server_info()

    db = client["ai_orchestration"]

    users_collection = db["userslist"]
    employees_collection = db["employees"]
    roles_collection = db["roles"]
    departments_collection = db["departments"]
    teams_collection = db["teams"]
    documents_collection = db["documents"]
    workflows_collection = db["workflows"]
    audit_collection = db["audit_logs"]
    ai_collection = db["ai_queries"]

    mongo_connected = True

except Exception:
    mongo_connected = False


# =========================================================
# SESSION STATE
# =========================================================

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "admin_username" not in st.session_state:
    st.session_state.admin_username = ""

if "admin_page" not in st.session_state:
    st.session_state.admin_page = "Dashboard"


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f7f9fc;
    }

    [data-testid="stSidebar"] {
        background-color: #111827 !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: white !important;
    }

    [data-testid="stSidebar"] details {
        background-color: #111827 !important;
        border: none !important;
        margin-bottom: 4px !important;
    }

    [data-testid="stSidebar"] details summary {
        background-color: #1f2937 !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 8px 10px !important;
    }

    [data-testid="stSidebar"] details summary p {
        color: white !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    [data-testid="stSidebar"] details summary svg {
        color: white !important;
        fill: white !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background-color: #1f2937 !important;
        color: white !important;
        border: 1px solid #374151 !important;
        border-radius: 5px !important;
        font-size: 12px !important;
        padding: 5px 8px !important;
        min-height: 30px !important;
    }

    [data-testid="stSidebar"] .stButton > button p {
        color: white !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #374151 !important;
        color: white !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #374151 !important;
    }

    .login-box {
        max-width: 450px;
        margin: 80px auto;
        padding: 30px;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        background-color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DEFAULT ADMIN ACCOUNT
# =========================================================

def create_default_admin():

    if not mongo_connected:
        return

    existing_admin = users_collection.find_one(
        {
            "email": "admin@organization.com",
            "role": "Administrator"
        }
    )

    if not existing_admin:

        password = "admin123"

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        users_collection.insert_one(
            {
                "name": "System Administrator",
                "email": "admin@organization.com",
                "phone": "",
                "department": "Administration",
                "designation": "Administrator",
                "role": "Administrator",
                "password": hashed_password,
                "status": "Active",
                "created_at": datetime.now()
            }
        )


create_default_admin()


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    st.markdown(
        '<div class="login-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        "<h1 style='text-align:center;'>🤖</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h2 style='text-align:center;'>AI Orchestration</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>Administrator Login</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    email = st.text_input(
        "Email",
        placeholder="Enter admin email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password"
    )

    if st.button(
        "🔐 Login",
        use_container_width=True,
        type="primary"
    ):

        if not mongo_connected:

            st.error(
                "MongoDB is not connected. "
                "Please start MongoDB."
            )

            return

        if not email or not password:

            st.warning(
                "Please enter email and password."
            )

            return

        user = users_collection.find_one(
            {
                "email": email,
                "role": "Administrator",
                "status": "Active"
            }
        )

        if user:

            stored_password = user.get("password")

            try:

                valid_password = bcrypt.checkpw(
                    password.encode("utf-8"),
                    stored_password
                )

            except Exception:

                valid_password = False

            if valid_password:

                st.session_state.admin_logged_in = True
                st.session_state.admin_username = user["email"]
                st.session_state.admin_page = "Dashboard"

                audit_collection.insert_one(
                    {
                        "action": "ADMIN_LOGIN",
                        "user": user["email"],
                        "resource": "Admin Panel",
                        "timestamp": datetime.now()
                    }
                )

                st.rerun()

            else:

                st.error(
                    "Invalid email or password."
                )

        else:

            st.error(
                "Administrator account not found."
            )

    st.markdown("---")

    st.info(
        "Default admin: "
        "admin@organization.com"
    )

    st.info(
        "Default password: admin123"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# SHOW LOGIN IF NOT LOGGED IN
# =========================================================

if not st.session_state.admin_logged_in:

    login_page()
    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## ⚙️ AI Organization")

st.sidebar.caption(
    "Administrator Panel"
)

st.sidebar.caption(
    f"Logged in as: {st.session_state.admin_username}"
)

st.sidebar.markdown("---")


# MongoDB status

if mongo_connected:

    st.sidebar.success(
        "MongoDB Connected"
    )

else:

    st.sidebar.error(
        "MongoDB Not Connected"
    )


# =========================================================
# USER MANAGEMENT
# =========================================================

with st.sidebar.expander(
    "👥 User Management",
    expanded=True
):

    if st.button(
        "Employees",
        use_container_width=True
    ):
        st.session_state.admin_page = "Employees"

    if st.button(
        "Add Employee",
        use_container_width=True
    ):
        st.session_state.admin_page = "Add Employee"

    if st.button(
        "Delete Employee",
        use_container_width=True
    ):
        st.session_state.admin_page = "Delete Employee"


# =========================================================
# SECURITY
# =========================================================

with st.sidebar.expander(
    "🔐 Security",
    expanded=False
):

    if st.button(
        "Roles & Permissions",
        use_container_width=True
    ):
        st.session_state.admin_page = "Roles"


# =========================================================
# ORGANIZATION
# =========================================================

with st.sidebar.expander(
    "🏢 Organization",
    expanded=False
):

    if st.button(
        "Departments",
        use_container_width=True
    ):
        st.session_state.admin_page = "Departments"

    if st.button(
        "Teams",
        use_container_width=True
    ):
        st.session_state.admin_page = "Teams"


# =========================================================
# KNOWLEDGE BASE
# =========================================================

with st.sidebar.expander(
    "📄 Knowledge Base",
    expanded=False
):

    if st.button(
        "Documents",
        use_container_width=True
    ):
        st.session_state.admin_page = "Documents"


# =========================================================
# WORKFLOWS
# =========================================================

with st.sidebar.expander(
    "🔄 Workflows",
    expanded=False
):

    if st.button(
        "Workflow Configuration",
        use_container_width=True
    ):
        st.session_state.admin_page = "Workflows"


# =========================================================
# AI ASSISTANT
# =========================================================

with st.sidebar.expander(
    "🤖 AI Assistant",
    expanded=False
):

    if st.button(
        "Ask Gemini",
        use_container_width=True
    ):
        st.session_state.admin_page = "Ask Gemini"


# =========================================================
# MONITORING
# =========================================================

with st.sidebar.expander(
    "📊 Monitoring",
    expanded=False
):

    if st.button(
        "Reports",
        use_container_width=True
    ):
        st.session_state.admin_page = "Reports"

    if st.button(
        "Audit Logs",
        use_container_width=True
    ):
        st.session_state.admin_page = "Audit"

    if st.button(
        "AI Activity",
        use_container_width=True
    ):
        st.session_state.admin_page = "AI Activity"


# =========================================================
# DASHBOARD
# =========================================================

if st.sidebar.button(
    "🏠 Dashboard",
    use_container_width=True
):

    st.session_state.admin_page = "Dashboard"


# =========================================================
# LOGOUT
# =========================================================

st.sidebar.markdown("---")

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    audit_collection.insert_one(
        {
            "action": "ADMIN_LOGOUT",
            "user": st.session_state.admin_username,
            "resource": "Admin Panel",
            "timestamp": datetime.now()
        }
    )

    st.session_state.admin_logged_in = False
    st.session_state.admin_username = ""

    st.rerun()


# =========================================================
# CURRENT PAGE
# =========================================================

page = st.session_state.admin_page


# =========================================================
# ASK GEMINI
# =========================================================

if page == "Ask Gemini":

    st.title("🤖 Ask Gemini")

    st.write(
        "Ask Gemini a simple question."
    )

    st.markdown("---")

    question = st.text_area(
        "Enter your question",
        placeholder="Example: What is Artificial Intelligence?"
    )

    if st.button(
        "🤖 Ask query",
        type="primary"
    ):

        if question.strip() == "":

            st.warning(
                "Please enter a question."
            )

        else:

            data = {
                "question": question
            }

            try:

                response = requests.post(
                    f"{API_URL}/chat",
                    json=data,
                    timeout=60
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "✅ Response"
                    )

                    st.write(
                        result.get(
                            "answer",
                            "No answer returned."
                        )
                    )

                else:

                    st.error(
                        f"❌ Gemini request failed "
                        f"(HTTP {response.status_code})"
                    )

                    st.code(
                        response.text
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Cannot connect to FastAPI server. "
                    "Make sure Uvicorn is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "❌ Request timed out. "
                    "Please try again."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"❌ Request failed: {e}"
                )

            except Exception as e:

                st.error(
                    f"❌ Unexpected error: {e}"
                )


# =========================================================
# DASHBOARD
# =========================================================

if page == "Ask Gemini":
    pass

elif page == "Dashboard":

    st.title("⚙️ Administrator Dashboard")

    st.write(
        "Manage organization users, security, "
        "documents, workflows and system activities."
    )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        count = (
            employees_collection.count_documents({})
            if mongo_connected else 0
        )

        st.metric(
            "Employees",
            count
        )

    with col2:

        count = (
            departments_collection.count_documents({})
            if mongo_connected else 0
        )

        st.metric(
            "Departments",
            count
        )

    with col3:

        count = (
            documents_collection.count_documents({})
            if mongo_connected else 0
        )

        st.metric(
            "Documents",
            count
        )

    with col4:

        count = (
            ai_collection.count_documents({})
            if mongo_connected else 0
        )

        st.metric(
            "AI Queries",
            count
        )

    st.markdown("---")

    st.subheader(
        "🔔 Recent Administrative Activities"
    )

    if mongo_connected:

        data = list(
            audit_collection.find(
                {},
                {
                    "_id": 0,
                    "action": 1,
                    "user": 1,
                    "resource": 1,
                    "timestamp": 1
                }
            )
            .sort("timestamp", -1)
            .limit(10)
        )

        if data:

            st.dataframe(
                pd.DataFrame(data),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No administrative activity recorded."
            )

    else:

        st.error(
            "MongoDB is not connected."
        )


# =========================================================
# ADD EMPLOYEE
# =========================================================

elif page == "Add Employee":

    st.title("➕ Add Employee")

    st.write(
        "Add a new employee to the organization."
    )

    if not mongo_connected:

        st.error(
            "MongoDB is not connected."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                "Employee Name"
            )

            email = st.text_input(
                "Email"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            phone = st.text_input(
                "Phone"
            )

        with col2:

            department = st.text_input(
                "Department"
            )

            designation = st.text_input(
                "Designation"
            )

            role = st.selectbox(
                "Role",
                [
                    "Employee",
                    "Supervisor",
                    "Manager",
                    "Department Head",
                    "Executive"
                ]
            )

            status = st.selectbox(
                "Status",
                [
                    "Active",
                    "Inactive"
                ]
            )

        st.markdown("---")

        if st.button(
            "➕ Add Employee",
            type="primary"
        ):

            if not name or not email or not password:

                st.warning(
                    "Name, email and password are required."
                )

            else:

                existing_user = users_collection.find_one(
                    {"email": email}
                )
                existing_employee = employees_collection.find_one(
                    {"email": email}
                )

                if existing_user or existing_employee:

                    st.error(
                        "An employee with this email already exists."
                    )

                else:

                    hashed_password = bcrypt.hashpw(
                        password.encode("utf-8"),
                        bcrypt.gensalt()
                    )

                    employee = {
                        "name": name,
                        "email": email,
                        "password": hashed_password,
                        "phone": phone,
                        "department": department,
                        "designation": designation,
                        "role": role,
                        "status": status,
                        "created_at": datetime.now()
                    }

                    result = employees_collection.insert_one(
                        employee
                    )

                    audit_collection.insert_one(
                        {
                            "action": "CREATE_EMPLOYEE",
                            "user": st.session_state.admin_username,
                            "resource": name,
                            "timestamp": datetime.now()
                        }
                    )

                    st.success(
                        f"Employee {name} added successfully."
                    )

                    st.write(
                        "MongoDB ID:",
                        str(result.inserted_id)
                    )


# =========================================================
# EMPLOYEES
# =========================================================

elif page == "Employees":

    st.title("👥 Employees")

    if not mongo_connected:

        st.error(
            "MongoDB is not connected."
        )

    else:

        employees = list(
            employees_collection.find(
                {},
                {
                    "_id": 0,
                    "password": 0
                }
            )
        )

        if employees:

            df = pd.DataFrame(
                employees
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No employees found."
            )


# =========================================================
# DELETE EMPLOYEE
# =========================================================

elif page == "Delete Employee":

    st.title("🗑️ Delete Employee")

    st.write(
        "Remove an employee from MongoDB."
    )

    if not mongo_connected:

        st.error(
            "MongoDB is not connected."
        )

    else:

        employees = list(
            employees_collection.find(
                {
                    "role": {
                        "$ne": "Administrator"
                    }
                },
                {
                    "_id": 1,
                    "name": 1,
                    "email": 1,
                    "department": 1,
                    "role": 1
                }
            )
        )

        if not employees:

            st.info(
                "No employees available for deletion."
            )

        else:

            employee_options = {}

            for employee in employees:

                label = (
                    f"{employee.get('name', 'Unknown')} - "
                    f"{employee.get('email', '')}"
                )

                employee_options[label] = employee["_id"]

            selected_employee = st.selectbox(
                "Select Employee",
                list(employee_options.keys())
            )

            st.markdown("---")

            selected_id = employee_options[
                selected_employee
            ]

            selected_data = employees_collection.find_one(
                {
                    "_id": selected_id
                }
            )

            if selected_data:

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        "**Name**"
                    )

                    st.write(
                        selected_data.get(
                            "name",
                            ""
                        )
                    )

                with col2:

                    st.write(
                        "**Department**"
                    )

                    st.write(
                        selected_data.get(
                            "department",
                            ""
                        )
                    )

                with col3:

                    st.write(
                        "**Role**"
                    )

                    st.write(
                        selected_data.get(
                            "role",
                            ""
                        )
                    )

            st.markdown("---")

            confirm = st.checkbox(
                "I confirm that I want to delete this employee."
            )

            if st.button(
                "🗑️ Delete Employee",
                type="primary"
            ):

                if not confirm:

                    st.warning(
                        "Please confirm deletion first."
                    )

                else:

                    employee = employees_collection.find_one(
                        {
                            "_id": selected_id
                        }
                    )

                    if employee:

                        employees_collection.delete_one(
                            {
                                "_id": selected_id
                            }
                        )

                        audit_collection.insert_one(
                            {
                                "action": "DELETE_EMPLOYEE",
                                "user": st.session_state.admin_username,
                                "resource": employee.get(
                                    "name",
                                    ""
                                ),
                                "timestamp": datetime.now()
                            }
                        )

                        st.success(
                            f"Employee "
                            f"{employee.get('name', '')} "
                            f"deleted successfully."
                        )

                        st.rerun()


# =========================================================
# ROLES & PERMISSIONS
# =========================================================

elif page == "Roles":

    st.title("🔐 Roles & Permissions")

    role = st.selectbox(
        "Select Role",
        [
            "Employee",
            "Supervisor",
            "Manager",
            "Department Head",
            "Executive",
            "Administrator"
        ]
    )

    permissions = {

        "Employee": [
            "View own tasks",
            "Create requests",
            "View authorized documents"
        ],

        "Supervisor": [
            "View team tasks",
            "Approve team requests",
            "Generate team reports"
        ],

        "Manager": [
            "Manage team",
            "Approve requests",
            "Generate reports"
        ],

        "Department Head": [
            "Manage department",
            "Approve requests",
            "View department reports"
        ],

        "Executive": [
            "View organization reports",
            "View analytics",
            "Approve strategic requests"
        ],

        "Administrator": [
            "Manage users",
            "Manage roles",
            "Manage permissions",
            "Manage departments",
            "Manage documents",
            "Configure workflows",
            "View audit logs"
        ]
    }

    st.subheader(
        f"Permissions for {role}"
    )

    selected = []

    for permission in permissions[role]:

        if st.checkbox(
            permission,
            value=True
        ):

            selected.append(permission)

    if st.button(
        "💾 Save Permissions",
        type="primary"
    ):

        if mongo_connected:

            roles_collection.update_one(
                {
                    "role": role
                },
                {
                    "$set": {
                        "role": role,
                        "permissions": selected,
                        "updated_at": datetime.now()
                    }
                },
                upsert=True
            )

            audit_collection.insert_one(
                {
                    "action": "UPDATE_PERMISSIONS",
                    "user": st.session_state.admin_username,
                    "resource": role,
                    "timestamp": datetime.now()
                }
            )

            st.success(
                f"{role} permissions saved."
            )

        else:

            st.error(
                "MongoDB is not connected."
            )


# =========================================================
# DEPARTMENTS
# =========================================================

elif page == "Departments":

    st.title("🏢 Departments")

    if not mongo_connected:

        st.error(
            "MongoDB is not connected."
        )

    else:

        department_name = st.text_input(
            "Department Name"
        )

        if st.button(
            "➕ Add Department"
        ):

            if not department_name:

                st.warning(
                    "Enter department name."
                )

            else:

                existing = departments_collection.find_one(
                    {
                        "name": department_name
                    }
                )

                if existing:

                    st.warning(
                        "Department already exists."
                    )

                else:

                    departments_collection.insert_one(
                        {
                            "name": department_name,
                            "created_at": datetime.now()
                        }
                    )

                    audit_collection.insert_one(
                        {
                            "action": "CREATE_DEPARTMENT",
                            "user": st.session_state.admin_username,
                            "resource": department_name,
                            "timestamp": datetime.now()
                        }
                    )

                    st.success(
                        "Department added."
                    )

        st.markdown("---")

        departments = list(
            departments_collection.find(
                {},
                {
                    "_id": 0,
                    "name": 1,
                    "created_at": 1
                }
            )
        )

        if departments:

            st.dataframe(
                pd.DataFrame(departments),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No departments found."
            )


# =========================================================
# TEAMS
# =========================================================

elif page == "Teams":

    st.title("👥 Teams")

    if not mongo_connected:

        st.error(
            "MongoDB is not connected."
        )

    else:

        team_name = st.text_input(
            "Team Name"
        )

        department = st.text_input(
            "Department"
        )

        if st.button(
            "➕ Add Team"
        ):

            if not team_name:

                st.warning(
                    "Enter team name."
                )

            else:

                teams_collection.insert_one(
                    {
                        "name": team_name,
                        "department": department,
                        "created_at": datetime.now()
                    }
                )

                audit_collection.insert_one(
                    {
                        "action": "CREATE_TEAM",
                        "user": st.session_state.admin_username,
                        "resource": team_name,
                        "timestamp": datetime.now()
                    }
                )

                st.success(
                    "Team added to MongoDB."
                )

        st.markdown("---")

        teams = list(
            teams_collection.find(
                {},
                {
                    "_id": 0,
                    "name": 1,
                    "department": 1,
                    "created_at": 1
                }
            )
        )

        if teams:

            st.dataframe(
                pd.DataFrame(teams),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No teams found."
            )


# =========================================================
# DOCUMENTS
# =========================================================

elif page == "Documents":

    st.title("📄 Document Management")

    if not mongo_connected:

        st.error(
            "MongoDB is not connected."
        )

    else:

        document = st.file_uploader(
            "Upload Document",
            type=[
                "pdf",
                "docx",
                "txt"
            ]
        )

        access_level = st.selectbox(
            "Access Level",
            [
                "All Employees",
                "Department",
                "Managers",
                "Administrators"
            ]
        )

        if st.button(
            "📤 Save Document"
        ):

            if not document:

                st.warning(
                    "Select a document."
                )

            else:

                documents_collection.insert_one(
                    {
                        "filename": document.name,
                        "access_level": access_level,
                        "uploaded_by":
                            st.session_state.admin_username,
                        "uploaded_at": datetime.now()
                    }
                )

                audit_collection.insert_one(
                    {
                        "action": "UPLOAD_DOCUMENT",
                        "user":
                            st.session_state.admin_username,
                        "resource": document.name,
                        "timestamp": datetime.now()
                    }
                )

                st.success(
                    "Document information saved to MongoDB."
                )

        st.markdown("---")

        documents = list(
            documents_collection.find(
                {},
                {
                    "_id": 0,
                    "filename": 1,
                    "access_level": 1,
                    "uploaded_by": 1,
                    "uploaded_at": 1
                }
            )
        )

        if documents:

            st.dataframe(
                pd.DataFrame(documents),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No documents found."
            )


# =========================================================
# WORKFLOWS
# =========================================================

elif page == "Workflows":

    st.title("🔄 Workflow Configuration")

    if not mongo_connected:

        st.error(
            "MongoDB is not connected."
        )

    else:

        workflow_name = st.text_input(
            "Workflow Name",
            placeholder="Leave Approval"
        )

        request_type = st.selectbox(
            "Request Type",
            [
                "Leave",
                "Purchase",
                "Expense",
                "Travel",
                "Access",
                "Document Approval"
            ]
        )

        approver1 = st.selectbox(
            "First Approver",
            [
                "Supervisor",
                "Manager",
                "Department Head"
            ]
        )

        approver2 = st.selectbox(
            "Final Approver",
            [
                "Manager",
                "Department Head",
                "Executive"
            ]
        )

        if st.button(
            "💾 Save Workflow",
            type="primary"
        ):

            if not workflow_name:

                st.warning(
                    "Enter workflow name."
                )

            else:

                workflows_collection.insert_one(
                    {
                        "workflow_name":
                            workflow_name,
                        "request_type":
                            request_type,
                        "steps": [
                            approver1,
                            approver2
                        ],
                        "created_by":
                            st.session_state.admin_username,
                        "created_at":
                            datetime.now()
                    }
                )

                audit_collection.insert_one(
                    {
                        "action": "CREATE_WORKFLOW",
                        "user":
                            st.session_state.admin_username,
                        "resource":
                            workflow_name,
                        "timestamp":
                            datetime.now()
                    }
                )

                st.success(
                    "Workflow saved to MongoDB."
                )

        st.markdown("---")

        workflows = list(
            workflows_collection.find(
                {},
                {
                    "_id": 0,
                    "workflow_name": 1,
                    "request_type": 1,
                    "steps": 1,
                    "created_by": 1,
                    "created_at": 1
                }
            )
        )

        if workflows:

            st.dataframe(
                pd.DataFrame(workflows),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No workflows configured."
            )


# =========================================================
# REPORTS
# =========================================================

elif page == "Reports":

    st.title("📊 Organization Reports")

    if not mongo_connected:

        st.error(
            "MongoDB is not connected."
        )

    else:

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Employees",
                employees_collection.count_documents({})
            )

        with col2:

            st.metric(
                "Documents",
                documents_collection.count_documents({})
            )

        with col3:

            st.metric(
                "Workflows",
                workflows_collection.count_documents({})
            )

        st.markdown("---")

        st.subheader(
            "Employee Distribution"
        )

        pipeline = [
            {
                "$group": {
                    "_id": "$department",
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]

        result = list(
            employees_collection.aggregate(
                pipeline
            )
        )

        if result:

            df = pd.DataFrame(
                result
            ).rename(
                columns={
                    "_id": "Department",
                    "count": "Employees"
                }
            )

            st.bar_chart(
                df.set_index(
                    "Department"
                )
            )

        else:

            st.info(
                "No employee data available."
            )


# =========================================================
# AUDIT LOGS
# =========================================================

elif page == "Audit":

    st.title("🔍 Audit Logs")

    if not mongo_connected:

        st.error(
            "MongoDB is not connected."
        )

    else:

        logs = list(
            audit_collection.find(
                {},
                {
                    "_id": 0,
                    "action": 1,
                    "user": 1,
                    "resource": 1,
                    "timestamp": 1
                }
            )
            .sort(
                "timestamp",
                -1
            )
        )

        if logs:

            st.dataframe(
                pd.DataFrame(logs),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No audit logs available."
            )


# =========================================================
# AI ACTIVITY
# =========================================================

elif page == "AI Activity":

    st.title("🤖 AI Activity")

    if not mongo_connected:

        st.error(
            "MongoDB is not connected."
        )

    else:

        total = ai_collection.count_documents({})

        st.metric(
            "Total AI Queries",
            total
        )

        st.markdown("---")

        queries = list(
            ai_collection.find(
                {},
                {
                    "_id": 0,
                    "user": 1,
                    "question": 1,
                    "response": 1,
                    "timestamp": 1
                }
            )
            .sort(
                "timestamp",
                -1
            )
            .limit(20)
        )

        if queries:

            st.dataframe(
                pd.DataFrame(queries),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No AI activity recorded."
            )
