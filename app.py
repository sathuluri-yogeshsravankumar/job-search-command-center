# Import the Streamlit library and give it the short name "st".
import streamlit as st


# Return the starting sample job applications.
def get_sample_applications():
    # Return a list where each dictionary represents one application.
    return [
        {
            "Company": "Acme Health",
            "Role": "Python Developer",
            "Status": "Applied",
            "Applied Date": "2026-10-21"
        },
        {
            "Company": "Northstar Labs",
            "Role": "Full Stack Engineer",
            "Status": "Interview",
            "Applied Date": "2026-11-06"
        },
        {
            "Company": "Brightline Tech",
            "Role": "Data Analyst",
            "Status": "Follow-up",
            "Applied Date": "2026-11-02"
        },
    ]


# Display metrics calculated from the current application list.
def render_dashboard_summary(applications):
    # Count every application in the list.
    total_applications = len(applications)

    # Count applications whose status is Interview.
    interviews_scheduled = sum(
        1  # Add one for every matching application.
        for application in applications  # Check each application.
        if application["Status"] == "Interview"  # Keep Interview records only.
    )

    # Count applications whose status is Follow-up.
    follow_ups_due = sum(
        1  # Add one for every matching application.
        for application in applications  # Check each application.
        if application["Status"] == "Follow-up"  # Keep Follow-up records only.
    )

    # Create three columns for the metric cards.
    column_one, column_two, column_three = st.columns(3)

    # Show the total number of tracked applications.
    column_one.metric("Total Applications", total_applications)

    # Show the number of interview applications.
    column_two.metric("Interviews Scheduled", interviews_scheduled)

    # Show the number of applications needing follow-up.
    column_three.metric("Follow-ups Due", follow_ups_due)


# Display the form used to add one job application.
def render_add_application_form():
    # Create a form so all inputs are submitted together.
    with st.form("add_application_form"):
        # Ask the user for the company name.
        company = st.text_input("Company name")

        # Ask the user for the job role.
        role = st.text_input("Job role")

        # Let the user choose one application status.
        status = st.selectbox(
            "Application status",
            ["Applied", "Interview", "Follow-up", "Rejected"],
        )

        # Ask the user when they applied for this role.
        applied_date = st.date_input("Date applied")

        # Create the form submit button.
        submitted = st.form_submit_button("Add application")

    # Run this validation only after the button is clicked.
    if submitted:
        # Check that both required text fields contain a value.
        if not company or not role:
            # Show an error if required fields are missing.
            st.error("Please enter both a company name and a job role.")

        # Continue only when the required fields are valid.
        else:
            # Create a dictionary for the new application.
            new_application = {
                "Company": company,
                "Role": role,
                "Status": status,
                # Convert the Python date into a database-friendly ISO date string.
                "Applied Date": applied_date.isoformat(), 
            }

            # Add the new dictionary to the session-state list.
            st.session_state.applications.append(new_application)

            # Store a one-time success message for the next page rerun.
            st.session_state.success_message = (
                f"Added {role} at {company} successfully."
            )

            # Rerun the page so the dashboard metrics update immediately.
            st.rerun()


# Run the Streamlit application.
def main():
    # Configure the browser tab title and page layout.
    st.set_page_config(
        page_title="Job Search Command Center",
        page_icon="💼",
        layout="wide",
    )

    # Create session storage only once per browser session.
    if "applications" not in st.session_state:
        # Start the application with temporary sample data.
        st.session_state.applications = get_sample_applications()

    # Read the current application list from session storage.
    applications = st.session_state.applications

    # Let the user choose which application status to display.
    selected_status = st.sidebar.selectbox(
    "Filter applications by status",
    ["All", "Applied", "Interview", "Follow-up", "Rejected"],
)
    # Show every application when the user chooses All.
    if selected_status == "All":
        filtered_applications = applications

    # Otherwise, keep only applications with the selected status.
    else:
        filtered_applications = [
            application  # Keep the full application dictionary.
            for application in applications  # Check each application.
            if application["Status"] == selected_status  # Match its status.
        ]

    # Show the application title.
    st.title("💼 Job Search Command Center")

    # Explain the purpose of the dashboard.
    st.caption("Track applications, interviews, and follow-up tasks in one place.")

    # Display a success message after an application has been added.
    if "success_message" in st.session_state:
        # Show the stored success message.
        st.success(st.session_state.success_message)

        # Remove the message so it appears only once.
        del st.session_state.success_message

    # Display calculated dashboard metrics.
    render_dashboard_summary(applications)

    # Add a visual separator.
    st.divider()

    # Show the data-entry section heading.
    st.subheader("Add a job application")

    # Display the application form.
    render_add_application_form()

    # Add another visual separator.
    st.divider()

    # Show the saved application section heading.
    st.subheader("Your applications")

    # Display the table only when matching applications exist.
    if filtered_applications:
    # Show the applications that match the selected filter.
        st.dataframe(filtered_applications, use_container_width=True)

# Show a helpful message when no applications match the filter.
    else:
        st.info("No applications match the selected status.")


# Run main only when this file is executed directly.
if __name__ == "__main__":
    # Start the Streamlit application.
    main()