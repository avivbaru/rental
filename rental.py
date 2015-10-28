

class User(object):
    def __init__(self, user_name, first_name, last_name, **kwargs):
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
		self.id = generate_id()
        self.name = name
        self.desciption = None
        self.price = None
        self.category = category
        self.available = True
        self.start_date = None
        self.end_date = None

    def generate_id():
        return ""
