import random
def generate_password(size=8):
    if size<8:
        return False,"PASSWORD_TOO_SHORT"
    if size>20:
        return False,"PASSWORD_TOO_LONG"
    UPPER_CASE="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    LOWER_CASE="abcdefghijklmnopqrstuvwxyz"
    NUMBERS="1234567890"
    SYMBOLS="!@#$%^&*=:><?/"
    CHARACTER_GROUPS=[UPPER_CASE,LOWER_CASE,NUMBERS,SYMBOLS]
    L_PASSWD=[]
    for i in CHARACTER_GROUPS:
        L_PASSWD+=[random.choice(i)]
    for i in range(size-4):
        CHARACTER_SET=random.choice(CHARACTER_GROUPS)
        L_PASSWD.append(random.choice(CHARACTER_SET))
    random.shuffle(L_PASSWD)
    password="".join(L_PASSWD)
    return True,password
            
    
