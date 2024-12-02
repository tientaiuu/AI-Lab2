import os

def readInput(fileName):
    f = open(fileName, 'r') 
    KB= f.readlines()
    for i in range(len(KB)):
        KB[i] = KB[i].replace(" ", '').replace('\n', '').split('OR')
   
    alpha = KB[0]
    n = KB[1]
    KB.pop(0)
    KB.pop(0)
        
    f.close()
    return alpha, n, KB

def writeOutput(data, result, fileName):
    f = open(fileName, 'w') 
    
    for i in range(len(data)):
        f.write(str(len(data[i])) + "\n")
        for j in range(len(data[i])):
            if(data[i][j] == []): continue
            f.write(" OR ".join(map(str,data[i][j] )))
            f.write("\n")
            
    if([] in data[i]):f.write("{}\n") 
    f.write("YES") if result else f.write("NO")
    f.close()
    return True

def PLResolution(KB, alpha):
    clauses = KB
    clauses= connect(clauses,negativeClause(alpha))
    new = []
    output = []
    pairs = []
    while True:
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                pairs.append([clauses[i], clauses[j]]) 
        loop = []
        for (ci, cj) in pairs:
            if isResolvable(ci, cj):
                resolvents = PLResolve(ci, cj)
                for i in resolvents:
                    if i not in new and i not in clauses:
                        new.append(i)
                        loop.append(i)
        output.append(loop)
        new = [list(x) for x in set(tuple(x) for x in new)]
        if isInside(new, clauses):
            return False, output
        for i in new:
            if not i in clauses:
                clauses.append(i)
        if [] in clauses:
            return True, output

def PLResolve(c1, c2):
    resolvents =[]

    for i in c1:
        for j in c2:
            if i == negativeLiteral(j) or negativeLiteral(i) == j:
                nC2 = c2.copy()
                nC1 = c1.copy()
                nC1.remove(i)
                nC2.remove(j)
                final_list = list(set(nC1) | set(nC2))
                clause = final_list
                if(hasTautology(clause)): continue
                sort(clause)
                resolvents.append(clause)
    return resolvents

def isResolvable(c1, c2):
    for i in c1:
        for j in c2:
            if i == negativeLiteral(j) or negativeLiteral(i) == j:
                return True
    return False

def negativeLiteral(l):
    if l.find('-') != -1:
        l = l.replace('-', '')
    else:
        l = '-' + l
    return l

def negativeClause(c):
    t = []
    for i in range(len(c)):
        if c[i].find('-') != -1:
            c[i] = c[i].replace('-', '')
        else:
            c[i] = '-' + c[i]
        t.append(c[i])
    return t

def connect(c1,c2):
    for i in range(len(c2)):
        c1.append([c2[i]])
    return c1
  
def hasTautology(c):
    if len(c) <= 1:
        return False
    else:
        for i in c:
            if negativeLiteral(i) in c:
                return True
    return False

def isInside(c1, c2):
    if len(c2) < len(c1): return False
    check = True
    for i in c1:
        check = False
        for j in c2:
            if i == j:
                check = True
                break
        if not check: return False
    return True

def myKey(e): 
    return e[-1]
def sort(c):
    return c.sort(key = myKey) 

if __name__ == '__main__':
    base_folder = 'PS5'
    input_folder = os.path.join(base_folder, 'input')
    output_folder = os.path.join(base_folder, 'output')
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i in range(1, 6):
        input_file = os.path.join(input_folder, f'input{i}.txt')
        output_file = os.path.join(output_folder, f'output{i}.txt')
        alpha, n, KB = readInput(input_file)
        c,output =PLResolution(KB,alpha)
        writeOutput( output,c, output_file)
        print(f"Processed input{i}.txt and generated output{i}.txt")
