from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import cx_Oracle
import time

"""
Sky rails 2k16.
Database management project.
Python ftw.

This file has almost all the queries and basically everything that happens on a webpage is guided through the code in this file.
All the requests from the user end and retrieved here.
Any context sensitive information must be returned through the render callback along with a tag.
"""

auth = "dbms/dbms@localhost/orcl"
user = ""

def cancelled(request):
	pnr_cancel = int(request.GET.get("PNR"))
	query = 'DELETE from tickets where pnr = '+str(pnr_cancel)
	con = cx_Oracle.connect(auth)
	cur = con.cursor()
	cur.execute(query)
	con.commit()
	cur.close()
	con.close()
	return render(request, "cancelled.html", {})

def confirmed(request):
	context = {}
	return render(request, "confirmed.html", context)

def history(request):
	pt = request.get_full_path()
	try:
		username = pt.split("?")[1].split("=")[1]
	except:
		return HttpResponseRedirect('login')

	con = cx_Oracle.connect(auth)
	cur = con.cursor()
	query = 'SELECT pnr, train_id, journey_distance, date_of_journey, p1.platform_name, p2.platform_name, cost from (booking_history natural join tickets), platform p1, platform p2  where person_id = (SELECT person_id from person where name = \'' + username +'\') and p1.platform_id = startplatform_id and p2.platform_id = endplatform_id order by pnr'
	cur.execute(query)
	rows = cur.fetchmany()
	cur.close()
	con.close()
	return render(request, "history.html", {'entries': rows})

def traininfo(request):
	context = {}
	con = cx_Oracle.connect(auth)
	cur = con.cursor()
	query = 'SELECT train_id, train_name from train order by train_id'
	cur.execute(query)
	trainlist = cur.fetchmany()
	information = None
	hasInformation = 0
	context = {'trains': trainlist}
	if (request.method == 'POST'):
		whichtrain = request.POST.get("traindrop")
		return HttpResponseRedirect("/red?train=" + str(whichtrain))

	return render(request, "traininfo.html", context)
	
def red(request):
	pt = request.get_full_path()
	trainid = pt.split('?train=')[1]
	return render(request, "red.html", {'train': trainid})


def informationpage(request):
	pt = request.get_full_path()
	trainid = pt.split('?trainid=')[1]
	con = cx_Oracle.connect(auth)
	cur = con.cursor()
	query = 'SELECT platform_name, departure_time, arrival_time from train natural join visits natural join platform where train_id = '
	query += str(trainid)
	query += ' order by arrival_time'
	cur.execute(query)
	visits = cur.fetchmany()

	startsat = visits[0][0]
	endsat = visits[len(visits)-1][0]

	query = 'SELECT capacity from train where train_id = ' + str(trainid)
	cur.execute(query)
	capacity = cur.fetchone()[0]

	query = 'SELECT train_name from train where train_id = ' + str(trainid)
	cur.execute(query)
	trainname = cur.fetchone()[0]

	query = 'SELECT base_fare, cost_per_km from pricing where train_id = ' + str(trainid)
	cur.execute(query)
	pricing_details = cur.fetchone()
	base_fare, cost_per_km =  pricing_details[0], pricing_details[1]
	cost_per_km/=100

	cur.close()
	con.close()

	context = {'visits': visits, 'trainid': trainid, 'trainname': trainname, 'startsat': startsat, 'endsat': endsat, 'base': base_fare, 'perkm': cost_per_km,'capacity': capacity}

	return render(request, "informationpage.html", context)

