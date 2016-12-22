import csv
import random
import math
import copy
import numpy
import pickle
#import matplotlib.pyplot as plt

x_middle=[]
y_middle=[]

def normalAngle(v_xMid, v_yMid):
	nPoints = np.size(v_xMid)
	normal_angle = zeros(nPoints)

	try: 
		normal_angle[0] = (math.pi/2-math.atan((y_middle[1]-y_middle[len(y_middle)-1])/(x_middle[1]-x_middle[len(x_middle)-1])))
	except:
		normal_angle[0] = (0)
	for i in range(1,nPoints-1):
		try:
			normal_angle[i] = (math.pi/2-math.atan((y_middle[i+1]-y_middle[i-1])/(x_middle[i+1]-x_middle[i-1])))
		except:
			normal_angle[i] = (0)
	try: 
		normal_angle[i] = (math.pi/2-math.atan((y_middle[0]-y_middle[len(y_middle)-2])/(x_middle[0]-x_middle[len(x_middle)-2])))
	except:
		normal_angle[0] = (0)


def fitness_calculator(creature):
	global x_middle, y_middle
	x=[]
	y=[]
	diff_x=[]
	diff_y=[]
	diff2_y=[]
	diff2_x=[]
	k=[] #curvature
	normal_angle=[]
	try: 
		normal_angle.append(math.pi/2-math.atan((y_middle[1]-y_middle[len(y_middle)-1])/(x_middle[1]-x_middle[len(x_middle)-1]))) #+
	except:
		normal_angle.append(0)
	for i in range(1,len(x_middle)-1):
		try:
			normal_angle.append(math.pi/2-math.atan((y_middle[i+1]-y_middle[i-1])/(x_middle[i+1]-x_middle[i-1]))) #+
		except:
			normal_angle.append(0)
	try: 
		normal_angle.append(math.pi/2-math.atan((y_middle[0]-y_middle[len(y_middle)-2])/(x_middle[0]-x_middle[len(x_middle)-2]))) #+
	except:
		normal_angle.append(0)
	for i in range(len(normal_angle)):
		x.append(x_middle[i]-creature[i]*math.cos(normal_angle[i])) #+
		y.append(y_middle[i]+creature[i]*math.sin(normal_angle[i]))
	for i in range(len(creature)-1):
		diff_x.append((x[i+1]-x[i])/math.sqrt((x[i+1]-x[i])**2+(y[i+1]-y[i])**2))
		diff_y.append((y[i+1]-y[i])/math.sqrt((x[i+1]-x[i])**2+(y[i+1]-y[i])**2))
	diff_x.append((x[0]-x[len(creature)-1])/math.sqrt((x[0]-x[len(creature)-1])**2+(y[0]-y[len(creature)-1])**2))
	diff_y.append((y[0]-y[len(creature)-1])/math.sqrt((x[0]-x[len(creature)-1])**2+(y[0]-y[len(creature)-1])**2))
	for i in range(len(creature)-1):
		diff2_x.append((diff_x[i+1]-diff_x[i])/math.sqrt((x[i+1]-x[i])**2+(y[i+1]-y[i])**2))
		diff2_y.append((diff_y[i+1]-diff_y[i])/math.sqrt((x[i+1]-x[i])**2+(y[i+1]-y[i])**2))
	diff2_x.append((diff_x[0]-diff_x[len(creature)-1])/math.sqrt((x[0]-x[len(creature)-1])**2+(y[0]-y[len(creature)-1])**2))
	diff2_y.append((diff_y[0]-diff_y[len(creature)-1])/math.sqrt((x[0]-x[len(creature)-1])**2+(y[0]-y[len(creature)-1])**2))
	for i in range(len(creature)):
		k.append((abs(diff2_y[i]*diff_x[i]-diff2_x[i]*diff_y[i]))/(diff_x[i]**2+diff_y[i]**2))
	fitness=0
	for i in range(1,len(creature)-1):
		fitness+=k[i]**2*(math.sqrt((x[i]-x[i-1])**2+(y[i]-y[i-1])**2)+math.sqrt((x[i+1]-x[i])**2+(y[i+1]-y[i])**2))/2
	fitness+=k[0]**2*(math.sqrt((x[1]-x[0])**2+(y[1]-y[0])**2)+math.sqrt((x[0]-x[len(creature)-1])**2+(y[0]-y[len(creature)-1])**2))/2
	fitness+=k[len(creature)-1]**2*(math.sqrt((x[0]-x[len(creature)-1])**2+(y[0]-y[len(creature)-1])**2)+math.sqrt((x[len(creature)-1]-x[len(creature)-2])**2+(y[len(creature)-1]-y[len(creature)-2])**2))
	return fitness

def random_creature(width_track):
	creature=[]
	for itr in range(len(x_middle)):
		deviation=random.random()*float(width_track)/2
		direction=2*random.randint(0,1)-1
		creature.append(deviation*float(direction))
	return creature

