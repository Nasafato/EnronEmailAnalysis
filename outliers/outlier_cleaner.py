#!/usr/bin/python

import pprint
pp = pprint.PrettyPrinter(indent=4)

def outlierCleaner(predictions, ages, net_worths):
    """
        clean away the 10% of points that have the largest
        residual errors (different between the prediction
        and the actual net worth)

        return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error)
    """
    
    cleaned_data = []
    differences = []
    num_total_elements = len(predictions)
    num_removed = num_total_elements * .1
    for index, (pred, real) in enumerate(zip(predictions, net_worths)):

        error = pred[0] - real[0]
        if error < 0:
            error *= -1

        cleaned_data.append((ages[index][0], real[0], error))

    cleaned_data.sort(key=lambda tup: tup[2], reverse=True)

    for i in range(10):
        cleaned_data.pop(0)

    return cleaned_data

