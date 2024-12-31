class KMap:
    def __init__(self,bs):
        self.bs=sorted(bs)
        self.ind={}
        self.len=0
        for i in self.bs:
           self.ind[i]=self.len
           self.len+=1
        self.reset()
    def reset(self,val=None):
        self.kmap=[val]*(2**len(self.bs))
    def index(self,vals):
        return sum([2**j for j in range(len(vals)) if vals[j]])
    def access(self,vals):
        return self.kmap[self.index(vals)]
    def Not(self):
        f={False:True,True:False,None:None}
        self.kmap=[f[i] if i!=None else None for i in self.kmap]
    def And(self,km2):
        assert self.bs==km2.bs
        f={(False,False):False,(False,True):False,(False,None):False,(True,False):False,(True,True):True,(True,None):None,(None,False):False,(None,True):None,(None,None):None}
        self.kmap=[f[(self.kmap[i],km2.kmap[i])] for i in range(len(self.kmap))]
    def Or(self,km2):
        assert self.bs==km2.bs
        f={(False,False):False,(False,True):True,(False,None):None,(True,False):True,(True,True):True,(True,None):True,(None,False):None,(None,True):True,(None,None):None}
        self.kmap=[f[(self.kmap[i],km2.kmap[i])] for i in range(len(self.kmap))]
    def Xor(self,km2):
        assert self.bs==km2.bs
        f={(False,False):False,(False,True):True,(False,None):None,(True,False):True,(True,True):False,(True,None):None,(None,False):None,(None,True):None,(None,None):None}
        self.kmap=[f[(self.kmap[i],km2.kmap[i])] for i in range(len(self.kmap))]
    def Nand(self,km2):
        assert self.bs==km2.bs
        self.And(km2)
        self.Not()
    def Nor(self,km2):
        assert self.bs==km2.bs
        self.Or(km2)
        self.Not()
    def Xnor(self,km2):
        assert self.bs==km2.bs
        self.Xor(km2)
        self.Not()
    def Import(self, expr):
        self.reset(False)
        km2=KMap(self.bs)
        if len(expr)==0:
            return
        match expr.split('(')[0].upper():
            case 'NOT':
                self.Import(expr[4:-1])
                self.Not()
            case 'AND':
                self.reset(True)
                b=0
                e=''
                for i in expr[4:-1].split(','):
                    b+=(i.count('('))-i.count(')')
                    e+=i
                    if b==0:
                        km2.Import(e)
                        self.And(km2)
                        e=''
                    else:
                        e+=','
            case 'OR':
                b=0
                e=''
                for i in expr[3:-1].split(','):
                    b+=(i.count('('))-i.count(')')
                    e+=i
                    if b==0:
                        km2.Import(e)
                        self.Or(km2)
                        e=''
                    else:
                        e+=','
            case 'XOR':
                b=0
                e=''
                for i in expr[4:-1].split(','):
                    b+=(i.count('('))-i.count(')')
                    e+=i
                    if b==0:
                        km2.Import(e)
                        self.Xor(km2)
                        e=''
                    else:
                        e+=','
            case 'NAND':
                self.reset(True)
                b=0
                e=''
                for i in expr[5:-1].split(','):
                    b+=(i.count('('))-i.count(')')
                    e+=i
                    if b==0:
                        km2.Import(e)
                        self.And(km2)
                        e=''
                    else:
                        e+=','
                self.Not()
            case 'NOR':
                b=0
                e=''
                for i in expr[4:-1].split(','):
                    b+=(i.count('('))-i.count(')')
                    e+=i
                    if b==0:
                        km2.Import(e)
                        self.Or(km2)
                        e=''
                    else:
                        e+=','
                self.Not()
            case 'XNOR':
                b=0
                e=''
                for i in expr[5:-1].split(','):
                    b+=(i.count('('))-i.count(')')
                    e+=i
                    if b==0:
                        km2.Import(e)
                        self.Xor(km2)
                        e=''
                    else:
                        e+=','
                self.Not()
            case _:
                if expr in self.bs:
                    self.kmap=[(i//(2**self.ind[expr]))%2==1 for i in range(2**len(self.bs))]
    def set(self,vals):
        for i in vals:
            self.kmap[self.index(i)]=vals[i]
    def dCare(self,vals):
        for i in vals:
            self.kmap[self.index(i)]=None
    def minSOP(self):
        mt=set([format(i,'0{}b'.format(len(self.bs))) for i in range(2**len(self.bs)) if self.kmap[i]==True])
        dc=[format(i,'0{}b'.format(len(self.bs))) for i in range(2**len(self.bs)) if self.kmap[i]==None]
        impl=[[set() for i in range(len(self.bs)+1)]]
        cont={}
        pi=set()
        for i in mt:
            impl[0][i.count('1')].add(i)
            cont[i]=set([i])
            pi.add(i)
        for i in dc:
            impl[0][i.count('1')].add(i)
            cont[i]=set()
        f=True
        while f:
            f=False
            nb=[set() for i in range(len(self.bs)+1)]
            for i in range(len(self.bs)):
                for j in impl[-1][i]:
                    for k in impl[-1][i+1]:
                        d=''
                        x=True
                        for ii in range(len(self.bs)):
                            if j[ii]==k[ii]:
                                d+=j[ii]
                            elif x:
                                d+='x'
                                x=False
                            else:
                                x=True
                                break
                        if not(x):
                            f=True
                            s=cont[j].union(cont[k])
##                            print(j,k,d,s)
                            nb[d.count('1')].add(d)
                            cont[d]=s
                            if j in pi:
                                pi.remove(j)
                            if k in pi:
                                pi.remove(k)
                            if len(s)>0:
                                pi.add(d)
            impl.append(nb)
##        print([(p,cont[p]) for p in pi])
        coby = {i:set() for i in mt}
        for p in pi:
            for t in cont[p]:
                coby[t].add(p)
        req=set()
        while len(mt)>0:
            tr=set()
            for i in mt:
                if len(coby[i])==1:
                    tr.add(coby[i].pop())
            if f:
                return req
            if len(tr)==0:
                break
            for i in tr:
                for j in cont[i]:
                    if i in coby[j]:
                        coby[j].remove(i)
                    if j in mt:
                        mt.remove(j)
            req.update(tr)
        if len(mt)>0:
            pet=[set()]
            for i in mt:
                np=[]
                for j in pet:
                    for k in coby[i]:
                        if j.union(set([k])) not in np:
                            np.append(j.union(set([k])))
                pet=np
            req.update(min(pet))
        return("OR("+','.join(["AND("+','.join([self.bs[-1-j] if i[j]=='1' else "NOT("+self.bs[-1-j]+")" for j in range(len(self.bs)) if i[j]!='x'])+")" for i in req])+")")
    def minPOS(self):
        mt=set([format(i,'0{}b'.format(len(self.bs))) for i in range(2**len(self.bs)) if self.kmap[i]==False])
        dc=[format(i,'0{}b'.format(len(self.bs))) for i in range(2**len(self.bs)) if self.kmap[i]==None]
        impl=[[set() for i in range(len(self.bs)+1)]]
        cont={}
        pi=set()
        for i in mt:
            impl[0][i.count('1')].add(i)
            cont[i]=set([i])
            pi.add(i)
        for i in dc:
            impl[0][i.count('1')].add(i)
            cont[i]=set()
        f=True
        while f:
            f=False
            nb=[set() for i in range(len(self.bs)+1)]
            for i in range(len(self.bs)):
                for j in impl[-1][i]:
                    for k in impl[-1][i+1]:
                        d=''
                        x=True
                        for ii in range(len(self.bs)):
                            if j[ii]==k[ii]:
                                d+=j[ii]
                            elif x:
                                d+='x'
                                x=False
                            else:
                                x=True
                                break
                        if not(x):
                            f=True
                            s=cont[j].union(cont[k])
##                            print(j,k,d,s)
                            nb[d.count('1')].add(d)
                            cont[d]=s
                            if j in pi:
                                pi.remove(j)
                            if k in pi:
                                pi.remove(k)
                            if len(s)>0:
                                pi.add(d)
            impl.append(nb)
##        print([(p,cont[p]) for p in pi])
        coby = {i:set() for i in mt}
        for p in pi:
            for t in cont[p]:
                coby[t].add(p)
        req=set()
        while len(mt)>0:
            tr=set()
            for i in mt:
                if len(coby[i])==1:
                    tr.add(coby[i].pop())
            if f:
                return req
            if len(tr)==0:
                break
            for i in tr:
                for j in cont[i]:
                    if i in coby[j]:
                        coby[j].remove(i)
                    if j in mt:
                        mt.remove(j)
            req.update(tr)
        if len(mt)>0:
            pet=[set()]
            for i in mt:
                np=[]
                for j in pet:
                    for k in coby[i]:
                        if j.union(set([k])) not in np:
                            np.append(j.union(set([k])))
                pet=np
            req.update(min(pet))
        return("AND("+','.join(["OR("+','.join([self.bs[-1-j] if i[j]=='0' else "NOT("+self.bs[-1-j]+")" for j in range(len(self.bs)) if i[j]!='x'])+")" for i in req])+")")
    def __str__(self):
        b=len(self.bs)//2
        a=len(self.bs)-b
        v=['']
        for i in range(a):
            v=['0'+i for i in v]+['1'+i for i in v[::-1]]
        h=['']
        for i in range(b):
            h=['0'+i for i in h]+['1'+i for i in h[::-1]]
        s=''.join(self.bs[b:])+'\\'+''.join(self.bs[:b])+'\n'+' '*a+'|'+'|'.join(h)
        for i in v:
            s+='\n'+i+'|'+' '*((b-1)//2)+(' '*(b-1-(b-1)//2)+'|'+' '*((b-1)//2)).join(['X' if self.kmap[int(i[::-1]+j[::-1],2)]==None else str(int(self.kmap[int(i[::-1]+j[::-1],2)]==True)) for j in h])
        return(s)
if __name__=="__main__":
    k=KMap(input("Enter variable names: ").split())
    k.Import(input("Enter boolean expression: ").strip())
    k.dCare([[int(j) for j in i] for i in input("Enter each of the dont cares as binary strings: ").split()])
    print("Your K Map:")
    print(k)
    ms=k.minSOP()
    print("Minimal Sum of Products Form:",ms)
    ks=KMap(k.bs)
    ks.Import(ms)
    print(ks)
    mp=k.minPOS()
    print("Minimal Product of Sums Form:",mp)
    km=KMap(k.bs)
    km.Import(mp)
    print(km)
