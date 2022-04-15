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
        
        # list of possible courses
        possible_courses = csp.add_courses(self)
        
    def add_courses(self):
        # variables: courses, domains: day/time
        courses = self.course_list[:]
        
        n = len(courses)
        temp = set(range(n))
        # Remove closed courses (avail_status = 'O')
        for i in range(n):
            if courses[i]['avail_status'] != 'O':
                temp.remove(i)
                
        # Remove course_taken
        taken = [v['taken'] for v in self.course_taken_unit]
        for j in range(n):
            if courses[j]['course_code'] in taken:
                if j in temp:
                    temp.remove(j)

        possible_courses = [courses[p] for p in temp]
        return possible_courses
        