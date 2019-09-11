from itertools import combinations
import json

def main():
    #read json
    with open("sampleTwoDinasour.json") as jf:
        data=json.load(jf)
    N=data["number_of_types_of_food"]
    A=data["calories_for_each_type_for_raphael"]
    B=data["calories_for_each_type_for_leonardo"]
    Q=data["maximum_difference_for_calories"]
    
    print(A,B,N,Q)
    #Create two lists 
    ATotalCalList=list()# reach value represents the total calories of each combination
    BTotalCalList=list()
    for i in range(N+1):
        ACom=combinations(A,i)
        for c in list(ACom):
            ATotalCalList.append(sum(c))

    for j in range(N+1):
        BCom=combinations(B,j)
        for c in list(BCom):
            BTotalCalList.append(sum(c))
    
    #sort two lists
    ATotalCalList.sort()
    BTotalCalList.sort()
    print(ATotalCalList,BTotalCalList)
    #start 2 sum problem
    countSuccessCase=0
    for a in ATotalCalList:
        for b in BTotalCalList:
            if abs(a-b)<=Q:
                countSuccessCase+=1
            elif b-a>Q:
                break
            else:
                pass

    res=countSuccessCase
    print(res)

if __name__=="__main__":
    main()