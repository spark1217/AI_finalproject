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
                    dic['preference'] = int(t.split('_')[2])
                    course_request.append(dic)
            course_request_unit = course_request
        elif temp[0] == 'day_preference':
            day_prefer = {}
            for d in temp[1:]:
                if len(d) > 0:
                    day = {}
                    date = d.split('_')[0]
                    is_pref = d.split('_')[1]
                    day[date] = int(is_pref)
                    day_prefer.update(day)
            day_preference = day_prefer
    return degree, status, min_credit, max_credit, course_taken_unit, course_request_unit, day_preference


if __name__ == "__main__":
    filename = sys.argv[1]
    degree, status, min_credit, max_credit, course_taken_unit, course_request_unit, day_preference = read_profile(filename)
    course_list = read_data()
    
    # CSP
    CSP = csp.csp(degree, status, min_credit, max_credit, course_taken_unit, course_request_unit, course_list, day_preference)
    
    #Process for saving the solutions as txt file(solutions.txt)
    #Solution : All available schedule lists which are consistent with all constraints.
    dir_name = os.getcwd()

    CSP.csp_backtracking()
    # sys.stdout = open(dir_name+"\\"+"solutions_"+filename+".txt", "w")
    z = CSP.soft_constraints()
    w = CSP.timetable()
    CSP.yml(w)

    # sys.stdout.close()

    # Generate pdf files for solutions
    for i in range(5):
        cmd = "pdfschedule "+"new"+str(i)+".yml"
        os.system(cmd)