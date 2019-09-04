
import json

class SkillTree(object):
    def __init__(self):#all here are instance variable
        self.skilltree=dict()
        #skilltree stores 
        ##name of skill: Skillobject
        self.nullskill={
        "name": "null",
        "offense": "0",
        "points": "0",
        "require":"null"}
        self.rootskill=Skill(self.nullskill)
        self.addSkill(self.rootskill)

    def addSkill(self,skill):# assuming pass by reference 
        '''
        input:Skill object,skill
        output: add the skill object to corresponding key's value
        '''
        self.skilltree.update({(skill.name):skill})#??
        #case 1: if the skill is the root skill, no need to update its parent's potentialskills
        if skill.require =="null" and skill.name=="null":
            pass
        #case 2: if the skill is the second layer or upper,update the root's potentialskill list(child)
        elif skill.name!="null":
            parentSkillName=skill.require#required skill is a parent skill
            parentSkill=self.skilltree[parentSkillName]# actual Parent Skill
            parentSkillPSList=parentSkill.potentialSkill# Skill's potentialSkill THe problem is HERE! need to copy list values.
            parentSkillPSList.append(skill.name)
            self.skilltree.update({parentSkillName:parentSkill})

        else:
            pass
    def getSkill(self,skillname):
        '''
        retrieve a single skill object based on the name of the skill provided
        '''
        return self.skilltree[skillname]

class Skill(object):
    '''
    this class will represent the blue print of a single skill.
    Attribute of skills:
    string name; 
    int offense;
    int points;
    string require;
    string[] potentialskills;
    '''
    def __init__(self,skilldict):
        # here we assume each skill only have one required skill.
        # most likely, the input is a dictionary that contains the skill details.
        self.name=skilldict["name"]
        self.offense=int(skilldict["offense"])
        self.points=int(skilldict["points"])
        self.potentialSkill=list()
        if skilldict["require"]==None:
            self.require="null"
        else:
            self.require=skilldict["require"]

class Path(object):
    def __init__(self):
        self.skillpath=list()
        self.accumulatedpoints=0
        self.accumulatedoffense=0
        
def DFS(tree:SkillTree,start,bossoffense,path,pathlist):
    '''
    Input: SkillTree, and the root skill (null or start) and bossoffense
    return a path? or return a path array?
    '''
    #add the start point to part of the path
    #global path, pathlist,skilltree
    print("entering DFS")
    #if the current path already exceed 11 which is boss offense
    if path.accumulatedoffense>=bossoffense: 
        #we dont append the current skill to path
        #add the path to pathlist,reset path to empty
        pathlist.append(path)
        path=Path()
        #we stop the recursive method
        return
    #if the current point is an end point in the tree (no children point)
    elif start.potentialSkill[:]==[]:
        #try to add the end point first
        path.skillpath.append(start.name)
        path.accumulatedoffense+=start.offense
        path.accumulatedpoints+=start.points
        if path.accumulatedoffense<bossoffense:
            #that means the current path is a failed path, we need to reset path
            path=Path()
            #continue to the next path
            return
        else:
            pathlist.append(path)
    #if the current point is not an end point
    else:
        #add the current skill to the path
        path.skillpath.append(start.name)
        path.accumulatedoffense+=start.offense
        path.accumulatedpoints+=start.points
        if path.accumulatedoffense>=bossoffense:
            pathlist.append(path)
            path=Path()
            #we stop the recursive method
            return
        else:
            for child in start.potentialSkill:
                DFS(tree,tree.getSkill(child),bossoffense,path,pathlist)

def main():
    print("opening and parsing the file")
    with open("sampleSkills.json") as json_file:
        data=json.load(json_file)
    boss=data["boss"] #a dict
    skills=data["skills"] #a list of dicts
    skilltree=SkillTree()
    for skill in skills:
        newskill=Skill(skill)
        skilltree.addSkill(newskill)
    print("skill tree is constructed")
    #now tree is constructed.
    #we need to set up the algorithms
    root=skilltree.getSkill("null")
    #then we need to perform depth first search 
    print("we are searching")
    pathlist=list()
    path=Path()
    DFS(skilltree,root,boss.offense,path,pathlist)
    print("printing pathlist")
    minpt=100000
    index=10000;
    for p in pathlist:
        pt=p.accumulatedpoints
        if pt<minpt:
            minpt=pt
            index=pathlist.index(p)
    
    res=pathlist[index].skillpath[1:]
    print(res)

if __name__ == "__main__":
    main()