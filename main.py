import streamlit as st  # type: ignore


def main():
    st.set_page_config(
        page_title="Appointment System",
        page_icon="👋",
    )

    with st.sidebar:
        st.page_link("main.py", label="Appointment System")
        st.page_link("pages/clients.py", label="Clients Manager")
        st.page_link("pages/services.py", label="Services Manager")

    st.header("Appointment System")
    st.subheader("By: Danilo")

    st.write(
        "This is a simple project that was created to manage appointments. Navigate using the sidebar."
    )


if __name__ == "__main__":
    main()
