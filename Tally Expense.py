import json
with open('sample.json') as json_file: # or json_file=open('sample.json')
    data = json.load(json_file) #type of data is dictionary

# check number of people here
person=data["persons"]
numberOfPeople=len(person)

#print(numberOfPeople)

# create two lists: actual payment and shouldpaid
actualPaid=[0]*numberOfPeople
shouldpaid=[0]*numberOfPeople

#need to read the expenses one by one

listofExpenses=data["expenses"]
for expense in listofExpenses:
    
    # find the actual person who paid
    nameOfPerson=expense["paidBy"]
    #check the index of that person
    index=person.index(nameOfPerson)
    #add the amount that the person paid to the index
    actualPaid[index]+=expense["amount"]
    #print(actualPaid)
    #check if there is an exclude key, if no, raise an error
    try:
        listOfExclusion=expense["exclude"]
        numberOfPeopleToShare=numberOfPeople-len(listOfExclusion)
        for name in person:
            if name not in listOfExclusion:
                shouldpaid[person.index(name)]+=expense["amount"]/numberOfPeopleToShare
    except Exception as e:
        for name in person:
            shouldpaid[person.index(name)]+=expense["amount"]/numberOfPeople

#output list
transaction=list()

# create two dictionaries e.g. Alice:85 means alice should contribute 85
shouldContribute={}
shouldReceive={}

for i in range(numberOfPeople):
    if actualPaid[i]>shouldpaid[i]:
        shouldReceive.update({person[i]:actualPaid[i]-shouldpaid[i]})
    elif actualPaid[i]<shouldpaid[i]:
        shouldContribute.update({person[i]:shouldpaid[i]-actualPaid[i]})

#iterate through the two dictionary and update transactions and values. 

for contributor in shouldContribute:
    if shouldContribute[contributor]==0:
        continue
    for receiver in shouldReceive:
        if shouldReceive[receiver]==0:
            continue
        elif shouldContribute[contributor]<=shouldReceive[receiver]:
            temp={'from':contributor,'to':receiver,'amount':shouldContribute[contributor]}
            transaction.append(temp)
            #update receiver and contributor
            shouldReceive[receiver]-=shouldContribute[contributor]
            shouldContribute[contributor]=0

        elif shouldContribute[contributor]>shouldReceive[receiver]:
            temp={'from':contributor,'to':receiver,'amount':shouldReceive[receiver]}
            transaction.append(temp)
            #delete the receiver, update receiver
            shouldContribute[contributor]-=shouldReceive[receiver]
            shouldReceive[receiver]=0

        else:
            pass
       

res={"transactions":transaction}
json_output=json.dumps(res)
print(json_output)

    
