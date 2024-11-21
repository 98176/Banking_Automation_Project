#!/usr/bin/env python
# coding: utf-8

# In[3]:


from tkinter import * 
from tkinter.ttk import Combobox 
from tkinter import messagebox
import time 
import sqlite3
import re




try:
    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("create table acn(acn_no integer primary key autoincrement,acn_name text,acn_pass text,acn_email text,acn_mob text,acn_bal float,acn_opendate text,acn_gender text)")
    conobj.close()
    print("Table Created")
except:
    print("Something went wrong, migth be table already exists")





win=Tk()  # creating window
win.state('zoomed') # full screen
win.configure(bg='pink') # screen background color
win.resizable(width=False,height=False) # disable window resize option


title=Label(win,text="Banking Automation",font=('arial',50,'bold','underline'),bg='pink') # title
title.pack() # set title position on top

dt=time.strftime("%d %b,%Y")
date=Label(win,text=f"{dt}",font=('arial',20,'bold'),bg='pink',fg='black') # set date on window
date.place(relx=.85,rely=.1)


def main_screen():          # create frame over the window for authorization
    frm=Frame(win)
    frm.configure(bg='white')
    frm.place(relx=.0,rely=.15,relwidth=1,relheight=1)


    def forgotpass():
        frm.destroy()
        forgotpass_screen()


    def newuser():
        frm.destroy()
        newuser_screen()


    def login():
        global gacn
        gacn=e_acn.get()
        pwd=e_pass.get()
        if len(gacn)==0 or len(pwd)==0:
            messagebox.showwarning("Validation","Empty Fields are not allowed")
            return 
        else:
            gacn=e_acn.get()
            pwd=e_pass.get()
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select * from acn where acn_no=? and acn_pass=?",(gacn,pwd))
            tup=curobj.fetchone()
            conobj.close()   #(not close connection raise error database lock)
            if tup==None:
                messagebox.showerror("Login","Invalid ACN/PASS")
            else:
                frm.destroy()
                welcome_screen()


    def clear(): #for clear the input
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()



        

    lbl_acn=Label(frm,text="Account Number",font=('arial',20,'bold'),bg='pink')
    lbl_acn.place(relx=.3,rely=.1)
    
    e_acn=Entry(frm,font=('arial',20,'bold'),bg='pink',fg='black',bd=0)
    e_acn.place(relx=.5,rely=.1)
    e_acn.focus()  # blinck cursor

    lbl_pass=Label(frm,text="Password",font=('arial',20,'bold'),bg='pink')
    lbl_pass.place(relx=.3,rely=.2)
    
    e_pass=Entry(frm,font=('arial',20,'bold'),bg='pink',fg='black',bd=0,show='*')
    e_pass.place(relx=.5,rely=.2)

    btn_login=Button(frm,text='Login',font=('arial',15,'bold'),bd=5,bg='pink',command=login) 
    btn_login.place(relx=.54,rely=.25)

    btn_clr=Button(frm,text='Reset',font=('arial',15,'bold'),bd=5,bg='pink',command=clear)
    btn_clr.place(relx=.6,rely=.25)

    btn_fp=Button(frm,width=15,text='Forgot Password',font=('arial',15,'bold'),bd=5,bg='pink',command=forgotpass)
    btn_fp.place(relx=.53,rely=.32)

    btn_new=Button(frm,command=newuser,width=15,text='Open New Account',font=('arial',15,'bold'),bd=5,bg='pink')
    btn_new.place(relx=.53,rely=.4)

    

