# Dependencies
#get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


data_path = "raw_data.csv"

cancer_df = pd.read_csv(data_path, encoding="ISO-8859-1")

df = cancer_df.drop(['Unnamed: 32'], axis=1)


df['diagnosis'] = df['diagnosis'].map({'M':1,'B':0})
df.head()


data_final = df.drop("id", axis=1)
feature_names = data_final.columns
data_final.head()


df_final = data_final[['diagnosis','radius_worst', 'concave points_worst', 'area_worst','perimeter_worst']]
df_final.head()


X = df_final.drop("diagnosis", axis=1)
y = df_final["diagnosis"]
print(X.shape, y.shape)


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from keras.utils import to_categorical

X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=200, stratify=y)
X_scaler = StandardScaler().fit(X_train)
X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)


# Step 1: Label-encode data set
label_encoder = LabelEncoder()
label_encoder.fit(y_train)
encoded_y_train = label_encoder.transform(y_train)
encoded_y_test = label_encoder.transform(y_test)

# Step 2: Convert encoded labels to one-hot-encoding
y_train_categorical = to_categorical(encoded_y_train)
y_test_categorical = to_categorical(encoded_y_test)


from keras.models import Sequential
from keras.layers import Dense

# Create model and add layers
model = Sequential()
model.add(Dense(units=100, activation='relu', input_dim=4))
model.add(Dense(units=100, activation='relu'))
model.add(Dense(units=2, activation='softmax'))



# Compile and fit the model
model.compile(optimizer='adam',
             loss='categorical_crossentropy',
             metrics=['accuracy'])
model.fit(
   X_train_scaled,
   y_train_categorical,
   epochs=100,
   shuffle=True,
   verbose=2
)

model_loss, model_accuracy = model.evaluate(
   X_test_scaled, y_test_categorical, verbose=2)
print(
   f"Normal Neural Network - Loss: {model_loss}, Accuracy: {model_accuracy}")


encoded_predictions = model.predict_classes(X_test_scaled[:5])
prediction_labels = label_encoder.inverse_transform(encoded_predictions)

print(f"Predicted classes: {prediction_labels}")
print(f"Actual Labels: {list(y_test[:5])}")



# Save the model
model.save("models/cancer_model_trained.h5")

model_loss, model_accuracy = model.evaluate(X_test_scaled, y_test_categorical, verbose=2)
print(f"Loss: {model_loss}, Accuracy: {model_accuracy}")


from keras.models import load_model
model = load_model("models/cancer_model_trained.h5")


model_loss, model_accuracy = model.evaluate(
    X_test_scaled, y_test_categorical, verbose=2)
print(
    f"Normal Neural Network - Loss: {model_loss}, Accuracy: {model_accuracy}")



from numpy import array
patient = array([6, 7, 8, 9])
print(patient.shape)


reshaped_patient = patient.reshape(1, -1)

X_scaler = StandardScaler().fit(X_train)
patient_test_scaled = X_scaler.transform(reshaped_patient)

yhat = model.predict_classes(patient_test_scaled)

prediction_labels = label_encoder.inverse_transform(yhat)


print(f"Predicted classes: {prediction_labels}")

