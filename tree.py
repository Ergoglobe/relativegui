with open('pygui.py','r') as file:
    raw = file.readlines()

classes = []
for line in raw:
    if line.startswith('class'):
        classes.append(line.replace(':\n','').replace('class ',''))

sortedclasses = {
    '_master_':[]
}
for clas in classes:
    bracketlocation=(clas.rfind('('),clas.rfind(')'))
    if bracketlocation[1]==bracketlocation[0]+1:
        sortedclasses['_master_'].append(clas.replace('()',''))
    else:
        for value in sortedclasses.values():
            if clas[bracketlocation[0]+1:-1] in value:
                try:
                    sortedclasses[clas[bracketlocation[0]+1:-1]].append(clas[:bracketlocation[0]])
                except:
                    sortedclasses[clas[bracketlocation[0]+1:-1]]=[clas[:bracketlocation[0]]]
                break

def is_objects(key):
    try:
        test = sortedclasses[key]
        return True
    except:
        return False

tree=''
for master in sortedclasses['_master_']:
    tree += master+'\n'
    if is_objects(master):
        branch = []
        searched = []
        
        for object in sortedclasses[master]:
            if is_objects(object):
                branch.append(object)
                temp = []
                while branch != []:
                    test = []
                    if branch[-1] not in searched:
                        tree += '|'+'-'*(len(branch)-1)+branch[-1]+'\n'
                    for dependent in sortedclasses[branch[-1]]:
                        if not is_objects(dependent) and dependent not in searched:
                            tree += '|'+'-'*(len(branch))+dependent+'\n'
                            test.append(False)
                            searched.append(dependent)
                        elif dependent not in searched:
                            temp.append(dependent)
                            test.append(True)
                    if True not in test:
                        searched.append(branch.pop())
                    else:
                        try:
                            searched.append(branch[-1])
                            branch.append(temp.pop())
                        except:
                            print('Empty Temp')
                    searched.append(object)

            else:
                tree += '|'+object+'\n'
                searched.append(object)

with open('classtree.txt','w') as file:
    file.write(tree)