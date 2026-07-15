import storagemanager as sm
class PasswordManager:
    def __init__(self,data):
        self.data=data
    def add_account(self,website,account):
        if website not in self.data:
            self.data[website] = []
            sm.write_database(self.data)
        for i in self.data[website]:
            if account['username']==i['username']:
                 return False,"USERNAME_ALREADY_EXISTS"
        else:
            self.data[website].append(account)
            sm.write_database(self.data)
            return True,"SUCCESS"
    def search_account(self,website,username):
        if website in self.data:
            for i in self.data[website]:
                if i['username']==username:
                    return i
            else:
                return False,"ACCOUNT_NOT_FOUND"
        else:
            return False,"WEBSITE_NOT_FOUND"
    def delete_account(self,website,account):
        if website in self.data:
            if account in self.data[website]:
                self.data[website].remove(account)
                if self.data[website]==[]:
                    del self.data[website]
                sm.write_database(self.data)
                return True,"SUCCESS"
            else:
                return False,"ACCOUNT_NOT_FOUND"
        else:
            return False,"WEBSITE_NOT_FOUND"
    def edit_account(self,website,account,new_password):
        if website in self.data:
            if account in self.data[website]:
                if account['password']!=new_password:
                    account['password']=new_password
                    return True,"SUCCESS"
                
                else:
                    return False,"PASSWORD_UNCHANGED"
            else:
                return False,"ACCOUNT_NOT_FOUND"
        else:
            return False,"WEBSITE_NOT_FOUND"
    def add_website(self,website):
        website = website.strip().lower()
        self.data[website]=[]
        sm.write_database(self.data)
    def del_website(self,website):
        website = website.strip().lower()
        del self.data[website]
        sm.write_database(self.data)
    
            
            
        
