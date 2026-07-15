import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import passwordManager as pm
import generator as g




        
        
        
        
class website_frame(tk.Frame):
    def __init__(self,parent,coordinator):
        super().__init__(parent)
        self.coordinator=coordinator
        self.title=tk.Label(self,text="WEBSITES")
        self.title.pack(pady=4)
        self.listbox = tk.Listbox(self)
        self.listbox.pack()
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.open_button = tk.Button(self, text="Open Website",command=self.open_clicked)
        self.open_button.pack()
        self.add_button = tk.Button(self, text="Add Website",command=self.add_clicked)
        self.add_button.pack()
        self.delete_button = tk.Button(self, text="Delete Website",command=self.delete_clicked)
        self.delete_button.pack()     
    def add_clicked(self):
        self.coordinator.add_website()
    def open_clicked(self):
        self.coordinator.open_accounts()
    def delete_clicked(self):
        self.coordinator.del_website(self.get_selected_website())
    def refresh_websites(self,data):
        self.listbox.delete(0,tk.END)
        for website in data.keys():
            self.listbox.insert(tk.END,website)
    def ask_website(self):
        website = simpledialog.askstring(
            "Add website",
            "Enter website name:")
        return website
    def get_selected_website(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning('Error',"No website selected!")
            return 
        website = self.listbox.get(selected_index[0])
        return website

class account_frame(tk.Frame):
    def __init__(self,parent,coordinator):
        super().__init__(parent)
        self.coordinator=coordinator
        self.title=tk.Label(self,text="ACCOUNTS")
        self.title.pack(pady=4)
        self.listbox = tk.Listbox(self)
        self.listbox.pack()
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.open_button = tk.Button(self, text="Open Account",command=self.open_clicked)
        self.open_button.pack()
        self.add_button = tk.Button(self, text="Add Account",command=self.add_clicked)
        self.add_button.pack()
        self.delete_button = tk.Button(self, text="Delete Account",command=self.delete_clicked)
        self.delete_button.pack()
        self.back_button = tk.Button(self, text="Back",command=self.back_clicked)
        self.back_button.pack()
    def refresh_accounts(self,data,current_website):
        self.listbox.delete(0,tk.END)
        for account in data[current_website]:
            self.listbox.insert(tk.END,account["username"])
    def ask_account(self):
        username = simpledialog.askstring(
            "Add account",
            "Enter username:")
        return username
    def add_clicked(self):
        self.coordinator.add_account()
    def open_clicked(self):
        self.coordinator.open_details()
    def delete_clicked(self):
        self.coordinator.del_account()
    def back_clicked(self):
        self.coordinator.back_to_websites()
    def get_selected_account(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning('Error',"No account selected!")
            return 
        account_username = self.listbox.get(selected_index[0])
        return account_username
    def get_current_account(self,data,current_website):
        acc_username=self.get_selected_account()
        for i in data[current_website]:
            if acc_username in i.values():
                return i





class frame_details(tk.Frame):
    def __init__(self,parent,coordinator):
        super().__init__(parent)
        self.coordinator = coordinator
        self.title=tk.Label(self,text="ACCOUNT DETAILS")
        self.title.pack(pady=4)
        self.label_username=tk.Label(self,text="")
        self.label_username.pack(pady=4)
        self.label_password=tk.Label(self,text="")
        self.label_password.pack(pady=4)
        self.hide_show_button=tk.Button(self,text="Show Password",command=self.show_clicked)
        self.hide_show_button.pack(pady=4)
        self.change_password_button=tk.Button(self,text="Change Password",command=self.change_clicked)
        self.change_password_button.pack(pady=4)
        self.back_button=tk.Button(self,text="Back",command=self.back_clicked)
        self.back_button.pack(pady=4)


    def hide_clicked(self): 
        self.coordinator.hide_password()
    def show_clicked(self):
        self.coordinator.show_password()
    def change_clicked(self):
        self.coordinator.change_password()
    def back_clicked(self):
        self.coordinator.back_to_accounts()


    
        
    
                
            
class password_GUI:
    def __init__(self,data):
        self.root=tk.Tk()
        self.root.geometry("500x300")
        self.root.title("Password Manager")  
        self.websites=website_frame(self.root,self)
        self.accounts=account_frame(self.root,self)
        self.details=frame_details(self.root,self)
        self.data=data
        self.pm=pm.PasswordManager(self.data)
        self.current_website=None


    def add_website(self):
        website=self.websites.ask_website()
        if website=="":
            messagebox.showwarning('Error',"Website name cannot be empty!")
            return
        if website is None:
            return
        self.pm.add_website(website)
        self.websites.refresh_websites(self.data)


    def del_website(self,website):
        website = self.websites.get_selected_website()
        if website=="":
            messagebox.showwarning('Error',"No website selected!")
            return
        if website is None:
            return
        self.pm.del_website(website)
        self.websites.refresh_websites(self.data)

    
    def add_account(self):
        username=self.accounts.ask_account()
        if username=="":
            messagebox.showwarning('Error',"Username cannot be empty!")
            return
        if username is None:
            return
        password = simpledialog.askstring('change password','Enter the new password')
        if password=="":
            messagebox.showwarning('Error',"Password cannot be empty!")
            return
        if password is None:
            return  
        acc_dict={"username":username,"password":password}
        condition=self.pm.add_account(self.current_website,acc_dict)
        self.accounts.refresh_accounts(self.data,self.current_website)
        return condition
        
        
    def del_account(self):
        account_username=self.accounts.get_selected_account()
        if account_username=="":
            messagebox.showwarning('Error',"No account selected!")
            return
        if account_username is None:
            return
        self.pm.delete_account(self.current_website,account_username)
        self.accounts.refresh_accounts(self.data,self.current_website)

    
    def hide_password(self):
        
        current_account=self.accounts.get_current_account(self.data,self.current_website)
        self.details.label_password.config(text=f"Password:{'*' * len(current_account['password'])} ")
        self.details.hide_show_button.config(text="Show Password",command=self.details.show_clicked)


    def show_password(self):
        
        current_account=self.accounts.get_current_account(self.data,self.current_website)
        self.details.label_password.config(text=f"Password: {current_account['password']}")
        self.details.hide_show_button.config(text="Hide Password",command=self.details.hide_clicked)


    def change_password(self):
        current_account=self.accounts.get_current_account(self.data,self.current_website)
        answer=messagebox.askyesno(title='Change password',message='Generate a password?')
        if not answer:
            new_password = simpledialog.askstring('change password','Enter the new password')
            condition=self.pm.edit_account(self.current_website,current_account,new_password)
            if condition[0]:
                self.details.label_password.config(text=f"{new_password}")
                messagebox.showinfo('success','password has been changed')
                return
            else:
                messagebox.showerror('Error',f"{condition[1]}")
                return
        else:
            new_password=g.generate_password()[1]
            ans=messagebox.askyesno(title='generate password',message=f'generated password: {new_password}\n save this Password?')
            if ans:
                condition=self.pm.edit_account(self.current_website,current_account,new_password)
                if condition[0]:
                    self.details.label_password.config(text=f"Password: {new_password}")
                    messagebox.showinfo('success','password has been changed')
                    return
                else:
                    messagebox.showerror('Error',f"{condition[1]}")
                    return
            else:  
                return
            

    def open_accounts(self):
        self.current_website=self.websites.get_selected_website()
        if self.current_website==None:
            messagebox.showwarning('Error',"No website selected!")
            return
        self.accounts.refresh_accounts(self.data,self.current_website)
        self.websites.pack_forget()
        self.accounts.pack(fill="both",expand=True)

        
    def open_details(self):

        current_account=self.accounts.get_current_account(self.data,self.current_website)
        if current_account==None:
            messagebox.showwarning('Error',"No account selected!")
            return
        self.details.label_username.config(text=f"Username: {current_account['username']}")
        self.details.label_password.config(text=f"Password: {'*' * len(current_account['password'])}")
        self.accounts.pack_forget()
        self.details.pack(fill="both",expand=True)


    def back_to_websites(self):
        self.accounts.pack_forget()
        self.websites.pack(fill="both",expand=True)

  
    def back_to_accounts(self):
        self.details.pack_forget()
        self.accounts.pack(fill="both",expand=True)
    
    def run(self):
        self.websites.pack(fill="both",expand=True)
        self.websites.refresh_websites(self.data)
        self.root.mainloop()
    
        
        