def forgotpass_screen():
    frm=Frame(win)
    frm.configure(bg='white')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=1)
    


    def back():
        frm.destroy()
        main_screen()


    def forgotpass_db():
        acn=e_acn.get()
        email=e_email.get()
        mob=e_mob.get()
        
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_pass from acn where acn_no=? and acn_email=? and acn_mob=?",(acn,email,mob))
        tup=curobj.fetchone()
        if tup==None:
            messagebox.showerror("Forgot Pass","Record not found")
        else:
            messagebox.showinfo("Forgot Pass",f"Your Pass={tup[0]}")
        conobj.close()
        
        
    btn_new=Button(frm,width=5,text='Back',font=('arial',15,'bold'),bd=4,bg='pink',command=back)
    btn_new.place(relx=0,rely=0)

    lbl_acn=Label(frm,text="Account Number",font=('arial',20,'bold'),bg='pink')
    lbl_acn.place(relx=.3,rely=.1)
    
    e_acn=Entry(frm,font=('arial',20,'bold'),bg='pink',fg='black',bd=0)
    e_acn.place(relx=.5,rely=.1)
    e_acn.focus()

    lbl_email=Label(frm,text="E-MailID",font=('arial',20,'bold'),bg='pink')
    lbl_email.place(relx=.3,rely=.2)
    
    e_email=Entry(frm,font=('arial',20,'bold'),bg='pink',fg='black',bd=0)
    e_email.place(relx=.5,rely=.2)

    lbl_mob=Label(frm,text="Mobile Number",font=('arial',20,'bold'),bg='pink')
    lbl_mob.place(relx=.3,rely=.3)
    
    e_mob=Entry(frm,font=('arial',20,'bold'),bg='pink',fg='black',bd=0)
    e_mob.place(relx=.5,rely=.3)


    btn_sub=Button(frm,width=5,text='Submit',font=('arial',15,'bold'),bd=4,bg='pink',command=forgotpass_db)
    btn_sub.place(relx=.57,rely=.35)
    


def newuser_screen():
    frm=Frame(win)
    frm.configure(bg='white')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=1)
    


    def back():
        frm.destroy()
        main_screen()


    def newuser_db():       # this function work for to store data in database by given this inputs
        name=e_name.get()        
        pwd=e_pass.get()
        email=e_mail.get()
        mob=e_mob.get()
        gender=cb_gender.get()
        bal=0
        opendate=dt=time.strftime("%d %b,%Y,%A")
        
        
        match=re.fullmatch("[6-9][0-9]{9}",mob)
        if match==None:
            messagebox.showwarning("Validation","Invalid format of mobile number")
            return 

        match=re.fullmatch("[a-zA-Z0-9_]+@[a-zA-Z]+\.[a-zA-Z]+",email)
        if match==None:
            messagebox.showwarning("Validation","Invalid format of E-Mail ID")
            return 

            
        
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("insert into acn(acn_name,acn_pass,acn_email,acn_mob,acn_gender,acn_opendate,acn_bal) values(?,?,?,?,?,?,?)",(name,pwd,email,mob,gender,opendate,bal))
        conobj.commit()
        conobj.close()


        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select max(acn_no) from acn")
        tup=curobj.fetchone()
        conobj.close()

        messagebox.showinfo("New User",f"Account Created Sucessfully with ACN No={tup[0]}")
    def reset():
        e_name.delete(0,"end")
        e_pass.delete(0,"end")
        e_mail.delete(0,"end")
        e_mob.delete(0,"end")

    
    btn_new=Button(frm,width=5,text='Back',font=('arial',15,'bold'),bd=4,bg='pink',command=back)
    btn_new.place(relx=0,rely=0)

    lbl_welcome=Label(frm,text='Account Opening Screen',font=('arial',15,'bold'),bg='white',fg='black')
    lbl_welcome.pack()


    lbl_name=Label(frm,text="Name",font=('arial',20,'bold'),bg='pink')
    lbl_name.place(relx=.3,rely=.1)
    
    e_name=Entry(frm,font=('arial',20,'bold'),bg='pink',fg='black',bd=0)
    e_name.place(relx=.5,rely=.1)
    e_name.focus()

    lbl_pass=Label(frm,text="Create Password",font=('arial',20,'bold'),bg='pink')
    lbl_pass.place(relx=.3,rely=.2)
    
    e_pass=Entry(frm,font=('arial',20,'bold'),bg='pink',fg='black',bd=0,show='*')
    e_pass.place(relx=.5,rely=.2)

    lbl_mob=Label(frm,text='Mobile Number',font=('arial',20,'bold'),bg='pink')
    lbl_mob.place(relx=.3,rely=.3)

    e_mob=Entry(frm,font=('arial',20,'bold'),bg='pink',fg='black',bd=0)
    e_mob.place(relx=.5,rely=.3)

    lbl_mail=Label(frm,text='Email-ID',font=('arial',20,'bold'),bg='pink')
    lbl_mail.place(relx=.3,rely=.4)

    e_mail=Entry(frm,font=('arial',20,'bold'),bg='pink',fg='black',bd=0)
    e_mail.place(relx=.5,rely=.4)

    lbl_gender=Label(frm,text='Gender',font=('arial',20,'bold'),bg='pink')
    lbl_gender.place(relx=.3,rely=.5)

    cb_gender=Combobox(frm,width=15,values=['-------select--------','Male','Female','Third Gender'],font=('arial',20,'bold'))
    cb_gender.place(relx=.5,rely=.5)

    lbl_atype=Label(frm,text='Type',font=('arial',20,'bold'),bg='pink')
    lbl_atype.place(relx=.3,rely=.6)

    cb_atype=Combobox(frm,width=15,values=['----select-----','Saving A\C','Current A\C','DEMAT A\C','Fixed Deposit A\C'],font=('arial',20,'bold'))
    cb_atype.place(relx=.5,rely=.6)
    

    btn_opn=Button(frm,width=5,text='Open',font=('arial',15,'bold'),bd=4,bg='pink',command=newuser_db)
    btn_opn.place(relx=.7,rely=.7)

    btn_rst=Button(frm,width=5,text='Reset',font=('arial',15,'bold'),bd=4,bg='pink',command=reset)
    btn_rst.place(relx=.75,rely=.7)






