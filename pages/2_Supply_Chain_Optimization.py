import streamlit as st

# Page configuration
st.set_page_config(page_title="Supply Chain Optimization", page_icon="🏭", layout="centered")

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


def supply_chain_optimization(materials, benefits, costs, budget):
    n = len(benefits)
    
    # DP table
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        for b in range(1, budget + 1):
            if costs[i - 1] <= b:
                dp[i][b] = max(benefits[i - 1] + dp[i - 1][b - costs[i - 1]], 
                               dp[i - 1][b])
            else:
                dp[i][b] = dp[i - 1][b]

    # Backtrack to find selected suppliers/materials
    res = dp[n][budget]
    b = budget
    chosen = []
    
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == dp[i - 1][b]:
            continue
        else:
            chosen.append(i - 1)
            res -= benefits[i - 1]
            b -= costs[i - 1]

    chosen.reverse()

    # Build descriptive advice
    if chosen:
        selection_list = []
        for i in chosen:
            selection_list.append(f"**{materials[i]}** (cost {costs[i]}, benefit {benefits[i]})")
        
        if len(selection_list) == 1:
            materials_text = selection_list[0]
        else:
            materials_text = ", ".join(selection_list[:-1]) + f", and {selection_list[-1]}"

        return (f"🏭 To optimize your supply chain within a budget of {budget}, "
                f"you should source {materials_text}. "
                f"This selection will yield the **maximum achievable production output/profit of {dp[n][budget]}**.")
    else:
        return (f"⚠️ Given the budget of {budget}, no combination of suppliers or raw materials "
                f"can improve production output.")


# ---- App Title ----
st.title("🏭 Supply Chain Optimization Tool")
st.write("This tool helps manufacturers select the **best mix of raw materials or suppliers** to maximize profit or output while staying within budget.")


# ---- Inputs ----
st.subheader("Enter Supplier/Material Details")

col1, col2, col3 = st.columns(3)
with col1:
    materials = st.text_area("Enter supplier/material names (comma separated)", placeholder="e.g. Steel, Plastic, Copper")
with col2:
    benefits = st.text_input("Enter benefits/profit values (space separated)", placeholder="e.g. 60 100 120")
with col3:
    costs = st.text_input("Enter costs (space separated)", placeholder="e.g. 10 20 30")

budget = st.text_input("Enter budget available", placeholder="e.g. 50")


# ---- Button ----
if st.button("🚀 Optimize Supply Chain"):
    material_list = [m.strip() for m in materials.split(",") if m.strip()]
    ben = [int(i) for i in benefits.split()]
    cost = [int(c) for c in costs.split()]
    bud = int(budget.split()[0])

    # Get result
    result_text = supply_chain_optimization(material_list, ben, cost, bud)

    # Styled result box
    st.markdown(f"<div class='result-box'>{result_text}</div>", unsafe_allow_html=True)

    # Full Code Section
    st.subheader("📝 Full Code Implementation")
    full_code = '''
    def supply_chain_optimization(materials, benefits, costs, budget):
    n = len(benefits)
    
    # DP table
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        for b in range(1, budget + 1):
            if costs[i - 1] <= b:
                dp[i][b] = max(benefits[i - 1] + dp[i - 1][b - costs[i - 1]], 
                               dp[i - 1][b])
            else:
                dp[i][b] = dp[i - 1][b]

    # Backtrack to find selected suppliers/materials
    res = dp[n][budget]
    b = budget
    chosen = []
    
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == dp[i - 1][b]:
            continue
        else:
            chosen.append(i - 1)
            res -= benefits[i - 1]
            b -= costs[i - 1]

    chosen.reverse()

    # Build descriptive advice
    if chosen:
        selection_list = []
        for i in chosen:
            selection_list.append(f"**{materials[i]}** (cost {costs[i]}, benefit {benefits[i]})")
        
        if len(selection_list) == 1:
            materials_text = selection_list[0]
        else:
            materials_text = ", ".join(selection_list[:-1]) + f", and {selection_list[-1]}"

        return (f"🏭 To optimize your supply chain within a budget of {budget}, "
                f"you should source {materials_text}. "
                f"This selection will yield the **maximum achievable production output/profit of {dp[n][budget]}**.")
    else:
        return (f"⚠️ Given the budget of {budget}, no combination of suppliers or raw materials "
                f"can improve production output.")
    '''
    st.code(full_code, language="python")

    # Complexity Info
    st.subheader("📊 Complexity Analysis")
    st.info("⏱ **Time Complexity:** O(n * budget) — Filling DP table of size n * budget, each entry computed in O(1). Backtracking is O(n).")
    st.info("💾 **Space Complexity:** O(n * budget) — DP table size (n+1) * (budget+1). Additional backtracking storage O(n).")
