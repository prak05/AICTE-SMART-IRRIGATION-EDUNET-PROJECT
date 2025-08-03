import streamlit as st
import numpy as np
import joblib  

# Model load kar rahe hain. Agar .pkl file nahi mili toh error aayega. 😭
model = joblib.load("Farm_Irrigation_System.pkl")  

st.title("Smart Sprinkler System")
st.subheader("Sensor values daalo, sprinkler status pata chal jayega. Simple! 😎")

# Sensor inputs collect kar rahe hain. 20 sliders, bas next-next karte jao. 😩
sensor_values = []
for i in range(20):
    val = st.slider(f"Sensor {i}", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    sensor_values.append(val)

# Predict button. Ab bas click karo aur dekho magic. ✨
if st.button("Predict Sprinklers"):
    input_array = np.array(sensor_values).reshape(1, -1)
    prediction = model.predict(input_array)[0]

    st.markdown("### Prediction:")
    # Output dikha rahe hain. Hopefully sab ON ho! 🙏
    for i, status in enumerate(prediction):
        st.write(f"Sprinkler {i} (parcel_{i}): {'ON' if status == 1 else 'OFF'}")
