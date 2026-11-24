

import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from pathlib import Path

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌱",
    layout="wide"
)

# -------------------------------
# TITLE
# -------------------------------
st.title("🌱 AI Plant Disease Detection")
st.markdown(
    "Upload a plant leaf image to identify possible diseases "
    "using Artificial Intelligence."
)

st.divider()

# -------------------------------
# MODEL CONFIGURATION
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "plant_model.keras"

# These class names and their order MUST match model training
classes = [
    "Healthy",
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Tomato Leaf Mold",
    "Tomato Bacterial Spot"
]

# -------------------------------
# DISEASE INFORMATION
# -------------------------------
disease_info = {
    "Healthy": {
        "description": "The model predicts that the leaf appears healthy.",
        "suggestion": [
            "Continue regular watering.",
            "Monitor the plant regularly.",
            "Maintain proper soil nutrients."
        ]
    },

    "Tomato Early Blight": {
        "description": "A fungal disease that can cause brown spots on leaves.",
        "suggestion": [
            "Remove affected leaves.",
            "Avoid overhead watering.",
            "Maintain good air circulation."
        ]
    },

    "Tomato Late Blight": {
        "description": "A disease that can cause dark lesions on leaves.",
        "suggestion": [
            "Remove severely affected plant material.",
            "Avoid excess moisture on leaves.",
            "Consult a local agricultural expert."
        ]
    },

    "Tomato Leaf Mold": {
        "description": "A fungal disease that commonly affects tomato leaves.",
        "suggestion": [
            "Improve air circulation.",
            "Avoid excessive humidity.",
            "Remove affected leaves carefully."
        ]
    },

    "Tomato Bacterial Spot": {
        "description": "A bacterial disease that causes spots on tomato leaves.",
        "suggestion": [
            "Use disease-free seeds and seedlings.",
            "Avoid handling wet plants.",
            "Remove affected plant material."
        ]
    }
}

# -------------------------------
# LOAD MODEL
# -------------------------------
@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

if not MODEL_PATH.exists():
    st.error(
        "Trained model not found! "
        "Please add plant_model.keras inside the models folder."
    )
    st.stop()

try:
    model = load_model()
except Exception as e:
    st.error(f"Unable to load model: {e}")
    st.stop()

# -------------------------------
# IMAGE UPLOAD
# -------------------------------
st.subheader("Upload Plant Leaf Image")

uploaded_file = st.file_uploader(
    "Choose a leaf image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            image,
            caption="Uploaded Plant Leaf",
            use_container_width=True
        )

    with col2:
        st.info("Image uploaded successfully!")
        st.write("File name:", uploaded_file.name)

    st.divider()

    # -------------------------------
    # DISEASE PREDICTION
    # -------------------------------
    if st.button("🔍 Detect Plant Disease", use_container_width=True):

        with st.spinner("AI is analyzing the leaf image..."):

            try:
                # Preprocessing must match model training
                processed_image = image.resize((224, 224))

                image_array = np.array(
                    processed_image
                ).astype("float32") / 255.0

                image_array = np.expand_dims(
                    image_array, axis=0
                )

                # Predict
                prediction = model.predict(
                    image_array, verbose=0
                )[0]

                if len(prediction) != len(classes):
                    st.error(
                        "Model output does not match the configured "
                        "disease classes. Check the training class order."
                    )
                    st.stop()

                predicted_index = np.argmax(prediction)
                disease = classes[predicted_index]

                confidence = float(
                    prediction[predicted_index]
                ) * 100

                st.subheader("🌿 Detection Results")

                # Confidence threshold
                if confidence < 70:
                    st.warning(
                        "The model is uncertain about this prediction. "
                        "Try a clearer leaf image."
                    )
                else:
                    if disease == "Healthy":
                        st.success("Prediction: Healthy")
                    else:
                        st.error(f"Possible Disease: {disease}")

                    st.write(
                        f"Model confidence: {confidence:.2f}%"
                    )

                    st.progress(
                        float(np.clip(confidence / 100, 0, 1))
                    )

                    # Disease details
                    st.subheader("📋 Disease Information")

                    info = disease_info[disease]

                    st.write(info["description"])

                    st.subheader("💡 Management Suggestions")

                    for suggestion in info["suggestion"]:
                        st.write("•", suggestion)

                st.caption(
                    "AI predictions are experimental and may be incorrect. "
                    "Confirm suspected diseases with an agricultural expert "
                    "before taking treatment decisions."
                )

            except Exception as e:
                st.error(f"Prediction failed: {e}")

else:
    st.info("Please upload a plant leaf image to begin detection.")

st.divider()
st.caption("AI-Based Smart Agriculture System | Plant Disease Detection")
