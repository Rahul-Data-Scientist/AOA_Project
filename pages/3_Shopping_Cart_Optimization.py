import streamlit as st

# Page configuration
st.set_page_config(page_title="Shopping Cart Optimization", page_icon="🛒", layout="centered")

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


def shopping_cart_optimization(items, values, prices, budget):
    n = len(values)
    
    # DP table
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        for b in range(1, budget + 1):
            if prices[i - 1] <= b:
                dp[i][b] = max(values[i - 1] + dp[i - 1][b - prices[i - 1]], 
                               dp[i - 1][b])
            else:
                dp[i][b] = dp[i - 1][b]

    # Backtrack to find selected items
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
            res -= values[i - 1]
            b -= prices[i - 1]

    chosen.reverse()

    # Build descriptive advice
    if chosen:
        selection_list = []
        total_spent = 0
        for i in chosen:
            selection_list.append(f"**{items[i]}** (price {prices[i]}, value {values[i]})")
            total_spent += prices[i]
        
        if len(selection_list) == 1:
            items_text = selection_list[0]
        else:
            items_text = ", ".join(selection_list[:-1]) + f", and {selection_list[-1]}"

        return (f"🛒 To optimize your shopping within a budget of {budget}, "
                f"you should buy {items_text}. "
                f"This selection will give you the **maximum achievable value/utility of {dp[n][budget]}** "
                f"while spending a total of {total_spent}.")
    else:
        return (f"⚠️ Given the budget of {budget}, no combination of items "
                f"can provide positive value.")


# ---- App Title ----
st.title("🛒 Automated Shopping Cart Optimization")
st.write("This tool helps customers select the **best combination of products** to maximize value or utility while staying within a budget.")


# ---- Inputs ----
st.subheader("Enter Shopping Details")

col1, col2, col3 = st.columns(3)
with col1:
    items = st.text_area("Enter item names (comma separated)", placeholder="e.g. Laptop, Phone, Headphones")
with col2:
    values = st.text_input("Enter values/utility scores (space separated)", placeholder="e.g. 60 100 120")
with col3:
    prices = st.text_input("Enter prices (space separated)", placeholder="e.g. 10 20 30")

budget = st.text_input("Enter budget", placeholder="e.g. 50")


# ---- Button ----
if st.button("🚀 Optimize Shopping Cart"):
    item_list = [m.strip() for m in items.split(",") if m.strip()]
    val = [int(i) for i in values.split()]
    price = [int(c) for c in prices.split()]
    bud = int(budget.split()[0])

    # Get result
    result_text = shopping_cart_optimization(item_list, val, price, bud)

    # Styled result box
    st.markdown(f"<div class='result-box'>{result_text}</div>", unsafe_allow_html=True)

    # Full Code Section
    st.subheader("📝 Full Code Implementation")
    full_code = '''
    def shopping_cart_optimization(items, values, prices, budget):
        n = len(values)
        
        # DP table
        dp = [[0] * (budget + 1) for _ in range(n + 1)]

        # Fill DP table
        for i in range(1, n + 1):
            for b in range(1, budget + 1):
                if prices[i - 1] <= b:
                    dp[i][b] = max(values[i - 1] + dp[i - 1][b - prices[i - 1]], 
                                dp[i - 1][b])
                else:
                    dp[i][b] = dp[i - 1][b]

        # Backtrack to find selected items
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
                res -= values[i - 1]
                b -= prices[i - 1]

        chosen.reverse()

        # Build descriptive advice
        if chosen:
            selection_list = []
            total_spent = 0
            for i in chosen:
                selection_list.append(f"**{items[i]}** (price {prices[i]}, value {values[i]})")
                total_spent += prices[i]
            
            if len(selection_list) == 1:
                items_text = selection_list[0]
            else:
                items_text = ", ".join(selection_list[:-1]) + f", and {selection_list[-1]}"

            return (f"🛒 To optimize your shopping within a budget of {budget}, "
                    f"you should buy {items_text}. "
                    f"This selection will give you the **maximum achievable value/utility of {dp[n][budget]}** "
                    f"while spending a total of {total_spent}.")
        else:
            return (f"⚠️ Given the budget of {budget}, no combination of items "
                    f"can provide positive value.")
    '''
    st.code(full_code, language="python")

    # Complexity Info
    st.subheader("📊 Complexity Analysis")
    st.info("⏱ **Time Complexity:** O(n * budget) — Filling DP table of size n * budget, each entry computed in O(1). Backtracking is O(n).")
    st.info("💾 **Space Complexity:** O(n * budget) — DP table size (n+1) * (budget+1). Additional backtracking storage O(n).")
