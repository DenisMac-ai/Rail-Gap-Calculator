import streamlit as st
import bisect

# Expansion gap data from the specification (in mm)
expansion_data = {
    -10: [11, 21, 32, 42, 53, 63, 74, 84, 95, 105, 116, 126, 137, 148, 158, 169, 179, 190, 200, 211],
    0:   [9,  17, 26, 35, 44, 52, 61, 70, 79, 87,  96, 105, 114, 122, 131, 140, 149, 157, 166, 175],
    10:  [6,  13, 19, 26, 32, 39, 45, 52, 58, 64,  71, 77,  84,  90,  97, 103, 109, 116, 122, 129],
    20:  [4,  8,  12, 17, 21, 25, 29, 33, 37, 41,  46, 50,  54,  58,  62, 66,  70,  75,  79,  83],
    30:  [2,  4,  6,  7,  9,  11, 13, 15, 17, 18,  20, 22,  24,  26,  28, 29,  31,  33,  35,  37]
}

rail_lengths = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]
temperatures = [-10, 0, 10, 20, 30]

def calculate_expansion_gap(length, temperature):
    L = max(20, min(400, length))
    T = max(-10, min(30, temperature))

    idx_T = bisect.bisect_left(temperatures, T)
    if idx_T == 0:
        T1 = T2 = temperatures[0]
    elif idx_T == len(temperatures):
        T1 = T2 = temperatures[-1]
    else:
        T1 = temperatures[idx_T - 1]
        T2 = temperatures[idx_T]

    idx_L = bisect.bisect_left(rail_lengths, L)
    if idx_L == 0:
        L1 = L2 = rail_lengths[0]
    elif idx_L == len(rail_lengths):
        L1 = L2 = rail_lengths[-1]
    else:
        L1 = rail_lengths[idx_L - 1]
        L2 = rail_lengths[idx_L]

    idx_L1 = rail_lengths.index(L1)
    idx_L2 = rail_lengths.index(L2)

    if T1 == T2:
        G_L1 = expansion_data[T1][idx_L1]
        G_L2 = expansion_data[T1][idx_L2]
    else:
        G_T1_L1 = expansion_data[T1][idx_L1]
        G_T2_L1 = expansion_data[T2][idx_L1]
        factor_T = (T - T1) / (T2 - T1)
        G_L1 = G_T1_L1 + factor_T * (G_T2_L1 - G_T1_L1)

        G_T1_L2 = expansion_data[T1][idx_L2]
        G_T2_L2 = expansion_data[T2][idx_L2]
        G_L2 = G_T1_L2 + factor_T * (G_T2_L2 - G_T1_L2)

    if L1 == L2:
        return G_L1
    else:
        factor_L = (L - L1) / (L2 - L1)
        G = G_L1 + factor_L * (G_L2 - G_L1)
        return G

st.title("Rail Gap Calculator")
st.markdown("Enter temperature and track length to calculate the required rail gap.")

temp = st.number_input("Enter temperature (°C):", value=20.0, step=0.1)
length = st.number_input("Enter track length (meters):", value=100.0, step=1.0)

if st.button("Calculate Gap"):
    result = calculate_expansion_gap(length, temp)
    st.success(f"The required gap for {temp}°C and {length}m is {result:.10g} mm")
