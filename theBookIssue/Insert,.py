def a(list1):
    b=''
    for l in list1:
        if l==list1[-1]:
            b=b+',and '+l
            break
        if b!='':
            b=b+','+l
        else :
            b=b+l
    print (b)

def listtostr(lst):
  return ','.join(lst[:-1]+['and '+lst[-1]])

c=['apples', 'bananas', 'tofu', 'cats']
a(c)
print (listtostr(c))
