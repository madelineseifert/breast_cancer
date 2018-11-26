from Neural_Net import X_scaler, label_encoder
from keras.models import load_model
model = load_model("models/cancer_model_trained.h5")
from sklearn.preprocessing import LabelEncoder

from numpy import array
patient = array([32, 71, 3, 17])
print(patient.shape)


reshaped_patient = patient.reshape(1, -1)

#X_scaler = StandardScaler().fit(X_train)
patient_test_scaled = X_scaler.transform(reshaped_patient)

yhat = model.predict_classes(patient_test_scaled)



prediction_labels = label_encoder.inverse_transform(yhat)


print(f"Predicted classes: {prediction_labels}")