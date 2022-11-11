import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler


iris = datasets.load_iris()
Class_1 = iris['target']
df_data = pd.DataFrame(iris['data'], columns=iris['feature_names'])
label = dict((i, j) for i, j in enumerate(list(iris['target_names'])))
df_data['Class'] = Class_1
df_data['Species'] = df_data['Class'].map(label)

" 檢查缺失值 "
X = df_data.drop(labels=['Species', 'Class'], axis=1).values
print("Check missing data(NAN miunt):", len(np.where(np.isnan(X))[0]))
rolName = list(df_data)
n = X.shape[1]

class DataCleaning:
    def StandardScaler():
        scaler = StandardScaler().fit(X)
        X_scaled = scaler.transform(X)
        return X_scaled
    
    def MinMaxScaler():
        scaler = MinMaxScaler(feature_range=(0, 1)).fit(X)
        X_scaled = scaler.transform(X)
        return X_scaled
    
    def MaxAbsScaler():
        scaler = MaxAbsScaler().fit(X)
        X_scaled = scaler.transform(X)
        return X_scaled
    
    def RobustScaler():
        scaler = RobustScaler().fit(X)
        X_scaled = scaler.transform(X)
        return X_scaled

def draw(X_scaled):
    print('資料集 X 的平均值：', X.mean(axis=0))
    print('資料集 X 的標準差：', X.std(axis=0))
    print('縮放過後資料集 X 的平均值：', X_scaled.mean(axis=0))
    print('縮放過後資料集 X 的標準差：', X_scaled.std(axis=0))
    
    fig, axes = plt.subplots(nrows = 1, ncols = n)
    fig.set_size_inches(15,5)
    
    for i in range(n):
        sns.distplot(X_scaled[:, i], ax = axes[i])
        axes[i].set(xlabel = rolName[i], title = "Distribution of " + rolName[i])

draw(DataCleaning.MaxAbsScaler())
draw(DataCleaning.MinMaxScaler())
draw(DataCleaning.RobustScaler())
draw(DataCleaning.StandardScaler())
