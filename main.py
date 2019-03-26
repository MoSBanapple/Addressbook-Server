import webapp2
from google.appengine.ext import ndb
kind = "Listing"



class Listing(ndb.Model):
    name = ndb.StringProperty()
    address = ndb.StringProperty()


def add(name_input, address_input):
    input = Listing(name=name_input, address=address_input)
    input.key = ndb.Key(kind, name_input)
    input.put()


	
def delete(name):
    target = ndb.Key(kind, name).get()
    if not target:
        return False
    target.key.delete()
    return True
	
def find(name):
    target = ndb.Key(kind, name).get()
    if not target:
        return False
    return target.address

	
	
def list():
    output = ""
    listings = Listing.query().fetch()
    for entity in listings:
        output += entity.name + ": " + entity.address + "\n"
    return output



		


class MainPage(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        action = str(self.request.get("action"))
        name = str(self.request.get("name"))
        address = str(self.request.get("address"))
        if action == "delete":
            if delete(name):
                self.response.write(name + " has been removed.\n")
            else:
                self.response.write(name + " is not in the list.\n")
       	elif action == "add":
       	    add(name, address)
       	    self.response.write(name + " has been added/updated.\n")
        elif action == "find":
            found = find(name)
            if found:
                self.response.write("The address of " + name + " is " + found + ".\n")
            else:
                self.response.write(name + " is not in the list.\n")
        elif action == "list":
            self.response.write(list())
        else:
            self.response.write("Invalid entry, please try again.\n")
        


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
