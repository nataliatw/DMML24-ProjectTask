import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
titanic = pd.read_csv('C:/Users/ASUS/SurvivalPredictionAnalysis/Dataset/train.csv')

# Function to fill missing values in Age column
def fill_age_missing_values(titanic):
    Age_Nan_Indices = list(titanic[titanic["Age"].isnull()].index)
    for index in Age_Nan_Indices:
        temp_Pclass = titanic.iloc[index]["Pclass"]
        temp_SibSp = titanic.iloc[index]["SibSp"]
        temp_Parch = titanic.iloc[index]["Parch"]
        age_mean = titanic["Age"][((titanic["Pclass"] == temp_Pclass) & 
                                   (titanic["SibSp"] == temp_SibSp) & 
                                   (titanic["Parch"] == temp_Parch))].mean()
        if not np.isnan(age_mean):
            titanic.at[index, "Age"] = age_mean
        else:
            titanic.at[index, "Age"] = titanic["Age"].mean()
    return titanic

# Filling missing values and feature engineering
titanic = fill_age_missing_values(titanic)
titanic['Embarked'] = titanic['Embarked'].fillna('S')
titanic['Fare'] = titanic['Fare'].fillna(titanic['Fare'].mean())
titanic["Ftotal"] = 1 + titanic["SibSp"] + titanic["Parch"]
titanic["Sex"] = titanic["Sex"].astype('category')
titanic["sex"] = titanic["Sex"].cat.codes
titanic["Embarked"] = titanic["Embarked"].astype('category')
titanic["embarked"] = titanic["Embarked"].cat.codes

# Dropping unnecessary columns
titanic = titanic.drop(['Sex', 'Cabin', 'Embarked', 'SibSp', 'Parch', 'Name', 'Ticket', 'PassengerId'], axis=1)
titanic = titanic.drop(['Fare'], axis=1)

# Assigning X and y variables
X = titanic.drop('Survived', axis=1)
y = titanic['Survived']

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initializing and training the Gradient Boosting model
classifier = GradientBoostingClassifier()
classifier.fit(X_train, y_train)

# Evaluating the model on training data
y_pred_train = classifier.predict(X_train)
print("Training Accuracy:", accuracy_score(y_train, y_pred_train))
print("Training Classification Report:")
print(classification_report(y_train, y_pred_train))

# Evaluating the model on testing data
y_pred_test = classifier.predict(X_test)
print("Testing Accuracy:", accuracy_score(y_test, y_pred_test))
print("Testing Classification Report:")
print(classification_report(y_test, y_pred_test))

# Saving the model to a file
joblib.dump(classifier, 'gradient_boosting_model.joblib')

# Loading the model from the file to ensure it works correctly
loaded_model = joblib.load('gradient_boosting_model.joblib')

# Verifying the predictions from the loaded model
y_pred_loaded = loaded_model.predict(X_test)

# Ensure predictions are the same for both models
print("Predictions from loaded model:", y_pred_loaded[:5])  # Display first 5 predictions
