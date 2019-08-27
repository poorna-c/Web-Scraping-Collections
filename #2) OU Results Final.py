from selenium import webdriver
import re

file_name = input("ENTER A FILE NAME TO BE SAVED : ")
pattern = input("ENTER PATTERN : ")

file = open(f"{file_name}.txt","w")
PATH="/usr/lib/chromium-browser/chromedriver"
browser=webdriver.Chrome(executable_path=PATH)
url="https://www.osmania.ac.in/res07/20190855.jsp"
browser.get(url)
detained = 0

def findResults(pattern,start,end):
	global detained
	htno = pattern+"000"
	for i in range(start,end+1):
		try:
			if len(str(abs(i)))==1: htno=htno[:-1]+str(i)
			if len(str(abs(i)))==2: htno=htno[:-2]+str(i)
			if len(str(abs(i)))==3: htno=htno[:-3]+str(i)
			browser.find_element_by_name('htno').send_keys(htno)
			browser.find_element_by_name('Submit').click()
			details_table = browser.find_element_by_id('AutoNumber3').text

			pin_area = re.search("\d{12}",details_table).span()
			pin_no = details_table[pin_area[0]:pin_area[1]]

			name_span = re.search("Name [A-Z .]*\s",details_table).span()
			file.writelines("\n\n-------------------------------------------------------------\n")
			file.writelines("PIN NO : "+pin_no+"\t"+str(details_table[name_span[0]:name_span[-1]])+"\n")
			file.writelines("-------------------------------------------------------------\n")
			marks_table = browser.find_element_by_id('AutoNumber4').text
			marks_list = marks_table.splitlines()

			for subject in marks_list[2:]:
				subject_code_span = re.search("\d{3}",subject).span()
				subject_code = subject[subject_code_span[0]:subject_code_span[1]]
				subject_name = re.findall("[A-Z -.&]*",subject)[4]
				subject_grade_secured = subject[-1]
				gpa_scored = re.findall("\d+",subject)[-1]
				tabs = "\t\t"
				file.writelines(str(subject_code)+"\t"+str(subject_name)+tabs+str(gpa_scored)+"\n")
			result_table = browser.find_element_by_id('AutoNumber5').text
			a = result_table.splitlines()
			if "DETAINED" in str(a[-1]):
				detained += 1
			file.writelines(str(["RESULT : ",str(a[-1])])+"\n")
			file.writelines("-------------------------------------------------------------\n\n\n\n")
		except Exception as e:
			print(e)
			file.writelines("---------SKIPING ONE PIN HERE-------------\n\n\n")
findResults(pattern,1,59)
findResults(pattern,301,311)
file.seek(0, 0)
file.writelines("NO. OF STUDENTS DETAINED: "+str(detained)+"\n")
file.close()