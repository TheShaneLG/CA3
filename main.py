#############################################################
# Created By: Shane LG
# Welcome to my assignment CA3
# This is the landing page that orchestrate the project flow
#############################################################

from execFileUpload import OperationUpload
from execCleanup import OperationCleanup

courseid = 5
operation = input("Enter the Action - (Upload - 1, Cleanup - 0):")

if operation == "1":
   print("Initiated the Moodle Upload Process")
   OperationUpload(courseid)
   print("Moodle Data Upload is completed")
else:
   print("Initiated the Moodle Cleanup Process")
   OperationCleanup(courseid)
   print('Clean up process completed')
   re_input=input("Do you wish to run the Upload process again-(1-Yes,0-No) ?")
   if re_input == "1":
      OperationUpload(courseid)
   else:
      print('Execution completed')
      exit()
