from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import joblib  # For saving the model

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
#cancer_dataset['filename']

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

# XGBoost Classifier
from xgboost import XGBClassifier
xgb_classifier = XGBClassifier()
xgb_classifier.fit(X_train, y_train)
y_pred_xgb = xgb_classifier.predict(X_test)
accuracy_score(y_test, y_pred_xgb)

# Train with Standard scaled Data
xgb_classifier2 = XGBClassifier()
xgb_classifier2.fit(X_train_sc, y_train)
y_pred_xgb_sc = xgb_classifier2.predict(X_test_sc)
accuracy_score(y_test, y_pred_xgb_sc)

# XGBoost classifier most required parameters
params={
 "learning_rate"    : [0.05, 0.10, 0.15, 0.20, 0.25, 0.30 ] ,
 "max_depth"        : [ 3, 4, 5, 6, 8, 10, 12, 15],
 "min_child_weight" : [ 1, 3, 5, 7 ],
 "gamma"            : [ 0.0, 0.1, 0.2 , 0.3, 0.4 ],
 "colsample_bytree" : [ 0.3, 0.4, 0.5 , 0.7 ] 
}

# Randomized Search
from sklearn.model_selection import RandomizedSearchCV
random_search = RandomizedSearchCV(xgb_classifier, param_distributions=params, scoring= 'roc_auc', n_jobs= -1, verbose= 3)
random_search.fit(X_train, y_train)

# training XGBoost classifier with best parameters
# xgb_classifier_pt = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
#        colsample_bynode=1, colsample_bytree=0.4, gamma=0.2,
#        learning_rate=0.1, max_delta_step=0, max_depth=15,
#        min_child_weight=1, missing=None, n_estimators=100, n_jobs=1,
#        nthread=None, objective='binary:logistic', random_state=0,
#        reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
#        silent=None, subsample=1, verbosity=1)
 
 # training XGBoost classifier with best parameters
xgb_classifier_pt = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bynode=1, colsample_bytree=0.4, gamma=0.2,
       learning_rate=0.1, max_delta_step=0, max_depth=15,
       min_child_weight=1, missing=np.nan, n_estimators=100, n_jobs=1,
       nthread=None, objective='binary:logistic', random_state=0,
       reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
       silent=None, subsample=1, verbosity=1)


xgb_classifier_pt.fit(X_train, y_train)
y_pred_xgb_pt = xgb_classifier_pt.predict(X_test)

# Save the model and scaler
joblib.dump(xgb_classifier, "model/breast_cancer_model.pkl")
joblib.dump(sc, "model/scaler.pkl")

print("Model and scaler saved successfully!")
