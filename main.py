import math
import random
import matplotlib.pyplot as plt

#LISTS THAT HOLD GOODS AND FACTORIES
good_list=[]
factory_list=[]

#Global values for the year and the months
year = 1980
months = ["January", "April", "July", "October"]
m = 0

#Population value
population = 1000

class Good:
	"""This defines what a Good is, as well as some functions to change its amount and
		price"""

	def __init__(self, name, amount, price, name_list):
		self.name = name
		self.amount = amount
		self.price = price
		self.name_list = name_list

	def update_price(self):
		for i in range(len(self.price)-1):
			self.price[i] = self.price[i+1]

	def change_price(self, new_price):
		self.price[9] = self.price[9] + new_price

	def change_amount(self, change_amount):
		self.amount += change_amount

	def get_name(self):
		rand = random.randint(0,9)
		return self.name_list[rand]

class Factory:
	"""This defines what a Factory is, as well as some functions that determine its
		behaviour"""

	def __init__(self, company, name, ftype, balance, req_goods, req_amounts, good,
				efficiency, maintenence):
		self.company = company
		self.name = name
		self.ftype = ftype
		self.balance = balance
		self.req_goods = req_goods
		self.req_amounts = req_amounts
		self.good = good
		self.efficiency = efficiency
		self.maintenence = maintenence
		self.produced_goods = self.efficiency

	def buy_good(self):
		"""This function purchases required goods and produces the output good"""

		#At best the produced good's amount is the efficiency of the factory
		self.produced_goods = self.efficiency

		#Find out the total cost of 1 produced good
		total_cost = 0
		i = 0
		for good in self.req_goods:
			total_cost += good.price[9] * self.req_amounts[i]
			i += 1

		#The amount of produced goods is how much 90% of the balance can afford to buy
		#so lower it if necessary
		if math.floor((0.9*self.balance) / total_cost) < self.produced_goods:
			self.produced_goods = math.floor((0.9*self.balance) / total_cost)

		#However, maybe there isn't enough of a good in the world market to satisfy this
		#If that is the case, readjust the produced goods to use all the goods that DO
		#actually exist
		i = 0
		new_produced_goods = self.produced_goods
		for good in self.req_goods:
			if (self.produced_goods * self.req_amounts[i]) > good.amount:
				#Increase the price of the good
				good.change_price(((self.produced_goods * self.req_amounts[i]) - good.amount) / 100)
				#And set the produced goods to be lower, unless it is already lower
				if (good.amount / self.req_amounts[i]) < new_produced_goods:
					new_produced_goods = (good.amount / self.req_amounts[i])
			i += 1
		#Finally update the actual produced goods to be this new value
		#The extra step is required to make sure ALL required goods get a price increase
		self.produced_goods = new_produced_goods

		#If the factory cannot produce at least ONE unit, it will not produce at all
		if self.produced_goods < 1:
			self.produced_goods = 0

		#Once the amount of goods to be produced has been found out, buy the goods
		i = 0
		for good in self.req_goods:
			self.balance -= good.price[9] * self.produced_goods * self.req_amounts[i]
			good.amount -= self.produced_goods * self.req_amounts[i]
			i += 1

	def sell_good(self):
		self.balance += self.produced_goods * self.good.price[9]
		self.good.amount += self.produced_goods

	def pay_for_maintenence(self):
		self.balance -= self.maintenence
		if self.balance <= 0:
			print "FACTORY CLOSED" #PLACEHOLDER FOR NEWS
			factory_list.remove(self)

	def expand_company(self):
		"""When a factory has enough money, it will create a new factory in the same
			company"""

		if self.balance >= 30000:
			self.balance -= 25000
			create_factory(self.company)

