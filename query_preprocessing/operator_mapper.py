from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib



def operatorMapperPipeline():
    type_clf = Pipeline([('vect', TfidfVectorizer(sublinear_tf=True, max_df=0.5, token_pattern="\w{1,}")),
                         ('sel', SelectPercentile(f_classif, percentile=100)),
                         ('clf', MultinomialNB())
                         ])
#     data = open('new_train_2.data').readlines()
#     labels = open('new_train_2.labels').readlines()
    data = open('query_preprocessing/traindata_all/operator_train.data').readlines()
    labels = open('query_preprocessing/traindata_all/operator_train.labels').readlines()
#     features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(data, labels, test_size=0.1, random_state=42)
    features_train = data
    labels_train = labels
    
    type_clf.fit(features_train, labels_train)
    joblib.dump(type_clf, '/home/rohith/nitk/main_project/query_preprocessing/pkl/operator_clf.pkl')
    

def findOperator(query):
    type_clf = joblib.load('/home/rohith/nitk/main_project/query_preprocessing/pkl/operator_clf.pkl')
    query = [query]
    operator = type_clf.predict(query)
    return operator[0].rstrip('\n')
