import time
import json

class User(object):
    def __init__(self, user_name, first_name, last_name, **kwargs):
        self.user_id = None
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.rate = 0
        self.comments = []
        self.offer = []
        self.rental = []

    def add_offer(self, offer):
        self.offer.append(offer)

    def add_rental(self, rental):
        self.rental.append(rental)

    def add_comment(self, comment):
        self.comments.append(comment)

    def calculate_rate(self):
        rates = [int(i.get("rate")) for i in self.comments]
        self.rate = reduce(lambda x, y: x + y, rates) / float(len(rates))


class Product(object):
    def __init__(self, name, category, **kwargs):
        self.id = self.generate_id()
        self.name = name
        self.desciption = None
        self.price = None
        self.category = category
        self.available = True
        self.start_date = None
        self.end_date = None
        self.is_offer = True
        self.user_id = None
        self.submit_date = int(time.time())

    def generate_id(self):
        return ""

    def __str__(self):
         return json.dumps(self.__dict__)

a=Product("tetes", "dsf")
print a 