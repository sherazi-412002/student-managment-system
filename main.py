

# main.py
import streamlit as st
from utils import export_to_pdf, export_to_word, export_to_json
from components import sidebar_inputs, display_marksheet

def main():
    st.set_page_config(
        page_title="Student Result Generator",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
        <style>
        .main { padding: 20px; }
        .sidebar .sidebar-content { padding: 20px; }
        .subject-box { 
            padding: 10px;
            border: 1px solid #ddd;
            margin: 5px 0;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🎓 Student Result Generator")
    
    # Initialize session state
    if 'subjects' not in st.session_state:
        st.session_state.subjects = []
    if 'student_info' not in st.session_state:
        st.session_state.student_info = {}
    if 'show_result' not in st.session_state:
        st.session_state.show_result = False
    
    # Sidebar for inputs
    with st.sidebar:
        student_info, photo = sidebar_inputs()
    
    # Main content area
    if st.session_state.show_result and len(st.session_state.subjects) > 0:
        result_container = display_marksheet(student_info, st.session_state.subjects, photo)
        
        # Export options
        st.markdown("### 📑 Export Result")
        export_col1, export_col2, export_col3 = st.columns(3)
        
        with export_col1:
            if st.button("Export as PDF"):
                pdf_data = export_to_pdf(student_info, st.session_state.subjects, photo)
                st.download_button(
                    label="Download PDF",
                    data=pdf_data,
                    file_name=f"result_{student_info['roll_no']}.pdf",
                    mime="application/pdf"
                )
        
        with export_col2:
            if st.button("Export as Word"):
                word_data = export_to_word(student_info, st.session_state.subjects, photo)
                st.download_button(
                    label="Download Word",
                    data=word_data,
                    file_name=f"result_{student_info['roll_no']}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        
        with export_col3:
            if st.button("Export as JSON"):
                json_data = export_to_json(student_info, st.session_state.subjects)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"result_{student_info['roll_no']}.json",
                    mime="application/json"
                )
    else:
        st.info("👈 Please add subjects and click 'Generate Result' to view the marksheet")


if __name__ == "__main__":
    main()