def random_generation(width_track,n):
	generation=[]
	for x in range(n):
		creature=random_creature(width_track[x])
		generation.append(creature)
	return generation

def order(generation):
	ranked=[]
	for creature in generation:
		ranked.append((fitness_calculator(creature),creature))
	ranked.sort(reverse=False) #From small to large
	fitness_list=[]
	ordered_list=[]
	for fitness,creature in ranked:
		ordered_list.append(creature)
		fitness_list.append(fitness)
	return ordered_list

def purge(generation):
	size_generation=len(ordered_generation)
	maximal_surviving=0
	surviving_part=size_generation/3 #Assuming strictly top third survives
	for i in range(surviving_part,size_generation):
		del ordered_generation[surviving_part]
	return(ordered_generation)

def length_mutation(creature,length,width,strategy):
	if strategy == 0:
		startvalue = 0.03
	elif strategy == 1:
		startvalue = 0.01
	for i in range(len(creature)): #Last update
		if random.random() < length**(-1)*startvalue:#^9     4->7 8->9 16->11 32->13
			mutation_direction=random.randint(1,2) #1 is inward 2 is outward 
			mutation_inward=100
			mutation_outward=100
			for itr in range(length):
				mutation_inward=min(mutation_inward,(creature[(i+itr)%len(x_middle)]+width[i]/2)*random.random())
				mutation_outward=min(mutation_outward,(width[i]/2-creature[(i+itr)%len(x_middle)])*random.random())
			for itr in range(length):
				if mutation_direction==1:
					creature[(i+itr)%len(x_middle)]=creature[(i+itr)%len(x_middle)]-mutation_inward
				else:
					creature[(i+itr)%len(x_middle)]=creature[(i+itr)%len(x_middle)]+mutation_outward
			for itr in range(int(math.ceil(float(length)/2.0)-1)):
				creature[(i+itr)%len(x_middle)]=(creature[(i+itr-1)%len(x_middle)]+creature[(i+itr+1)%len(x_middle)])/2
				creature[(i+length-itr)%len(x_middle)]=(creature[(i+length-itr-1)%len(x_middle)]+creature[(i+length-itr+1)%len(x_middle)])/2
	return creature

def reproduce(generation,width,strategy):
	max_inward=0;
	max_outward=0;
	length=len(generation)
	new_generation=[]
	for x in range(0,3):
		for i in range(length):
			new_generation.append(copy.deepcopy(generation[i]))
	new_generation.append(copy.deepcopy(generation[i]))
	for x in range(length,3*length+1): #Singular mutations

		"""	if strategy == 1: #Bias aversion, but I think there should be a better solution
			for i in  range(len(new_generation[x])):
				if random.random() < 0.08:
					mutation = True
				else:
					mutation = False
				if mutation == True:
					mutation_direction=random.randint(1,2) #1 is inward 2 is outward 
					mutation_inward=(new_generation[x][i]+width[i]/2)*random.random() #inward means down
					mutation_outward=(width[i]/2-new_generation[x][i])*random.random() #outward means up
					#max_outward=max(mutation_outward,max_outward)
					#max_inward=max(mutation_inward,max_inward)
					if mutation_direction==1:
						if mutation_inward<mutation_outward:
							new_generation[x][i]=new_generation[x][i]-mutation_inward
						else:
							mutation_amount=(mutation_inward+5*mutation_outward)/6
							new_generation[x][i]=new_generation[x][i]-mutation_amount
					else:
						if mutation_outward<mutation_inward:
							new_generation[x][i]=new_generation[x][i]+mutation_outward
						else:
							mutation_amount=(5*mutation_inward+mutation_outward)/6
							new_generation[x][i]=new_generation[x][i]+mutation_amount

			for i in  range(len(new_generation[x])-1):
				if random.random() < 0.02: 
					mutation = True
				else:
					mutation = False
				if mutation == True:
					mutation_direction=random.randint(1,2) #1 is inward 2 is outward 
					mutation_inward=100
					mutation_outward=100
					for itr in range(2):
						mutation_inward=min(mutation_inward,(new_generation[x][i+itr]+width[i]/2)*random.random())
						mutation_outward=min(mutation_outward,(width[i]/2-new_generation[x][i+itr])*random.random())
						#mutation_amount=min(mutation_inward,mutation_outward) #To not create any bias
					for itr in range(2):
						if mutation_direction==1:
							if mutation_inward<mutation_outward:
								new_generation[x][i+itr]=new_generation[x][i+itr]-mutation_inward
							elif mutation_outward<=mutation_inward:
								mutation_amount=(mutation_inward+2*mutation_outward)/3
								new_generation[x][i+itr]=new_generation[x][i+itr]-mutation_amount
		#	elif strategy == 0:
			new_generation[x]=length_mutation(new_generation[x],1,width)
			new_generation[x]=length_mutation(new_generation[x],2,width)
		"""
		#new_generation[x]=length_mutation(new_generation[x],4,width)
		if strategy == 1:
			new_generation[x]=length_mutation(new_generation[x],8,width,strategy)
		new_generation[x]=length_mutation(new_generation[x],16,width,strategy)
		new_generation[x]=length_mutation(new_generation[x],32,width,strategy)
		new_generation[x]=length_mutation(new_generation[x],64,width,strategy)
		if strategy == 0:
			new_generation[x]=length_mutation(new_generation[x],128,width,strategy)

	return new_generation
