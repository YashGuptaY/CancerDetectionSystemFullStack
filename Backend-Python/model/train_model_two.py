#importing libraries
import pandas as pd # for data manupulation or analysis
import numpy as np # for numeric calculation
import matplotlib.pyplot as plt # for data visualization
import seaborn as sns # for data visualization

#loading dataset of breast cancer 
from sklearn.datasets import load_breast_cancer
cancer_dataset = load_breast_cancer()

#keys that are used in dataset
cancer_dataset.keys()

# featurs of each cells in numeric format
cancer_dataset['data']

# target stores the values of malignant or benign tumors.
cancer_dataset['target']

# target value name malignant or benign tumor
# 0 means malignant tumor and 1 means benign tumor
cancer_dataset['target_names']

#store the description of breast cancer dataset.
cancer_dataset['DESCR']

# store the name of features
cancer_dataset['feature_names']

# location/path of data file
cancer_dataset['filename']

#creating dataframe by concating data and target together and name columns
cancer_df = pd.DataFrame(np.c_[cancer_dataset['data'],cancer_dataset['target']],
             columns = np.append(cancer_dataset['feature_names'], ['target']))

# Head of cancer DataFrame
cancer_df.head(6)

# Tail of cancer DataFrame
cancer_df.tail(6)


#Data Visualization 
# Paiplot of cancer dataframe
sns.pairplot(cancer_df, hue = 'target')


# pair plot of sample feature
sns.pairplot(cancer_df, hue = 'target', 
             vars = ['mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness'] )

# Count the target class
sns.countplot(cancer_df['target'])
#plt.show() #show the graph


#Data Preprocessing

# Split DataFrame in train and test
X = cancer_df.drop(['target'], axis = 1)
X.head(6)

# output variable
y = cancer_df['target']
y.head(6)

# split dataset into train and test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state= 5)

# Feature scaling Converting different units and magnitude data in one unit.
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train_sc = sc.fit_transform(X_train)
X_test_sc = sc.transform(X_test)

#importing required packages
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

#Support Vector CLassifier
from sklearn.svm import SVC
svc_classifier = SVC()
svc_classifier.fit(X_train, y_train)
y_pred_scv = svc_classifier.predict(X_test)
accuracy_score(y_test, y_pred_scv)

# Train with Standard scaled Data
svc_classifier2 = SVC()
svc_classifier2.fit(X_train_sc, y_train)
y_pred_svc_sc = svc_classifier2.predict(X_test_sc)
accuracy_score(y_test, y_pred_svc_sc)

# Logistic Regression
from sklearn.linear_model import LogisticRegression
lr_classifier = LogisticRegression(random_state = 51, penalty = 'l1')
lr_classifier.fit(X_train, y_train)
y_pred_lr = lr_classifier.predict(X_test)
accuracy_score(y_test, y_pred_lr)

# Train with Standard scaled Data
lr_classifier2 = LogisticRegression(random_state = 51, penalty = 'l1')
lr_classifier2.fit(X_train_sc, y_train)
y_pred_lr_sc = lr_classifier.predict(X_test_sc)
accuracy_score(y_test, y_pred_lr_sc)


# XGBoost Classifier
from xgboost import XGBClassifier
xgb_classifier = XGBClassifier()
xgb_classifier.fit(X_train, y_train)
y_pred_xgb = xgb_classifier.predict(X_test)
accuracy_score(y_test, y_pred_xgb)