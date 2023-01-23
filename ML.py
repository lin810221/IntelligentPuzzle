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
        draw(X_scaled)
    
    def MinMaxScaler():
        scaler = MinMaxScaler(feature_range=(0, 1)).fit(X)
        X_scaled = scaler.transform(X)
        draw(X_scaled)
    
    def MaxAbsScaler():
        scaler = MaxAbsScaler().fit(X)
        X_scaled = scaler.transform(X)
        draw(X_scaled)
    
    def RobustScaler():
        scaler = RobustScaler().fit(X)
        X_scaled = scaler.transform(X)
        draw(X_scaled)

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
    plt.show()


DataCleaning.StandardScaler()
DataCleaning.MaxAbsScaler()
DataCleaning.MinMaxScaler()
DataCleaning.RobustScaler()


# 計算在測試集上的準確度
from sklearn.metrics import accuracy_score, silhouette_score


# 分割資料集
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Class_1, test_size=0.3, random_state=0)

# 邏輯回歸
from sklearn.linear_model import LogisticRegression
clf_lr = LogisticRegression()
clf_lr.fit(X_train, y_train)
y_pred_lr = clf_lr.predict(X_test)
print("Accuracy of Logistic Regression: ", accuracy_score(y_test, y_pred_lr))

# 決策樹
from sklearn.tree import DecisionTreeClassifier
clf_dt = DecisionTreeClassifier()
clf_dt.fit(X_train, y_train)
y_pred_dt = clf_dt.predict(X_test)
print("Accuracy of Decision Tree: ", accuracy_score(y_test, y_pred_dt))

# 隨機森林
from sklearn.ensemble import RandomForestClassifier
clf_rf = RandomForestClassifier()
clf_rf.fit(X_train, y_train)
y_pred_rf = clf_rf.predict(X_test)
print("Accuracy of Random Forest: ", accuracy_score(y_test, y_pred_rf))


# 支援向量機
from sklearn.svm import SVC
clf_svm = SVC()
clf_svm.fit(X_train, y_train)
y_pred_svm = clf_svm.predict(X_test)
print("Accuracy of SVM: ", accuracy_score(y_test, y_pred_svm))

# KNN
from sklearn.neighbors import KNeighborsClassifier
clf_knn = KNeighborsClassifier()
clf_knn.fit(X_train, y_train)
y_pred_knn = clf_knn.predict(X_test)
print("Accuracy of KNN: ", accuracy_score(y_test, y_pred_knn))

# Stacking
from sklearn.ensemble import StackingClassifier
estimators = [('lr', LogisticRegression()), ('dt', DecisionTreeClassifier()), ('rf', RandomForestClassifier()),('svm', SVC())]
clf_stacking = StackingClassifier(estimators=estimators)
clf_stacking.fit(X_train, y_train)
y_pred_stacking = clf_stacking.predict(X_test)
print("Accuracy of Stacking: ", accuracy_score(y_test, y_pred_stacking))

# XGBoost
from xgboost import XGBClassifier
clf_xgb = XGBClassifier()
clf_xgb.fit(X_train, y_train)
y_pred_xgb = clf_xgb.predict(X_test)
print("Accuracy of XGBoost: ", accuracy_score(y_test, y_pred_xgb))

# K-Means
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
print("Predicted Clusters: ", kmeans.labels_)


# 視覺化
models = ['Logistic Regression', 'Decision Tree', 'Random Forest', 'SVM', 'KNN','Stacking','XGBoost','K-means']
scores = [accuracy_score(y_test, y_pred_lr), accuracy_score(y_test, y_pred_dt), accuracy_score(y_test, y_pred_rf), accuracy_score(y_test, y_pred_svm), accuracy_score(y_test, y_pred_knn), accuracy_score(y_test, y_pred_stacking),accuracy_score(y_test, y_pred_xgb), silhouette_score(X, kmeans.labels_)]

plt.bar(models, scores)
plt.ylabel('Accuracy')
plt.show()
