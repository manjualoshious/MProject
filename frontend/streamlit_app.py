import streamlit as st
import requests


# =================================
# Page Configuration
# =================================

st.set_page_config(
    page_title="AI Orchestration System",
    page_icon="🤖",
    layout="wide"
)


# =================================
# Backend URL
# =================================

API_URL = "https://mproject-knzg.onrender.com"


# =================================
# Session State
# =================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "username" not in st.session_state:
    st.session_state.username = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# =================================
# CSS
# =================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111827 !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    /* Expanders */
    [data-testid="stSidebar"] details {
        background-color: #111827 !important;
        border: none !important;
        margin-bottom: 5px !important;
    }

    [data-testid="stSidebar"] details summary {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        padding: 8px 10px !important;
    }

    [data-testid="stSidebar"] details summary p {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    [data-testid="stSidebar"] details summary svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #374151 !important;
        border-radius: 5px !important;
        font-size: 12px !important;
        padding: 5px 8px !important;
        min-height: 30px !important;
    }

    [data-testid="stSidebar"] .stButton > button p {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #374151 !important;
        color: #ffffff !important;
        border-color: #4b5563 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #374151 !important;
        margin: 7px 0 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =================================
# Main Title
# =================================

st.title("🤖 AI Orchestration System")


# =================================
# SIDEBAR
# =================================

st.sidebar.title("Menu")


# =================================
# NOT LOGGED IN
# =================================

if not st.session_state.logged_in:

    menu = st.sidebar.radio(
        "Select",
        ["Register", "Login"]
    )


# =================================
# LOGGED IN
# =================================

else:

    # -----------------------------
    # Dashboard
    # -----------------------------

    if st.sidebar.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
        st.rerun()


    # -----------------------------
    # AI Assistant
    # -----------------------------

    with st.sidebar.expander("🤖 AI Assistant", expanded=False):

        if st.button(
            "💬 Ask AI",
            use_container_width=True,
            key="ask_ai_menu"
        ):
            st.session_state.page = "Ask AI"
            st.rerun()

        if st.button(
            "🔍 Search Knowledge",
            use_container_width=True,
            key="search_knowledge_menu"
        ):
            st.session_state.page = "Search Knowledge"
            st.rerun()


    # -----------------------------
    # Work Management
    # -----------------------------

    with st.sidebar.expander("📋 Work Management", expanded=False):

        if st.button(
            "📌 My Tasks",
            use_container_width=True,
            key="my_tasks_menu"
        ):
            st.session_state.page = "My Tasks"
            st.rerun()

        if st.button(
            "📝 My Requests",
            use_container_width=True,
            key="my_requests_menu"
        ):
            st.session_state.page = "My Requests"
            st.rerun()


    # -----------------------------
    # Documents
    # -----------------------------

    with st.sidebar.expander("📄 Documents", expanded=False):

        if st.button(
            "📁 My Documents",
            use_container_width=True,
            key="my_documents_menu"
        ):
            st.session_state.page = "My Documents"
            st.rerun()

        if st.button(
            "⬆️ Upload Document",
            use_container_width=True,
            key="upload_document_menu"
        ):
            st.session_state.page = "Upload Document"
            st.rerun()


    st.sidebar.markdown("---")


    # -----------------------------
    # Logout
    # -----------------------------

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True,
        key="logout_menu"
    ):
        st.session_state.logged_in = False
        st.session_state.access_token = None
        st.session_state.username = None
        st.session_state.page = "Dashboard"
        st.rerun()


# =================================
# REGISTER
# =================================

if not st.session_state.logged_in and menu == "Register":

    st.header("👤 User Registration")

    username = st.text_input(
        "Username"
    )

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    role = st.selectbox(
        "Role",
        ["user", "admin"]
    )

    if st.button("Register"):

        if (
            username.strip() == ""
            or email.strip() == ""
            or password.strip() == ""
        ):

            st.warning(
                "Please fill all required fields."
            )

        else:

            data = {
                "username": username,
                "email": email,
                "password": password,
                "role": role
            }

            try:

                response = requests.post(
                    f"{API_URL}/register",
                    json=data,
                    timeout=30
                )

                if response.status_code == 200:

                    st.success(
                        "✅ Registration Successful!"
                    )

                    try:

                        st.json(
                            response.json()
                        )

                    except ValueError:

                        st.write(
                            response.text
                        )

                else:

                    try:

                        error = response.json()

                        st.error(
                            error.get(
                                "detail",
                                "Registration failed"
                            )
                        )

                    except ValueError:

                        st.error(
                            f"Registration failed "
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
                    "Please check the FastAPI server."
                )


# =================================
# LOGIN
# =================================

elif not st.session_state.logged_in and menu == "Login":

    st.header("🔐 User Login")

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if (
            email.strip() == ""
            or password.strip() == ""
        ):

            st.warning(
                "Please enter email and password."
            )

        else:

            data = {
                "email": email,
                "password": password
            }

            try:

                response = requests.post(
                    f"{API_URL}/login",
                    json=data,
                    timeout=30
                )

                if response.status_code == 200:

                    result = response.json()

                    st.session_state.access_token = (
                        result["access_token"]
                    )

                    st.session_state.logged_in = True

                    # Use username returned by backend
                    st.session_state.username = (
                        result.get("username", email)
                    )

                    st.session_state.page = "Dashboard"

                    st.success(
                        "✅ Login Successful!"
                    )

                    st.rerun()

                else:

                    try:

                        error = response.json()

                        st.error(
                            error.get(
                                "detail",
                                "Login failed"
                            )
                        )

                    except ValueError:

                        st.error(
                            f"Login failed "
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
                    "Please check the FastAPI server."
                )


