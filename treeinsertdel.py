import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as mb

r = tk.Tk()
r.geometry("600x600")
r.title("user details")

connect = mysql.connector.connect(host="localhost",user="root", passwd="mysql",
  database="trinityregistration",port="3307")

conn = connect.cursor()

conn.execute("SELECT * FROM reg_member ORDER BY student_id")

tree=ttk.Treeview(r)
tree['show'] = 'headings'

s = ttk.Style(r)
s.theme_use("clam")
s.configure(".", font=('Helvetica', 11))
s.configure("Treeview.Heading", foreground='red',font=('Helvetica', 11,"bold"))

# Define number of columns
tree["columns"]=("S_ID","Sname","gender","city","email","contactno","course")

#Assign the width,minwidth and anchor to the respective columns
tree.column("S_ID", width=50, minwidth=50,anchor=tk.CENTER)
tree.column("Sname", width=100, minwidth=100,anchor=tk.CENTER)
tree.column("gender", width=50, minwidth=50,anchor=tk.CENTER)
tree.column("city", width=150, minwidth=150,anchor=tk.CENTER)
tree.column("email", width=150, minwidth=150,anchor=tk.CENTER)
tree.column("contactno", width=150, minwidth=150,anchor=tk.CENTER)
tree.column("course", width=150, minwidth=150,anchor=tk.CENTER)


#Assign the heading names to the respective columns
tree.heading("S_ID", text="S.Id",anchor=tk.CENTER)
tree.heading("Sname", text="Student name",anchor=tk.CENTER)
tree.heading("gender", text="Gender",anchor=tk.CENTER)
tree.heading("city", text="City",anchor=tk.CENTER)
tree.heading("email", text="Email",anchor=tk.CENTER)
tree.heading("contactno", text="Contactno",anchor=tk.CENTER)
tree.heading("course", text="Course",anchor=tk.CENTER)


i = 0
for ro in conn:
	if ro[0]%2==0:
		tree.insert('', i, text="",values=(ro[0],ro[1],ro[2],ro[3],ro[4],ro[5],ro[6]),tags=("even",))
	else:
		tree.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6]), tags=("odd",))
	i = i + 1

tree.tag_configure("even",foreground="black",background="white")
tree.tag_configure("odd",foreground="white",background="black")

hsb = ttk.Scrollbar(r,orient="horizontal")
hsb.configure(command=tree.xview)
tree.configure(xscrollcommand=hsb.set)
hsb.pack(fill=X,side = BOTTOM)