def initialise():
	"""Is run at the start of a new game"""

	#Set the Goods as global since most scopes will use them
	global grain
	global timber
	global cattle
	global fish
	global wool
	global coal
	global iron
	global cotton
	global tea
	global coffee
	global tobacco
	global silk
	global opium
	global dye
	global gold
	global oil

	#And the goods list and factory list, of course
	global good_list
	global factory_list

	#Now create the actual objects
	grain=Good("Grain", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.1], ["Grain", "Grain", "Grain", "Grain", "Grain", "Grain", "Grain", "Grain", "Grain", "Grain"])
	timber=Good("Timber", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.5], ["Timber", "Timber", "Timber", "Timber", "Timber", "Timber", "Timber", "Timber", "Timber", "Timber"])
	cattle=Good("Cattle", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.7], ["Cattle", "Cattle", "Cattle", "Cattle", "Cattle", "Cattle", "Cattle", "Cattle", "Cattle", "Cattle"])
	fish=Good("Fish", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.1], ["Fish", "Fish", "Fish", "Fish", "Fish", "Fish", "Fish", "Fish", "Fish", "Fish"])
	wool=Good("Wool", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.3], ["Sheep", "Sheep", "Sheep", "Sheep", "Sheep", "Sheep", "Sheep", "Sheep", "Sheep", "Sheep", ])
	coal=Good("Coal", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 1.5], ["Coal Mine", "Coal Mine", "Coal Mine", "Coal Mine", "Coal Mine", "Coal Mine", "Coal Mine", "Coal Mine", "Coal Mine", "Coal Mine"])
	iron=Good("Iron", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 2.0], ["Iron Mine", "Iron Mine", "Iron Mine", "Iron Mine", "Iron Mine", "Iron Mine", "Iron Mine", "Iron Mine", "Iron Mine", "Iron Mine"])
	cotton=Good("Cotton", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 1.0], ["Cotton Fields", "Cotton Fields", "Cotton Fields", "Cotton Fields", "Cotton Fields", "Cotton Fields", "Cotton Fields", "Cotton Fields", "Cotton Fields", "Cotton Fields"])
	tea=Good("Tea", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.5], ["Tea", "Tea", "Tea", "Tea", "Tea", "Tea", "Tea", "Tea", "Tea", "Tea"])
	coffee=Good("Coffee", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.5], ["Coffee", "Coffee", "Coffee", "Coffee", "Coffee", "Coffee", "Coffee", "Coffee", "Coffee", "Coffee"])
	tobacco=Good("Tobacco", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 1.0], ["Tobacco", "Tobacco", "Tobacco", "Tobacco", "Tobacco", "Tobacco", "Tobacco", "Tobacco", "Tobacco", "Tobacco"])
	silk=Good("Silk", 100.0, [10.0, 10.0, 20.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 3.0], ["Silk", "Silk", "Silk", "Silk", "Silk", "Silk", "Silk", "Silk", "Silk", "Silk"])
	opium=Good("Opium", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 2.0], ["Opium", "Opium", "Opium", "Opium", "Opium", "Opium", "Opium", "Opium", "Opium", "Opium"])
	dye=Good("Dye", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 2.0], ["Dye", "Dye", "Dye", "Dye", "Dye", "Dye", "Dye", "Dye", "Dye", "Dye"])
	gold=Good("Gold", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0], ["Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold"])
	oil=Good("Oil", 100.0, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 11.0], ["Oil", "Oil", "Oil", "Oil", "Oil", "Oil", "Oil", "Oil", "Oil", "Oil"])

	#And add the goods to the goods list
	good_list.append(grain)
	good_list.append(timber)
	good_list.append(cattle)
	good_list.append(fish)
	good_list.append(wool)
	good_list.append(coal)
	good_list.append(iron)
	good_list.append(cotton)
	good_list.append(coffee)
	good_list.append(tobacco)
	good_list.append(silk)
	good_list.append(opium)
	good_list.append(dye)
	good_list.append(gold)
	good_list.append(oil)

	#These lists defines what goods the population will consume, and in what amounts
	global pop_req_goods
	pop_req_goods=[fish, tea, coffee, tobacco, opium]

	global pop_req_amounts
	pop_req_amounts=[2.0, 0.2, 0.3, 0.1, 0.1]