# =================================
# AUTHORIZATION HEADER
# =================================

headers = {
    "Authorization": (
        f"Bearer {st.session_state.access_token}"
    )
}


# =================================
# DASHBOARD
# =================================

if st.session_state.logged_in:

    page = st.session_state.page


    # =================================
    # DASHBOARD PAGE
    # =================================

    if page == "Dashboard":

        st.header("📊 Dashboard")

        st.success(
            f"Welcome, {st.session_state.username}! 👋"
        )

        st.markdown("---")

        st.subheader(
            "Welcome to AI Orchestration System"
        )

        st.write(
            """
            Use the menu on the left to access your
            AI assistant, work management and documents.
            """
        )

        # Small overview
        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("🤖\n\n**AI Assistant**\n\nAsk AI and search organizational knowledge.")

        with col2:
            st.info("📋\n\n**Work Management**\n\nView your tasks and requests.")

        with col3:
            st.info("📄\n\n**Documents**\n\nManage and upload documents.")


    # =================================
    # ASK AI
    # =================================

    elif page == "Ask AI":

        st.header("🤖 Ask AI")

        st.write(
            "Ask the AI assistant a question."
        )

        question = st.text_area(
            "Enter your question",
            placeholder=(
                "Example: What is Artificial Intelligence?"
            ),
            height=120
        )

        if st.button(
            "🤖 Ask AI",
            key="ask_ai_button"
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
                        headers=headers,
                        timeout=60
                    )

                    if response.status_code == 200:

                        result = response.json()

                        st.success(
                            "✅ AI Response"
                        )

                        st.write(
                            result.get(
                                "answer",
                                "No answer received."
                            )
                        )

                    else:

                        st.error(
                            f"❌ AI request failed "
                            f"(HTTP {response.status_code})"
                        )

                        st.code(
                            response.text
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ Cannot connect to FastAPI server."
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "❌ AI request timed out."
                    )


    # =================================
    # SEARCH KNOWLEDGE
    # =================================

    elif page == "Search Knowledge":

        st.header("🔍 Search Knowledge")

        st.write(
            "Search information from authorized organizational documents."
        )

        search_query = st.text_input(
            "Enter your search query",
            placeholder="Example: Leave policy"
        )

        if st.button(
            "🔍 Search",
            key="search_button"
        ):

            if search_query.strip() == "":

                st.warning(
                    "Please enter a search query."
                )

            else:

                st.info(
                    "Knowledge search will be connected "
                    "to the document/RAG system."
                )

                st.write(
                    f"Search query: **{search_query}**"
                )


    # =================================
    # MY TASKS
    # =================================

    elif page == "My Tasks":

        st.header("📌 My Tasks")

        st.write(
            "Tasks assigned to you."
        )

        st.info(
            "Task management will be connected to MongoDB."
        )

        st.markdown(
            """
            **Example task information**

            - Task Title
            - Description
            - Priority
            - Due Date
            - Status
            """
        )


    # =================================
    # MY REQUESTS
    # =================================

    elif page == "My Requests":

        st.header("📝 My Requests")

        st.write(
            "Submit and track your organizational requests."
        )

        request_type = st.selectbox(
            "Request Type",
            [
                "Leave",
                "Purchase",
                "Expense",
                "Travel",
                "Resource",
                "Document Approval"
            ]
        )

        description = st.text_area(
            "Request Description",
            placeholder="Enter request details..."
        )

        if st.button(
            "Submit Request",
            key="submit_request"
        ):

            if description.strip() == "":

                st.warning(
                    "Please enter the request description."
                )

            else:

                st.success(
                    f"✅ {request_type} request submitted."
                )

                st.info(
                    "Workflow processing will be connected "
                    "to MongoDB/FastAPI."
                )


    # =================================
    # MY DOCUMENTS
    # =================================

    elif page == "My Documents":

        st.header("📁 My Documents")

        st.write(
            "Documents available to you."
        )

        st.info(
            "Documents will be retrieved from MongoDB."
        )

        st.markdown(
            """
            **Document information**

            - Document Name
            - Document Type
            - Uploaded By
            - Uploaded Date
            - Access Level
            """
        )


    # =================================
    # UPLOAD DOCUMENT
    # =================================

    elif page == "Upload Document":

        st.header("⬆️ Upload Document")

        st.write(
            "Upload a PDF document to the AI Orchestration System."
        )

        uploaded_file = st.file_uploader(
            "Choose a PDF document",
            type=["pdf"]
        )

        if uploaded_file is not None:

            st.info(
                f"Selected file: {uploaded_file.name}"
            )

            if st.button(
                "📤 Upload Document",
                key="upload_document_button"
            ):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                }

                try:

                    response = requests.post(
                        f"{API_URL}/documents/upload",
                        files=files,
                        headers=headers,
                        timeout=60
                    )

                    if response.status_code == 200:

                        st.success(
                            "✅ Document uploaded successfully!"
                        )

                        try:

                            st.json(
                                response.json()
                            )

                        except ValueError:

                            st.write(
                                response.text
                            )

                    else:

                        st.error(
                            f"❌ Upload failed "
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
                        "❌ Document upload timed out."
                    )