def reserve(request):
	con = cx_Oracle.connect(auth)
	cur = con.cursor()
	query = 'SELECT platform_name from platform'
	cur.execute(query)
	stations = cur.fetchmany()
	stationnames = [station[0] for station in stations]
	cur.close()
	con.close()
	context = {"notrain": 0, "station_list": stationnames}

	f = open('savename', 'r')
	user_file = f.read()

	pt = request.get_full_path()
	try:
		username = pt.split("?")[1].split("=")[1]
	except:
		return HttpResponseRedirect('login')
	if (request.method == 'POST'):
		con = cx_Oracle.connect(auth)
		cur = con.cursor()
		start = request.POST.get("stationfrom")
		end = request.POST.get("stationto")
		doj = request.POST.get("doj")
		ntickets = request.POST.get("NOT")
		conv = time.strptime(doj, "%Y-%m-%d")
		formatted_date = time.strftime("%d-%b-%Y", conv)


		
		if start == end:
			context = {"notrain":1, "station_list": stationnames}
			return render(request, "reservation.html", context)

		try:
			query = 'SELECT platform_id FROM platform WHERE platform_name like \'%'+start+'%\''
			cur.execute(query)
			startid = cur.fetchone()[0]
			query = 'SELECT platform_id FROM platform WHERE platform_name like \'%'+end+'%\''
			cur.execute(query)
			endid = cur.fetchone()[0]
		except:
			context = {"notrain":0, "station_list": stationnames}
			return render(request, "reservation.html", context)

		query = 'select distinct(train_id) from visits where train_id in((select train_id from visits where platform_id like '+str(startid)+') intersect (select train_id from visits where platform_id like '+str(endid)+'))'
		cur.execute(query)
		train_nums = cur.fetchmany()
		trainlist = []
		for num in train_nums:
			query = 'SELECT train_name from train where train_id = ' + str(num[0])
			cur.execute(query)
			trainlist.append(cur.fetchone()[0])

		if(len(trainlist) == 0):
			context = {"notrain": 1, "station_list": stationnames}
			return render(request, "reservation.html", context)

		else:
			return HttpResponseRedirect('booklist?trains='+str(trainlist)+'&from='+str(startid)+'&to='+str(endid)+'&doj='+str(formatted_date)+'&count='+str(ntickets)+'&user='+str(user_file))

		cur.close()
		con.close()

	return render(request, "reservation.html", context)

def booklist(request):
	trains = str(request.GET.getlist('trains')).split('\'')[1::2]
	trainsTuples = []
	doj = str(request.GET.get("doj"))
	con = cx_Oracle.connect(auth)
	cur = con.cursor()

	for train in trains:
		query = 'SELECT sum(total) from tickets where date_of_journey = \''+ str(doj) + '\' and train_id in (SELECT train_id from train where train_name = \''+str(train)+'\')'
		booked = 0
		try:
			cur.execute(query)
			booked = int(cur.fetchone()[0])
		except:
			booked = 0

		query = 'SELECT capacity from train where train_id in (SELECT train_id from train where train_name = \''+str(train)+'\')'
		cur.execute(query)
		seats_left = int(cur.fetchone()[0]) - booked;
		item = (train, seats_left)
		trainsTuples.append(item)
	

	context = {"trainsAvailable": trainsTuples}
	return render(request, "booklist.html", context)

def checkout(request):
	pt = request.get_full_path()
	context ={}

	try:
		chosen, details = pt.split('?')[1].split('=')[1].split('&')[0].split('%20')[0]+' '+pt.split('?')[1].split('=')[1].split('&')[0].split('%20')[1], pt.split('?')[2]
		startid = details.split('&from=')[1].split('&')[0]
		endid = details.split('&to=')[1].split('&')[0]
		doj = details.split('&doj=')[1].split('&')[0]
		count = int(details.split('&count=')[1].split('&')[0])
		user = details.split('&user=')[1]

		con = cx_Oracle.connect(auth)
		cur = con.cursor()
		query = 'SELECT pnr from tickets order by pnr desc'
		try:
			cur.execute(query)
			last_pnr = cur.fetchone()[0]
		except:
			last_pnr = 0
		last_pnr += 1

		query = 'SELECT platform_name from platform where platform_id = \'' + str(startid) + '\''
		cur.execute(query)
		startname = cur.fetchone()[0]

		query = 'SELECT platform_name from platform where platform_id = \'' + str(endid) + '\''
		cur.execute(query)
		endname = cur.fetchone()[0]

		query = 'SELECT train_id from train where train_name like \'%' + str(chosen) + '%\''
		cur.execute(query)
		train_id = cur.fetchone()[0]

		query = 'select departure_time from visits where train_id ='+str(train_id)+' and platform_id =' + str(startid)
		cur.execute(query)
		time = cur.fetchone()[0]

		query = 'SELECT person_id from person where name = \'' + str(user) + '\''
		cur.execute(query)
		person_id = cur.fetchone()[0]

		b_query = 'SELECT xcoord, ycoord from platform where platform_id = '
		query = b_query + str(startid)
		cur.execute(query)
		_coords1 = cur.fetchone()

		query = b_query + str(endid)
		cur.execute(query)
		_coords2 = cur.fetchone()

		distance = (_coords2[0]-_coords1[0])**2 + (_coords2[1]-_coords1[1])**2

		query = 'SELECT base_fare, cost_per_km from pricing where train_id = ' + str(train_id)
		cur.execute(query)
		pricing_details = cur.fetchone()

		cost = int(pricing_details[0] + (distance * pricing_details[1]/100))
		cost*= count
		#print cost

		place_values = {'user_id': person_id, 'PNR': last_pnr, 'chosen': chosen, 'from': startname, 'to': endname, 'doj': doj, 'ntickets': count, 'time': time, 'cost': cost}

		cur.close()
		con.close()

		conins = cx_Oracle.connect(auth)
		cur2 = conins.cursor()
		row = (person_id, last_pnr)
		insquery = 'insert into booking_history(person_id, pnr) values (:1, :2)'
		try:
			cur2.execute(insquery, row)
			conins.commit()
		except:
		 	print "Error"
		finally:
			cur2.close()
			conins.close()

		conins2 = cx_Oracle.connect(auth)
		cur3 = conins2.cursor()
		insquery = 'insert into tickets(pnr, train_id, journey_distance, date_of_journey, startplatform_id, endplatform_id, person_id, total, cost) values(:1, :2, :3, :4, :5, :6, :7, :8, :9)'
		row = (last_pnr, train_id, distance, doj, startid, endid, person_id, count, cost)
		try:
			cur3.execute(insquery, row)
			conins2.commit()
		except:
			print "More error"
		finally:
			cur3.close()
			conins2.close()

		context = {'all_values': place_values}
		
	except:
		return HttpResponseRedirect('login')
		pass

	return render(request, "checkout.html", context)

