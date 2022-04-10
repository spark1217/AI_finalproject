import requests 
from bs4 import BeautifulSoup 
import json 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import csv


final_ouput = []
driver = webdriver.Chrome(ChromeDriverManager().install())

url = "https://webappprd.acs.ncsu.edu/php/coursecat/index.php"


driver.get(url)

sub = driver.find_element_by_name("subject")
sub.send_keys("CSC - Computer Science")
sub.submit()

time.sleep(10)

page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')

course_elements = soup.find_all("section", class_="course")
for course in course_elements:
        course_info = course.find("h1").text.split()
        course_code = course_info[1]
        course_title = ' '.join(course_info[2:-3])
        course_units = course_info[-1]

        course_desc = course.find_all("p")
        description = []
        for desc in course_desc:
                description.append(desc.text)
        course_requisite = description[-1]
        
        # Sections table
        sec_table = course.find("table", class_="table")
        sec_table_head = sec_table.thead.find_all("tr")  
        sec_table_row = sec_table.tbody.find_all("tr")

        # Get all the headings of Lists
        headings = []
        for th in sec_table_head[0].find_all("th"):
                headings.append(th.text)
        
        # Table of sections
        row_data = []
        
        for r in sec_table_row:
                i = 0
                for tr in r.find_all("td"):
                        row_data.append(tr.text)
        
        
        row_data_copy = []
        while row_data:
                each_row = {headings[i] : row_data[i] for i in range(10)}
                temp = each_row['Day/Time'].split()[:-5]
                time = ''.join(each_row['Day/Time'].split()[-5:])
                for t in temp:
                        if 'meets' not in t:
                                temp.remove(t)
                each_row['Day/Time'] = '/'.join(temp).replace('meets','') + ' ' + time.lstrip()
                row_data_copy.append(each_row)
                
                row_data = row_data[10:]        
                        
                        
        # print(course_info, course_requisite, '\n')
        f = open("course_list.txt", "a+")
        f.write(str(course_info) + '\n')
        f.write(course_requisite + '\n')
        f.write(str(row_data_copy))
        f.write('\n\n')

        json_output = [course_code, course_title, course_units, course_requisite, row_data_copy]
        final_ouput.append(json_output)

jsonStr = json.dumps(final_ouput)
with open('course_list_table.csv', 'w') as c:
      
    # using csv.writer method from CSV package
    write = csv.writer(c)
      
    write.writerow(['Course code', 'Course title', 'Units', 'Requisite', 'Sections'])
    write.writerows(final_ouput)