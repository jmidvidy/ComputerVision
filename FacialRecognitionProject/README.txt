-------------------------------------------------------------------------------
 This directory contains the final submission
materials for my final project for EECS 332.
-------------------------------------------------------------------------------
Here is a beif description of the materials
in this direcory:
 - /cascades/
	This directory stores the many haar cascades
	that the program uses.
 - /database/
	This directory stores the database of enrolled faces
	created by the program during enrollment.
 - /testing/
	This directory stores the 100 images of a claimaint 
	when the program is running input.
 - FaceCapture.py
	This Python file is called by FacesRun.py to launch the camera
	and capture images of a face for training and testing.
 - FacesRun.py
	This the main driver of the program.  To run the program, enter
	$ py FacesRun.py $ from the command line.
 - FacesTest.py
	This Python file is called by FacesRun.py to perform testing
	on input images.
 - FacesTrain.py
	This Python file is called by FacesRun.py to train the recognizer
	after the enrollment of the database.
 - Presentation.PDF
	This is a PDF print-out of the slides I presented to the class during
	my talk on 12/4.
 - FinalReport.PDF
	This is the PDF of my Final Report.
 - trinner.yml
	This .yml file is used by the recognizer after training.
 - README.txt
	This README file.
-------------------------------------------------------------------------------
Author: Jeremy Midvidy, jam658