from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import cross_validation
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib

def prepareTrainData():
    data = open('new_train_2.data').readlines()
    labels = open('new_train_2.labels').readlines()
    
    features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(data, labels, test_size=0.1, random_state=42)
    
    # Preparing the training data and test data
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
    features_train_transformed = vectorizer.fit_transform(features_train)
    features_test_transformed  = vectorizer.transform(features_test)
    
    
    selector = SelectPercentile(f_classif, percentile=50)
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
      

def trainTypeClassifierPipeline():
    type_clf = Pipeline([('vect', TfidfVectorizer(sublinear_tf=True, max_df=0.5)),
                         ('sel', SelectPercentile(f_classif, percentile=100)),
                         ('clf', MultinomialNB())
                         ])
#     data = open('new_train_2.data').readlines()
#     labels = open('new_train_2.labels').readlines()
    data = open('query_preprocessing/traindata_all/train_all_1.data').readlines()
    labels = open('query_preprocessing/traindata_all/train_all_1.labels').readlines()
#     features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(data, labels, test_size=0.1, random_state=42)
    features_train = data
    labels_train = labels
    
    type_clf.fit(features_train, labels_train)
    joblib.dump(type_clf, 'query_preprocessing/pkl/type_clf.pkl')
    

def predictType(query):
    type_clf = joblib.load('query_preprocessing/pkl/type_clf.pkl')
    query = [query]
    query_type = type_clf.predict(query)
    return query_type[0].rstrip('\n')
