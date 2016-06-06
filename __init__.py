from flask import Flask, render_template, url_for, request
import csv

app = Flask(__name__)

ranked_criteria = []
minors = []
majors = []

@app.route('/')
def homepage():
	
	return render_template("home.html")


@app.route('/major/')
def major():

	title = 'Selecting your Majors'
	subtext = 'Enter your majors. Or, select undecided.'
	#Send majors and minors to results
	return render_template("step_1.html", title = title, subtext = subtext)	



@app.route('/minor/', methods=['POST'])
def minor():

	global majors
	majors = [(request.form['major1']), (request.form['major2'])]
	#global majors = request.form



	title = 'Selecting your Minors'
	subtext = 'Enter your minors. Or, select undecided.'
	#Send majors and minors to results
	return render_template("minor.html", title = title, subtext = subtext)


@app.route('/select_and_rank/', methods=['POST'])
def select():

	global minors
	minors = [(request.form['minor1']), (request.form['minor2'])]



	title = 'Select and Rank'
	subtext = 'Select the criteria that are the most important to you in your college search, and rank them in order from top to bottom.'
	#Send criteria to rank
	return render_template("step_3.html", title = title, subtext = subtext)	
	

@app.route('/results/', methods=['POST'])
def results():
	#This is where we are doing all the calculations!
	global ranked_criteria
	global minors
	global majors

	x=1

	while x < 11:

		if request.form['c' + str(x)] != 'No Selection':
			number_of_criteria += 1
		ranked_criteria.append(request.form['c' + str(x)])
		x += 1

	f = open('/var/www/FlaskApp/FlaskApp/Gov_Data.csv')
	#a row is a list of strings
	#one row=one college
	csv_f = csv.reader(f)
	#for each college (row), we want to find what its total number of points is
	for row in csv_f:

		pt = float(row[31])
		#first check for public vs private
		#slice the row into rows 5 through 16


		priv = row[5:17]
		# priv indices go from 0-11
		
		
		if priv[0] != 'NULL' or priv[2] != 'NULL' or priv[3] != 'NULL' or priv[4] != 'NULL' or priv[5] != 'NULL' or priv[6] != 'NULL':
			#if the college is public
			if 'Public School' in ranked_criteria:
				pt += (100 / ranked_criteria.index('Public School'))
			else:
				pt += (20 / ranked_criteria.index('Public School'))


		elif priv[1] != 'NULL' or priv[7] != 'NULL' or priv[8] != 'NULL' or priv[9] != 'NULL' or priv[10] != 'NULL' or priv[11] != 'NULL':
			if 'Private School' in ranked_criteria:
				pt += (100 / ranked_criteria.index('Private School'))
			else:
				pt += (20 / ranked_criteria.index('Private School'))

		else:
			number_of_criteria -= 2


		#for the affordability part, first take the average of all the costs, (divide by number of non-null values). Then, proportionalize from a scale of 0-60,000 (arbitrary value) to a 0-100 scale

  








		row[31] = str(pt)/number_of_criteria





	#give each college a number of points for each category (use ranks of criteria here)



	#When each college has a score, loop again to put the top 10 colleges FOR EACH ADMISSIONS RATE BRACKET into THREE SEPERATE lists
	#Then output data

		




	title = 'Results'
	subtext = ''
	#Need to send all the data here
	return render_template('step_4.html', title = title, subtext = subtext)

	
if __name__ == "__main__":
	app.run(debug=True)


#Combine select and rank pages into one page, using awesomplete, where you type your choices into the boxes that are already numbered
