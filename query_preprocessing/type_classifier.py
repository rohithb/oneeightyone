from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import cross_validation
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.metrics import accuracy_score


def prepareTrainData():
    data = open('new_train_2.data').readlines()
    labels = open('new_train_2.labels').readlines()
    
    features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(data, labels, test_size=0.1, random_state=42)
    
    # Preparing the training data and test data
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
    features_train_transformed = vectorizer.fit_transform(features_train)
    features_test_transformed  = vectorizer.transform(features_test)
    
    
    selector = SelectPercentile(f_classif, percentile=10)
    selector.fit(features_train_transformed, labels_train)
    features_train_transformed = selector.transform(features_train_transformed).toarray()
    features_test_transformed  = selector.transform(features_test_transformed).toarray()
    
    return features_train_transformed, features_test_transformed, labels_train, labels_test, selector, vectorizer



def trainTypeClassifier():
    
    features_train, features_test, labels_train, labels_test, selector, vectorizer = prepareTrainData()
    clf = MultinomialNB()
    clf.fit(features_train, labels_train)
    pred = clf.predict(features_test)
    acc = accuracy_score(labels_test, pred)
    return acc, clf, selector, vectorizer
      


def predict(question, clf, selector, vectorizer):
    question_transformed = vectorizer.transform(question)
    question_transformed = selector.transform(question_transformed)
    
    return clf.predict(question_transformed)
