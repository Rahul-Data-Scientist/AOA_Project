import streamlit as st

# Page configuration
st.set_page_config(page_title="Optimal Course Selection", page_icon="🎓", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .result-box {
        background-color: #ffffff;
        padding: 20px;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        font-size: 16px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)


def course_selection(course_names, values, credits, max_credits):
    n = len(values)
    
    # DP table
    dp = [[0] * (max_credits + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        for c in range(1, max_credits + 1):
            if credits[i - 1] <= c:
                dp[i][c] = max(values[i - 1] + dp[i - 1][c - credits[i - 1]], 
                               dp[i - 1][c])
            else:
                dp[i][c] = dp[i - 1][c]

    # Backtrack to find selected courses
    res = dp[n][max_credits]
    c = max_credits
    chosen = []
    
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == dp[i - 1][c]:
            continue
        else:
            chosen.append(i - 1)
            res -= values[i - 1]
            c -= credits[i - 1]

    chosen.reverse()

    # Build descriptive advice
    if chosen:
        course_list = []
        for i in chosen:
            course_list.append(f"**{course_names[i]}** ({credits[i]} credits, academic value {values[i]})")
        
        if len(course_list) == 1:
            courses_text = course_list[0]
        else:
            courses_text = ", ".join(course_list[:-1]) + f", and {course_list[-1]}"

        return (f"🎓 To maximize your learning this semester within a limit of {max_credits} credits, "
                f"you should enroll in {courses_text}. "
                f"This plan will give you the **maximum achievable academic value of {dp[n][max_credits]}**.")
    else:
        return (f"⚠️ Given your credit limit of {max_credits}, no combination of courses "
                f"provides additional academic value.")


# ---- App Title ----
st.title("🎓 Optimal Course Selection Advisor")
st.write("This tool helps you choose the **best combination of courses** to maximize learning or GPA within your semester credit limit.")


# ---- Inputs ----
st.subheader("Enter Course Details")

col1, col2, col3 = st.columns(3)
with col1:
    course_names = st.text_area("Enter course names (comma separated)", placeholder="e.g. Data Science, Algorithms, Machine Learning")
with col2:
    values = st.text_input("Enter academic values (space separated)", placeholder="e.g. 60 100 120")
with col3:
    credits = st.text_input("Enter credit hours (space separated)", placeholder="e.g. 10 20 30")

max_credits = st.text_input("Enter maximum credits allowed", placeholder="e.g. 50")


# ---- Button ----
if st.button("📊 Get the Best Course Plan"):
    course_list = [c.strip() for c in course_names.split(",") if c.strip()]
    val = [int(i) for i in values.split()]
    cr = [int(c) for c in credits.split()]
    cap = int(max_credits.split()[0])

    # Get result
    result_text = course_selection(course_list, val, cr, cap)

    # Styled result box
    st.markdown(f"<div class='result-box'>{result_text}</div>", unsafe_allow_html=True)

    # Full Code Section
    st.subheader("📝 Full Code Implementation")
    full_code = '''
    def course_selection(course_names, values, credits, max_credits):
    n = len(values)
    
    # DP table
    dp = [[0] * (max_credits + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        for c in range(1, max_credits + 1):
            if credits[i - 1] <= c:
                dp[i][c] = max(values[i - 1] + dp[i - 1][c - credits[i - 1]], 
                               dp[i - 1][c])
            else:
                dp[i][c] = dp[i - 1][c]

    # Backtrack to find selected courses
    res = dp[n][max_credits]
    c = max_credits
    chosen = []
    
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == dp[i - 1][c]:
            continue
        else:
            chosen.append(i - 1)
            res -= values[i - 1]
            c -= credits[i - 1]

    chosen.reverse()

    # Build descriptive advice
    if chosen:
        course_list = []
        for i in chosen:
            course_list.append(f"**{course_names[i]}** ({credits[i]} credits, academic value {values[i]})")
        
        if len(course_list) == 1:
            courses_text = course_list[0]
        else:
            courses_text = ", ".join(course_list[:-1]) + f", and {course_list[-1]}"

        return (f"🎓 To maximize your learning this semester within a limit of {max_credits} credits, "
                f"you should enroll in {courses_text}. "
                f"This plan will give you the **maximum achievable academic value of {dp[n][max_credits]}**.")
    else:
        return (f"⚠️ Given your credit limit of {max_credits}, no combination of courses "
                f"provides additional academic value.")
    '''
    st.code(full_code, language="python")

    # Complexity Info
    st.subheader("📊 Complexity Analysis")
    st.info("⏱ **Time Complexity:** O(n * max_credits) — We fill a DP table of size n * max_credits, each entry computed in O(1). Backtracking takes O(n).")
    st.info("💾 **Space Complexity:** O(n * max_credits) — We maintain a DP table of size (n+1) * (max_credits+1). Backtracking needs O(n) extra space, which is negligible.")
