import streamlit as st

# Define the table data as a dictionary of dictionaries
table = {
    -10: [11, 21, 32, 42, 53, 63, 74, 84, 95, 105, 116, 126, 137, 148, 158, 169, 179, 190, 200, 211],
    0: [9, 17, 26, 35, 44, 52, 61, 70, 79, 87, 96, 105, 114, 122, 131, 140, 149, 157, 166, 175],
    10: [6, 13, 19, 26, 32, 39, 45, 52, 58, 64, 71, 77, 84, 90, 97, 103, 109, 116, 122, 129],
    20: [4, 8, 12, 17, 21, 25, 29, 33, 37, 41, 46, 50, 54, 58, 62, 66, 70, 75, 79, 83],
    30: [2, 4, 6, 7, 9, 11, 13, 15, 17, 18, 20, 22, 24, 26, 28, 29, 31, 33, 35, 37]
}

# List of track lengths (in meters)
lengths = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]

def find_nearest_values(temp, length):
    temps = sorted(table.keys())
    t1 = max([t for t in temps if t <= temp], default=temps[0])
    t2 = min([t for t in temps if t >= temp], default=temps[-1])
    l1 = max([l for l in lengths if l <= length], default=lengths[0])
    l2 = min([l for l in lengths if l >= length], default=lengths[-1])
    return t1, t2, l1, l2

def get_gap(temp, length):
    t1, t2, l1, l2 = find_nearest_values(temp, length)
    idx1 = lengths.index(l1)
    idx2 = lengths.index(l2)
    g_t1_l1 = table[t1][idx1]
    g_t1_l2 = table[t1][idx2]
    g_t2_l1 = table[t2][idx1]
    length_step = (g_t1_l2 - g_t1_l1) / (l2 - l1) if l2 != l1 else 0
    temp_step = (g_t1_l1 - g_t2_l1) / (t2 - t1) if t2 != t1 else 0
    adjust = 0.01
    delta_t = temp - t1
    delta_l = length - l1
    gap = g_t1_l1 + (length_step * delta_l) - (temp_step * delta_t) - (adjust * delta_t * delta_l)
    return gap

# Streamlit UI
st.title("Rail Gap Calculator")
st.markdown("Enter temperature and track length to calculate the required rail gap.")

# User Input
temp = st.number_input("Enter temperature (°C):", value=20.0, step=0.1)
length = st.number_input("Enter track length (meters):", value=100.0, step=1.0)

# Calculate & Display Result
if st.button("Calculate Gap"):
    result = get_gap(temp, length)
    st.success(f"The required gap for {temp}°C and {length}m is {result:.2f} mm")
