#to schedule in bound flights. 
#You will be provided a list of flights with their arrival times 
#and you will need to determine their landing times based on runway availability. 
#In order to land each flight will need to reserve the runway for a fixed amount of time in order to safely land and taxi off the runway.
# If a flight is scheduled to arrive at the airport whilst the runway is occupied 
# it will have to wait for the runway to be cleared before it can land.
import json
class Flight(object):
    def __init__(self,planeid,time,distress=None):
        self.planeID=planeid
        self.time=time
        self.distress=distress
        self.dictionaryForm={"PlaneID":self.planeID,"Time":self.time}#here time and planeID pass by value
        self.runway=None
    def __lt__(self,other):
        S=int(self.time)
        O=int(other.time)
        SinMinutes=int(S/100)*60+S%100
        OinMinutes=int(O/100)*60+S%100
        if self.distress==None and other.distress==None:
            if SinMinutes==OinMinutes:
                return(self.planeID<other.planeID)
            else:
                return SinMinutes<OinMinutes
        elif self.distress=="true" and other.distress==None:
            return True
        else:
            return False
    def toDictionaryForm(self):
        return {"PlaneID":self.planeID,"Time":self.time, "Runway":self.runway}


def main():
    #part 1
    with open("sampleAirTrafficControl1.json") as json_file:
        data=json.load(json_file)
    #print(data)
    flights=data["Flights"] # a list of dictionaries
    static=data["Static"]
    reserveTime=int(static["ReserveTime"]) #in seconds
    reserveTimeMinutes=reserveTime/60

    #FLights schedule
    FlightsList=list()
    for fl in flights:
        ID=fl["PlaneId"]
        T=fl["Time"]
        FlightsList.append(Flight(ID,T))
    FlightsList.sort()
    # print results
    res={"Flight":list()}
    for sortedFlight in FlightsList:
        res["Flight"].append(sortedFlight.dictionaryForm)
    json_res1=json.dumps(res)
   # print(json_res1)

    #part 2---------------------------------------------------
    with open("sampleAirTrafficControl2.json") as json_file:
        data=json.load(json_file)
    print(data)
    flights=data["Flights"] # a list of dictionaries
    static=data["Static"]
    reserveTime=int(static["ReserveTime"]) #in seconds
    runways=static["Runways"]# a list of letters
    reserveTimeMinutes=reserveTime/60
    #schedule FLights
    FlightsList=list()
    for fl in flights:
        ID=fl["PlaneId"]
        T=fl["Time"]
        FlightsList.append(Flight(ID,T))
    FlightsList.sort()
    #arrange runways
    runwayrecord=dict()
    for rw in runways:
        runwayrecord[rw]=list()
    #for each flight
    for f in FlightsList:
      
        #for each runway

        for k in runwayrecord:    
         
            #if runway is  not occupied
            if runwayrecord[k]==list():

                #ask the flight to occupy it
                f.runway=k
              
                runwayrecord[k].append(f)
                
                break
                
            # if runway is occupied
            else:
                # retrieve the last one in the queue and record its departure time
                previousFlightTime=int((runwayrecord[k][-1].time))
                # record my current departure time
                currentFlightTime=int(f.time)
                # check if can fit
         
                if (int(currentFlightTime/100)*60+currentFlightTime%100)-(int(previousFlightTime/100)*60+previousFlightTime%100)>=reserveTimeMinutes:
                    f.runway=k
                    runwayrecord[k].append(f)
                    
                    break
                    
                else:
                    continue

    # print results
    res={"Flight":list()}
    for sortedFlight in FlightsList:
        updatedDict=sortedFlight.dictionaryForm
        updatedDict["Runway"]=sortedFlight.runway
        res["Flight"].append(updatedDict)
    json_res2=json.dumps(res)
    print("printting result2")
    print(json_res2)

    #part 3-------------------------------------------
   
    with open("sampleAirTrafficControl3.json") as json_file:
        data=json.load(json_file)
    print(data)
    flights=data["Flights"] # a list of dictionaries
    static=data["Static"]
    reserveTime=int(static["ReserveTime"]) #in seconds
    runways=static["Runways"]# a list of letters
    reserveTimeMinutes=reserveTime/60
    #schedule FLights
    FlightsList=list()
    for fl in flights:
        ID=fl["PlaneId"]
        T=fl["Time"]
        if len(fl)>2:
            D=fl["Distressed"]
            FlightsList.append(Flight(ID,T,D))
        else:
            FlightsList.append(Flight(ID,T))
    FlightsList.sort()

    #arrange runways
    runwayrecord=dict()
    for rw in runways:
        runwayrecord[rw]=list()

    #for each flight
    for f in FlightsList:
        #for each runway
        for k in runwayrecord:     
            #if runway is  not occupied
            if runwayrecord[k]==list():
                #ask the flight to occupy it
                f.runway=k
                runwayrecord[k].append(f)
                break
            # if runway is occupied
            else:
                # retrieve the last one in the queue and record its departure time
                previousFlightTime=int((runwayrecord[k][-1].time))
                # record my current departure time
                currentFlightTime=int(f.time)
                # check if can fit
                if (int(currentFlightTime/100)*60+currentFlightTime%100)-(int(previousFlightTime/100)*60+previousFlightTime%100)>=reserveTimeMinutes:
                    f.runway=k
                    runwayrecord[k].append(f)
                    break
                # if cannot fit, check if there is another runwayavailble
                else:
                    continue
        #if f is not getting a queue in any runway, then need to reschedule it and queue to one runway
        if f.runway==None:
            #need to reschedule

            #f.time=min(previouTime+10mins for all runways)
            minPT=1000000000000
            runwaytoschedule=None
            for k in runwayrecord:
                # retrieve the last one in the queue and record its departure time
                previousFlightTime=int((runwayrecord[k][-1].time))
                previousFlightTimeinMinutes=int(previousFlightTime/100)*60+previousFlightTime%100
                if previousFlightTimeinMinutes<minPT:
                    minPT=previousFlightTimeinMinutes
                    runwaytoschedule=k
                else:
                    pass
            currentRescheduleTimeInMinutes=previousFlightTimeinMinutes+reserveTimeMinutes
            currentTime=int(currentRescheduleTimeInMinutes/60)*100+currentRescheduleTimeInMinutes%60
            f.time="{0:0>4d}".format(int(currentTime))
            f.runway=runwaytoschedule
            runwayrecord[runwaytoschedule].append(f)
            #print(f.time,f.planeID)
        else:
            pass
    # print results
    res={"Flight":list()}
    for sortedFlight in FlightsList:
        #print(sortedFlight.time,sortedFlight.planeID)
        updatedDict=sortedFlight.toDictionaryForm()
        #print(updatedDict)
        res["Flight"].append(updatedDict)
    json_res3=json.dumps(res)
    print("printting result3")
    print(json_res3)
if __name__=="__main__":
    main()