"""
def draw(width,creature):
	global x_middle, y_middle
	x_creature=[]
	y_creature=[]
	x_lower=[]
	y_lower=[]
	x_upper=[]
	y_upper=[]
	normal_angle=[]
	try: 
		normal_angle.append(math.pi/2-math.atan((y_middle[1]-y_middle[len(y_middle)-1])/(x_middle[1]-x_middle[len(x_middle)-1])))
	except:
		normal_angle.append(0)
	for i in range(1,len(x_middle)-1):
		try:
			normal_angle.append(math.pi/2-math.atan((y_middle[i+1]-y_middle[i-1])/(x_middle[i+1]-x_middle[i-1])))
		except:
			normal_angle.append(0)
	try: 
		normal_angle.append(math.pi/2-math.atan((y_middle[0]-y_middle[len(y_middle)-2])/(x_middle[0]-x_middle[len(x_middle)-2])))
	except:
		normal_angle.append(0)
	#print "The Maximum normal_angle is: ", max(normal_angle)
	#print "The Minimum normal_angle is: ", min(normal_angle)
	for i in range(len(normal_angle)):
		x_lower.append(x_middle[i]-abs(width[i]/2*math.cos(normal_angle[i])))
		y_lower.append(y_middle[i]+abs(width[i]/2*math.sin(normal_angle[i])))
		x_upper.append(x_middle[i]+abs(width[i]/2*math.cos(normal_angle[i])))
		y_upper.append(y_middle[i]-abs(width[i]/2*math.sin(normal_angle[i])))
		x_creature.append(x_middle[i]-creature[i]*math.cos(normal_angle[i]))
		y_creature.append(y_middle[i]+creature[i]*math.sin(normal_angle[i]))
	print "Gonna Plot"
	normal_plot_x=[]
	normal_plot_y=[]
	for i in range(len(normal_angle)):
		if i%2==0:
			for itr in range(10):
				normal_plot_x.append(x_middle[i]-(-5.0+float(itr))/5.0*width[i]/2*math.cos(normal_angle[i]))
				normal_plot_y.append(y_middle[i]+(-5.0+float(itr))/5.0*width[i]/2*math.sin(normal_angle[i]))


	plt.plot(x_creature,y_creature,'ro',x_lower,y_lower,'g^',x_upper,y_upper,'g^',x_middle,y_middle,'x',normal_plot_x,normal_plot_y,'r.')
	plt.show()
	print "Plot should have appeared"
"""

with open('track_coordinates.csv','rb') as csvfile:
	x_middle, y_middle
	track_reader=csv.reader(csvfile)
	for row in track_reader:
		try:
			x_middle.append(float(row[0]))
			y_middle.append(float(row[1]))
		except:
			pass	

zero_creature=[]
for itr in range(len(x_middle)):
		zero_creature.append(0)
width = [10]*len(x_middle)
zero_fitness=fitness_calculator(zero_creature)
print "Fitness of zero_creature: ",zero_fitness
creatures_number = 50
print "The number of creatures per generation is: ",creatures_number
first_generation=random_generation(width,creatures_number)
next_generation=first_generation
next_generation[0]=zero_creature;
gen_count=1;
#for x in range(len(random_generation(9,10,100))):
#	print x
proceed='Y'
print "Alright, let us commence with the creation of life and its evolution!"
print "The evolution will continue indefinetely"
breakthrough = 3.6
while True:
	generation = next_generation
	ordered_generation = order(generation)
	best_fitness = fitness_calculator(ordered_generation[0])
	print 'Current generation is: ', gen_count
	print 'Current best (zero_creature) fitness is: ',best_fitness
	print 'Current best non-zero_creature fitness is: ',fitness_calculator(ordered_generation[1])
	modal_fitness = fitness_calculator(ordered_generation[creatures_number/2])
	print 'Current modal creature fitness is: ',modal_fitness,'\n'
	#print 'Average radius of best creature is: ', numpy.mean(ordered_generation[0])
	#print 'Current modal fitness is: ', fitness_calculator(50)
	purged_generation=purge(ordered_generation)
	if modal_fitness>3.1:
		strategy=0
	else:
		print "Entering strategy!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		strategy=1
	next_generation=reproduce(purged_generation,width,strategy)
	gen_count+=1

	if best_fitness < breakthrough:
		breakthrough -=0.05
		fileName="fitness"+str(best_fitness)+".p"
		pickle.dump(next_generation, open(fileName,"wb"))


print 'Done evolving, plotting best figure:'
creature=next_generation[0]
draw(width,creature)