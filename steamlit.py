import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

# Helper function for grade calculations
def calculate_prelim_grade(absence, exams, quizzes, requirement, recitation):
    # Validate absence
    if absence > 4:
        st.error("Failed due to absence!")
        return None
    
    # Calculate prelim grade based on weights
    prelim_avg = (0.1 * (100 - (10 * absence))) + (0.6 * exams) + \
                 (0.3 * ((0.4 * quizzes) + (0.3 * requirement) + (0.3 * recitation)))
    
    return prelim_avg

# Calculate the minimum midterm grade needed
def calculate_minimum_midterm(prelim, target_grade):
    return max(0, min((target_grade - (prelim * 0.2)) / 0.8, 100))

# Set up the UI layout
st.title("Grade Calculator")

# Input fields
absence = st.number_input("No. of Absences (Max 4)", min_value=0, max_value=4, value=0, step=1)
exams = st.number_input("Exams", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
quizzes = st.number_input("Quizzes", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
requirement = st.number_input("Requirement", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
recitation = st.number_input("Recitation", min_value=0.0, max_value=100.0, value=0.0, step=0.1)

# Calculate Prelim Grade
if st.button("Calculate Prelim Grade"):
    prelim_grade = calculate_prelim_grade(absence, exams, quizzes, requirement, recitation)
    
    if prelim_grade is not None:
        st.write(f"**Calculated Prelim Grade:** {prelim_grade:.2f}")

        # Determine if passed prelim
        if prelim_grade >= 75:
            st.success("Prelim Passed")
        else:
            st.error("Prelim Failed")

        # Calculate minimum midterm grades for passing and Dean's Lister
        min_midterm_pass = calculate_minimum_midterm(prelim_grade, 75)
        min_midterm_dean = calculate_minimum_midterm(prelim_grade, 90)

        # Display min midterm required to pass or to be a Dean's lister
        st.write(f"**Minimum Midterm Grade to Pass:** {min_midterm_pass:.2f}")
        if min_midterm_dean <= 100:
            st.write(f"**Minimum Midterm Grade for Dean's Lister:** {min_midterm_dean:.2f}")
        else:
            st.write("Dean's Lister is not possible with current Prelim Grade.")

# Sliders for Midterm and Final
midterm_grade_pass = st.slider("Midterm Grade (for passing)", 0, 100, int(min_midterm_pass) if 'min_midterm_pass' in locals() else 0)
midterm_grade_dean = st.slider("Midterm Grade (for Dean's Lister)", 0, 100, int(min_midterm_dean) if 'min_midterm_dean' in locals() else 0)

# Calculate Final Grade needed to Pass or to be a Dean's Lister
if 'prelim_grade' in locals():
    final_grade_pass = (75 - (prelim_grade * 0.2) - (midterm_grade_pass * 0.3)) / 0.5
    final_grade_dean = (90 - (prelim_grade * 0.2) - (midterm_grade_dean * 0.3)) / 0.5

    final_grade_pass = np.clip(final_grade_pass, 0, 100)
    final_grade_dean = np.clip(final_grade_dean, 0, 100)

    st.write(f"**Final Grade Needed to Pass:** {final_grade_pass:.2f}")
    st.write(f"**Final Grade Needed for Dean's Lister:** {final_grade_dean:.2f}")

# Visualizing the Grades for Passing
def plot_grade_needed(prelim, target):
    midterm_grades = np.arange(0, 101, 1)
    final_grades = [(target - (prelim * 0.2) - (midterm * 0.3)) / 0.5 for midterm in midterm_grades]
    final_grades = np.clip(final_grades, 0, 100)

    df = pd.DataFrame({'Midterm Grade': midterm_grades, 'Final Grade': final_grades})
    fig = px.scatter(df, x='Midterm Grade', y='Final Grade', title=f'Grades Needed to Achieve {target} Final Grade')
    return fig

# Plot graphs for Passing and Dean's List
if 'prelim_grade' in locals():
    st.plotly_chart(plot_grade_needed(prelim_grade, 75), use_container_width=True)
    st.plotly_chart(plot_grade_needed(prelim_grade, 90), use_container_width=True)
