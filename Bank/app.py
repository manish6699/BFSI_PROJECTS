#!C:\Users\ADMIN\AppData\Local\Programs\Python\Python37-32\python
print("Content-Type: text/html\n\n")
import datetime,time
import cgi
from flask import Flask,request,render_template,redirect,url_for,session
import mysql.connector
con=mysql.connector.connect(host="localhost",user="root",passwd="manish6699",database="bankwithfd")
cursor=con.cursor()
form=cgi.FieldStorage()
app=Flask(__name__)
@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/cushome')
def cushome():
	return render_template('cushome.html')


@app.route('/signin')
def signin():
	return render_template('signin.html')

check=0
@app.route('/validate',methods=['POST','GET'])
def validate():
	global check
	if request.form['submit']:
		cuid=request.form['cusid']
		passwd=request.form['pass']
		cursor.execute('''SELECT f_name,cus_id FROM customer WHERE `cus_id`=%s AND password=%s''',(cuid,passwd))
		result=cursor.fetchone()
		if result:
			session['customer']=result[0]
			session['cusid']=result[1]
			check=0
			return render_template('cushome.html')
		else:
			check+=1
			if(check>2):
				return redirect(url_for('home'))
			else:
				return redirect(url_for('signin'))


@app.route('/signup')
def signup():
	return render_template('signup.html')
 

