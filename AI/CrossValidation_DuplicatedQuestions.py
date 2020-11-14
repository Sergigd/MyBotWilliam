from sklearn.model_selection import cross_val_score, RepeatedStratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from numpy import mean
import DataBase.DB

# Duplicated_english.db has each question 10 times repeated: different ids = 1659; total questions = 18249
data = DataBase.DB.MyData("Duplicated_english.db")

questions_db = data.get_all_titles()
y = data.get_all_ids()

vectorizer = CountVectorizer(strip_accents='ascii', lowercase=True, stop_words='english')
X = vectorizer.fit_transform(questions_db)

model = DecisionTreeClassifier()
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=9, random_state=1)
scores = cross_val_score(model, X, y, cv=cv, n_jobs=-1)
score = mean(scores)
print('Mean ROC AUC: ', score)
