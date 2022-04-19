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
        # print(degree, status, min_credit, max_credit, course_taken_unit, course_request_unit)

    def add_courses(self):
        # variables: courses, domains: day/time
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
        if self.degree == "Undergraduate":
            for l in range(n):
                if int(courses[l]["course_code"][0]) > 4:
                    if l in temp:
                        temp.remove(l)
                
        elif self.degree == "Graduate":
            for l in range(n):
                if int(courses[l]["course_code"][0]) < 5:
                    if l in temp:
                        temp.remove(l)

                    
        possible_courses = [courses[p] for p in temp]

        return possible_courses

    # def assigning_value(self, course, assignment):
    #     if "M" in course["day"]:
    #         assignment["M"].append(course)
            
    #     if "T" in course["day"] and course["day"] != "Th":
    #         assignment["T"].append(course)
            
    #     if "W" in course["day"]:
    #         assignment["W"].append(course)
            
    #     if "Th" in course["day"]:
    #         assignment["Th"].append(course)
            
    #     if "F" in course["day"]:
    #         assignment["F"].append(course)

    #     return assignment

    def csp_backtracking(self):
        
        # credit counts
        global set_solutions
        credit_cnt = 0
        set_solutions = []

        #The list of possible courses

        credit_cnt = 0
        possible_courses = csp.add_courses(self)

        return csp.backtracking_hard_constraint(self,possible_courses, [], credit_cnt)

    def isgoal(self, credit):

        if credit >= int(self.min_credit) and credit <= int(self.max_credit):

            if credit + 3 <= int(self.max_credit):
                return "Continue"

            else:
                return "Yes"

        else:
            return "No"

    def isoverlap(self,course_1, course_2):

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

            if templist[1] >= templist[2] or templist[3] >= templist[0]:
                return True

            else:
                return False
        else:
            return False



    def forwardchecking(self,cur_course, cur_possible_variables, credit):

        "After forward checking.."
        next_possible_variables = copy.deepcopy(cur_possible_variables)
        next_credit = credit + int(cur_course["course_units"])

        for variable in cur_possible_variables:

            if next_credit + int(variable["course_units"]) > int(self.max_credit) or csp.isoverlap(self,cur_course, variable) or variable["course_code"] == cur_course["course_code"]:
                
                next_possible_variables.remove(variable)

        return next_possible_variables


    def backtracking_hard_constraint(self,possible_variables, assignment, credit):

        # print(possible_variables)
        #Possible coursee = {M:[....], T: [....], F: [....]}

        if csp.isgoal(self,credit) == "Yes":
            new = []
            for course in assignment:
                new.append((course["course_code"], course["section"]))
            new.sort()
            set_solutions.append(new)

        elif csp.isgoal(self,credit) == "No":
            pass

        elif csp.isgoal(self,credit) == "Continue":
            new = []
            for course in assignment:
                new.append((course["course_code"], course["section"]))
            new.sort()
            set_solutions.append(new)
            pass


        if possible_variables == []:

            return "failure"

        else:
        
            possible_Lec_list = [lec for lec in possible_variables if lec["component"] == "Lec"]

            for lec in possible_Lec_list:

                Lablist = [x for x in possible_variables if x["course_code"] == lec["course_code"] and x["component"] == "Lab"]

                if Lablist != []:

                    for lab in Lablist:

                        x = csp.forwardchecking(self, lec, possible_variables, credit)

                        if x!= []:
                            temp_credit = credit + int(lec["course_units"])
                            y = csp.forwardchecking(self, lab, x, temp_credit)
                            assignment.append(lec)
                            assignment.append(lab)
                            credit += (int(lec["course_units"]) + int(lab["course_units"])) 
                            result = csp.backtracking_hard_constraint(self, x, assignment, credit)

                            if result != "failure":
                                    return result

                            assignment.remove(lec)
                            assignment.remove(lab)
                            credit -= (int(lec["course_units"]) + int(lab["course_units"])) 

                else:
                    x = csp.forwardchecking(self, lec, possible_variables, credit)

                    assignment.append(lec)
                    credit += (int(lec["course_units"]))

                    result = csp.backtracking_hard_constraint(self, x, assignment, credit)
                    if result != "failure":
                        return result

                    assignment.remove(lec)
                    credit -= (int(lec["course_units"]))


        return "failure"

    def solutions(self):
        result = []
        for value in set_solutions:
            if value not in result:
                result.append(value)
        return result