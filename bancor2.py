import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

#	get the resulting price of token
#	
def getPrice(balance,supply,CRR):
	return balance/(supply*CRR)

#	The actual price of a smart token is calulated as a function of the transaction size

#	global
#	R: Reserve Token Balance
#	S: Smart Token Supply
#	F: Constant Reserve Ratio(CRR)
R = 60000.0
S = 300000.0
F = 0.2

rnd = np.random
start = []	# x-coordinate of left line of each Bar
width = []	# width of each Bar
height = []	# height of each Bar(effective price)
h = []		# height of each price(starting price and resulting price)

#	initialize variables that holds current value
st = 0.00 		# x-coordinate of current Bar(first bar starts from '0')
ht = R/(S*F)	# current price(starting price of ETH/BNT)

color = [] # color of each har, 0: Red, 1:Green

epoch = 0 # count transactions

def result():
	global R,S,F,epoch
	print '|'
	print '|   *** Result ***'
	print '|   Reserve Balance: ', R
	print '|   BNT Supply: ',S
	p = R/(S*F)
	print '|   Price(Ether/BNT): ',p
	print ' - - - - - - - - - - - - - - - - - - - - - - - - - -'
	print ''
	return p

#	t = Smart tokens received(issued) in exchange for E, given r,s, and f.
#	E: Reserve token paid
def getSmart_(E):
	global R,S,F
	t = S*( ( 1.0 + E/R )**F - 1.0 )
	R += E 		# increment Reserve Balance
	S += t 		# issue Smart Token
	return t

#	Wrapper method
def getSmart(E):
	global epoch, tx, price, st, ht
	epoch += 1
	t = getSmart_(E)
	p = E/t
	width.append(np.array([t]))
	start.append(st)
	st += t
	height.append(np.array([p]))
	color.append(1)
	print ' - - transaction: No. ', epoch,' - - - - - - - - - - - - - -'
	print '|   Paid: ', E, ' ETH'
	print '|   Received:', t, ' BNT'
	print '|   Effective Rate: ', p, ' ETH/BNT'
	h.append(ht)
	ht = result()	# ht = new effective price
	return t

#	e = Reserve tokens received in exchange for T, given r,s, abd f.
#	T: Smart token paid (destroyed)
def getReserve_(T):
	global R,S,F
	e = R*( 1.0 - (1.0 - T/S)**(1.0/F) )
	R -= e 		# decrement Reserve Balance
	S -= T 		# destroy Smart Token
	return e

#	Wrapper method
def getReserve(T):
	global epoch, tx,  price, st, ht
	epoch += 1
	e = getReserve_(T)
	p = e/T
	width.append(np.array([T]))
	start.append(st)
	st += T
	height.append(np.array([p]))
	color.append(0)
	print ' - - transaction: No. ', epoch,' - - - - - - - - - - - - - -'
	print '|   Paid: ', T, ' BNT'
	print '|   Received:', e, ' ETH'
	print '|   Effective Rate: ', p, ' ETH/BNT'
	h.append(ht)
	ht = result()	# ht = new effective price
	return e

num_of_tx = 4


# ---- Transaction Registration Starts -----

# * Parameters should be float type
# * first transaction comes first
# * multiple Reserve is not yet supported
	
getSmart(300.0)			# Convert 300.0 ETH to BNT
getSmart(700.0)			# Convert 700.0 ETH to BNT
getReserve(1302.0)		# Convert 1302.0 BNT to ETH
getSmart(100.0)			# Convert 100.0 ETH to BNT

# ---- Transaction Registration Ends --------


start.append(st)
h.append(ht)

c1 = '#000000'
c2 = '#000000'

#	plot bars and lines
for i in range(0,num_of_tx):
	if color[i] == 1:
		c1 = '#3FC380'
		c2 = '#1E824C'
	else:
		c1 = '#D24D57'
		c2 = '#96281B'

	plt.bar(start[i],height[i],width = width[i], color= c1)
	plt.plot([start[i], start[i+1]], [h[i],h[i+1]],color = c2)


plt.plot(start,h,'ro',color = '#000000')

plt.axis([-50.0, 2550.0, 0.95, 1.02])
plt.xlabel('Amount [BNT] Green: issued, Red: destroyed')
plt.ylabel('Price [ ETH/BNT ]')
plt.title('Flow of Transactions')
ax = plt.gca()
y_formatter = ticker.ScalarFormatter(useOffset=False)
ax.yaxis.set_major_formatter(y_formatter)
plt.grid(True)
plt.show()
