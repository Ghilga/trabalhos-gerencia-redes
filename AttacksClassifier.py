import ClassesDict
import pandas as pd
import numpy as np
import collections
from sklearn.tree import DecisionTreeClassifier
from imblearn.under_sampling import RandomUnderSampler 
from imblearn.over_sampling import SMOTE

class AttacksClassifier():
    def __init__(self):
        self.attacksClassifier = DecisionTreeClassifier(max_depth=5, class_weight='balanced', random_state=42)
        self.initializeClassifier()

    # Initialize Classifier
    def initializeClassifier(self):
        data = self.initializeData()
        attributes, classes = self.balanceInstances(data)
        encodedClasses = self.encodeClasses(classes)
        self.attacksClassifier.fit(attributes.values, encodedClasses)
    
    # Load dataset and remove unused classes and attributes
    def initializeData(self):
        data = pd.read_csv('all_data.csv')

        # Remove unused classes
        data = data.drop(data[data['class'] == 'slowpost'].index)
        data = data.drop(data[data['class'] == 'bruteForce'].index)

        # Remove less important attributes
        data = data.drop(['ifInOctets11', 'ifoutDiscards11', 'ifInNUcastPkts11', 'ifInDiscards11',
                        'ifOutUcastPkts11', 'ifOutNUcastPkts11', 'tcpOutRsts', 'tcpOutSegs',
                        'tcpPassiveOpens', 'tcpRetransSegs', 'tcpCurrEstab', 'tcpEstabResets',
                        'tcp?ActiveOpens', 'udpInDatagrams', 'udpNoPorts', 'ipInReceives', 
                        'ipOutRequests', 'ipInDiscards', 'ipForwDatagrams', 'ipOutNoRoutes',
                        'icmpOutMsgs', 'icmpOutDestUnreachs', 'icmpInEchos', 'ipInAddrErrors', 'icmpInMsgs']
                        , axis = 1)
        return data
    
    # Use Undersampling and SMOTE to balance the dataset instances, so all instances have the same quantity
    def balanceInstances(self, data):
        # Separe dataset into attributes (x) and classes (y)
        x = data.drop(['class'], axis = 1)
        y = data.loc[:,'class'].values

        # Frequency for each class - For using Undersampling
        classFrequency = collections.Counter(data['class'])

        # Define SMOTE strategy
        sm = SMOTE(sampling_strategy = 'minority')

        # Define Undersample strategy
        undersamplingStrategy = {'tcp-syn': classFrequency.get('normal'), 
                                'slowloris': classFrequency.get('normal'),
                                'udp-flood': classFrequency.get('normal'),
                                'icmp-echo': classFrequency.get('normal'),
                                'normal': classFrequency.get('normal'),
                                'httpFlood': classFrequency.get('httpFlood')}
        undersample = RandomUnderSampler(sampling_strategy = undersamplingStrategy)

        # Normalize data
        x, y = undersample.fit_resample(x,y)
        x, y = sm.fit_resample(x, y)
        return x, y
    
    # Encode the classes with nominal categorical value to numeric value
    def encodeClasses(self, classes):
        return pd.get_dummies(classes, columns=['class'])
    
    # Predict the result (class) from the given data (attributes)
    # 'data' has to be a 1D array, but on predict function it has to be 2D
    def predict (self, data):
        predictedValue = self.attacksClassifier.predict([data])
        valueIndex = np.where(predictedValue[0] == True)[0][0]
        return ClassesDict.get[valueIndex]


## Some small code to test the classifier, using values from the dataset

test = AttacksClassifier()
# result should be 'icmp-echo'
aux = test.predict([166456215,136110598,1541,238793,0,314763,574,42,35])
print(aux)
# result should be 'normal'
aux = test.predict([934203604,53611733,709,193506,1,253106,569,27,24])
print(aux)
# result should be 'tcp-syn'
aux = test.predict([613919708,70303007,143,113379,33,158256,21,3,1])
print(aux)
# result should be 'udp-flood'
aux = test.predict([468727289,53883940,1567,174769,2,255566,201,53,50])
print(aux)
# result should be 'httpFlood'
aux = test.predict([3940172569,23366596,55,37048,12,53624,6,0,0])
print(aux)
# result should be 'slowloris'
aux = test.predict([78708299,4234673,272,14511,0,32360,7,4,4])
print(aux)
