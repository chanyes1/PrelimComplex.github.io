import streamlit as st
import numpy as np

# Function to calculate the preliminary average
def calculate_prelim_avg(grades):
    if len(grades) > 0:
        prelim_avg = np.mean(grades)
        return round(prelim_avg, 2)
    return None

# Function to calculate the minimum midterm grade to pass or be a Dean's Lister
def calculate_required_midterm(prelim):
    # Calculate the minimum midterm grades required to pass and be a Dean's Lister
    min_midterm_pass = (75 - (prelim * 0.2)) / 0.8
    min_midterm_dean = (90 - (prelim * 0.2)) / 0.8

    min_midterm_pass = max(0, min(min_midterm_pass, 100))
    min_midterm_dean = max(0, min(min_midterm_dean, 100))

    return round(min_midterm_pass, 2), round(min_midterm_dean, 2)

# Function to calculate the required final grade based on midterm performance
def calculate_final_grade(prelim, midterm, target):
    required_final = (target - (prelim * 0.2) - (midterm * 0.3)) / 0.5
    required_final = max(0, min(required_final, 100))
    return round(required_final, 2)

# Streamlit app layout
st.title('Grade Calculator')

# Input section for Prelim Grades and Prelim Average Calculation
st.header("Preliminary Grades")
grades_input = st.text_input("Enter your prelim grades separated by commas (e.g., 85, 90, 78)", "")
if st.button('Calculate Prelim Average'):
    try:
        grades = [float(g) for g in grades_input.split(',')]
        prelim_avg = calculate_prelim_avg(grades)
        if prelim_avg is not None:
            st.success(f'Your Prelim Average is: {prelim_avg}')
        else:
            st.error('Please enter valid grades.')
    except:
        st.error('Please enter valid numeric grades.')

# Input section for calculating the required midterm grades
st.header("Required Midterm Grades")
prelim_input = st.text_input("Enter your Prelim Average", "")
if st.button('Calculate Midterm Requirements'):
    try:
        prelim = float(prelim_input)
        min_midterm_pass, min_midterm_dean = calculate_required_midterm(prelim)
        st.success(f'Minimum Midterm Grade to Pass: {min_midterm_pass}')
        st.success(f'Minimum Midterm Grade to be a Dean\'s Lister: {min_midterm_dean}')
    except:
        st.error('Please enter a valid Prelim Average.')

# Input section for calculating the required final grade based on target
st.header("Final Grade Requirement")
midterm_input = st.text_input("Enter your Midterm Grade", "")
target_input = st.text_input("Enter your target final grade", "")
if st.button('Calculate Final Requirement'):
    try:
        prelim = float(prelim_input)
        midterm = float(midterm_input)
        target = float(target_input)
        required_final = calculate_final_grade(prelim, midterm, target)
        st.success(f'Required Final Grade to achieve target: {required_final}')
    except:
        st.error('Please enter valid numeric values for prelim, midterm, and target grades.')

