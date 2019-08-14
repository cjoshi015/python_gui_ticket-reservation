from Tkinter import *
import tkMessageBox
import ttk
import MySQLdb
import pyqrcode
import qrcode
from PIL import ImageTk, Image
import uuid
import datetime
import smtplib
from email.mime.text import MIMEText


class GUI():

	def __init__(self):	
		self.root = Tk()
		self.root.geometry("800x600+80+30")
		self.root.title("Ticket Checker App")
		self.root.resizable(width=False, height=False)
		self.root.columnconfigure(1, weight=1)
		self.root.rowconfigure(0, weight=1)
		self.panel1 = Frame(self.root,borderwidth=2,
            width=200,
            height=570,
            relief=GROOVE)
		self.panel1.grid(column= 0, row = 0, sticky=(N, S, E, W))
		self.panel2 = None
		self.db = MySQLdb.connect("localhost","root","Cjoshi@015","tc" )
		self.cursor = self.db.cursor()	
		self.server =smtplib.SMTP('smtp.gmail.com',587)
		self.server.starttls()
		self.server.login('candypy015@gmail.com','Cjoshi@015')
		self.user_login_button=Button(self.panel1,text="User",width=20,command=self.Userlogin)
		self.user_login_button.grid(column=0, row=0, sticky=(W,N))
		self.admin_login_button=Button(self.panel1,text="Admin",width=20,command=self.Adminlogin)
		self.admin_login_button.grid(column=0, row=1, sticky=(W,N))
		self.tc_button=Button(self.panel1,text="Ticket Checker",width=20,command=self.Tc_login)
		self.tc_button.grid(column=0, row=2, sticky=(W,N))
		self.logout_button=Button(self.panel1,text="Logout",width=20,state='disable',command=self.logoutfunction)
		self.logout_button.grid(column=0, row=3,pady=455, sticky=S)
		bottom_panel= Frame(self.root, borderwidth=1, height=10, relief=SUNKEN)
		bottom_panel.grid(column=0, columnspan=2, row=1, sticky=(S,W,E))
		bottom_panel.columnconfigure(0, weight=1)
		bottom_label = Label(bottom_panel, font="Times 13")
		bottom_label.config(text="Ticket Checkar App,Created by Chandan Joshi " + u"\u00a9" + "2018",)
		bottom_label.grid(row=0, column=1) 
		
		self.status_label = Label(bottom_panel,font="Times 14")
		self.status_label.grid(row=0, column=0, sticky=W)
		self.welcome()
		self.statusUpdate("Ok")
		self.root.mainloop()
		   
    
    	
	def welcome(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		self.panel2 = Frame(self.root,borderwidth=2,width=650,height=570,relief=GROOVE)    
		self.panel2.grid(column=1, row=0, sticky=(N, S, E, W))
		welcome_text = "\nWelcome to Ticket Checker App"
		welcome_label = Label(self.panel2, text=welcome_text, font="Times 28")
		welcome_label.place(x=80, y=200)
	def logoutfunction(self):
		result = tkMessageBox.askquestion("Warning", "Confirm logout?", icon='warning')
		
		if result=='yes':
			self.Userlogin()
			self.user_login_button.config(state='active')
			self.admin_login_button.config(state='active')
			self.tc_button.config(state='active')
			self.logout_button.config(state='disable')
		else:
			pass
		
	def statusUpdate(self, msg):
		self.status_label.config(text="Status: " + msg)
		
	def Userlogin(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)
		Label(addform, text="\n\nLogin or Register", font="Time 16").grid(row=0,column=0, sticky=N+E+W, pady=20, columnspan=3)

		global username
		global password
	
		username=StringVar()
		password=StringVar()
		Label(addform, text='username'+':', font="16").grid(row=1, column=0, sticky=E)
		Entry(addform, width=30, font="16",textvariable=username, relief=SUNKEN).grid(row=1, column=1, 	sticky=W,pady=5, columnspan=2)
		Label(addform, text='password'+':', font="16").grid(row=2, column=0, sticky=E)
		Entry(addform,show="*",width=30, font="16",textvariable=password, relief=SUNKEN).grid(row=2, column=1, sticky=W,pady=5, columnspan=2)
		
		Button(addform,text="Sign in",command=self.login).grid(row = 3, column=1, sticky=E, pady=20,padx=10)
		Button(addform,text="Sign up",command=self.Signup).grid(row = 3, column=2, sticky=W, pady=20)
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
	
	def Adminlogin(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)
		Label(addform, text="\n\nLogin", font="Time 16").grid(row=0,column=0, sticky=N+E+W, pady=20, columnspan=3)

		global username_admin
		global password_admin
	
		username_admin=StringVar()
		password_admin=StringVar()
		Label(addform, text='username'+':', font="16").grid(row=1, column=0, sticky=E)
		Entry(addform, width=30, font="16",textvariable=username_admin, relief=SUNKEN).grid(row=1, column=1, 	sticky=W,pady=5, columnspan=2)
		Label(addform, text='password'+':', font="16").grid(row=2, column=0, sticky=E)
		Entry(addform,show="*",width=30, font="16",textvariable=password_admin, relief=SUNKEN).grid(row=2, column=1, sticky=W,pady=5, columnspan=2)
		
		Button(addform,text="Sign in",command=self.admin_login).grid(row = 3, column=1, sticky=E, pady=20,padx=10)
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)

	def Signup(self):
		def SaveData():
			sql="insert into Registration values('%s','%s','%s','%s','%s','%s')"%(name.get(),username1.get(),password1.get(),address.get(),phoneno.get(),email.get())
			self.cursor.execute(sql)
			self.db.commit()
			tkMessageBox.showinfo("Warning","Please Insert valid details")
			self.Userlogin()
			
		
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)
		Label(addform, text="\nRegister", font="Time 16").grid(row=0,column=0, sticky=N+E+W, pady=20, columnspan=3)

		global username1
		global password1
		global name
		global address
		global phoneno
		global email
	
		username1=StringVar()
		password1=StringVar()
		name=StringVar()
		address=StringVar()
		phoneno=StringVar()
		email=StringVar()
		
		Label(addform, text='Name'+':', font="16").grid(row=1, column=0, sticky=W,padx=20,pady=10)
		Entry(addform, width=30, font="16",textvariable=name).grid(row=1, column=1, sticky=W,pady=10)
		
		Label(addform, text='Username'+':', font="16").grid(row=2, column=0, sticky=W,padx=20,pady=10)
		Entry(addform, width=30, font="16",textvariable=username1).grid(row=2, column=1,sticky=W,pady=10)
		
		Label(addform,text='Password'+':', font="16").grid(row=3, column=0, sticky=W,padx=20,pady=10)
		Entry(addform,show="*", width=30, font="16",textvariable=password1).grid(row=3, column=1,sticky=W,pady=10)
		
		Label(addform, text='Address'+':', font="16").grid(row=4, column=0, sticky=W,padx=20,pady=10)
		Entry(addform, width=30, font="16",textvariable=address).grid(row=4, column=1, 	sticky=W,pady=10)
		
		Label(addform, text='Contact No'+':', font="16").grid(row=5, column=0, sticky=W,padx=20,pady=10)
		Entry(addform, width=30, font="16",textvariable=phoneno).grid(row=5, column=1, 	sticky=W,pady=10)
		
		Label(addform, text='Email'+':', font="16").grid(row=6, column=0, sticky=W,padx=20,pady=10)
		Entry(addform, width=30, font="16",textvariable=email).grid(row=6, column=1,sticky=W,pady=10)
		
		Button(addform,text="Register",command=SaveData).grid(row = 7, column=1, sticky=W, pady=10,padx=20)
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		self.statusUpdate("Registration for new customer")
            
	def login(self):
		if username.get()=='' or password.get()=='':	
			tkMessageBox.showinfo("Warning","Username or password can't be empty",icon='warning')		
		else:
			a=username.get()
			b=password.get()
			self.cursor.execute('select username,passowrd from Registration')
			self.entries = self.cursor.fetchall()
			flag=0
			for i in self.entries:
				if i[0]==a:
					if i[1]==b:
						flag=1
						self.BuyTicket()
    		if flag==1:
    			self.user_login_button.config(state='disable')
    			self.admin_login_button.config(state='disable')
    			self.tc_button.config(state='disable')
    			self.logout_button.config(state='active')
    		elif flag==0:
    			tkMessageBox.showinfo("Warning","Please Insert valid details",icon='warning')
				
	def admin_login(self):
		if username_admin.get()=='' or password_admin.get()=='':	
			tkMessageBox.showinfo("Warning","username or password can't be empty",icon='warning')	
		else:
			a=username_admin.get()
			b=password_admin.get()
			self.cursor.execute('select username,password from admin_login')
			self.entries = self.cursor.fetchall()
			flag=0
			for i in self.entries:
				if i[0]==a:
					if i[1]==b:
						flag=1
						self.admin_window()
			if flag==1:
				self.user_login_button.config(state='disable')
				self.admin_login_button.config(state='disable')
				self.tc_button.config(state='disable')
				self.logout_button.config(state='active')
			if flag==0:
				tkMessageBox.showinfo("Warning","Please Insert valid details",icon='warning')
				
    		
	def BuyTicket(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)
		Label(addform, text="\nBuy Ticket", font="Time 16").grid(row=0,column=0, sticky=N+E+W, pady=20, columnspan=3)
		sql_departure='select Departure from routes'
		sql_arrival='select Arrival from routes'
		self.cursor.execute(sql_departure)
		self.departure=self.cursor.fetchall()
		
		self.cursor.execute(sql_arrival)
		self.arrival=self.cursor.fetchall()
		
		global source
		global destination		
		source=StringVar()
		destination=StringVar()
		source.set("Source")
		destination.set("Destination") # default value		
		Label(addform, text="Select your Source :", font="16").grid(row=1, column=0, sticky=E)
		Label(addform, text="Select your Destination :", font="16").grid(row=2, column=0, sticky=E)
		a=[]
		for i in self.departure:
				a.append(i[0])			
		
		a=list(set(a))
		OptionMenu(addform, source,*a).grid(row=1, column=1, sticky=W, pady=5, columnspan=2)
		b=[]
		for i in self.arrival:
			b.append(i[0])
		
		b=list(set(b))		
		OptionMenu(addform, destination,*b).grid(row=2, column=1, sticky=W, pady=5, columnspan=2)
		Button(addform,text="Buy Ticket",command=self.Display_route).grid(row=3,column=1,sticky=W,padx=20,pady=20)
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		self.statusUpdate("Buy Your Ticket..")
		
	def to_destoy_frame(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		self.QR_code_show()
		
		
	def QR_code_show(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		
		import pyqrcode
		import Tkinter
		#id=1233434
		global id
		id = uuid.uuid4()
		id=str(id)[:8]
		a='Source :'+str(l[0])+'\n'+'Destination : '+str(l[1])+'\n'+'Time of booking : '+str(datetime.datetime.now().strftime("%H:%M"))+'\n'+'Transaction id :'+str(id)+'\n'+'Ticket Price : '+str(l[2])+'\n'+'Time of journey'+str(l[3])
		code = pyqrcode.create(a)
		code_xbm = code.xbm(scale=3)
		code_bmp = Tkinter.BitmapImage(data=code_xbm)
		code_bmp.config(background="white")
		
		label = Tkinter.Label(image=code_bmp)
		label.grid(row=0,column=1,sticky=E)
 		msg='Your Ticket Details are \nSource :'+source.get()+'\n'+'Destination : '+destination.get()+'\n'+'Time : '+str(datetime.datetime.now().strftime("%H:%M"))+'\n'+'Transaction id :'+str(id)+'\n'+'Thank You'+'\n'+'Happy Journey'
 		msg=MIMEText(a)
 		sql="select email from Registration where username='%s'"%(username.get())
 		self.cursor.execute(sql)
 		b=self.cursor.fetchall()
 		self.server.sendmail('Ticket Confirmation',b[0][0],msg.as_string(),'Ticket Details')
 		self.server.quit()
 		self.statusUpdate("Ticket Details...Happy Journey")
		Tkinter.mainloop()

	def PasswordCheck(self):
			if self.panel2 is not None:
				self.panel2.destroy()
			def validate_password():
				if passcheck.get()==password.get():
					self.seat_allocation()
				else:
					tkMessageBox.showinfo("Warning","Please Insert valid details",icon='warning')
			global passcheck
			passcheck=StringVar()
			addform=Frame(self.root,borderwidth=2,relief=GROOVE)
			Label(addform, text='\n\n', font="16").grid(row=1, column=0, sticky=E)
			Label(addform, text='Password :', font="16").grid(row=2, column=0, sticky=E)
			Entry(addform, width=30, font="16",textvariable=passcheck,show="*" ,relief=SUNKEN).grid(row=2, column=1, 	sticky=W,pady=5, columnspan=2)
			Button(addform,text="Confirm",command=validate_password).grid(row = 3, column=1, sticky=E, pady=20,padx=10)
			Button(addform,text="Go Back",command=self.BuyTicket).grid(row = 3, column=2, sticky=W, pady=20)
			addform.grid(column=1, row=0, sticky=(N+S+E+W))
			addform.columnconfigure(0, weight=1)
			addform.columnconfigure(1, weight=1)
			addform.columnconfigure(2, weight=1)
			self.statusUpdate("Ticket Confirmation")
			
	def seat_allocation(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		sql="select no_of_seats,starting_value from routes where Departure='%s' and Arrival='%s' and Schedule='%s'"%(source.get(),destination.get(),l[3])
		self.cursor.execute(sql)
		e=self.cursor.fetchall()
		x=[]
		for i in range(int(e[0][1]),int(e[0][0]+1)):
			x.append(i)
		print len(x)
		if len(x)>int(option_selected.get()):
		
			k=x[:int(option_selected.get())]
			del x[:int(option_selected.get())]
			print k
			sql1="update routes set starting_value ='%s' where  Departure ='%s' and Arrival='%s' and Schedule='%s'"%(x[0],source.get(),destination.get(),l[3])
			self.cursor.execute(sql1)
			self.db.commit()
	
			get_name="select name from Registration where username='%s'"%(username.get())
			self.cursor.execute(get_name)
			list1=self.cursor.fetchall()
			for i in range(0,int(option_selected.get())):
				sql2="insert into booking_details(name,transaction_id,no_of_seats,departure,arrival,train_time) values('%s','%s','%s','%s','%s','%s')"%(list1[0][0],id,k[i],source.get(),destination.get(),l[3])
				print sql2
				self.cursor.execute(sql2)
				self.db.commit()
	
			addform=Frame(self.root,borderwidth=2,relief=GROOVE)
	
			Label(addform,text="Your ticket Details are",font='14').grid(row=0,column=0,sticky=W,pady=25)
			Label(addform,text="Transaction id is :",font='14').grid(row=1,column=0,sticky=W,pady=10)
			Label(addform,text=id,font='10').grid(row=1,column=1,sticky=W)
			Label(addform,text="Source :",font='10').grid(row=2,column=0,sticky=W,pady=10)
			Label(addform,text=source.get(),font='10').grid(row=2,column=1,sticky=W)
			Label(addform,text="Destination :",font=10).grid(row=3,column=0,sticky=W,pady=10)
			Label(addform,text=destination.get(),font='10').grid(row=3,column=1,sticky=W)
			Label(addform,text="Time :",font=10).grid(row=4,column=0,sticky=W,pady=10)
			Label(addform,text=l[3],font='10').grid(row=4,column=1,sticky=W)
			Label(addform,text="Ticket Amount :",font=10).grid(row=5,column=0,sticky=W,pady=10)
			Label(addform,text=l[2]*int(option_selected.get()),font='10').grid(row=5,column=1,sticky=W)
			Label(addform,text='seat no ',font='10').grid(row=6,column=0,sticky=W)
			Label(addform,text=repr(k),font='10').grid(row=6,column=1,sticky=W,pady=10)
	
			Button(addform,text='Continue',command=self.QR_code_show).grid(row=7,column=1,sticky=W,padx=5,pady=10)
			Button(addform,text='Home',command=self.BuyTicket).grid(row=8,column=1,sticky=W,padx=5,pady=10)
	
	
			addform.grid(column=1, row=0, sticky=(N+S+E+W))
			addform.columnconfigure(0, weight=1)
			addform.columnconfigure(1, weight=1)
			addform.columnconfigure(2, weight=1)
	
		else:
			result = tkMessageBox.askquestion("Seats full", "You will added to Waiting?", icon='warning')
			if result == 'yes':
				get_name="select name from Registration where username='%s'"%(username.get())
				self.cursor.execute(get_name)
				list1=self.cursor.fetchall()
				sql2="insert into Waiting_list(name,tansaction_id,no_of_seats,departure,arrival,trains_time) values('%s','%s','%s','%s','%s','%s')"%(list1[0][0],id,option_selected.get(),source.get(),destination.get(),l[3])
				self.cursor.execute(sql2)
				self.db.commit()
				tkMessageBox.showinfo("Info", "Will Inform you while seat got confirmed", icon='warning')
				self.BuyTicket()
				
			else:
				self.BuyTicket()
				

	def Display_route(self):
		if self.panel2 is not None:
			self.panel2.destroy()
			
		def display_selected_route():
			j=v.get()
			Label(addform,text='Selected Train',font='12').grid(row=z+3,column=1,padx=5,pady=30)
			global option_selected
			option_selected=StringVar()
			global l
			l=b[int(j)]
			sql23="select no_of_seats,starting_value from routes where Departure='%s' and Arrival='%s' and Schedule='%s'"%(l[0],l[1],l[3])
			self.cursor.execute(sql23)
			count_of_cust=self.cursor.fetchall()
			print count_of_cust
			print count_of_cust[0][0]
			print count_of_cust[0][1]
			Label(addform,text='Seats Available',font='12').grid(row=z+3,column=2,padx=5,pady=30)
			Label(addform,text=int(count_of_cust[0][0])-int(count_of_cust[0][1]),font='12').grid(row=z+3,column=4,padx=5,pady=30)
			
			
			Label(addform,text=l[0],font='12').grid(row=z+4,column=1,padx=5,pady=10)
			Label(addform,text=l[1],font='12').grid(row=z+4,column=2,padx=5,pady=10)
			Label(addform,text=l[2],font='12').grid(row=z+4,column=3,padx=5,pady=10)
			Label(addform,text=l[3],font='12').grid(row=z+4,column=4,padx=5,pady=10)
			j=[1,2,3,4,5]
			Label(addform,text='No of Seats',font='12').grid(row=z+5,column=0,padx=5,pady=10)
			OptionMenu(addform,option_selected ,*j).grid(row=z+5, column=2, sticky=W,padx=10,pady=10)
			Button(addform,text='Confirm Ticket',command=self.PasswordCheck).grid(row=z+6,column=4,sticky=W,padx=5,pady=10)
			
		addform=Frame(self.root,borderwidth=2,relief=GROOVE)
		Label(addform,text='Source',font='12').grid(row=0,column=1,padx=5,pady=10)
		Label(addform,text='Destination',font='12').grid(row=0,column=2,padx=5,pady=10)
		Label(addform,text='Price',font='12').grid(row=0,column=3,padx=5,pady=10)
		Label(addform,text='Time',font='12').grid(row=0,column=4,padx=5,pady=10)
		sql="select Departure,Arrival,fare,Schedule from routes where Departure='%s' and Arrival='%s'"%(source.get(),destination.get())
		self.cursor.execute(sql)
		b=self.cursor.fetchall()
		z=1
		k=[]
		for i in range(len(b)):
			k.append(i) 
	#	e_doct={}
		v=StringVar()
		p=1
		for i in k:
			#e_doct[i[0]]=StringVar()
			Radiobutton(addform,variable =v, value =i).grid(row=p,column=0,pady=10)
			p=p+1
		
		for i in b:
			Label(addform,text=i[0],font='12').grid(row=z,column=1,padx=5,pady=10)
			Label(addform,text=i[1],font='12').grid(row=z,column=2,padx=5,pady=10)
			Label(addform,text=i[2],font='12').grid(row=z,column=3,padx=5,pady=10)
			Label(addform,text=i[3],font='12').grid(row=z,column=4,padx=5,pady=10)
			z=z+1
			
		Button(addform,text='Continue',command=display_selected_route).grid(row=z+1,column=4,sticky=W,padx=10,pady=10)
		Button(addform,text='Back',command=self.BuyTicket).grid(row=z+1,column=3,sticky=W,padx=10,pady=10)
		
		
			
		
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		self.statusUpdate("Select your prefrences")
	def admin_window(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		addform=Frame(self.root,borderwidth=2,relief=GROOVE)
		Label(addform,text="\n\n\nSelect the option",font='14').grid(row=0,column=2,sticky=W)
		Button(addform,text='Add new location',command=self.admin_service).grid(row=1,column=1,sticky=W,padx=10,pady=150)
		Button(addform,text='Add new Route',command=self.admin_route_service).grid(row=1,column=2,sticky=W,padx=10,pady=150)
		Button(addform,text='Manage Route',command=self.admin_manage).grid(row=1,column=3,sticky=W,padx=10,pady=150)
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		self.statusUpdate("Admin Panel ....")
	
	def admin_service(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		def add_in_database():
			if new_location_vari.get()=='':
				tkMessageBox.showinfo("Warning","Please Insert valid details",icon='warning')
			else:
				sql="insert into routes(Departure,Arrival) values('%s','%s')"%(new_location_vari.get(),new_location_vari.get())
				self.cursor.execute(sql)
				self.db.commit()
				tkMessageBox.showinfo("Warning","Location added Succesfully")
		addform=Frame(self.root,borderwidth=2,relief=GROOVE)
		Label(addform,text='Add New Location',font='16').grid(row=0,column=1,sticky=W,padx=20,pady=20)
		Label(addform,text='Enter the location',font='14').grid(row=1,column=0,sticky=W,padx=20,pady=20)
		global new_location_vari
		new_location_vari=StringVar()
		Entry(addform,width=25,font='14',textvariable=new_location_vari,relief=SUNKEN).grid(row=1,column=1,sticky=W,padx=20,pady=20)
		Button(addform,text='Add Location',command=add_in_database).grid(row=2,column=0,padx=20,pady=20)
		Button(addform,text='Back',command=self.admin_window).grid(row=2,column=1,padx=20,pady=20)
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
				
				
	def admin_route_service(self):
		
		if self.panel2 is not None:
			self.panel2.destroy()
			
		def add_route():
			print add_destination.get()
			print add_source.get()
			print price.get()
			print schedule.get()
			if add_destination.get() and add_source.get() and schedule.get() and price.get() == None:
				tkMessageBox.showinfo("Warning","Please Insert valid details",icon='warning')
			else:
				sql="insert into routes values('%s','%s','%s','%s','%s','%s')"%(add_source.get(),add_destination.get(),price.get(),schedule.get(),seats.get(),starting_value.get())
				self.cursor.execute(sql)
				self.db.commit()
				tkMessageBox.showinfo("Warning","Route Added Successfully")
				
		addform=Frame(self.root,borderwidth=2,relief=GROOVE)
		global add_destination
		global add_source
		global schedule
		global price
		global seats
		global starting_value
		add_destination=StringVar()
		add_source=StringVar()
		schedule=StringVar()
		price=StringVar()
		seats=StringVar()
		starting_value=StringVar()
		Label(addform,text='Add New route details',font='14').grid(row=0,column=1,sticky=W,padx=20,pady=30)
		Label(addform,text='Source',font='14').grid(row=1,column=0,sticky=W,padx=20,pady=20)
		Entry(addform,width=30,font='14',textvariable=add_source).grid(row=1,column=1,sticky=W,padx=10,pady=20)
		Label(addform,text='Destination',font='14').grid(row=2,column=0,sticky=W,padx=20,pady=20)
		Entry(addform,width=30,font='14',textvariable=add_destination).grid(row=2,column=1,sticky=W,padx=10,pady=20)
		Label(addform,text='Price',font='14').grid(row=3,column=0,sticky=W,padx=20,pady=20)
		Entry(addform,width=30,font='14',textvariable=price).grid(row=3,column=1,sticky=W,padx=10,pady=20)
		Label(addform,text='Schedule',font='14').grid(row=4,column=0,sticky=W,padx=20,pady=20)
		Entry(addform,width=30,font='14',textvariable=schedule).grid(row=4,column=1,sticky=W,padx=10,pady=20)
		Label(addform,text='No of Seats',font='14').grid(row=5,column=0,sticky=W,padx=20,pady=20)
		Entry(addform,width=30,font='14',textvariable=seats).grid(row=5,column=1,sticky=W,padx=10,pady=20)
		Label(addform,text='Starting Value',font='14').grid(row=6,column=0,sticky=W,padx=20,pady=20)
		Entry(addform,width=30,font='14',textvariable=starting_value).grid(row=6,column=1,sticky=W,padx=10,pady=20)
		Button(addform,text='Add',command=add_route).grid(row=7,column=0,padx=10,sticky=W)
		Button(addform,text='Back',command=self.admin_window).grid(row=7,column=1,padx=10,sticky=W)
		
		
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		
		
	def admin_manage(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		
		
		global remove_station
		global change_time
		global remove_route_source
		global remove_route_departure
		remove_station=StringVar()
		change_time=StringVar()
		remove_route_source=StringVar()
		remove_route_departure=StringVar()
		
		def delete_route():
			if remove_route_source.get() and remove_route_departure.get()==None:
				tkMessageBox.showinfo("Warning","Please Insert valid details",icon='warning')
			else:					
				sql="delete from routes where Departure='%s'and Arrival='%s'"%(remove_route_source.get(),remove_route_departure.get())
				self.cursor.execute(sql)
				self.db.commit()
				remove_route_source.set('')
				remove_route_departure.set('')
				tkMessageBox.showinfo("Warning","Succesfullt Removed")
		
		def time_to_change():
			if change_time.get()==None:
				tkMessageBox.showinfo("Warning","Please Insert valid details",icon='warning')
			else:					
				sql="delete from routes where Departure='%s'"%(change_time.get())
				self.cursor.execute(sql)
				self.db.commit()
				sql="delete from routes where Arrival='%s'"%(change_time.get())
				self.cursor.execute(sql)
				self.db.commit()
				tkMessageBox.showinfo("Warning","Please Insert valid details",icon='warning')
			
		addform=Frame(self.root,borderwidth=2,relief=GROOVE)
		Label(addform,text='Manage Activities',font='12').grid(row=0,column=1,sticky=W,pady=10)
		
		Label(addform,text='Remove Station',font='12').grid(row=1,column=0,sticky=W,padx=20,pady=10)
		Entry(addform,width=20,textvariable=remove_station).grid(row=1,column=1,sticky=W,padx=20,pady=10)
		Button(addform,text='G0').grid(row=2,column=1,padx=20,pady=10,sticky=W)
		
		Label(addform,text='Change Time',font='12').grid(row=3,column=0,sticky=W,padx=20,pady=10)
		Entry(addform,width=20,textvariable=change_time).grid(row=3,column=1,sticky=W,padx=20,pady=10)
		Button(addform,text='G0',command=time_to_change).grid(row=4,column=1,padx=20,pady=10,sticky=W)
		
		Label(addform,text='Remove Route',font='12').grid(row=5,column=0,sticky=W,padx=20,pady=10)
		Label(addform,text='Source',font='12').grid(row=6,column=0,sticky=W,padx=20,pady=10)
		Label(addform,text='Destination',font='12').grid(row=7,column=0,sticky=W,padx=20,pady=10)	
		Entry(addform,width=20,textvariable=remove_route_source).grid(row=6,column=1,sticky=W,padx=20,pady=10)
		Entry(addform,width=20,textvariable=remove_route_departure).grid(row=7,column=1,sticky=W,padx=20,pady=10)
		Button(addform,text='Go',command=delete_route).grid(row=8,column=1,padx=20,pady=10,sticky=W)
		Button(addform,text='Back',command=self.admin_window).grid(row=9,column=0,padx=20,pady=10,sticky=W)
		
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
		
	
	def Tc_login(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		addform = Frame(self.root, borderwidth=2,relief=GROOVE)
		Label(addform, text="\n\nLogin", font="Time 16").grid(row=0,column=0, sticky=N+E+W, pady=20, columnspan=3)

		global username_tc
		global password_tc
	
		username_tc=StringVar()
		password_tc=StringVar()
		Label(addform, text='username'+':', font="16").grid(row=1, column=0, sticky=E)
		Entry(addform, width=30, font="16",textvariable=username_tc, relief=SUNKEN).grid(row=1, column=1, 	sticky=W,pady=5, columnspan=2)
		Label(addform, text='password'+':', font="16").grid(row=2, column=0, sticky=E)
		Entry(addform,show="*",width=30, font="16",textvariable=password_tc, relief=SUNKEN).grid(row=2, column=1, sticky=W,pady=5, columnspan=2)
		
		Button(addform,text="Sign in",command=self.tc_login).grid(row = 3, column=1, sticky=E, pady=20,padx=10)
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
	
				
	def tc_login(self):
		if username_tc.get()=='' or password_tc.get()=='':	
			tkMessageBox.showinfo("Warning","Please Insert valid details",icon='warning')		
		else:
			a=username_tc.get()
			b=password_tc.get()
			self.cursor.execute('select username,password from admin_login')
			self.entries = self.cursor.fetchall()
			flag=0
			for i in self.entries:
				if i[0]==a:
					if i[1]==b:
						flag=1
						self.Ticket_checker()
			if flag==1:
				self.user_login_button.config(state='disable')
				self.admin_login_button.config(state='disable')
				self.tc_button.config(state='disable')
				self.logout_button.config(state='active')
			if flag==0:
				tkMessageBox.showinfo("Warning","Please Insert valid details",icon='warning')
	
	def Ticket_checker(self):
		if self.panel2 is not None:
			self.panel2.destroy()
		
		global tc_source
		global tc_destination
		global tc_schedule
		
		tc_source=StringVar()
		tc_destination=StringVar()
		tc_schedule=StringVar()
		
		addform=Frame(self.root,borderwidth=2,relief=GROOVE)
		Label(addform,text='Ticket Collector Manual',font='12').grid(row=0,column=1,sticky=W,pady=10)
		
		Label(addform,text='Destination',font='12').grid(row=1,column=0,sticky=W,padx=20,pady=10)
		Entry(addform,width=20,textvariable=tc_source).grid(row=1,column=1,sticky=W,padx=20,pady=10)
		
		Label(addform,text='Source',font='12').grid(row=2,column=0,sticky=W,padx=20,pady=10)
		Entry(addform,width=20,textvariable=tc_destination).grid(row=2,column=1,sticky=W,padx=20,pady=10)
		
		Label(addform,text='Schedule',font='12').grid(row=3,column=0,sticky=W,padx=20,pady=10)
		Entry(addform,width=20,textvariable=tc_schedule).grid(row=3,column=1,sticky=W,padx=20,pady=10)
		
		Button(addform,text='Go',command=self.Show_all_customer).grid(row=4,column=1,padx=20,pady=10,sticky=W)
		
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
	
	def Show_all_customer(self):
		if self.panel2 is not None:
			self.panel2.destroy()
			
		def cust_present():
			tkMessageBox.showinfo("Warning","No Changes Made")
		
		def cust_vecant():
			l=pk[int(jk.get())]
			print l
			sql1="select no_of_seats from booking_details where id='%s'"%(l[6])
			self.cursor.execute(sql1)
			f1=self.cursor.fetchall()
			
			
			v1= int(f1[0][0])
			v2=int(l[2])
			sql=" update routes set starting_value=%s where Departure='%s' and Arrival='%s' and Schedule='%s';"%((v1-1),l[3],l[4],l[5])
			self.cursor.execute(sql)
			self.db.commit()
			print l[6]
		
			sql3="delete from booking_details where id='%s'"%(l[6])
			self.cursor.execute(sql3)
			self.db.commit()
			
			tkMessageBox.showinfo("Warning","okay,Seat is empty now")
			
			sql5="select * from Waiting_list where arrival='%s' and departure='%s' and trains_time='%s'"%(l[4],l[3],l[5])
			self.cursor.execute(sql5)
			a=self.cursor.fetchall()
			print a
			
			if len(a)>0:
				sql="insert into booking_details(name,transaction_id,no_of_seats,departure,arrival,train_time) values('%s','%s','%s','%s','%s','%s')"%(a[0][0],a[0][1],v1,a[0][3],a[0][4],a[0][5])
				self.cursor.execute(sql)
				self.db.commit()
				
				sql5="delete from Waiting_list where arrival='%s' and departure='%s' and trains_time='%s'"%(a[0][4],a[0][3],a[0][5])
				self.cursor.execute(sql5)
				self.db.commit()

				
				
						
		addform=Frame(self.root,borderwidth=2,relief=GROOVE)
		scrollbar = Scrollbar(addform)
		scrollbar.grid(sticky=E)
		Label(addform,text='Name',font='12').grid(row=0,column=1,padx=5,pady=10)
		Label(addform,text='Seats No',font='12').grid(row=0,column=2,padx=5,pady=10)
		Label(addform,text='Departure',font='12').grid(row=0,column=3,padx=5,pady=10)
		Label(addform,text='Arrival',font='12').grid(row=0,column=4,padx=5,pady=10)
		Label(addform,text='Train Time',font='12').grid(row=0,column=5,padx=5,pady=10)
		
		
		sql="select * from booking_details where arrival='%s' and departure='%s' and train_time='%s'"%(tc_source.get(),tc_destination.get(),tc_schedule.get())
		self.cursor.execute(sql)
		global pk
		pk=self.cursor.fetchall()
		global jk
		jk=StringVar()
		f=1
		k=[]
		for i in range(len(pk)):
			k.append(i) 
		for i in k:
			Radiobutton(addform,variable =jk, value =i).grid(row=f,column=0,pady=10)
			f=f+1
			
		
		z=1
		for i in pk:
			Label(addform,text=i[0],font='12').grid(row=z,column=1,padx=5,pady=10)
			Label(addform,text=i[2],font='12').grid(row=z,column=2,padx=5,pady=10)
			Label(addform,text=i[3],font='12').grid(row=z,column=3,padx=5,pady=10)
			Label(addform,text=i[4],font='12').grid(row=z,column=4,padx=5,pady=10)
			Label(addform,text=i[5],font='12').grid(row=z,column=5,padx=5,pady=10)
			z=z+1
		
		Button(addform,text='Present',command=cust_present).grid(row=z+2,column=1,padx=20,pady=10,sticky=W)
		Button(addform,text='Vecant',command=cust_vecant).grid(row=z+2,column=2,padx=20,pady=10,sticky=W)
		
		Button(addform,text='Refresh',command=self.Show_all_customer).grid(row=z+4,column=1,padx=20,pady=10,sticky=W)
		Button(addform,text='Back',command=self.Ticket_checker).grid(row=z+4,column=2,padx=20,pady=10,sticky=W)
		addform.grid(column=1, row=0, sticky=(N+S+E+W))
		addform.columnconfigure(0, weight=1)
		addform.columnconfigure(1, weight=1)
		addform.columnconfigure(2, weight=1)
	
	
	
			
if __name__ == '__main__':
    g = GUI()
    

            
            
        
