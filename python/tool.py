#工程测量闭合导线计算验算器
#Wirte by 栀瑾鱼(Zheng Wanyu)
# ********************************************************

import math
#输入数据
def inputdata():
    data=input("请输入所有观测角，各角度用英文逗号相隔，角度值用空格相隔").split(",")
    data2=input("输入坐标方位角")
    data3=input("边长").split(",")
    data4=input("x,y的已知坐标").split(",")
    return data,data2,data3,data4

def inputlongdata():
    data="34.006,39.829,71.180,39.083,37.666,69.724".split(",")
    return data


#转秒
def AngleToNum(a):
    a=a.split(" ")
    num=0
    for i in range(len(a)):
        num=int(a[i])*pow(60,2-i)+num
    return num

#转度分秒
def NumToAngle(num):
    list=[]
    if num<0:
        num=1296000+num
    if num>=1296000:
        num=num%1296000
    for i in range(3):
        if i <=1:
            list.append(num%60)
        else:
            list.append(num)
        num=num//60
    strlist=str(list[2]) + " " + str(list[1]) + " " + str(list[0])
    return strlist
#转度
def Anglefloat(a):
    a=a.split(" ")
    num=0
    for i in range(len(a)):
        num=int(a[i])/pow(60,i)+num
    return num

#判断角度闭合差是否符合要求
def JudegeAngleError(list):
    sumdata=0
    for i in list:
        sumdata=AngleToNum(i)+sumdata
    Value=((len(list)-2)*180*60*60)-sumdata
    if abs(Value)<=58:
        return True ,Value
    else:
        print("误差不符合要求")
        return False,Value

#角度改正数
def AngleChangedata(data):
    dataNum=[]
    ChangeNum=[]
    for i in range(len(data)):
        dataNum.append(AngleToNum(data[i]))
    if JudegeAngleError(data)[0]==True:
        a=JudegeAngleError(data)[1]//len(data)
        b=JudegeAngleError(data)[1]%len(data)
        for i in range(len(data)):
            ChangeNum.append(a)
        for i in range(abs(int(b))):
            if JudegeAngleError(data)[1]>=0:
                ChangeNum[dataNum.index(max(dataNum))]+=1
            else:
                ChangeNum[dataNum.index(max(dataNum))]-=1
            dataNum[dataNum.index(max(dataNum))]=0
    return ChangeNum

# 改正后的角值
def ChangeAngle(list1,list2):
    list=[]
    for i in range(len(list1)):
        list.append(NumToAngle(AngleToNum(list1[i])+list2[i]))
    return list

# 坐标方位角
def DirectionsAngle(num,list):
    list1=[num]
    mark=AngleToNum(num)
    for i in list:
        mark=AngleToNum(i)-180*60*60+mark
        list1.append(NumToAngle(mark))
    list1.pop()
    return(list1)
        
#Dx and Dy
def dx(list1,list2):
    list=[]
    for i in range(len(list2)):
        list.append('{:.3f}'.format(math.cos(math.radians(Anglefloat(list1[i])))*float(list2[i])))
    return list

def dy(list1,list2):
    list=[]
    for i in range(len(list2)):
        list.append('{:.3f}'.format(math.sin(math.radians(Anglefloat(list1[i])))*float(list2[i])))
    return list
#dx dy判断是否符合要求
def JudgeD(list1,list2,list3):
    sum1=0
    sum2=0
    sum3=0
    for i in range(len(list1)):
        sum1+=eval(list1[i])
        sum2+=eval(list2[i])
        sum3+=eval(list3[i])
    k=pow(pow(sum2,2)+pow(sum3,2),0.5)/sum1
    if k<=1/6000:
        return True,sum1,round(sum2,3),round(sum3,3)
    else:
        return False
#dx dy改正数
def changedx(list1,list2,list3):
    Judge=JudgeD(list1,list2,list3)
    list1=list(map(float,list1))
    listChange1=[]
    b=0
    if Judge[0]:
        if Judge[1]==0:
            listChange1=[0]*len(list1)
        else:
            for i in range(len(list1)):
                a=round(list1[i]/Judge[1]*Judge[2]*(-1),3)
                listChange1.append(a)
                b+=a
            if abs(b)!=abs(Judge[2]):
                if b>0:
                    listChange1[list1.index(max(list1))]=listChange1[list1.index(max(list1))]-(abs(b)-abs(Judge[2]))
                else:
                    listChange1[list1.index(max(list1))]=listChange1[list1.index(max(list1))]+(abs(b)-abs(Judge[2]))
    return listChange1

def changedy(list1,list2,list3):
    Judge=JudgeD(list1,list2,list3)
    list1=list(map(float,list1))
    listChange1=[]
    b=0
    if Judge[0]:
        if Judge[2]==0:
            listChange1=[0]*len(list1)
        else:
            for i in range(len(list1)):
                a=round(list1[i]/Judge[1]*Judge[3]*(-1),3)
                listChange1.append(a)
                b+=a
            if b!=abs(Judge[3]):
                if b>0:
                    listChange1[list1.index(max(list1))]=listChange1[list1.index(max(list1))]-(abs(b)-abs(Judge[3]))
                else:
                    listChange1[list1.index(max(list1))]=listChange1[list1.index(max(list1))]+(abs(b)-abs(Judge[3]))
    return listChange1

# 改正后的dx,dy
def truedd(list1,list2):
    list3=[]
    for i in range(len(list1)):
        list3.append(round(eval(list1[i])+list2[i],3))
    return list3

# 坐标
def zuobiao(list1,list2,listinput):
    list3=[]
    list4=[]
    a=eval(listinput[0])
    b=eval(listinput[1])
    for i in range(len(list1)):
        a+=list1[i]
        b+=list2[i]
        list3.append(round(a,3))
        list4.append(round(b,3))
    return list3,list4
    



excel=[["观测角","改正数","改正后的角度","坐标方位角","边长(m)","得塔X/m","得塔Y/m","x改正数","y改正数","x改","y改","x","y"]]
data=inputdata()
excel.append(data[0])
excel.append(AngleChangedata(data[0]))
excel.append(ChangeAngle(excel[1],excel[2]))
excel.append(DirectionsAngle(data[1],excel[3]))
excel.append(data[2])
excel.append(dx(excel[4],excel[5]))
excel.append(dy(excel[4],excel[5]))
excel.append(changedx(excel[5],excel[6],excel[7]))
excel.append(changedy(excel[5],excel[6],excel[7]))
excel.append(truedd(excel[6],excel[8]))
excel.append(truedd(excel[7],excel[9]))

zuobiaozhi=zuobiao(excel[10],excel[11],data[3])
excel.append(zuobiaozhi[0])
excel.append(zuobiaozhi[1])

for i in excel[0]:
      print("{:^9}".format(i),end="")
print("\n",end="")
for i in range(len(excel[1])):
    for j in range(1,len(excel)):
            print("{:^12}".format(excel[j][i]),end="")
    print("\n",end="")