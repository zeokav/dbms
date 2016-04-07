from django.shortcuts import render
from django.http import HttpResponse
import cx_Oracle

def dashboard(request):
	return render(request, "Dashboard.html", {})

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
		if  (not retpass == None) and (pw == retpass):
			context = {"name": user}
			return render(request, "Dashboard.html", context)

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
		mob_no = request.POST.get("phone")
		email = request.POST.get("email")
		gender = request.POST.get("gender")
		password = request.POST.get("password")
		newUser = [p_id, user, mob_no, email, gender, password]
		cur.close()
		cur2 = con.cursor()
		#For batch inserts, there's a cx_Oracle function called execute many. This requires an array bind size.

		cur2.execute('INSERT into Person(person_id, name, mob_no, email, gender, password) values(:1, :2, :3, :4, :5, :6)', newUser)
		con.commit()
		cur2.close()

		context = {
			"template_title": "Thanks for signing up!"
		}

		#this thingy below is the in built form saving function of django. Let's go raw, instead. :D
		#instance.save()

	return render(request, "signup.html", context)

