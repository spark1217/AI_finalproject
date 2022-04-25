import copy


class csp:
    def __init__(self, degree:str, status:str, min_credit:int, max_credit:int, course_taken_unit:list, course_request_unit:list, course_list:list):
        self.degree = degree
        self.status = status
        self.min_credit = min_credit
        self.max_credit = max_credit
        self.course_taken_unit = course_taken_unit
        self.course_request_unit = course_request_unit
        self.course_list = course_list

    def add_courses(self):
        # variables: courses, domains: Taken or Not taken
        courses = self.course_list[:]
        
        n = len(courses)
        temp = set(range(n))

        # Remove closed courses (avail_status = 'O')
        for i in range(n):
            if courses[i]['avail_status'] != 'O':
                temp.remove(i)

        #Remove "Distance Education" course, research and independent study
        for j in range(n):
            if courses[j]["start_time"] == "TBD":
                temp.remove(j)
                
        # Remove course_taken
        taken = [v['taken'] for v in self.course_taken_unit]
        for k in range(n):
            if courses[k]['course_code'] in taken:
                if k in temp:
                    temp.remove(k)

        # Remove course followed by degree
        # Undergraduate student cannot take courses which are over or equal to 500.
        if self.degree == "Undergraduate":
            for l in range(n):
                if int(courses[l]["course_code"][0]) > 4:
                    if l in temp:
                        temp.remove(l)

        # Graduate student cannot take courses which are less than 500.
        elif self.degree == "Graduate":
            for l in range(n):
                if int(courses[l]["course_code"][0]) < 5:
                    if l in temp:
                        temp.remove(l)

                    
        possible_courses = [courses[p] for p in temp]

        return possible_courses


    def csp_backtracking(self):
        
        global set_solutions, Lablist

        set_solutions = [] #List of available schedule which are consistent with all constraints

        credit_cnt = 0 #Number of credits

        possible_courses = csp.add_courses(self) #Possible courses which are only filtered by students profile so far. 

        Lablist = [lab for lab in possible_courses if lab["component"] == "Lab"] #The courses which also contain laboratory attendance. 

        return csp.backtracking_hard_constraint(self,possible_courses, [], credit_cnt)

    def isgoal(self, credit):

        #Check whether the current assignment is our goal.
        # min_credit < assignment_credit < max_credit
        if credit >= int(self.min_credit) and credit <= int(self.max_credit):  
            return "Yes"

        else:
            return "No"

    def isoverlap(self,course_1, course_2):

        # One of the hard constraints is whether the class time of each courses are overlapped
        # Check whether there is an overlap in diffrent courses.
        
        # If the "day" of two courses are same,
        #   Convert the expression of "time" from original expression to float expression.
        #   e.g. AM 10:30 -> 10.5 // PM 02:15 => 14.25 
        if course_1["day"] in course_2["day"] or course_2["day"] in course_1["day"]:
        
            templist = [course_1["start_time"], course_1["end_time"],course_2["start_time"], course_2["end_time"]]

            for index, time in enumerate(templist):
                if len(time) == 8:
                    if "PM" in time and "12" not in time:
                        templist[index] = (int(time[0:2]) + 12) + (int(time[3:5]) / 60)

                    else:
                        templist[index] = int(time[0:2]) + (int(time[3:5]) / 60)
                else:
                    if "PM" in time and "12" not in time:
                        templist[index] = (int(time[0]) + 12) + (int(time[2:4]) / 60)

                    else:
                        templist[index] = int(time[0]) + (int(time[2:4]) / 60)

            s_1, e_1, s_2, e_2 = templist[0], templist[1], templist[2], templist[3]

            #If start time of course 1 <= start time of course 2 <= end time of course 1, two courses are overlapped.
            if s_1 <= s_2 and s_2 <= e_1:
                return True
            
            #Or start time of course 1 <= end time of course 2 <= end time of course 1, two courses are overlapped.
            elif s_1 <= e_2 and e_2 <= e_1:
                return True

            #Or start time of course 2 <= start time of course 1 <= end time of course 2, two courses are overlapped.
            elif s_2 <= s_1 and s_1 <= e_2:
                return True

            #Or start time of course 2 <= end time of course 1 <= end time of course 2, two courses are overlapped.
            elif s_2 <= e_1 and e_1 <= e_2:
                return True

            else:
                return False

        else:
            return False



    def forwardchecking(self,cur_lec, cur_lab, cur_possible_variables, credit):

        #Variable : Course / Domain : Taken or Not taken

        #Constraints
        # 1) Less than max_credit 
        # 2) The courses should not be overlapped 
        # 3) The course code of each courses should be different.(except laboratory course)

        #If a variable(course) cannot satisfy all of the constraints,
        #   The variable is "Not taken."   
        #   The variable is removed in the list of "next possible variables."
        
        next_possible_variables = copy.deepcopy(cur_possible_variables)

        next_credit = credit + int(cur_lec["course_units"])


        #If the current considered course does not contain "lab", Only 3 constraints are considered.
        if cur_lab == {}:
            
            for variable in cur_possible_variables:

                ismorecredit = next_credit + int(variable["course_units"]) > int(self.max_credit) 
                isoverlap = csp.isoverlap(self,cur_lec, variable)
                issamecourse = variable["course_code"] == cur_lec["course_code"]

                if ismorecredit or isoverlap or issamecourse:
                    next_possible_variables.remove(variable)

        #Else, the current considered course contain "lab", 
        # Only 4 constraints("lab" course also should not be overlapped with other courses) are considered.
        else:

            for variable in cur_possible_variables:

                ismorecredit = next_credit + int(variable["course_units"]) > int(self.max_credit) 
                isoverlap = csp.isoverlap(self,cur_lec, variable)
                isoverlap_lab = csp.isoverlap(self, cur_lab, variable)
                issamecourse = variable["course_code"] == cur_lec["course_code"]

                if ismorecredit or isoverlap or isoverlap_lab or issamecourse:
                    next_possible_variables.remove(variable)

        return next_possible_variables


    def backtracking_hard_constraint(self,possible_variables, assignment, credit):

        # If the current assignment is goal, the goal is added in list of solutions. Else, just pass.
        # There is no return as there are possibilities that more courses can be added.
        if csp.isgoal(self,credit) == "Yes":

            new = []
        
            for course in assignment:
                new.append((course["course_code"], course["section"]))
            # new.sort()

            # set_solutions.append(list(assignment))
            set_solutions.append(new)

        elif csp.isgoal(self,credit) == "No":
            pass

        
        #Return "failure" if there are no possible variables.
        if possible_variables == []:
            return "failure"

        else:
            """
            1. Simple background of Backtracking in problem.

            For var in variables:
                   ** there are just 2 values, No need to use "Order-Domain-Values
               Next possible variables = Forwardchecking(var = taken, possible variables)
                   **In Forwardchecking, if a specific variable in possible variables are assigned as "Not taken"
                     The variable cannot be in the list of next possible variable as the variable is no more considered.
               result <- backtracking(var = taken | Assignment, next possible values)


            2. Procedure of backtracking in problem.

            For "lecture" in "possible lecture list"

               If the lecture is in  "non_visited lecture list"

                   Remove the lecture in "non_visited lecture list"

                   If the lecture should be with lab attendance

                       Next possible variables = Reduced variables using forwardchecking with assignment containing "lecture" and "lab"
                       Backtracking with Next possible variables

                   Else 
                       Next possible variables = Reduced variables using forwardchecking with assignment containing "lecture" 
                       Backtracking with next possible variables"""

            possible_Lec_list = [lec for lec in possible_variables if lec["component"] == "Lec"]

            non_visited_lec_list = copy.deepcopy(possible_Lec_list)

            for lec in possible_Lec_list:

                if lec in non_visited_lec_list:

                    non_visited_lec_list.remove(lec)

                    possible_Lablist = [x for x in possible_variables if x["course_code"] == lec["course_code"] and x["component"] == "Lab"]

                    if possible_Lablist != []:

                        for lab in possible_Lablist:

                            x = csp.forwardchecking(self, lec, lab, possible_variables, credit)
                        
                            assignment.append(lec)
                            assignment.append(lab)
                            credit += int(lec["course_units"])

                            result = csp.backtracking_hard_constraint(self, x, assignment, credit)

                            if result != "failure":
                                return result

                            assignment.remove(lec)
                            assignment.remove(lab)
                            credit -= int(lec["course_units"])

                    else:
                        possible = True

                        for lab in Lablist:
                            if lab["course_code"] == lec["course_code"]:
                                possible = False
                            
                            
                        if possible:

                            x = csp.forwardchecking(self, lec, {}, non_visited_lec_list, credit)

                            assignment.append(lec)
                            credit += (int(lec["course_units"]))

                            result = csp.backtracking_hard_constraint(self, x, assignment, credit)

                            if result != "failure":
                                return result

                            assignment.remove(lec)
                            credit -= (int(lec["course_units"]))

                else:
                    pass

        return "failure"

    
    #The entire set of solutions(Raw version)
    # [[{course data}, {course data}] , [{course data}, {course data}, {course data}]........]
    #   -----------------------------   =============================================
    #           SOLUTION 1                                SOLUTION 2                 ........
    def hard_constraint_solutions(self):
        return set_solutions


    
    # Filter out soft constraints
    def soft_constraints(self):
        # global possible_solution
        possible_solution = set_solutions[::]
        c = []
        for k in self.course_request_unit:
            temp = k['request'].split('-')
            if len(temp) > 1:
                c.append((temp[0], int(temp[1]), k['preference']))
            else:
                c.append((temp[0], -1, k['preference']))                     # -1 is a placeholder of section num when it is unknown in requests.
        
        requested_course = list(map(list, zip(*c)))[0]
        requested_section = list(map(list, zip(*c)))[1]
        requested_preference = list(map(list, zip(*c)))[2]
        year = self.status

        # calculating weights depending on how many courses in possible solutions are matching with lists in requests
        for i in possible_solution:
            temp_course = list(map(list, zip(*i)))[0]
            temp_sec = list(map(list, zip(*i)))[1]
            if temp_course == requested_course:
                i.append(len(temp) + sum(requested_preference))
            else:
                a = set(requested_course).intersection(set(temp_course))
                count_matching = len(a)
                for c in a:
                    idx_s1 = temp_course.index(c)
                    idx_s2 = requested_course.index(c)
                    if requested_section[idx_s2] != -1 and temp_sec[idx_s1] != requested_section[idx_s2]:
                        count_matching -= 1
                    else:
                        if requested_preference[idx_s2] < 0:
                            count_matching -= 100                               # If there is a course that a student doesn't want to take it, calculate as -100 (consider ignoring)
                        else:
                            count_matching += requested_preference[idx_s2]
                i.append(count_matching)

        possible_solution.sort(key = lambda x: x[-1], reverse=False)
        # print(possible_solution)
        self.maximize_soft_constraints(possible_solution)
        
    

    def status_checking(self, x):
        # Check academic status. If a student is on a certain academic level, he/she should not take lower level courses.
        year = self.status
        min_course = 0
        max_course = 0
        checking = True
        if year == 'Freshman' or year == 'Sophomore':
            min_course = 100
            max_course = 300
        elif year == 'Junior':
            min_course = 200
            max_course = 500
        elif year == 'Senior':
            min_course = 300
            max_course = 500
        elif year == 'Masters' or year == 'Doctorate':
            min_course = 500
            max_course = 900

        c_temp = [int(i) for i in list(map(list, zip(*x)))[0]]
        if max(c_temp) < min_course:
            checking = False
        elif min(c_temp) < min_course and max(c_temp) < max_course:
            checking = False
        elif min(c_temp) < max_course and max(c_temp) > max_course:
            checking = False
        elif min(c_temp) > max_course:
            checking = False
        return checking

    # Find solutions with maximum number of soft constraints
    def maximize_soft_constraints(self, possible_solution):
        solution = [x for x in possible_solution if x[-1]> 0 and self.status_checking(x[:-1])]
        print(solution[:5])
        # print(len(solution))
        
        return [x for x in possible_solution if x[-1]> 0 and self.status_checking(x[:-1])]