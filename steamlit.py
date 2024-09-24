import streamlit as st
import numpy as np

# Function to calculate grades
def calculate_grades(prelim1, prelim2, prelim3, prelim4, prelim5):
    if prelim1 > 4:
        return "Failed", None, None, None, None
    if prelim1 < 0:
        return "Please insert a valid absence", None, None, None, None

    if prelim2 < 0 or prelim2 > 100:
        return "Please insert a valid grade for Exams", None, None, None, None
    if prelim3 < 0 or prelim3 > 100:
        return "Please insert a valid grade for Quizzes", None, None, None, None
    if prelim4 < 0 or prelim4 > 100:
        return "Please insert a valid grade for Requirement", None, None, None, None
    if prelim5 < 0 or prelim5 > 100:
        return "Please insert a valid grade for Recitation", None, None, None, None

    # Calculate the Prelim Average
    prelim_average = (0.1 * (100 - (10 * prelim1))) + (0.6 * prelim2) + (0.3 * ((0.4 * prelim3) + (0.3 * prelim4) + (0.3 * prelim5)))
    
    # Determine if Prelim is Passed or Failed
    if prelim_average >= 75:
        prelim_status = "Prelim Passed"
    else:
        prelim_status = "Prelim Failed"

    return prelim_status, prelim_average

# Streamlit UI
st.title("Grade Calculator")

# Input for Absences and Grades
prelim1 = st.number_input("Enter absence for Prelim 1 (0-4):", min_value=0.0, max_value=4.0, value=0.0)
prelim2 = st.number_input("Enter grade for Exams (0-100):", min_value=0.0, max_value=100.0, value=0.0)
prelim3 = st.number_input("Enter grade for Quizzes (0-100):", min_value=0.0, max_value=100.0, value=0.0)
prelim4 = st.number_input("Enter grade for Requirement (0-100):", min_value=0.0, max_value=100.0, value=0.0)
prelim5 = st.number_input("Enter grade for Recitation (0-100):", min_value=0.0, max_value=100.0, value=0.0)

# Button to Calculate
if st.button("Calculate Prelim Grade"):
    prelim_status, prelim_average = calculate_grades(prelim1, prelim2, prelim3, prelim4, prelim5)
    
    # Display results
    if prelim_average is not None:
        st.write(f"Prelim Average: {prelim_average:.2f}")
    st.write(prelim_status)

    if prelim_average is not None:
        # Calculate minimum midterm grades
        min_midterm_pass = (75 - (prelim_average * 0.2)) / 0.8
        min_midterm_dean = (90 - (prelim_average * 0.2)) / 0.8

        # Ensure midterm grades are within valid range (0-100)
        min_midterm_pass = max(0, min(min_midterm_pass, 100))

        if min_midterm_dean > 100:
            st.write("Dean's lister is not possible with your grade.")
            min_midterm_dean = None
        else:
            min_midterm_dean = max(0, min(min_midterm_dean, 100))
            st.write(f"Minimum Midterm Grade to be Dean's Lister: {min_midterm_dean:.2f}")

        st.write(f"Minimum Midterm Grade to Pass: {min_midterm_pass:.2f}")

        # Calculate Finals Requirements
        if min_midterm_dean is not None:
            final_dean = (90 - (prelim_average * 0.2) - (min_midterm_dean * 0.3)) / 0.5
            final_dean = max(0, min(final_dean, 100))
            st.write(f"To be a Dean's Lister, you need a midterm of {min_midterm_dean:.2f} and a final of {final_dean:.1f}.")

        final_pass = (75 - (prelim_average * 0.2) - (min_midterm_pass * 0.3)) / 0.5
        final_pass = max(0, min(final_pass, 100))
        st.write(f"To pass, you need a midterm of {min_midterm_pass:.2f} and a final of {final_pass:.1f}.")

# Optionally, add more visualizations or graphs using libraries like matplotlib or Plotly
