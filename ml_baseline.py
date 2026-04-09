import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# 1. 读取数据
df = pd.read_csv("Labeled_pairs.csv")

# 2. 去掉空label
df = df[df["label"].notna()]

# 3. 特征 & 标签
X = df["text"]
y = df["label"]

print("样本数量:", len(df))
print(y.value_counts())

# 4. 切分数据[70%训练，30%测试]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 5. TF-IDF[向量化]
vectorizer = TfidfVectorizer(
    max_features=2000,
    ngram_range=(1,2),
    stop_words="english"
)
#.fit 学习词表， .transform 转换文本为向量
X_train_tfidf = vectorizer.fit_transform(X_train) 
X_test_tfidf = vectorizer.transform(X_test)


model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# 7. 预测
y_pred = model.predict(X_test_tfidf)

# 8. 结果
print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred))

# 9. 看预测
results = pd.DataFrame({
    "text": X_test,
    "true": y_test,
    "pred": y_pred
})

print("\n=== Sample Predictions ===")
print(results.head(10))