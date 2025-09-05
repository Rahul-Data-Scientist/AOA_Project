import streamlit as st

# Page configuration
st.set_page_config(page_title="Optimal Package Selection", page_icon="📦", layout="centered")

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


def knapsack(values, weights, capacity):
    n = len(values)
    
    # DP table
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], 
                               dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtrack to find selected items
    res = dp[n][capacity]
    w = capacity
    chosen_items = []
    
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == dp[i - 1][w]:
            continue
        else:
            chosen_items.append(i - 1)
            res -= values[i - 1]
            w -= weights[i - 1]

    chosen_items.reverse()

    # Manager-style descriptive output
    if chosen_items:
        items_desc = []
        for i in chosen_items:
            items_desc.append(f"a package worth {values[i]} units with weight {weights[i]}")
        
        if len(items_desc) > 1:
            items_text = ", ".join(items_desc[:-1]) + f", and {items_desc[-1]}"
        else:
            items_text = items_desc[0]
        
        return (f"📦 After evaluating the available packages and the vehicle's capacity of {capacity}, "
                f"the most valuable loading plan will give us a total declared value of 💰 {dp[n][capacity]}. "
                f"This can be achieved by selecting {items_text}.")
    else:
        return (f"⚠️ Given the vehicle's capacity of {capacity}, no combination of packages "
                f"can provide a positive declared value.")


# ---- App Title ----
st.title("📦 Optimal Package Selection for Shipping")
st.write("Use this tool to determine the **best combination of packages** to maximize value within your vehicle's capacity.")


# ---- Inputs ----
st.subheader("Enter Package Details")

col1, col2 = st.columns(2)
with col1:
    value = st.text_input("Enter values of packages (space separated)", placeholder="e.g. 60 100 120")
with col2:
    weight = st.text_input("Enter weights of packages (space separated)", placeholder="e.g. 10 20 30")

capacity = st.text_input("Enter vehicle capacity", placeholder="e.g. 50")


# ---- Button ----
if st.button("🚀 Get the Best Combination"):
    val = [int(i) for i in value.split()]
    wt = [int(w) for w in weight.split()]
    cap = int(capacity.split()[0])

    # Get result
    result_text = knapsack(val, wt, cap)

    # Styled result box (all-in-one)
    st.markdown(f"<div class='result-box'>{result_text}</div>", unsafe_allow_html=True)

    # Full Code Section
    st.subheader("📝 Full Code Implementation")
    full_code = '''
    import streamlit as st

    def knapsack(values, weights, capacity):
        n = len(values)
        
        # DP table
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        # Fill DP table
        for i in range(1, n + 1):
            for w in range(1, capacity + 1):
                if weights[i - 1] <= w:
                    dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], 
                                dp[i - 1][w])
                else:
                    dp[i][w] = dp[i - 1][w]

        # Backtrack to find selected items
        res = dp[n][capacity]
        w = capacity
        chosen_items = []
        
        for i in range(n, 0, -1):
            if res <= 0:
                break
            if res == dp[i - 1][w]:
                continue
            else:
                chosen_items.append(i - 1)
                res -= values[i - 1]
                w -= weights[i - 1]

        chosen_items.reverse()

        # Manager-style descriptive output
        if chosen_items:
            items_desc = []
            for i in chosen_items:
                items_desc.append(f"a package worth {values[i]} units with weight {weights[i]}")
            
            if len(items_desc) > 1:
                items_text = ", ".join(items_desc[:-1]) + f", and {items_desc[-1]}"
            else:
                items_text = items_desc[0]
            
            return (f"After evaluating the available packages and the vehicle's capacity of {capacity}, "
                    f"the most valuable loading plan will give us a total declared value of {dp[n][capacity]}. "
                    f"This can be achieved by selecting {items_text}.")
        else:
            return (f"Given the vehicle's capacity of {capacity}, no combination of packages "
                    f"can provide a positive declared value.")


    st.title("Optimal Package Selection for Shipping")

    value = st.text_input("Enter value of each package")
    weight = st.text_input("Enter weight of each package")
    capacity = st.text_input("Enter the capacity")

    if st.button("Get the best combination"):
        st.write("Time complexity: O(n * capacity)")
        st.write("We fill a DP table of size n * capacity, and each cell computation takes O(1). Hence, total time = O(n * capacity). The backtracking step takes at most O(n).")
        st.write("")

        st.write("Space Complexity: O(n * capacity)")
        st.write("We maintain a 2D DP table of size (n+1) * (capacity+1), so space = O(n * capacity). The extra backtracking storage for chosen items is O(n), which is negligible compared to DP table.")
        st.write("")

        val = value.split()
        val = [int(i) for i in val]
        wt = weight.split()
        wt = [int(w) for w in wt]
        cap = int(capacity.split()[0])

        st.write(knapsack(val, wt, cap))
    '''
    st.code(full_code, language="python")

    # Complexity Info
    st.subheader("📊 Complexity Analysis")
    st.info("⏱ **Time Complexity:** O(n * capacity) — Filling DP table with n * capacity entries. Each entry computed in O(1). Backtracking is O(n).")
    st.info("💾 **Space Complexity:** O(n * capacity) — DP table size (n+1) * (capacity+1). Additional backtracking storage O(n).")
