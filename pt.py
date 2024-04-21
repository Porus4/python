def func(nt,prodns,act):
    new_gram=dict()
    nt_dash=nt+"'"
    a=[]
    for prod in prodns:
        prod1=prod.split(" ")
        if prod[0] != nt:
            a_dash=prod+" "+nt_dash
            a.append(a_dash)
    alpha=act.split(" ")[1:]
    alpha1=alpha[0]
    for i in range(1,len(alpha)):
        alpha1=alpha1+" "+alpha[i]
    new_gram[nt]=a
    new_gram[nt_dash]=['ε',alpha1+" "+nt_dash]
    return new_gram
def remove_left_recur(gram):
    new_gram=dict()
    for nt in gram:
        prodns=gram[nt]
        for i,prod in enumerate(prodns):
            prod1=prod.split(" ")
            if prod1[0]==nt:
                a=prodns[::]
                b=a.pop(i)
                nu_gram=func(nt,a,b)
                for i in nu_gram:
                    if i not in new_gram:
                        new_gram[i] = nu_gram[i]
                    if new_gram[i]!=nu_gram[i]:
                        for j in nu_gram[i]:
                            if j not in new_gram[i]:
                                new_gram[i].append(j)
    for i in gram:
        if i not in new_gram:
            new_gram[i]=gram[i]
    return new_gram;
def comp_first(gram,var):
    prods=gram[var]
    first=[]
    for prod in prods:
        prod1=prod.split(" ")
        if not prod1[0].isupper() :
            first.append(prod1[0])
        else:
            i,flag=0,0
            while i<len(prod1)-1:
                if not prod1[i].isupper():
                    first.append(prod1[i])
                    break;
                else:
                    a=comp_first(gram,prod1[i])
                    if 'ε' in a:
                        first.extend(a)
                        first.remove('ε')
                    else:
                        first.extend(a)
                        flag=1
                        break;
                   
                i+=1
            if not flag:
                if not prod1[-1].isupper():
                    first.append(prod1[-1])
                else:
                    first.extend(comp_first(gram,prod1[-1]))
    return first;
def first_rhs(gram,var):
    first=[]
    if var:
        print(var[0])
        if not var[0].isupper():
            first.append(var[0])
            return first
        i,flag=0,0
        while i<len(var)-1:
            if not var[i].isupper():
                first.append(var[i])
                break;
            else:
                a=first_rhs(gram,var[i])
                if 'ε' in a:
                    first.extend(a)
                    first.remove('ε')
                else:
                    first.extend(a)
                    flag=1
                    break;
            i+=1
        if not flag:
            if not var[-1].isupper():
                first.append(var[-1])
            else:
                first.extend(first_rhs(gram,var[-1]))
    else:
        return None
    return  first
glob_fol={}    
def comp_follow(gram,var,st):
    follow=set()
    if var in glob_fol:
        return glob_fol[var]
    else:    
        if st==var:
            glob_fol[var]=['$']
        for nt in gram:
            for prod in gram[nt]:
                prod1=prod.split(" ")
                if var in prod1:
                    a=prod1.index(var)+1
                    if a==len(prod1):
                        return None
                    print(var,nt,prod1)
                    print(a)
                    se=first_rhs(gram,prod1[a:])
                    if se:
                        if 'ε' in se:
                            se.remove('ε')
                            if var in glob_fol:
                                lis=set(glob_fol[var]+se)
                                glob_fol[var]=list(lis)
                                lis1=list(set(glob_fol[var]+comp_follow(gram,nt,st)))
                                glob_fol[var]=list(set(glob_fol[var]+lis1))
                            else:
                                lis=set(se)
                                glob_fol[var]=list(lis)
                                lis1=list(set(glob_fol[var]+comp_follow(gram,nt,st)))
                                glob_fol[var]=list(set(glob_fol[var]+lis1))
                        else:
                            if var in glob_fol:
                                glob_fol[var]=list(set(glob_fol[var]+se))
                            else:
                                glob_fol[var]=list(set(se))
                    else: 
                        if var in glob_fol:
                            se=comp_follow(gram,nt,st)
                            glob_fol[var]=list(set(glob_fol[var]+se))
                        else:
                            glob_fol[var]=list(set(se))                
    return glob_fol[var]

if __name__=='__main__':
    gram={'E':['E + T','T'],'T':['T * F','F'],'F':['( E )','id']}
    #gram = {'S':['Sa','Sb','c','d']}
    #gram={'S':'aBC'}
    new_gram=remove_left_recur(gram)
    print(new_gram)
    first={}
    follow={}
    st='E'
    for nt in new_gram:
        a=comp_first(new_gram,nt)
        if len(a) == 1:
            first[nt]=[a]
        else:
            first[nt]=a
    for nt in new_gram:
        print(nt)
        a=comp_follow(new_gram,nt,st)
        if a:
            if len(a) == 1:
                follow[nt]=[a]
            else:
                follow[nt]=a
        print(follow[nt])    
    print("Firsts")
    for i in first:
        print(f'{i}:{first[i]}')
    print("\nFollows")
    for i in follow:
        print(f'{i}:{follow[i]}')