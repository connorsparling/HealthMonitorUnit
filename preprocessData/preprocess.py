# Libraries
import pandas as pd # used for handling the dataset

from sklearn.impute import SimpleImputer # used for handling missing data
from sklearn.preprocessing import LabelEncoder # used for encoding categorical data
from sklearn.model_selection import train_test_split # used for splitting training and testing data
from sklearn.preprocessing import StandardScaler # used for feature scaling


# Load the dataset.
df = pd.read_csv('heartRateActivity.csv')
df2 = pd.read_csv('heartNormalVsAbnormal.csv')

df2 = df2.drop(["cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang",
                "oldpeak", "slope", "ca", "thal"], axis=1)

# Classify the dependend and independent variables.
X = df.iloc[:, :-1].values
Y = df.iloc[:, -1].values
X2 = df2.iloc[:, :-1].values
Y2 = df2.iloc[:, -1].values
    
# Deal with missing data by replacing 0 values with the mean.
imputer = SimpleImputer(missing_values=0, strategy='mean') 
X = imputer.fit_transform(X)
    
# Deal with categorical data by translating text into integers.
le = LabelEncoder()
Y = le.fit_transform(df['activity'])

# Split dataset into training and testing sets.
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
X2_train, X2_test, Y2_train, Y2_test = train_test_split(X2, Y2, test_size=0.2, random_state=0)
    
# Feature scaling
scX = StandardScaler()
X_train = scX.fit_transform(X_train)
X_test = scX.fit_transform(X_test)

X2_train = scX.fit_transform(X2_train)
X2_test = scX.fit_transform(X2_test)
    
scY = StandardScaler()
Y_train = Y_train.reshape((len(Y_train), 1))
Y_train = scY.fit_transform(Y_train)
Y_train = Y_train.ravel()
    
Y_test = Y_test.reshape((len(Y_test), 1))
Y_test = scY.fit_transform(Y_test)
Y_test = Y_test.ravel()