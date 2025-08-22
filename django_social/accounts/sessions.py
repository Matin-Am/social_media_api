

'''
 {
    "user_data" : {
        "phone_number" : {
            "email" : "" , 
            "password" : "" 
            
        }
    } ,
 
 
 }
'''

SESSION_ID = "user_data"

class Data:
    def __init__(self,request,phone_number,email):
        self.session = request.session
        self.phone_number = phone_number
        self.email = email

        if SESSION_ID not in self.session:
            self.session[SESSION_ID] = {}
        if phone_number not in self.session[SESSION_ID]:
            self.session[SESSION_ID][phone_number] = {}

    def save_data(self,password):
        self.session[SESSION_ID] = {
            self.phone_number:{
                "email" : self.email , 
                "password" : password
            }   
        }
        self.save()

    def save(self):
        self.session.modified = True