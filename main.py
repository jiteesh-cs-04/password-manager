import storagemanager as st
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from passwordManager import *
import generator as g
data=st.load_database()
pm=PasswordManager(data)
current_website=None
current_account=None
def refresh_website(data):
    listbox.delete(0,tk.END)
    for i in data:
        listbox.insert(tk.END,i)
def add_website():
    website = simpledialog.askstring(
    "Add Website",
    "Enter website name:")
    if website=="":
        messagebox.showwarning('Error',"website name cannot be empty!")
    if website==None:
        return
    website = website.strip().lower()
    pm.add_website(website)
    refresh_website(data)
    st.write_database(data)
def delete_website():
    selected=listbox.curselection()# returns the index according to the position of the website (listbox)in a tuple
    if selected==():
        messagebox.showwarning("delete website","Select a website to delete")
    website=listbox.get(selected)
    answer=messagebox.askyesno(
    title="Delete Website",
    message=f"Are you sure you want to delete the website {website}?\n\nAll accounts stored in it will be permanently deleted.")
    if answer:
        pm.del_website(website)
        st.write_database(data)
        refresh_website(data)
def open_accounts():
    selected=listbox.curselection()
    if selected==():
        messagebox.showwarning("open website","Select a website to open")
        return
    website=listbox.get(selected[0])
    global current_website
    current_website=website
    frame_websites.pack_forget()
    frame_accounts.pack()
    label_title.config(text=f"Webiste:{current_website}")
    refresh_accounts(data)
    
    
root=tk.Tk()
root.geometry("500x600")
root.title("Password Manager")
frame_websites=tk.Frame(root)
frame_websites.pack()
label_title=tk.Label(frame_websites,text="PASSWORD MANAGER")
label_title.pack(pady=4)
label_website=tk.Label(frame_websites,text="Webistes:")
label_website.pack(pady=4)
listbox=tk.Listbox(frame_websites,width=35,height=16)
refresh_website(data)
scroll=tk.Scrollbar(root)
listbox.config(yscrollcommand=scroll.set)
scroll.config(command=listbox.yview)
listbox.pack(pady=10)
button_open_web=tk.Button(frame_websites,text="Open",command=open_accounts)
button_open_web.pack(pady=4)
button_add_web=tk.Button(frame_websites,text="add website",command=add_website)
button_add_web.pack(pady=4)
button_del_web=tk.Button(frame_websites,text="delete website",command=delete_website)
button_del_web.pack(pady=4)
def back_to_website():
    frame_accounts.pack_forget()
    frame_websites.pack()
def add_accounts():
    username = simpledialog.askstring(
    "Add accounts",
    "Enter username:")
    if username=="":
        messagebox.showwarning('Error',"Username cannot be empty!")
        return
    if username is None:
        return
    password = simpledialog.askstring(
    "Add accounts",
    "Enter password:")
    if password=="":
        messagebox.showwarning('Error',"password cannot be empty!")
        return
    if password is None:
        return
    account={"username":username,"password":password}
    pm.add_account(current_website,account)
    st.write_database(data)
    refresh_accounts(data)
    
def del_accounts():
    selected=listbox_accounts.curselection()# returns the index according to the position of the website (listbox)in a tuple
    if selected==():
        messagebox.showwarning("delete account","Select an account to delete")
        return
    account=listbox.get(selected)
    answer=messagebox.askyesno(
    title="Delete Account",
    message=f"Are you sure you want to delete the account {account}?\n\nAll information stored in it will be permanently deleted.")
    if answer:
        pm.delete_account(account)
        st.write_database(data)
        refresh_accounts(data)
def refresh_accounts(data):
    listbox_accounts.delete(0,tk.END)
    for i in data[current_website]:
        listbox_accounts.insert(tk.END,i['username'])

def open_acc_details():
    selected=listbox_accounts.curselection()
    if selected==():
        messagebox.showwarning("open account","Select an account to open")
        return
    username=listbox_accounts.get(selected[0])
    global current_account
    current_account=pm.search_account(current_website,username)
    frame_accounts.pack_forget()
    frame_details.pack()
    label_username.config(text=f"Username : {current_account['username']}")
    label_password.config(text=f"Password : {'*' * len(current_account['password'])}")
    label_title.config(text=f"Your Account")

    

frame_accounts=tk.Frame(root)

listbox_accounts=tk.Listbox(frame_accounts,width=35,height=16)
label_title=tk.Label(frame_accounts,text=f"Website:{current_website}")
label_title.pack(pady=4)
label_accounts=tk.Label(frame_accounts,text="Accounts:")
label_accounts.pack(pady=4)
scroll_accounts=tk.Scrollbar(root)
listbox_accounts.config(yscrollcommand=scroll_accounts.set)
scroll_accounts.config(command=listbox_accounts.yview)
listbox_accounts.pack(pady=10)
button_open_acc=tk.Button(frame_accounts,text="Open",command=open_acc_details)
button_open_acc.pack(pady=4)
button_add_acc=tk.Button(frame_accounts,text="add account",command=add_accounts)
button_add_acc.pack(pady=4)
button_del_acc=tk.Button(frame_accounts,text="delete account",command=del_accounts)
button_del_acc.pack(pady=4)
button_back_web=tk.Button(frame_accounts,text="back",command=back_to_website)
button_back_web.pack(pady=4)

def hide_password():
    label_password.config(text=f"Password : {'*' * len(current_account['password'])}")
    button_show_password.config(text="Show Password",command=show_password)
def show_password():
    label_password.config(text=f"Password : {current_account['password']}")
    button_show_password.config(text="hide password",command=hide_password)
def back_to_account():
    frame_details.pack_forget()
    frame_accounts.pack()
def change_password():
    answer=messagebox.askyesno(title='Change password',message='Generate a password?')
    if not answer:
        new_password = simpledialog.askstring('change password','Enter the new password')
        condition=pm.edit_account(current_website,current_account,new_password)
        if condition[0]:
            label_password.config(text=f"{new_password}")
            messagebox.showinfo('success','password has been changed')
            return
        else:
            messagebox.showerror('Error',f"{condition[1]}")
            return
    else:
        new_password=g.generate_password()[1]
        ans=messagebox.askyesno(title='generate password',message=f'generated password: {new_password}\n save this Password?')
        if ans:
            condition=pm.edit_account(current_website,current_account,new_password)
            if condition[0]:
                label_password.config(text=f"Password: {new_password}")
                messagebox.showinfo('success','password has been changed')
                return
            else:
                messagebox.showerror('Error',f"{condition[1]}")
                return
        else:
            return
    
frame_details=tk.Frame(root)
label_username=tk.Label(frame_details,text="")
label_username.pack(pady=4)
label_password=tk.Label(frame_details,text="")
label_password.pack(pady=4)
button_show_password=tk.Button(frame_details,text="Show Password",command=show_password)
button_show_password.pack(pady=4)
button_change_password=tk.Button(frame_details,text='Change Password',command=change_password)
button_change_password.pack(pady=4)
button_back_acc=tk.Button(frame_details,text='back',command=back_to_account)
button_back_acc.pack(pady=4)








root.mainloop()
