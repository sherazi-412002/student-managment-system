import streamlit as st
import pandas as pd
from PIL import Image
from utils import calculate_grade, calculate_percentage

def sidebar_inputs():
    """Handle all sidebar inputs"""
    st.markdown("## Enter Student Details")
    
    # Student details section
    student_info = {
        "name": st.text_input("Student Name", key="student_name"),
        "roll_no": st.text_input("Roll Number", key="roll_no"),
        "class": st.text_input("Class", key="class"),
        "academic_year": st.text_input("Academic Year", key="academic_year")
    }
    
    # Photo upload section
    st.markdown("---")
    st.markdown("## Student Photo")
    photo = st.file_uploader("Upload Photo", type=['jpg', 'png', 'jpeg'], key="photo")
    
    # Multiple subjects input section
    st.markdown("---")
    st.markdown("## Add Multiple Subjects")
    
    # Dynamic subject addition
    with st.form(key="subject_form"):
        subject_name = st.text_input("Subject Name")
        col1, col2 = st.columns(2)
        with col1:
            obtained_marks = st.number_input("Obtained Marks", min_value=0, max_value=100)
        with col2:
            total_marks = st.number_input("Total Marks", min_value=1, value=100)
        
        submit_subject = st.form_submit_button("Add Subject")
        if submit_subject and subject_name:
            st.session_state.subjects.append({
                "subject": subject_name,
                "obtained_marks": obtained_marks,
                "total_marks": total_marks
            })
            st.success(f"Added {subject_name}")
    
    # Display and manage existing subjects
    if st.session_state.subjects:
        st.markdown("### Manage Subjects")
        
        # Display subjects with checkboxes for selection
        selected_subjects = []
        for idx, subject in enumerate(st.session_state.subjects):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{subject['subject']}: {subject['obtained_marks']}/{subject['total_marks']}")
            with col2:
                if st.checkbox("Select", key=f"select_{idx}"):
                    selected_subjects.append(idx)
        
        # Actions for selected subjects
        if selected_subjects:
            if st.button("Remove Selected Subjects"):
                st.session_state.subjects = [
                    subject for idx, subject in enumerate(st.session_state.subjects)
                    if idx not in selected_subjects
                ]
                st.success("Selected subjects removed!")
        
        if st.button("Clear All Subjects"):
            st.session_state.subjects = []
            st.success("All subjects cleared!")
    
    # Generate Result button
    if st.session_state.subjects:
        if st.button("Generate Result"):
            st.session_state.show_result = True
    
    return student_info, photo

def display_marksheet(student_info, subjects, photo):
    """Display the complete marksheet"""
    st.markdown("## 📄 Student Marksheet")
    
    # Student info and photo section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Student Information")
        st.write(f"**Name:** {student_info['name']}")
        st.write(f"**Roll Number:** {student_info['roll_no']}")
        st.write(f"**Class:** {student_info['class']}")
        st.write(f"**Academic Year:** {student_info['academic_year']}")
    
    with col2:
        if photo is not None:
            try:
                image = Image.open(photo)
                st.image(image, width=150, caption="Student Photo")
            except Exception as e:
                st.error("Error loading photo")
    
    # Results section
    st.markdown("---")
    st.markdown("### Subject Wise Results")
    
    if subjects:
        # Create DataFrame
        df = pd.DataFrame(subjects)
        df["Percentage"] = df.apply(
            lambda x: calculate_percentage(x["obtained_marks"], x["total_marks"]),
            axis=1
        )
        df["Grade"] = df["Percentage"].apply(lambda x: calculate_grade(x)[0])
        
        # Display styled DataFrame
        st.dataframe(
            df.style.format({
                "Percentage": "{:.2f}%"
            }).set_properties(**{
                'background-color': 'white',
                'color': 'black'
            }),
            use_container_width=True
        )
        
        # Calculate overall results
        total_obtained = df["obtained_marks"].sum()
        total_marks = df["total_marks"].sum()
        overall_percentage = calculate_percentage(total_obtained, total_marks)
        overall_grade, remarks = calculate_grade(overall_percentage)
        
        # Display overall results
        st.markdown("### Overall Result")
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            st.metric("Total Marks", f"{total_obtained}/{total_marks}")
        with metrics_col2:
            st.metric("Overall Percentage", f"{overall_percentage:.2f}%")
        with metrics_col3:
            st.metric("Overall Grade", overall_grade)
        
        st.markdown(f"**Remarks:** {remarks}")
    else:
        st.warning("No subjects added yet!")