def welcome_screen():
    frm=Frame(win)
    frm.configure(bg='white')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=1)


    def logout():
        frm.destroy()
        main_screen()
        
    def details():
        ifrm=Frame(frm,highlightbackground='powder blue',highlightthickness=3)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.15,rely=.1,relwidth=.7,relheight=.5)
   
        lbl_welcome=Label(ifrm,text='This is Details Screen',font=('arial',15,'bold'),bg='pink',fg='blue')
        lbl_welcome.pack()


        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_opendate,acn_bal,acn_gender,acn_email,acn_mob from acn where acn_no=?",(gacn,))
        tup=curobj.fetchone()
        conobj.close()
        
        lbl_opendate=Label(ifrm,text=f"Open Date:{tup[0]}",font=('arial',15,'bold'),bg='pink',fg='black')
        lbl_opendate.place(relx=.2,rely=.12)

        lbl_bal=Label(ifrm,text=f"Balance:{tup[1]}",font=('arial',15,'bold'),bg='pink',fg='black')
        lbl_bal.place(relx=.2,rely=.2)

        lbl_gender=Label(ifrm,text=f"Gender:{tup[2]}",font=('arial',15,'bold'),bg='pink',fg='black')
        lbl_gender.place(relx=.2,rely=.28)

        lbl_email=Label(ifrm,text=f"E-Mail:{tup[3]}",font=('arial',15,'bold'),bg='pink',fg='black')
        lbl_email.place(relx=.2,rely=.36)

        lbl_mob=Label(ifrm,text=f"Mobile No.-:{tup[4]}",font=('arial',15,'bold'),bg='pink',fg='black')
        lbl_mob.place(relx=.2,rely=.44)

        

        conobj.close()

    def update():
        ifrm=Frame(frm,highlightbackground='powder blue',highlightthickness=3)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.15,rely=.1,relwidth=.7,relheight=.5)

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_name,acn_pass,acn_mob,acn_email from acn where acn_no=?",(gacn,))
        tup=curobj.fetchone()
        conobj.close()
   
        lbl_welcome=Label(ifrm,text='This is Update Screen',font=('arial',15,'bold'),bg='pink',fg='blue')
        lbl_welcome.pack()
        
        
        lbl_name=Label(ifrm,text="Name",font=('arial',20,'bold'),bg='pink')
        lbl_name.place(relx=.1,rely=.1)
    
        e_name=Entry(ifrm,font=('arial',20,'bold'),bg='white',fg='black',bd=0)
        e_name.place(relx=.1,rely=.2)
        e_name.insert(0,tup[0])
        e_name.focus()

        lbl_pass=Label(ifrm,text="Create Password",font=('arial',20,'bold'),bg='pink')
        lbl_pass.place(relx=.1,rely=.4)
    
        e_pass=Entry(ifrm,font=('arial',20,'bold'),bg='white',fg='black',bd=0,show='*')
        e_pass.place(relx=.1,rely=.5)
        e_pass.insert(0,tup[1])

        lbl_mob=Label(ifrm,text='Mobile Number',font=('arial',20,'bold'),bg='pink')
        lbl_mob.place(relx=.4,rely=.1)

        e_mob=Entry(ifrm,font=('arial',20,'bold'),bg='white',fg='black',bd=0)
        e_mob.place(relx=.4,rely=.2)
        e_mob.insert(0,tup[2])

        lbl_mail=Label(ifrm,text='Email-ID',font=('arial',20,'bold'),bg='pink')
        lbl_mail.place(relx=.4,rely=.4)

        e_mail=Entry(ifrm,font=('arial',20,'bold'),bg='white',fg='black',bd=0)
        e_mail.place(relx=.4,rely=.5)
        e_mail.insert(0,tup[3])


        def update_db():
            name=e_name.get()
            pwd=e_pass.get()
            email=e_mail.get()
            mob=e_mob.get()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update acn set acn_name=?,acn_pass=?,acn_mob=?,acn_email=? where acn_no=?",(name,pwd,mob,email,gacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update","Recor Updated Sucessfully")
            welcome_screen()

        

        btn_update=Button(ifrm,text='Update',font=('arial',15,'bold'),bd=5,bg='pink',command=update_db)
        btn_update.place(relx=.6,rely=.7)


        



    def deposit():
         ifrm=Frame(frm,highlightbackground='powder blue',highlightthickness=3)
         ifrm.configure(bg='pink')
         ifrm.place(relx=.15,rely=.1,relwidth=.7,relheight=.5)
   
         lbl_welcome=Label(ifrm,text='This is Deposit Screen',font=('arial',15,'bold'),bg='pink',fg='blue')
         lbl_welcome.pack()
         
         lbl_amt=Label(ifrm,text="Amount",font=('arial',20,'bold'),bg='pink')
         lbl_amt.place(relx=.1,rely=.2)
    
         e_amt=Entry(ifrm,font=('arial',20,'bold'),bg='white',fg='black',bd=0)
         e_amt.place(relx=.3,rely=.2)
         e_amt.focus()

         def deposit_db():
             amt=float(e_amt.get())
             conobj=sqlite3.connect(database="bank.sqlite")
             curobj=conobj.cursor()
             curobj.execute("update acn set acn_bal=acn_bal+? where acn_no=?",(amt,gacn))
             conobj.commit()
             conobj.close()
             messagebox.showinfo("Update",f"{amt} Amount Deposited Sucessfully")
             
             

         btn_sub=Button(ifrm,text='Submit',font=('arial',15,'bold'),bd=5,bg='pink',command=deposit_db)
         btn_sub.place(relx=.3,rely=.4)

     


    def widthdraw():
        ifrm=Frame(frm,highlightbackground='powder blue',highlightthickness=3)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.15,rely=.1,relwidth=.7,relheight=.5)
   
        lbl_welcome=Label(ifrm,text='This is Widthdraw Screen',font=('arial',15,'bold'),bg='pink',fg='blue')
        lbl_welcome.pack()

        lbl_amt=Label(ifrm,text="Widthdraw Cash",font=('arial',20,'bold'),bg='pink')
        lbl_amt.place(relx=.1,rely=.2)
    
        e_amt=Entry(ifrm,font=('arial',20,'bold'),bg='white',fg='black',bd=0)
        e_amt.place(relx=.3,rely=.2)
        e_amt.focus()

        def widthdraw_db():
            amt=float(e_amt.get())

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from acn where acn_no=?",(gacn,))
            tup=curobj.fetchone()
            avail_bal=tup[0]
            conobj.close()

            if avail_bal>=amt:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("update acn set acn_bal=acn_bal-? where acn_no=?",(amt,gacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Widthdraw",f"{amt} Widthdraw Amount")
            else:
                messagebox.showwarning("widthdraw","Insufficient Balance to Widthdraw")
             

        btn_sub=Button(ifrm,text='Submit',font=('arial',15,'bold'),bd=5,bg='pink',command=widthdraw_db)
        btn_sub.place(relx=.3,rely=.4)




    def transfer():
        ifrm=Frame(frm,highlightbackground='powder blue',highlightthickness=3)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.15,rely=.1,relwidth=.7,relheight=.5)
   
        lbl_welcome=Label(ifrm,text='This is Transfer Screen',font=('arial',15,'bold'),bg='pink',fg='blue')
        lbl_welcome.pack()

        lbl_amt=Label(ifrm,text="Amount",font=('arial',20,'bold'),bg='pink')
        lbl_amt.place(relx=.1,rely=.2)
    
        e_amt=Entry(ifrm,font=('arial',20,'bold'),bg='white',fg='black',bd=0)
        e_amt.place(relx=.3,rely=.2)
        e_amt.focus()

        lbl_to=Label(ifrm,text="To",font=('arial',20,'bold'),bg='pink')
        lbl_to.place(relx=.1,rely=.3)
    
        e_to=Entry(ifrm,font=('arial',20,'bold'),bg='white',fg='black',bd=0)
        e_to.place(relx=.3,rely=.3)
        e_to.focus()

        def tansfer_db():
            to_acn=e_to.get()
            amt=float(e_amt.get())

            if to_acn==gacn:
                messagebox.showwarning("Transfer","To and From can't be same")
                return 
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from acn where acn_no=?",(gacn,))
            tup=curobj.fetchone()
            avail_bal=tup[0]
            conobj.close()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from acn where acn_no=?",(to_acn,))
            tup=curobj.fetchone()
            conobj.close()

            if tup==None:
                messagebox.showwarning("Transfer","Invalid To ACN")
                return
            if avail_bal>=amt:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("Update acn set acn_bal=acn_bal+? where acn_no=?",(amt,to_acn))
                curobj.execute("Update acn set acn_bal=acn_bal-? where acn_no=?",(amt,gacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Transfer",f"{amt} transfered to ACN {to_acn}")


            

            

        btn_sub=Button(ifrm,text='Submit',font=('arial',15,'bold'),bd=5,bg='pink',command=tansfer_db)
        btn_sub.place(relx=.3,rely=.5)

        



    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("select acn_name from acn where acn_no=?",(gacn,))
    tup=curobj.fetchone()
    conobj.close()
          
    lbl_welcome=Label(frm,text=f"Welcome,{tup[0]}",font=('arial',20,'bold'),bg='white')
    lbl_welcome.place(relx=0,rely=0)

    btn_logout=Button(frm,width=5,text='Logout',font=('arial',15,'bold'),bd=4,bg='pink',command=logout)
    btn_logout.place(relx=.9,rely=0)

    btn_details=Button(frm,command=details,width=10,text='Details',font=('arial',15,'bold'),bd=4,bg='pink')
    btn_details.place(relx=0,rely=.1)

    btn_update=Button(frm,command=update,width=10,text='Update',font=('arial',15,'bold'),bd=4,bg='pink')
    btn_update.place(relx=0,rely=.15)

    btn_deposit=Button(frm,command=deposit,width=10,text='Deposit',font=('arial',15,'bold'),bd=4,bg='pink')
    btn_deposit.place(relx=0,rely=.2)

    btn_widthdraw=Button(frm,command=widthdraw,width=10,text='Widthdraw',font=('arial',15,'bold'),bd=4,bg='pink')
    btn_widthdraw.place(relx=0,rely=.25)

    btn_transfer=Button(frm,command=transfer,width=10,text='Transfer',font=('arial',15,'bold'),bd=4,bg='pink')
    btn_transfer.place(relx=0,rely=.3)






main_screen()
win.mainloop() # visible window


# In[ ]:




