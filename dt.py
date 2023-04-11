import math

class TreeNode:
    #clas is for class
    def __init__(self, data, clas):
        self.data = data
        self.clas = clas
        self.children = {}
        self.attribute = None
        self.build()

    def entropy(self, clas):
        unique_labels = set(clas)
        entropy = 0
        total = len(clas)
        for label in unique_labels:
            count = clas.count(label)
            prob = count / total
            entropy += -prob * math.log2(prob)
        return entropy

    def info_gain(self, data, clas, attribute):
        attribute_values = [row[attribute] for row in data]
        unique_attribute = set(attribute_values)
        t_one = self.entropy(clas)
        t_two = 0
        for val in unique_attribute:
            subset = [clas[i] for i in range(len(clas)) if data[i][attribute] == val]
            t_two += (len(subset) / len(clas)) * self.entropy(subset)
        gain = t_one - t_two
        return gain

    def find_best_split(self, data, clas):
        best_gain = 0
        best_attribute = 0
        for attribute in range(len(data[0])):
            gain = self.info_gain(data, clas, attribute)
            if gain > best_gain:
                best_gain = gain
                best_attribute = attribute
        return best_attribute

    def build(self):
        #terminate case a
        if len(set(self.clas)) == 1:
            return
        self.attribute = self.find_best_split(self.data, self.clas)
        unique_attribute = set([row[self.attribute] for row in self.data])
        #terminate case b
        if len(unique_attribute) == 1:
            yes_count = self.clas.count('yes')
            no_count = self.clas.count('no')
            if yes_count >= no_count:
                self.clas = ['yes']
            else:
                self.clas = ['no']
            return
        for val in unique_attribute:
            subset_data = [row for row in self.data if row[self.attribute] == val]
            subset_clas = [self.clas[i] for i, row in enumerate(self.data) if row[self.attribute] == val]

            self.children[val] = TreeNode(subset_data, subset_clas)

    def predict(self, instance):
        if not self.children:
            yes_count = self.clas.count('yes')
            no_count = self.clas.count('no')
            if yes_count >= no_count:
                return 'yes'
            else:
                return 'no'

        attribute = instance[self.attribute]
        if attribute in self.children:
            return self.children[attribute].predict(instance)
        else:
            #terminate case c, subset empty, attribute not in children
            yes_count = self.clas.count('yes')
            no_count = self.clas.count('no')
            if yes_count >= no_count:
                return 'yes'
            else:
                return 'no'

    
def classify_dt(training_filename, testing_filename):
    with open(training_filename, 'r') as file:
        data_str = file.readlines()
    x_train = []
    y_train = []
    for row in data_str:
        train_row = row.strip().split(',')
        x_train.append(train_row[:-1])
        y_train.append(train_row[-1])
    with open(testing_filename, 'r') as file:
      data_str = file.readlines()
    test_data = []
    for row in data_str:
        test_data.append(row.strip().split(','))
    root = TreeNode(x_train, y_train)
    return [root.predict(test) for test in test_data]

predictions = classify_dt("trainingd.txt", "testingd.txt")
print(predictions)