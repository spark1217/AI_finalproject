import os
import sys
import csv
import csp


# read proprocessed course list 
def read_data():
    courses = []
    with open('data/course_list_csp.csv','r') as f: 
        reader = csv.DictReader(f)
        for row in reader:
            courses.append(row)
    return courses

# read student profile
def read_profile(filename):
    file = "students/" + filename + '.txt'
    with open(file) as file:
        profile = file.read().replace('\n',' ').split('#')
    for i in profile[1:]:
        temp = i.split(' ')
        if temp[0] == 'degree':
            degree = temp[1]
        elif temp[0] == 'degree_status':
            status = temp[1]
        elif temp[0] == 'min_credit':
            min_credit = temp[1]
        elif temp[0] == 'max_credit':
            max_credit = temp[1]
        elif temp[0] == 'course_taken_unit':
            course_taken = []
            for t in temp[1:]:
                if len(t) > 0:
                    dic = {}
                    dic['taken'] = t.split('_')[0]
                    dic['unit'] = t.split('_')[1]
                    course_taken.append(dic)
            course_taken_unit = course_taken
        elif temp[0] == 'course_request_unit':
            course_request = []
            for t in temp[1:]:
                if len(t) > 0:
                    dic = {}
                    dic['request'] = t.split('_')[0]
                    dic['unit'] = t.split('_')[1]
                    course_request.append(dic)
            course_request_unit = course_request
    return degree, status, min_credit, max_credit, course_taken_unit, course_request_unit

if __name__ == "__main__":
    filename = sys.argv[1]
    degree, status, min_credit, max_credit, course_taken_unit, course_request_unit = read_profile(filename)
    course_list = read_data()
    
    # CSP
    x = csp.csp(degree, status, min_credit, max_credit, course_taken_unit, course_request_unit, course_list)
    
    dir_name = os.getcwd()
    sys.stdout = open(dir_name+"\\"+"solutions.txt", "w")
    
    y = x.csp_backtracking()
    sys.stdout.close()