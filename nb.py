import math

def mean(nums):
    return sum(nums) / len(nums)

def stdev(nums):
    avg = mean(nums)
    var = sum([(x - avg) ** 2 for x in nums]) / len(nums)
    return math.sqrt(var)

def summarize(data):
    separated = {
        'yes': [],
        'no': []
    }
    for feature, label in data:
        separated[label].append(feature)
    summaries = {}
    summaries['yes'] = [(mean(feature), stdev(feature)) for feature in zip(*separated['yes'])]
    prob_yes = len(separated['yes']) / len(data)
    summaries['no'] = [(mean(feature), stdev(feature)) for feature in zip(*separated['no'])]
    prob_no = len(separated['no']) / len(data)
    return summaries, prob_yes, prob_no


def f_x(summaries, input, prob_yes, prob_no):
    probabilities = {}
    probabilities['yes'] = prob_yes
    print(summaries)
    for i in range(8):
        mean, stdev = summaries['yes'][i]
        probabilities['yes'] *= math.exp(-(math.pow(input[i] - mean, 2) / (2 * math.pow(stdev, 2)))) / (math.sqrt(2 * math.pi) * stdev)
    probabilities['no'] = prob_no
    print(summaries)
    for i in range(8):
        mean, stdev = summaries['no'][i]
        probabilities['no'] *= math.exp(-(math.pow(input[i] - mean, 2) / (2 * math.pow(stdev, 2)))) / (math.sqrt(2 * math.pi) * stdev)
    return probabilities

def predict(summaries, input, prob_yes, prob_no):
    probabilities = f_x(summaries, input, prob_yes, prob_no)
    return max(probabilities, key=probabilities.get)

def classify_nb(training_filename, testing_filename):
    with open(training_filename, 'r') as file:
      data_str = file.readlines()
    training_data = [line.strip().split(",") for line in data_str]
    training_data = [([float(x) for x in row[:-1]], row[-1]) for row in training_data]

    with open(testing_filename, 'r') as file:
      data_str = file.readlines()
    testing_data = [line.strip().split(",") for line in data_str]
    testing_data = [[float(x) for x in row] for row in testing_data]
    
    summaries, prob_yes, prob_no = summarize(training_data)
    predictions = []
    
    for input in testing_data:
        result = predict(summaries, input, prob_yes, prob_no)
        predictions.append(result)
    
    return predictions

predictions = classify_nb("training.txt", "testing.txt")
print(predictions)