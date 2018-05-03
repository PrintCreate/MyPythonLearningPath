def collatz(number):
    if number%2==0:
        print(number//2)
        #return 1
    else:
        print(3*number+1)

while True:
    try:
        a=int(input())
        collatz(a)
    except:
        print('输入整数')
    
  #  if collatz(a)==1:
   #     break
#print('nice job')
