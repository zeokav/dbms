from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import cx_Oracle


#13287 train, start 90006 end 90007
def history(request):
	pt = request.get_full_path()
	try:
		username = pt.split("?")[1].split("=")[1]
	except:
		return HttpResponseRedirect('login')

	con = cx_Oracle.connect("dbms/dbms@localhost/orcl")
	cur = con.cursor()
	query = 'SELECT pnr, train_id, journey_distance, date_of_journey, p1.platform_name, p2.platform_name from (booking_history natural join tickets), platform p1, platform p2  where person_id = (SELECT person_id from person where name = \'' + username +'\') and p1.platform_id = startplatform_id and p2.platform_id = endplatform_id order by date_of_journey'
	cur.execute(query)
	rows = cur.fetchmany()
	print rows
	cur.close()
	con.close()
	return render(request, "history.html", {'entries': rows})

def traininfo(request):
	return render(request, "traininfo.html", {})
	

def reserve(request):
	context = {}
	if (request.method == 'POST'):
		con = cx_Oracle.connect("dbms/dbms@localhost/orcl")
		cur = con.cursor()
		start = request.POST.get("from")
		end = request.POST.get("to")
		doj = request.POST.get("date")
		query = 'SELECT train_name from '
		#cur.execute(query)
		cur.close()
		con.close()

	return render(request, "reservation.html", context)

def redirect(request):
	return HttpResponseRedirect('login')

def dashboard(request):
	pt = request.get_full_path()
	username = ""
	try:
		username = pt.split("?")[1].split("=")[1]
	except:
		return HttpResponseRedirect('login')
	
	#To avoid direct access - 
	con = cx_Oracle.connect("dbms/dbms@localhost/orcl")
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
		con = cx_Oracle.connect("dbms/dbms@localhost/orcl")
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


def signup(request):
	#request is whenever you're changing contexts.
	#It contains information about get and post.

	#if(request.method == "POST"):
		#print request.POST

#	form = PersonForm(request.POST or None) #In case there's no information in the post data, don't send through the validator

	context = {}

	if (request.method == 'POST'):
		con = cx_Oracle.connect('dbms/dbms@localhost/orcl')
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
		#For batch inserts, there's a cx_Oracle function called executemany. This requires an array bind size.

		cur2.execute('INSERT into Person(person_id, name, mob_no, email, gender, password) values(:1, :2, :3, :4, :5, :6)', newUser)
		con.commit()
		cur2.close()
		context = {}

		#this thingy below is the in built form saving function of django. Let's go raw, instead. :D
		#instance.save()

	return render(request, "signup.html", context)

