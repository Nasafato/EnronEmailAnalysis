#!/usr/bin/python

""" 
    starter code for exploring the Enron dataset (emails + finances) 
    loads up the dataset (pickled dict of dicts)

    the dataset has the form
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person
    you should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle
import pprint

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))
pp = pprint.PrettyPrinter(indent=4)

def main():

    print("Number of people: {}".format(len(enron_data)))
    print("Number of features per person: {}".format(len(enron_data.values()[0])))

    poi_count = 0
    poi_without_total_payments = 0

    print("Keys = {}".format(enron_data.values()[0]))


    restricted_stock_deferred = 0
    for i in enron_data.values():
        if i["poi"] == 1:
            poi_count += 1
            if i["total_payments"] == 'NaN':
                poi_without_total_payments += 1
        if i['restricted_stock_deferred'] != 'NaN':
            restricted_stock_deferred += 1


    print("People with restricted stock deferred = {}".format(restricted_stock_deferred))
    print("PoI's without total payments: {}".format(poi_without_total_payments))
    print("Percentage PoI's without total payments: {}".format(float(poi_without_total_payments)/poi_count))


    print("Number of persons of interest: {}".format(poi_count))
    # print(enron_data["PRENTICE JAMES"].keys())
    print("James Prentice's stock value: {}".format(enron_data["PRENTICE JAMES"]["total_stock_value"]))
    print("Wesley Colwell's email messages to poi's: {}".format(enron_data["COLWELL WESLEY"]["from_this_person_to_poi"]))
    print("Jeffrey Skilling's exercised stock option value: {}".format(returnPerson("Jeffrey K Skilling")["exercised_stock_options"]))

    for person in ["Kenneth L Lay", "Jeffrey K Skilling", "Andrew S Fastow"]:
        print("{}: {}".format(person, returnPerson(person)["total_payments"]))

    pp.pprint(returnPerson("Kenneth L Lay"))

    number_of_known_emails = 0
    number_of_quantified_salaries = 0
    number_of_existing_total_payments = 0
    for i in enron_data.values():
        if i["salary"] != 'NaN':
            number_of_quantified_salaries += 1
        if i["email_address"] != 'NaN':
            number_of_known_emails += 1
        if i["total_payments"] != 'NaN':
            number_of_existing_total_payments += 1
    print("Number of known emails: {}".format(number_of_known_emails))
    print("Number of quantified salaries: {}".format(number_of_quantified_salaries))
    print("Number of people with total payments: {}".format(number_of_existing_total_payments))
    print("Percentage of people with total payments: {}".format(float(number_of_existing_total_payments)/len(enron_data)))

    exercised_options_list = []
    salary_list = []
    enron_data.pop("TOTAL", 0)
    for key, value in enron_data.items():
        exercised_options_list.append(value["exercised_stock_options"])
        salary_list.append(value["salary"])

    exercised_options_list.sort()
    salary_list.sort()
    print(exercised_options_list)
    print(salary_list)




def returnPerson(name):
    names = name.split(" ")
    first_name = names[0].upper()
    last_name = ''
    middle_initial = ''

    if len(names) == 2:
        last_name = names[1].upper()
        return enron_data["{} {}".format(last_name, first_name)]
    elif len(names) == 3:
        middle_initial = names[1].upper()
        last_name = names[2].upper()
        return enron_data["{} {} {}".format(last_name, first_name, middle_initial)]

if __name__ == "__main__":
    main()





