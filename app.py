
import streamlit as st
from pathlib import Path

# Page Configuration
st.set_page_config(
    page_title="FileFlow | Smart File Manager",
    page_icon="📁",
    layout="wide"
)

# File storage folder
BASE_DIR = Path("user_files")
BASE_DIR.mkdir(parents=True, exist_ok=True)

# Custom CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #1b2140);
    color: white;
}
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #a78bfa;
}
.subtitle {
    color: #b8c1d9;
    font-size: 16px;
}
div.stButton > button {
    border-radius: 10px;
    background: #7955e8;
    color: white;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}
div.stButton > button:hover {
    background: #9675ff;
    color: white;
}
[data-testid="stMetric"] {
    background: #252d49;
    padding: 18px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# Helper Function
def get_file(name):
    name = name.strip()

    if not name or Path(name).name != name or name in (".", ".."):
        return None

    return BASE_DIR / name


# Header
st.markdown(
    '<div class="main-title">📁 FileFlow</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your Smart File Management System | Built with Python & Streamlit</div>',
    unsafe_allow_html=True
)

st.divider()

# Sidebar
st.sidebar.title("📂 FileFlow")
st.sidebar.caption("SMART FILE MANAGER")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Create File",
        "Read File",
        "Update File",
        "Delete File"
    ]
)

# File List (Alphabetically Sorted)
files = sorted(
    [p for p in BASE_DIR.iterdir() if p.is_file()],
    key=lambda p: p.name.lower()
)

# Dashboard
if menu == "Dashboard":

    st.subheader("Welcome to FileFlow 👋")
    st.write("Manage your files easily from one place.")

    col1, col2, col3 = st.columns(3)

    total_size = sum(p.stat().st_size for p in files)
    storage_kb = total_size / 1024

    col1.metric("Total Files", len(files))
    col2.metric("Storage Used", f"{storage_kb:.2f} KB")
    col3.metric("Available Actions", "4")

    st.divider()

    st.subheader("📂 Your Files")

    if files:
        for file in files:
            st.markdown(f"📄 **{file.name}**")
    else:
        st.info("No files found. Create your first file!")


# Create File
elif menu == "Create File":

    st.subheader("➕ Create New File")

    name = st.text_input("Enter file name", placeholder="example.txt")
    content = st.text_area("Write your content", height=180)

    if st.button("Create File"):

        file = get_file(name)

        if file is None:
            st.error("Please enter a valid file name.")

        elif file.exists():
            st.error("This file already exists!")

        else:
            try:
                with file.open("x", encoding="utf-8") as f:
                    f.write(content)

                st.success("File created successfully! 🎉")

            except OSError as err:
                st.error(f"Error: {err}")


# Read File
elif menu == "Read File":

    st.subheader("📖 Read Your File")

    if files:
        selected = st.selectbox(
            "Select a file",
            [f.name for f in files]
        )

        if st.button("Read File"):
            file = get_file(selected)

            try:
                content = file.read_text(encoding="utf-8")
                st.text_area("File Content", content, height=250)

            except OSError as err:
                st.error(f"Error: {err}")

    else:
        st.info("No files available to read.")


# Update File
elif menu == "Update File":

    st.subheader("✏️ Update Your File")

    if files:
        selected = st.selectbox(
            "Select a file",
            [f.name for f in files]
        )

        operation = st.radio(
            "Choose Operation",
            ["Append Content", "Overwrite Content", "Rename File"]
        )

        if operation == "Append Content":

            content = st.text_area("Enter additional content")

            if st.button("Append"):
                file = get_file(selected)

                try:
                    with file.open("a", encoding="utf-8") as f:
                        f.write("\n" + content)

                    st.success("Content appended successfully!")

                except OSError as err:
                    st.error(str(err))

        elif operation == "Overwrite Content":

            content = st.text_area("Enter new content")

            if st.button("Overwrite"):
                file = get_file(selected)

                try:
                    file.write_text(content, encoding="utf-8")
                    st.success("File overwritten successfully!")

                except OSError as err:
                    st.error(str(err))

        elif operation == "Rename File":

            new_name = st.text_input("Enter new file name")

            if st.button("Rename"):
                old_file = get_file(selected)
                new_file = get_file(new_name)

                if new_file is None:
                    st.error("Invalid file name.")

                elif new_file.exists():
                    st.error("A file with this name already exists!")

                else:
                    try:
                        old_file.rename(new_file)
                        st.success("File renamed successfully!")

                    except OSError as err:
                        st.error(str(err))

    else:
        st.info("No files available to update.")


# Delete File
elif menu == "Delete File":

    st.subheader("🗑️ Delete File")

    if files:
        selected = st.selectbox(
            "Select file to delete",
            [f.name for f in files]
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this file."
        )

        if st.button("Delete File", disabled=not confirm):
            file = get_file(selected)

            try:
                file.unlink()
                st.success("File deleted successfully!")

            except OSError as err:
                st.error(str(err))

    else:
        st.info("No files available to delete.")


# Footer
st.divider()

st.markdown(
    "<center>Made with ❤️ using Python & Streamlit | FileFlow</center>",
    unsafe_allow_html=True
)
