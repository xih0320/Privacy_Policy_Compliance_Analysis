import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


df = pd.read_csv("Labeled_pairs.csv")


df = df[df["label"].notna()]

X = df["text"]
y = df["label"]

print("样本数量:", len(df))
print(y.value_counts())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 5. TF-IDF
vectorizer = TfidfVectorizer(
    max_features=2000,
    ngram_range=(1,2),
    stop_words="english"
)

X_train_tfidf = vectorizer.fit_transform(X_train) 
X_test_tfidf = vectorizer.transform(X_test)


model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)


y_pred = model.predict(X_test_tfidf)


print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred))


results = pd.DataFrame({
    "text": X_test,
    "true": y_test,
    "pred": y_pred
})

print("\n=== Sample Predictions ===")
print(results.head(10))
