import matplotlib.pyplot as plt


x_value=list(range(1,1001))
y_value=[x**2 for x in x_value]

plt.scatter(x_value,y_value,c=y_value,cmap=plt.cm.Blues)
plt.axis([0,1100,0,1100000])
#plt.title('square number',fontsize=24)
#plt.xlabel('value',fontsize=4)
#plt.ylabel('square of value',fontsize=14)
#plt.tick_params(axis='both',which='major',labelsize=14)
plt.savefig('123.png',bbox_inches='tight')
plt.show()

