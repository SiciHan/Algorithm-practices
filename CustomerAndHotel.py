#Part1:
    #What is the minimum distance that any person has to move in order to meet any other person on the island?
#Sample Input                    
#    [4, 7, 5, 1, 12, 13, 9, 2, 6, 3, 21]   
#Sample Output
#    {
#       "answer":1
#    }

# assuming the list of integer input will be given, as inputList
import numpy as np
import json
def MinimumDistance(inputList):
    '''
    for part 1
    '''
    #once we get the integer list,
    # we need to arrange them into ascending order
    inputList.sort()
    anotherList1=inputList[0:-1]
    anotherList2=inputList[1:]
    differenceList=np.array(anotherList2)-np.array(anotherList1)
    #print(differenceList)
    return {"answer":np.min(differenceList)}
#Par2:
#What will be optimum number of relief camps that can be placed on the island so that each customer can walk to the camp given the walking range of each customer?
#or maybe it is union-find
#Develop a RESTful API /customers-and-hotel/minimum-camps that takes in a list of the position of the customer and the distance the customer can walk in left or right direction and returns a number in String format which indicates the minimum number of camps required to be built by the hotel.
class Customer(object):
    def __init__(self,customerInDict):
        self.pos=customerInDict["pos"]
        self.distance=customerInDict["distance"]
        self.reachableRange=set()
        for i in range(self.pos-self.distance,self.pos+self.distance+1,1):
            self.reachableRange.add(i)
        self.station= Station()
        self.station.listOfCustomers.append(self)
        self.station.locationrange=self.reachableRange # make sure that the station is always reachable by customer.

class Station(object):
    def __init__(self):
        self.locationrange=set()
        self.listOfCustomers=list()
    
def MinimumCamp(inputList):
    '''
    input is a list of dictionaries:
    pos：4
    distance:3
    for each dict
    '''
    listOfStations=[]
    #convert the input into list of customers
    listOfCustomers=[]
    for person in inputList:
        listOfCustomers.append(Customer(person))
        listOfStations.append(Customer(person).station)
    #The approach is more like a Union-find data structure in this case. 

    # for each customer in the list, we need to compare the current customer to the rest of the customers. 
    # find out the union part the station range  
    k=len(listOfCustomers) #to keep track of no of stations,k
    for i in range(len(listOfCustomers)):
        currentCustomer=listOfCustomers[i]
        #Assuming the resource is unlimited that each customer has a station at his location
        #check if my current station can be reached by any of the remaining
        #if can reached, we share the station
        for remainingCustomer in listOfCustomers[i+1:]:
            if currentCustomer.station==remainingCustomer.station:
                continue
            else:
                range1=currentCustomer.station.locationrange
                range2=remainingCustomer.station.locationrange
                #try to find the common part of two range
                commonrange=range1.intersection(range2)
                #if the two customers from different stations can be grouped together
                if commonrange!=set():
                    k-=1
                    print("current k",k)         
                    remainingCustomer.station=currentCustomer.station#delete a station
                    currentCustomer.station.locationrange=commonrange# update the station
                    currentCustomer.station.listOfCustomers.append(remainingCustomer)#update the station
                    print("the merged station contains",currentCustomer.station.locationrange)
                #if the two customers cannot be grouped together, do nothing
                else:
                    pass
    return k


def main():
    with open("sampleCustomerAndHotelP1.json") as json_file:
        data1= json.load(json_file)# alist
        #print(data)
        #print(type(data))
    MinimumDistance(data1)

    with open("sampleCustomerAndHotelP2.json") as json_file:
        data2= json.load(json_file)# alist of dictionary

    res=MinimumCamp(data2)
    print(res)



if __name__=="__main__":
    main()