vsb = ttk.Scrollbar(r,orient="vertical")
vsb.configure(command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(fill=Y,side = RIGHT)

tree.pack()
name=tk.StringVar()
gender=tk.StringVar()
city=tk.StringVar()
email=tk.StringVar()
phone=tk.IntVar()
course=tk.StringVar()


def add_data(tree):
	f = Frame(r,width=400,height=320,background="grey")
	f.place(x=100,y=250)
	l1=Label(f,text="name",width=8,font=('Times',11,'bold'))
	e1=Entry(f,textvariable=name,width=25)
	l1.place(x=50,y=30)
	e1.place(x=170,y=30)

	l2 = Label(f, text="Gender", width=8, font=('Times', 11, 'bold'))
	e2 = Entry(f, textvariable=gender, width=25)
	l2.place(x=50, y=70)
	e2.place(x=170, y=70)

	l3 = Label(f, text="City", width=8, font=('Times', 11, 'bold'))
	l3.place(x=50, y=110)
	e3 = Entry(f, textvariable=city, width=25)
	e3.place(x=170, y=110)

	l4 = Label(f, text="email", width=8, font=('Times', 11, 'bold'))
	l4.place(x=50, y=150)
	e4 = Entry(f, textvariable=email, width=25)
	e4.place(x=170, y=150)

	l5 = Label(f, text="Phone", width=8, font=('Times', 11, 'bold'))
	l5.place(x=50, y=190)
	e5 = Entry(f, textvariable=phone, width=25)
	e5.place(x=170, y=190)
	e5.delete(0,END)

	l6 = Label(f, text="Course", width=8, font=('Times', 11, 'bold'))
	l6.place(x=50, y=230)
	e6 = Entry(f, textvariable=course, width=25)
	e6.place(x=170, y=230)

	def insert_data():
		nonlocal e1,e2,e3,e4,e5,e6
		s_name=name.get()
		g = gender.get()
		cit = city.get()
		e = email.get()
		p = phone.get()
		c = course.get()
		conn.execute('INSERT INTO reg_member(student_name,gender,city,email,contactno,course) VALUES(%s,%s,%s,%s,%s,%s)',
					 (s_name,g,cit,e,p,c))
		print(conn.lastrowid)
		connect.commit()
		tree.insert('','end',text="",values=(conn.lastrowid,s_name,g,cit,e,p,c))
		mb.showinfo("Success","student registered")
		e1.delete(0,END)
		e2.delete(0, END)
		e3.delete(0, END)
		e4.delete(0, END)
		e5.delete(0, END)
		e6.delete(0, END)
		f.destroy()


	submitbutton = tk.Button(f, text="submit", command=insert_data)
	submitbutton.configure(font=('Times', 11, 'bold'), bg='green', fg='white')
	submitbutton.place(x=100, y=280)
	cancelbutton = tk.Button(f, text="cancel", command=f.destroy)
	cancelbutton.configure(font=('Times', 11, 'bold'), bg='red', fg='white')
	cancelbutton.place(x=240, y=280)

def delete_data(tree):
	selected_item=tree.selection()[0]
	print(tree.item(selected_item)['values'])
	uid=tree.item(selected_item)['values'][0]
	del_query="DELETE FROM reg_member WHERE student_id=%s"
	sel_data=(uid,)
	conn.execute(del_query,sel_data)
	connect.commit()
	tree.delete(selected_item)
	mb.showinfo("success","student data deleted ")

def select_data(tree):
	curItem=tree.focus()
	values= tree.item(curItem,"values")
	print(values)
	f = Frame(r, width=400, height=320, background="grey")
	f.place(x=100, y=250)
	l1 = Label(f, text="name", width=8, font=('Times', 11, 'bold'))
	e1 = Entry(f, textvariable=name, width=25)
	l1.place(x=50, y=30)
	e1.place(x=170, y=30)

	l2 = Label(f, text="Gender", width=8, font=('Times', 11, 'bold'))
	e2 = Entry(f, textvariable=gender, width=25)
	l2.place(x=50, y=70)
	e2.place(x=170, y=70)

	l3 = Label(f, text="City", width=8, font=('Times', 11, 'bold'))
	l3.place(x=50, y=110)
	e3 = Entry(f, textvariable=city, width=25)
	e3.place(x=170, y=110)

	l4 = Label(f, text="email", width=8, font=('Times', 11, 'bold'))
	l4.place(x=50, y=150)
	e4 = Entry(f, textvariable=email, width=25)
	e4.place(x=170, y=150)

	l5 = Label(f, text="Phone", width=8, font=('Times', 11, 'bold'))
	l5.place(x=50, y=190)
	e5 = Entry(f, textvariable=phone, width=25)
	e5.place(x=170, y=190)
	e5.delete(0, END)

	l6 = Label(f, text="Course", width=8, font=('Times', 11, 'bold'))
	l6.place(x=50, y=230)
	e6 = Entry(f, textvariable=course, width=25)
	e6.place(x=170, y=230)

	e1.insert(0,values[1])
	e2.insert(0, values[2])
	e3.insert(0,values[3])
	e4.insert(0,values[4])
	e5.insert(0, values[5])
	e6.insert(0, values[6])

	def update_data():
		nonlocal e1,e2,e3,e4,e5,e6,curItem,values
		s_name = name.get()
		g = gender.get()
		cit = city.get()
		e = email.get()
		p = phone.get()
		c = course.get()
		tree.item(curItem,values=(values[0],s_name,g,cit,e,p,c))
		conn.execute(
			"UPDATE reg_member SET student_name=%s, gender=%s, city=%s, email=%s, contactno=%s, course=%s WHERE student_id=%s"
			, (s_name, g, cit, e, int(p), c, values[0]))
		connect.commit()
		mb.showinfo("success","student data updated")
		e1.delete(0,END)
		e2.delete(0, END)
		e3.delete(0, END)
		e4.delete(0, END)
		e5.delete(0, END)
		e6.delete(0, END)
		f.destroy()



	savebutton = tk.Button(f, text="Update", command=update_data)
	savebutton.place(x=100, y=270)
	cancelbutton = tk.Button(f, text="cancel", command=f.destroy)
	cancelbutton.place(x=200, y=270)

insertbutton = tk.Button(r,text="Insert",command=lambda:add_data(tree))
insertbutton.configure(font =('calibri', 14, 'bold'), bg = 'green',fg='white')
insertbutton.place(x=200,y=260)

deletebutton = tk.Button(r,text="delete",command=lambda:delete_data(tree))
deletebutton.configure(font =('calibri', 14, 'bold'), bg = 'red',fg='white')
deletebutton.place(x=300,y=260)

updatebutton = tk.Button(r,text="update",command=lambda:select_data(tree))
updatebutton.configure(font =('calibri', 14, 'bold'), bg = 'blue',fg='white')
updatebutton.place(x=400,y=260)


r.mainloop()