@app.route('/cusinsert',methods=['POST','GET'])
def cusinsert():
	if request.form['submit']:
		firstn=request.form['fname']
		lastn=request.form['lname']
		passwd=request.form['pass']
		addline1=request.form['adline1']
		addline2=request.form['adline2']
		s=request.form['state']
		c=request.form['city']
		pin=request.form['pincode']
		acctype=request.form['type']
		initamount=request.form['amount']
		dac=datetime.datetime.now()
		cursor.execute('''INSERT INTO customer(`f_name`, `l_name`, `ad_line1`, `ad_line2`, `state`, `city`, `pincode`, `password`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',(firstn,lastn,addline1,addline2,s,c,pin,passwd))
		cursor.execute('''SELECT `cus_id` FROM customer ORDER BY `cus_id` DESC LIMIT 1''')
		result=cursor.fetchone()
		cusid=result[0]
		cursor.execute('''INSERT INTO account(`type`,`balance`,`doac`,`cus_id`) VALUES (%s,%s,%s,%s)''',(acctype,initamount,dac,cusid))
		cursor.execute('''SELECT `cus_id`,`acc_no` FROM account ORDER BY `acc_no` DESC LIMIT 1''')
		result=cursor.fetchone()
		custid=result[0]
		acno=result[1]
		return render_template('dispaccnocusid.html',data=custid,data1=acno)


@app.route('/addupdate')
def addupdate():
	return render_template('addupdate.html')

@app.route('/updateadd',methods=['POST','GET'])
def updateadd():
	if request.form['submit']:
		if request.form['adline1']:
			cursor.execute('''UPDATE customer set `ad_line1`=%s WHERE `cus_id`=%s''',(request.form['adline1'],session['cusid']))
		if request.form['adline2']:
			cursor.execute('''UPDATE customer set `ad_line2`=%s WHERE `cus_id`=%s''',(request.form['adline2'],session['cusid']))
		if request.form['state']:
			cursor.execute('''UPDATE customer set `state`=%s WHERE `cus_id`=%s''',(request.form['state'],session['cusid']))
		if request.form['city']:
			cursor.execute('''UPDATE customer set `city`=%s WHERE `cus_id`=%s''',(request.form['city'],session['cusid']))
		if request.form['pin']:
			cursor.execute('''UPDATE customer set `pincode`=%s WHERE `cus_id`=%s''',(request.form['pin'],session['cusid']))
	return render_template('cushome.html')
 

@app.route('/moneydep')
def moneydep():
	return render_template('moneydep.html')

@app.route('/mondep',methods=['POST','GET'])
def mondep():
	if request.form['submit']:
		ama=request.form['amount']
		acc=request.form['accno']
		cursor.execute('''SELECT `acc_no` FROM account WHERE `acc_no`=%s AND `cus_id`=%s''',(acc,session['cusid']))
		result=cursor.fetchone()
		if result:
			cursor.execute('''SELECT `balance` FROM account WHERE `acc_no`=%s''',(acc,))
			result=cursor.fetchone()
			newresult=int(result[0])+int(ama)
			cursor.execute('''UPDATE account SET `balance`=%s WHERE `acc_no`=%s''',(newresult,acc))
			curtime=datetime.datetime.today().strftime('%y-%m-%d')
			cursor.execute('''INSERT INTO transaction_details(`acc_no`,`time_stamp`,`type`,`amount`) VALUES (%s,%s,%s,%s)''',(acc,curtime,'deposit',ama))
			return render_template('cushome.html')
		else:
			return "<h1>account number doesn't match, please enter valid account number</h1>"


@app.route('/moneywith')
def moneywith():
	return render_template('moneywith.html')

withcount=0
month=0
@app.route('/withmoney',methods=['POST','GET'])
def withmoney():
	global withcount,month
	if request.form['submit']:
		ama=request.form['amount']
		acc=request.form['accno']
		cursor.execute('''SELECT `acc_no` FROM account WHERE `acc_no`=%s AND `cus_id`=%s''',(acc,session['cusid']))
		result=cursor.fetchone()
		if result:
			cursor.execute('''SELECT `type`,`balance` FROM account WHERE `acc_no`=%s''',(acc,))
			result=cursor.fetchone()
			acctype=result[0]
			curtime=datetime.datetime.today().strftime('%y-%m-%d')
			if acctype=="savings":
				newresult=int(result[1])-int(ama)
				if withcount==0:
					month=datetime.datetime.now().strftime("%m")
				if newresult>=0:
					if month==datetime.datetime.now().strftime("%m"):
						withcount+=1
						if withcount>10:
							return "<h1>In a month you can withdraw only 10 times</h1>"
						else:	
							cursor.execute('''UPDATE account set `balance`=%s WHERE `acc_no`=%s''',(newresult,acc))
							cursor.execute('''INSERT INTO transaction_details(`acc_no`,`time_stamp`,`type`,`amount`) VALUES (%s,%s,%s,%s)''',(acc,curtime,'withdrawal',ama))
					else:
						withcount=0
						cursor.execute('''UPDATE account set `balance`=%s WHERE `acc_no`=%s''',(newresult,acc))
						cursor.execute('''INSERT INTO transaction_details(`acc_no`,`time_stamp`,`type`,`amount`) VALUES (%s,%s,%s,%s)''',(acc,curtime,'withdrawal',ama))
				else:
					return "<h1>insufficient balance</h1>"
			if acctype=="current":
				newresult=int(result[1])-int(ama)
				if newresult>=5000:
					cursor.execute('''UPDATE account set `balance`=%s WHERE `acc_no`=%s''',(newresult,acc))
					cursor.execute('''INSERT INTO transaction_details(`acc_no`,`time_stamp`,`type`,`amount`) VALUES (%s,%s,%s,%s)''',(acc,curtime,'withdrawal',ama))
				else:
					return "<h1>insufficient balance</h1>"
		else:
			return "<h1>account number doesn't match, please eneter valid account number</h1>"
		return render_template('cushome.html')


@app.route('/ministate')
def ministate():
	return render_template('ministate.html')


@app.route('/statmini',methods=['POST','GET'])
def statmini():
	if request.form['submit']:
		acc=request.form['accno']
		fromd=request.form['fdate']
		tod=request.form['tdate']
		cursor.execute('''SELECT `acc_no` FROM account WHERE `acc_no`=%s AND `cus_id`=%s''',(acc,session['cusid']))
		result=cursor.fetchone()
		if result:
			if fromd<=tod:
				cursor.execute('''SELECT `t_id`, `acc_no`, `time_stamp`, `type`, `amount` FROM `transaction_details` WHERE `acc_no`=%s and `time_stamp` BETWEEN %s AND %s''',(acc,fromd,tod))
				data=cursor.fetchall()
				cursor.execute('''SELECT `balance` FROM account WHERE `acc_no`=%s''',(acc,))
				data1=cursor.fetchone()
				return render_template('disp.html',data=data,data1=data1)
			else:
				return "<h1>invalid date entries</h1>"
		else:
			return "<h1>account number doesn't match, please eneter valid account number</h1>"

@app.route('/moneytrans')
def moneytrans():
	return render_template('moneytrans.html')

@app.route('/transmoney',methods=['POST','GET'])
def transmoney():
	if request.form['submit']:
		fromacno=request.form['fromaccno']
		toacno=request.form['toaccno']
		ama=request.form['amount']
		cursor.execute('''SELECT `acc_no`,`balance` FROM account WHERE `acc_no`=%s''',(toacno,))
		result=cursor.fetchone()
		bal=result[1]
		if result:
			cursor.execute('''SELECT `type`,`balance` FROM account WHERE `acc_no`=%s AND `cus_id`=%s''',(fromacno,session['cusid']))
			result=cursor.fetchone()
			if result:
				acctype=result[0]
				curtime=datetime.datetime.today().strftime('%y-%m-%d')
				if acctype=="savings":
					newresult=int(result[1])-int(ama)
					toresult=int(bal)+int(ama)
					if newresult>=0:
						cursor.execute('''UPDATE account set `balance`=%s WHERE `acc_no`=%s''',(newresult,fromacno))
						cursor.execute('''UPDATE account set `balance`=%s WHERE `acc_no`=%s''',(toresult,toacno))
						cursor.execute('''INSERT INTO transaction_details(`acc_no`,`time_stamp`,`type`,`amount`) VALUES (%s,%s,%s,%s)''',(fromacno,curtime,'transfer',ama))
						cursor.execute('''INSERT INTO `transfer`(`from_ac_no`, `to_ac_no`, `amount`) VALUES (%s,%s,%s)''',(fromacno,toacno,ama))
						return render_template("dispaftertranbal.html",data1=newresult,data2=toresult)
					else:
						return "<h1>insufficient balance</h1>"

				if acctype=="current":
					newresult=int(result[1])-int(ama)
					toresult=int(bal)+int(ama)
					if newresult>=5000:
						cursor.execute('''UPDATE account set `balance`=%s WHERE `acc_no`=%s''',(newresult,fromacno))
						cursor.execute('''UPDATE account set `balance`=%s WHERE `acc_no`=%s''',(toresult,toacno))
						cursor.execute('''INSERT INTO transaction_details(`acc_no`,`time_stamp`,`type`,`amount`) VALUES (%s,%s,%s,%s)''',(fromacno,curtime,'transfer',ama))
						cursor.execute('''INSERT INTO `transfer`(`from_ac_no`, `to_ac_no`, `amount`, `date`) VALUES (%s,%s,%s,%s)''',(fromacno,toacno,ama,curtime))
						return render_template("dispaftertranbal.html",data1=newresult,data2=toresult)
					else:
						return "<h1>insufficient balance</h1>"
				else:
					return "<h1>invalid account type</h1>"
			else:
				return "<h1>invalid sender account number</h1>"			
		else:
			return "<h1>invalid recipient account number</h1>"
			
			

@app.route('/accclose')
def accclose():
	return render_template('accclose.html')

@app.route('/closeacc',methods=['POST','GET'])
def closeacc():
	if request.form['submit']:
		accno=request.form['acno']
		cursor.execute('''SELECT `acc_no` FROM account WHERE `acc_no`=%s AND `cus_id`=%s''',(accno,session['cusid']))
		result=cursor.fetchone()
		if result:
			curtime=datetime.datetime.today().strftime('%y-%m-%d')
			cursor.execute('''SELECT `ad_line1`, `ad_line2`, `state`, `city`, `pincode` FROM customer WHERE `cus_id`=%s''',(session['cusid'],))
			result=cursor.fetchone()
			cursor.execute('''SELECT `balance` FROM account WHERE `acc_no`=%s''',(accno,))
			result1=cursor.fetchone()
			cursor.execute('''DELETE FROM account WHERE `acc_no`=%s''',(accno,))
			cursor.execute('''INSERT INTO closed_acc_history(`acc_no`, `closedate`) VALUES (%s,%s)''',(accno,curtime))
			return render_template('dispclosedetails.html',data=result,data1=result1,data2=accno)
		else:
			return "<h1>invalid account number</h1>"

@app.route('/adsignin')
def adsignin():
	return render_template('adsignin.html')

@app.route('/adminhome',methods=['POST','GET'])
def adminhome():
	if request.form['submit']:
		if request.form['name']=='admin' and request.form['pass']=='admin123':
			return render_template('adminhome.html')
		else:
			return "<h1>name and password mismatch</h1>"

@app.route('/adminhome1')
def adminhome1():
	return render_template('adminhome.html')


@app.route('/closehistory')
def closehistory():
	cursor.execute('''SELECT * FROM closed_acc_history''')
	result=cursor.fetchall()
	return render_template('dispaccclosehist.html',data=result)


@app.route('/opennewacc')
def opennewacc():
	return render_template('opennewacc.html')

@app.route('/newacc',methods=['POST','GET'])
def newacc():
	if request.form['submit']:
		session['acctype']=request.form['type']
		if session['acctype']=="savings":
			return render_template('savings.html')
		if session['acctype']=="current":
			return render_template('current.html')
		if session['acctype']=="fixed deposit":
			return render_template('fd.html')

@app.route('/createacc',methods=['POST','GET'])
def createacc():	
	curtime=datetime.datetime.now()	
	if session['acctype']=="savings":
		if request.form['submit']:
			inam=request.form['amount']
			cursor.execute('''INSERT INTO account(`type`,`balance`,`doac`,`cus_id`) VALUES (%s,%s,%s,%s)''',(session['acctype'],inam,curtime,session['cusid']))
			session.pop('acctype',None)			
			return render_template('cushome.html')

	if session['acctype']=="current":
		if request.form['submit']:
			inam=request.form['amount']
			cursor.execute('''INSERT INTO account(`type`,`balance`,`doac`,`cus_id`) VALUES (%s,%s,%s,%s)''',(session['acctype'],inam,curtime,session['cusid']))
			session.pop('acctype',None)	
			return render_template('cushome.html')

	if session['acctype']=="fixed deposit":
		if request.form['submit']:
			dam=request.form['damount']
			period=request.form['term']
			cursor.execute('''INSERT INTO account(`type`,`balance`,`doac`,`cus_id`) VALUES (%s,%s,%s,%s)''',(session['acctype'],dam,curtime,session['cusid']))
			cursor.execute('''SELECT `acc_no` FROM account ORDER BY `acc_no` DESC LIMIT 1''')
			result=cursor.fetchone()
			acno=result[0]
			cursor.execute('''INSERT INTO fd_account(`fd_accno`, `cus_id`, `fd_amount`, `fd_period`) VALUES (%s,%s,%s,%s)''',(acno,session['cusid'],dam,period))
			return render_template('cushome.html')

	else:
		return "<h1>enter valid account type</h1>"


@app.route('/availloan')
def availloan():
	return render_template('availloan.html')

@app.route('/applyloan',methods=['POST','GET'])
def applyloan():
	if request.form['submit']:
		loanamount=request.form['amount']
		period=request.form['term']
		cursor.execute('''SELECT SUM(`balance`) FROM account WHERE `cus_id`=%s AND `type`=%s''',(session['cusid'],'savings'))
		result=cursor.fetchone()
		if (int(loanamount))<=(2*int(result[0])):
			cursor.execute('''INSERT INTO loan_account(`cus_id`, `loan_amount`, `repayment_term`) VALUES (%s,%s,%s)''',(session['cusid'],loanamount,period))
			cursor.execute('''SELECT `loan_accno`, `loan_amount`, `repayment_term` FROM loan_account WHERE `cus_id`=%s''',(session['cusid'],))
			result=cursor.fetchall()
			return render_template('disploan.html',data=result)
		else:
			return "<h1>sorry you are not eligible to apply for loan</h1>"


@app.route('/fdrc')
def fdrc():
	return render_template('fdrc.html')

@app.route('/newfdrc',methods=['POST','GET'])
def newfdrc():
	if request.form['submit']:
		cusid=request.form['cid']
		cursor.execute('''SELECT `cus_id` FROM customer WHERE `cus_id`=%s''',(cusid,))
		result=cursor.fetchone()
		if result:
			cursor.execute('''SELECT `fd_accno`, `fd_amount`, `fd_period` FROM fd_account WHERE `cus_id`=%s''',(cusid,))
			result=cursor.fetchall()
			if result:
				return render_template('dispfrdc.html',data=result)
			else:
				return "<h1>N.A</h1>"

@app.route('/fdrcac')
def fdrcac():
	return render_template('fdrcac.html')

@app.route('/newfdrcac',methods=['POST','GET'])
def newfdrcac():
	if request.form['submit']:
		cusid=request.form['cid']
		cursor.execute('''SELECT `cus_id` FROM customer WHERE `cus_id`=%s''',(cusid,))
		result=cursor.fetchone()
		if result:
			cursor.execute('''SELECT sum(`fd_amount`) FROM fd_account WHERE `cus_id`=%s''',(cusid,))
			result=cursor.fetchone()
			if result:
				cursor.execute('''SELECT * FROM fd_account WHERE `fd_amount`>=%s AND `cus_id`!=%s''',(int(result[0]),cusid))
				result=cursor.fetchall()
				return render_template('dispfrdcac.html',data=result)
		else:
			return "<h1>N.A</h1>"


@app.route('/fdrcpa')
def fdrcpa():
	return render_template('fdrcpa.html')

@app.route('/newfdrcpa',methods=['POST','GET'])
def newfdrcpa():
	if request.form['submit']:
		ama=request.form['amount']
		cursor.execute('''SELECT * FROM fd_account WHERE `fd_amount`>=%s''',(ama,))
		result=cursor.fetchall()
		return render_template('dispfdrcpa.html',data=result)

@app.route('/lrc')
def lrc():
	return render_template('lrc.html')

@app.route('/newlrc',methods=['POST','GET'])
def newlrc():
	if request.form['submit']:
		cusid=request.form['cid']
		cursor.execute('''SELECT `cus_id` FROM customer WHERE `cus_id`=%s''',(cusid,))
		result=cursor.fetchone()
		if result:
			cursor.execute('''SELECT `loan_accno`, `loan_amount`, `repayment_term` FROM loan_account WHERE `cus_id`=%s''',(cusid,))
			result=cursor.fetchall()
			if result:
				return render_template('displrc.html',data=result)
			else:
				return "<h1>Not Availed</h1>"

@app.route('/lrcac')
def lrcac():
	return render_template('lrcac.html')

@app.route('/newlrcac',methods=['POST','GET'])
def newlrcac():
	if request.form['submit']:
		cusid=request.form['cid']
		cursor.execute('''SELECT `cus_id` FROM customer WHERE `cus_id`=%s''',(cusid,))
		result=cursor.fetchone()
		if result:
			cursor.execute('''SELECT sum(`loan_amount`) FROM loan_account WHERE `cus_id`=%s''',(cusid,))
			result=cursor.fetchone()
			if result:
				cursor.execute('''SELECT * FROM loan_account WHERE `loan_amount`>=%s AND `cus_id`!=%s''',(int(result[0]),cusid))
				result=cursor.fetchall()
				return render_template('displrcac.html',data=result)
		else:
			return "<h1>Not Availed</h1>"



@app.route('/lrcpa')
def lrcpa():
	return render_template('lrcpa.html')

@app.route('/newlrcpa',methods=['POST','GET'])
def newlrcpa():
	if request.form['submit']:
		ama=request.form['amount']
		cursor.execute('''SELECT * FROM loan_account WHERE `loan_amount`>=%s''',(ama,))
		result=cursor.fetchall()
		return render_template('displrcpa.html',data=result)



@app.route('/lfdc')
def lfdc():
	cursor.execute('''SELECT customer.`cus_id`, `f_name`, `l_name`,sum(`loan_amount`),sum(`fd_amount`) FROM customer,loan_account,fd_account WHERE customer.`cus_id`=loan_account.`cus_id` and customer.`cus_id`=fd_account.`cus_id` GROUP BY customer.`cus_id`''')
	result=cursor.fetchall()
	if result:
		return render_template('displfdc.html',data=result)
	else:
		return "no result to show"


@app.route('/yal')
def yal():
	cursor.execute('''SELECT customer.`cus_id`, `f_name`, `l_name` FROM customer,loan_account WHERE customer.`cus_id` not in  (SELECT cus_id from loan_account) GROUP BY customer.`cus_id`''')
	result=cursor.fetchall()
	if result:
		return render_template('dispyal.html',data=result)
	else:
		return "no result to show"

@app.route('/yofd')
def yofd():
	cursor.execute('''SELECT customer.`cus_id`, `f_name`, `l_name` FROM customer,fd_account WHERE customer.`cus_id` not in (SELECT cus_id from fd_account) GROUP BY `cus_id`''')
	result=cursor.fetchall()
	if result:
		return render_template('dispyofd.html',data=result)
	else:
		return "no result to show"

@app.route('/cdfdal')
def cdfdal():
	cursor.execute('''SELECT customer.`cus_id`, `f_name`, `l_name` FROM customer,fd_account,loan_account WHERE customer.`cus_id` not in (SELECT cus_id from fd_account) and customer.cus_id not in (SELECT cus_id from loan_account) GROUP BY `cus_id`''')
	result=cursor.fetchall()
	if result:
		return render_template('dispcdfdal.html',data=result)
	else:
		return "no result to show"


@app.route('/thankyou')
def thankyou():
	return render_template('thankyou.html')


@app.route('/logout')
def logout():
	session.pop('customer',None)
	session.pop('cusid',None)
	return redirect(url_for('home'))


if __name__=="__main__":
	app.secret_key='super secret key'
	app.config['SESSION_TYPE']='filesystem'
	app.run(port=5001,debug=True)