def next_turn():
	global population
	"""This function dictates what happens when the user advances the turn"""

	#First the factories will pay for maintenence, and shut down if they can't afford it
	for factory in factory_list:
		factory.pay_for_maintenence()

	#Then the prices get updated, without changing the latest price
	for good in good_list:
		good.update_price()

	#RGO producing factories sell their goods to the world market
	for factory in factory_list:
		if factory.ftype == "RGO":
			factory.sell_good()

	#Next Producer factories purchase goods from the world market that they require
	#to produce their output good
	for factory in factory_list:
		if factory.ftype == "Producer":
			factory.buy_good()

	#Next the Producer factories go on to sell their produced good
	for factory in factory_list:
		if factory.ftype == "Producer":
			factory.sell_good()

	#When the factories are done the population will consume their goods
	i = 0
	for good in pop_req_goods:
		#If the population cannot get enough goods to satisfy itself the price increases
		if good.amount < (pop_req_amounts[i] * population):
			good.change_price(((pop_req_amounts[i] * population) - good.amount) / 100.0)
			good.amount = 0.0
			population -= population*0.005
		#Otherwise the amount of goods drops by the need of the population
		else:
			good.amount = good.amount - (pop_req_amounts[i] * population)
			population += population*0.005
		i += 1

	#Finally when all goods have been sold and bought, any leftover will drop in price
	#but remain in the market
	for good in good_list:
		if good.amount > 0.0:
			good.change_price(-1.0 * (good.amount / 100.0))
			#And make sure the price doesn't hit 0
			if good.price[9] <= 0: good.price[9] = 0.01

	#When the selling and buying, as well as price drop is done, companies will expand
	for factory in factory_list:
		factory.expand_company()

	#We also need to advance the date
	global m
	global year
	m += 1
	if m > 3:
		m = 0
		year += 1

def show_graph(good):
	goods_plot=good.price[0:10]
	plt.plot(goods_plot)
	plt.ylabel('Price')
	plt.show()

def present_menu():
	"""This function presents the menu to the user, and will run constantly in the main
		loop of the game"""

	#First present the main list of options, as well as today's date	
	print "\n"
	print months[m] + ", " + str(year)
	print "Population: " + str(population)
	print "1. Goods"
	print "2. Factories"
	print "3. Next quarter"
	entered = input()

	#If the user chose Goods, first list all the goods
	if entered == 1:
		i = 1
		for good in good_list:
			print str(i) + ". " + str(good.name)
			i += 1
		#Then show him the graph, price, and supply of the chosen good
		entered = input()
		print "Current supply of " + good_list[entered-1].name + ": " + str(good_list[entered-1].amount)
		print "Current price of " + good_list[entered-1].name + ": " + str(good_list[entered-1].price[9])
		show_graph(good_list[entered-1])

	#If the user entered factories, show him a list of all the factories
	elif entered == 2:
		i = 1
		for factory in factory_list:
			print str(i) + ". " + factory.company + " " + factory.name
			i = i+1
		print str(i) + ". Back"
		#Then show him information about that factory
		entered = input()
		if entered == i: present_menu
		else:
			factory = factory_list[entered-1]
			print "Information for " + factory.company + " " + factory.name
			print "Balance: $" + str(factory.balance)
			print "Intake Goods: ",
			for good in factory.req_goods:
				print good.name + ",",
			print "\nOutput Good: " + factory.good.name
			print "Maintenence: $" + str(factory.maintenence)
			print "Max output: " + str(factory.efficiency)

	#Finally, if he entered next quarter, advance the turn
	elif entered == 3:
		next_turn()

	else:
		print "Invalid option!\n"
		present_menu

def create_factory(company):
	"""Function to create a random new factory"""

	#First we choose the type of factory this will be, randomly
	rand = random.randint(0,1)
	if rand == 1:
		ftype = "RGO"
	else:
		ftype = "RGO" #REPLACE WITH PRODUCER

	#Next we need to pick the good to be produced, depending on the type
	if ftype == "RGO":
		req_goods = []
		req_amounts = []

		rand = random.randint(0, 14)
		good = good_list[rand]

		name = good.get_name()

		efficiency = random.randint(20, 100)
		maintenence = random.randint(50, 200)


	#Now we create the actual factory with the attributes determined
	newFactory=Factory(company, name, ftype, 1000.0, req_goods, req_amounts, good, efficiency, 
						maintenence)
	factory_list.append(newFactory)

initialise()
create_factory("Larry's")
create_factory("Bob's")
create_factory("Carl's")
create_factory("Frank's")
create_factory("Harry's")
create_factory("John's")

#MESSAGE
print "1. You may get unprofitable factories generated, if so, just restart"
print "2. Don't press any other buttons than available, I haven't put in actual excpetion handling yet"
print "3. The game will crash once all factories are dead, if they all die that is"
#END OF MESSAGE

while True:
	present_menu()