def redirect(request):
	return HttpResponseRedirect('login')

def dashboard(request):
	pt = request.get_full_path()
	username = ""
	try:
		username = pt.split("?user=")[1].split("&")[0]
	except:
		return HttpResponseRedirect('login')
	

	try:
		deletepnr = int(pt.split("fromcheckout=")[1])
		query = 'DELETE from tickets where pnr = '+str(deletepnr)
		con = cx_Oracle.connect(auth)
		cur = con.cursor()
		cur.execute(query)
		cur.close()
		con.commit()
		con.close()

	except:
		pass

	f = open('savename', 'w')
	f.write(username)
	f.close()
	#To avoid direct access - 
	con = cx_Oracle.connect(auth)
	cur = con.cursor()
	query = 'SELECT count(*) from Person where name = \''+username+'\''
	cur.execute(query)
	isThere = cur.fetchone()[0]
	cur.close()
	con.close()

	if isThere == 0:
		return HttpResponseRedirect('login')

	return render(request, "Dashboard.html", {"name": username})

def login(request):

	context = {"checked": 0}

	if(request.method == 'POST'):
		user = request.POST.get("un")
		pw =  request.POST.get("pass")
		con = cx_Oracle.connect(auth)
		cur = con.cursor()
		query = 'SELECT password from Person where name = \'' + user + '\''
		cur.execute(query)
		retpass = None
		try:
			retpass = cur.fetchone()[0]
		except:
			context = {"checked": 1}
		cur.close()
		con.close()
		if (not retpass == None) and (pw == retpass):
			return HttpResponseRedirect('/dashboard?user='+user) #Ouiiiii finally

	return render(request, "login.html", context)


def created(request):
	return render(request, "created.html",{})

def signup(request):

	context = {}
	if (request.method == 'POST'):
		con = cx_Oracle.connect(auth)
		cur = con.cursor()
		cur.execute('SELECT person_id from Person order by person_id desc')
		top = cur.fetchone()[0]
		p_id = top+1
		user = request.POST.get("un")
		cur.execute("SELECT count(person_id) from Person where name = \'"+user+"\'")
		cnt = cur.fetchone()[0]
		if(cnt == 1):
			context = {"exists": 1}
			return render(request, "signup.html", context)
		mob_no = request.POST.get("phone")
		email = request.POST.get("email")
		gender = request.POST.get("gender")
		password = request.POST.get("password")
		newUser = [p_id, user, mob_no, email, gender, password]
		cur.close()
		cur2 = con.cursor()

		cur2.execute('INSERT into Person(person_id, name, mob_no, email, gender, password) values(:1, :2, :3, :4, :5, :6)', newUser)
		con.commit()
		cur2.close()
		return HttpResponseRedirect('/created')


	return render(request, "signup.html", context)