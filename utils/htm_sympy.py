#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://blog.csdn.net/chengde6896383/article/details/86738179
from sympy import *
import re,xlrd,time
# 根据变量类型，决定在公式中使用字符串还是数字，比如cos(0)可以自动计算为1，而不是生成"cos(0)"
global glmethod
global glerr_flags
global glfilename

# 把字符串变为SymPy变量
def s(varname):
    return Symbol(varname)

def getSymbol(var):
    if isinstance(var,str):
        s = Symbol(var)
        # print(s)
        # print(type(s))
    else:
        s=var
        # print('not str')
    return s

# 构造6x1零向量
def z61():
    return zeros(6,1)

# 构造零变换矩阵
def zhtm():
    return getHTMByArray(zeros(6,1))

# 获取完整的其次坐标变换矩阵
'''逆欧拉角：Rot(xx,aa)→Rot(yy,bb)→Rot(zz,cc)'''
def getHTM(xx,yy,zz,aa,bb,cc):
    x=getSymbol(xx)
    y=getSymbol(yy)
    z=getSymbol(zz)
    a=getSymbol(aa)
    b=getSymbol(bb)
    c=getSymbol(cc)

    t=Matrix([[cos(b)*cos(c), -sin(c)*cos(b), sin(b), x],
              [sin(a)*sin(b)*cos(c) + sin(c)*cos(a), -sin(a)*sin(b)*sin(c) + cos(a)*cos(c), -sin(a)*cos(b), y],
              [sin(a)*sin(c) - sin(b)*cos(a)*cos(c), sin(a)*cos(c) + sin(b)*sin(c)*cos(a), cos(a)*cos(b), z],
              [0, 0, 0, 1]])

    return t

def getHTMSymbol(x,y,z,a,b,c):
    t=Matrix([[cos(b)*cos(c), -sin(c)*cos(b), sin(b), x],
              [sin(a)*sin(b)*cos(c) + sin(c)*cos(a), -sin(a)*sin(b)*sin(c) + cos(a)*cos(c), -sin(a)*cos(b), y],
              [sin(a)*sin(c) - sin(b)*cos(a)*cos(c), sin(a)*cos(c) + sin(b)*sin(c)*cos(a), cos(a)*cos(b), z],
              [0, 0, 0, 1]])
    return t

# 获取完整的其次坐标变换矩阵
'''欧拉角：Rot(zz,aa)→Rot(yy,bb)→Rot(xx,cc)'''
def getHTMEuler(xx, yy, zz, aa, bb, cc):
    x = getSymbol(xx)
    y = getSymbol(yy)
    z = getSymbol(zz)
    a = getSymbol(aa)
    b = getSymbol(bb)
    c = getSymbol(cc)

    t = Matrix([[cos(b) * cos(c), -sin(c) * cos(b), sin(b), x],
                [sin(a) * sin(b) * cos(c) + sin(c) * cos(a), -sin(a) * sin(b) * sin(c) + cos(a) * cos(c),
                 -sin(a) * cos(b), y],
                [sin(a) * sin(c) - sin(b) * cos(a) * cos(c), sin(a) * cos(c) + sin(b) * sin(c) * cos(a),
                 cos(a) * cos(b), z],
                [0, 0, 0, 1]])

    return t

def getHTMByArray(arr):
    return getHTM(arr[0],arr[1],arr[2],arr[3],arr[4],arr[5])

# 获取其次坐标变换矩阵的逆矩阵
def getInvHTM(T):
    t_r=T[0:3,0:3]
    t_p=T[0:3,3]
    t_r_t=t_r.T
    t_inv=zeros(4,4)
    t_inv[0:3,0:3]=t_r_t
    t_inv[0:3,3]=-t_r_t*t_p
    t_inv[3,3]=1
    return t_inv

# 计算J矩阵：将微分运动矢量，从坐标系n转换到末端坐标系m
# Jze(T):从其次坐标变换矩阵Tnm(4x4)获取其逆向的微分变换矩阵Jmn(6*6)
# 公式参考文档：@2020年2月26日-微分运动笔记+三轴算法验证.docx
def Jze(T):
    # 构造R矩阵
    J=zeros(6,6)
    R=T[0:3,0:3]
    RT=R.T
    # 构造反对称矩阵PX
    px=T[0,3]
    py=T[1,3]
    pz=T[2,3]
    Px=Matrix([
        [0,-pz,py],
        [pz,0,-px],
        [-py,px,0],
    ])
    # 输出J（6x6）零矩阵
    # print(simplify(J))
    # 输出T矩阵的R部分
    # print('[R:]',simplify(R))
    # R矩阵的转置矩阵
    # print('[RT:]',simplify(RT))
    # 输出px,py,pz
    # print('[px: {0} py: {1} pz: {2}]'.format(px,py,pz))
    J[0:3,0:3]=RT
    J[0:3,3:6]=-RT*Px
    J[3:6,3:6]=RT
    # 输出J（6x6）零矩阵
    # print(simplify(J))
    return J

# 获取微分其次坐标变换矩阵 for Chen 论文：中心线为1
def getDelta(vdx,vdy,vdz,vex,vey,vez):
    dx=getSymbol(vdx)
    dy=getSymbol(vdy)
    dz=getSymbol(vdz)
    ex=getSymbol(vex)
    ey=getSymbol(vey)
    ez=getSymbol(vez)

    t=Matrix([
        [1,-(ez),ey,dx],
        [ez,1,-(ex),dy],
        [-(ey),ex,1,dz],
        [0,0,0,1]
        ])
    return t
def getDeltaByArray(arr):
    return  getDelta(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5])

# 在末端坐标系下的微分其次变换矩阵
# 获取微分其次坐标变换矩阵 for Fu(付国强) 论文：中心线为0
def getDeltaforFu(vdx,vdy,vdz,vex,vey,vez):
    dx=getSymbol(vdx)
    dy=getSymbol(vdy)
    dz=getSymbol(vdz)
    ex=getSymbol(vex)
    ey=getSymbol(vey)
    ez=getSymbol(vez)

    t=Matrix([
        [0,-(ez),ey,dx],
        [ez,0,-(ex),dy],
        [-(ey),ex,0,dz],
        [0,0,0,0]
        ])
    return t

def mypprint(varname,var):
    global glmethod
    global glfilename
    print('[==',glfilename,'--',glmethod,'--',varname,'==]')
    pprint(var,wrap_line=False)
    printLatForMathType(var)

def myprint(varname,var,**kwargs):
    print('[=====',varname,'By Origin()=====]')
    pprint(var,wrap_line=False)
    printLatForMathType(var)
    print('\n[=====',varname,'By expand()=====]')
    pprint(expand(var),wrap_line=False)
    printLatForMathType(var)
    try:
        if kwargs['simplify']:
            print('[=====',varname,'By simplify()=====]')
            simvar=simplify(var)
            pprint(simvar,wrap_line=False)
            printLatForMathType(simvar)
    except:
        pass

def srev(s):
    a=list(s)
    a.reverse()
    rs=''.join(a)
    return rs

def totalExpand(s):
    print(s)
    sr=srev(s)
    searchObj=re.findall(r'(\d+\*\*.*?)\*',sr,re.M|re.I) #把字符串反过来，正则匹配**n项
    # 替换"**n"为n次式子连乘
    # print(searchObj)
    for i in searchObj:
        ir=srev(i)
        [ifactor,iorder]=ir.split('**')
        iorder=int(iorder)
        # print(ir)
        # print(ifactor)
        # print(iorder)
        factor_arr=[]
        for j in range(iorder):
            factor_arr.append(ifactor)
        rfactor='*'.join(factor_arr)
        # print(rfactor)
        s=s.replace(ir,rfactor)
    print(s)
    return s

# 输入：表达式string
# 输出：忽略高阶项的表达式。误差项代号：D（运动位移误差)、E（运动角度误差）、A（垂直度误差）
def IgnHighOrder(expr,sname='no sname',isexpand=True):
    # 误差项标志前缀字符
    global glerr_flags
    err_flags=glerr_flags
    print('[%s--高阶简化前-完全展开式]'%sname)
    print('isexpand(是否展开):',isexpand)
    if isexpand:
        print('isexpand(是否展开):',isexpand)
        expr=expand(expr)
    # mypprint('expr',expr)
    # print('-----LaTex for MathTYpe==>')
    # print_latex(expr)
    # s="""Axy*Ayz*DyZ*ExX*EyY - Axy*Ayz*DyZ*ExY*EyX + Axy*Ayz*DzZ*ExX*EzY - Axy*Ayz*DzZ*EyX - Axy*Ayz*ExX*ExZ*EyY*Ztd + Axy*Ayz*ExX*ExZ*EzY*Ytd + Axy*Ayz*ExX*EyY*EzZ*Xtd + Axy*Ayz*ExX*EyY*Ytd - Axy*Ayz*ExX*EyZ*EzY*Xtd + Axy*Ayz*ExX*EzY*Z + Axy*Ayz*ExX*EzY*Ztd + Axy*Ayz*ExY*ExZ*EyX*Ztd - Axy*Ayz*ExY*EyX*EzZ*Xtd - Axy*Ayz*ExY*EyX*Ytd - Axy*Ayz*ExZ*EyX*Ytd + Axy*Ayz*EyX*EyZ*Xtd - Axy*Ayz*EyX*Z - Axy*Ayz*EyX*Ztd - Axy*Azx*DxZ*ExX*EyY + Axy*Azx*DxZ*ExY*EyX + Axy*Azx*DzZ*ExX + Axy*Azx*DzZ*EyX*EzY + Axy*Azx*ExX*ExZ*Ytd - Axy*Azx*ExX*EyY*EyZ*Ztd + Axy*Azx*ExX*EyY*EzZ*Ytd - Axy*Azx*ExX*EyY*Xtd - Axy*Azx*ExX*EyZ*Xtd + Axy*Azx*ExX*Z + Axy*Azx*ExX*Ztd + Axy*Azx*ExY*EyX*EyZ*Ztd - Axy*Azx*ExY*EyX*EzZ*Ytd + Axy*Azx*ExY*EyX*Xtd + Axy*Azx*ExZ*EyX*EzY*Ytd - Axy*Azx*EyX*EyZ*EzY*Xtd + Axy*Azx*EyX*EzY*Z + Axy*Azx*EyX*EzY*Ztd + Axy*DxY*ExX + Axy*DxZ*ExX + Axy*DxZ*EyX*EzY + Axy*DyY*EyX - Axy*DyZ*ExX*EzY + Axy*DyZ*EyX + Axy*DzZ*ExX*EyY - Axy*DzZ*ExY*EyX + Axy*ExX*ExZ*EyY*Ytd + Axy*ExX*ExZ*EzY*Ztd - Axy*ExX*EyY*EyZ*Xtd + Axy*ExX*EyY*Z + Axy*ExX*EyY*Ztd + Axy*ExX*EyZ*Ztd - Axy*ExX*EzY*EzZ*Xtd - Axy*ExX*EzY*Ytd - Axy*ExX*EzZ*Ytd + Axy*ExX*Xtd - Axy*ExY*ExZ*EyX*Ytd + Axy*ExY*EyX*EyZ*Xtd - Axy*ExY*EyX*Z - Axy*ExY*EyX*Ztd - Axy*ExZ*EyX*Ztd + Axy*EyX*EyZ*EzY*Ztd - Axy*EyX*EzY*EzZ*Ytd + Axy*EyX*EzY*Xtd + Axy*EyX*EzZ*Xtd + Axy*EyX*Y + Axy*EyX*Ytd - Ayz*DyZ*ExX*ExY - Ayz*DyZ*EyX*EyY + Ayz*DyZ - Ayz*DzZ*ExX - Ayz*DzZ*ExY - Ayz*DzZ*EyX*EzY + Ayz*ExX*ExY*ExZ*Ztd - Ayz*ExX*ExY*EzZ*Xtd - Ayz*ExX*ExY*Ytd - Ayz*ExX*ExZ*Ytd + Ayz*ExX*EyZ*Xtd - Ayz*ExX*Z - Ayz*ExX*Ztd - Ayz*ExY*ExZ*Ytd + Ayz*ExY*EyZ*Xtd - Ayz*ExY*Z - Ayz*ExY*Ztd + Ayz*ExZ*EyX*EyY*Ztd - Ayz*ExZ*EyX*EzY*Ytd - Ayz*ExZ*Ztd - Ayz*EyX*EyY*EzZ*Xtd - Ayz*EyX*EyY*Ytd + Ayz*EyX*EyZ*EzY*Xtd - Ayz*EyX*EzY*Z - Ayz*EyX*EzY*Ztd + Ayz*EzZ*Xtd + Ayz*Ytd + Azx*DxZ*ExX*ExY + Azx*DxZ*EyX*EyY - Azx*DxZ + Azx*DzZ*ExX*EzY - Azx*DzZ*EyX - Azx*DzZ*EyY + Azx*ExX*ExY*EyZ*Ztd - Azx*ExX*ExY*EzZ*Ytd + Azx*ExX*ExY*Xtd + Azx*ExX*ExZ*EzY*Ytd - Azx*ExX*EyZ*EzY*Xtd + Azx*ExX*EzY*Z + Azx*ExX*EzY*Ztd - Azx*ExZ*EyX*Ytd - Azx*ExZ*EyY*Ytd + Azx*EyX*EyY*EyZ*Ztd - Azx*EyX*EyY*EzZ*Ytd + Azx*EyX*EyY*Xtd + Azx*EyX*EyZ*Xtd - Azx*EyX*Z - Azx*EyX*Ztd + Azx*EyY*EyZ*Xtd - Azx*EyY*Z - Azx*EyY*Ztd - Azx*EyZ*Ztd + Azx*EzZ*Ytd - Azx*Xtd - DxY*EyX + DxZ*ExX*EzY - DxZ*EyX - DxZ*EyY + DyY*ExX + DyZ*ExX + DyZ*ExY + DyZ*EyX*EzY + DzX + DzY - DzZ*ExX*ExY - DzZ*EyX*EyY + DzZ - ExX*ExY*ExZ*Ytd + ExX*ExY*EyZ*Xtd - ExX*ExY*Z - ExX*ExY*Ztd - ExX*ExZ*Ztd + ExX*EyZ*EzY*Ztd - ExX*EzY*EzZ*Ytd + ExX*EzY*Xtd + ExX*EzZ*Xtd + ExX*Y + ExX*Ytd - ExY*ExZ*Ztd + ExY*EzZ*Xtd + ExY*Ytd - ExZ*EyX*EyY*Ytd - ExZ*EyX*EzY*Ztd + ExZ*Ytd + EyX*EyY*EyZ*Xtd - EyX*EyY*Z - EyX*EyY*Ztd - EyX*EyZ*Ztd + EyX*EzY*EzZ*Xtd + EyX*EzY*Ytd + EyX*EzZ*Ytd - EyX*Xtd - EyY*EyZ*Ztd + EyY*EzZ*Ytd - EyY*Xtd - EyZ*Xtd"""
    mypprint('befor str(expr):',expr)
    s=str(expr)
    print('after str(expr):',s)
    arr_p=[]

    # 识别"+"、"-"符号在字符串中的位置，方便分成单个因式
    for i,val in enumerate(s):
        if val=='+' or val=='-':
            arr_p.append(i)
            print(i,val)
    arr_p.append(len(s))

    # 如果第一位没有符号，那么就在数组头部补充一个0
    if arr_p[0] != 0:
        arr_p.insert(0,0)

    res=''
    for i in range(len(arr_p)-1):
        seg=s[int(arr_p[i]):int(arr_p[i+1])]
        seg1=totalExpand(seg) #完全展开：“针对有的**2，**3的高次项”
        # print('开始处理seg:', seg)
        ct=0

        # 新的算法：用“*”分隔
        factors=seg1.split('*')
        for f in factors:
            for err_flag in err_flags:
                if err_flag in f:
                    ct=ct+1

        if ct<2:
            print('采用seg:',seg)
            res=res+seg
    if len(res)==0:#如果啥也没有，就返回0
        res='0'
    print('[%s--高阶简化后]'%sname)
    print(res)
    return str(res)

# 微分运动学建模验证（测量机验证AFZXY）：成功！
def getErrorsof_FZXYZ_byMethod(method='F'):
    vars="""x y z alpha x_s y_s z_s
       h_ya h_za S_za S_ya delta_xa delta_ya delta_za epsilon_xa epsilon_yz epsilon_za
                           delta_xz delta_yz delta_zz epsilon_xz epsilon_yz epsilon_zz
                      S_zx delta_xx delta_yx delta_zx epsilon_xx epsilon_yx epsilon_zx
                 S_zy S_xy delta_xy delta_yy delta_zy epsilon_xy epsilon_yy epsilon_zy
    """
    var(','.join(vars.split()))
    # ========计算 理想的其次坐标变换矩阵
    T12=getHTM(0,0,0,0,0,0)*getHTM(0,0,0,0,0,0)
    T01=getHTM(0,0,0,0,0,0)*getHTM(0,0,0,'alpha',0,0)
    T03=getHTM(0,0,0,0,0,0)*getHTM(0,0,'z',0,0,0)
    T34=getHTM(0,0,0,0,0,0)*getHTM('x',0,0,0,0,0)
    T45=getHTM(0,0,0,0,0,0)*getHTM(0,'y',0,0,0,0)
    T56=getHTM('x_s','y_s','z_s',0,0,0)*getHTM(0,0,0,0,0,0)

    # 输出 所有Txx矩阵
    prefix_str='T'
    suffix_str='12 01 03 34 45 56'
    names=suffix_str.split(' ')
    for name in names:
        varname=prefix_str+name
        myprint(varname,locals()[varname])

    # =========计算 误差矢量
    if method=='F':
        Delta2=-zeros(6,1)
        Delta1=-Matrix([s('delta_xa'),s('delta_ya')+s('h_ya'),s('delta_za')+s('h_za'),s('epsilon_xa'),s('epsilon_ya')+s('S_za'),s('epsilon_za')+s('S_ya')])
        Delta0=zeros(6,1)
        Delta3=Matrix([s('delta_xz'),s('delta_yz'),s('delta_zz'),s('epsilon_xz'),s('epsilon_yz'),s('epsilon_zz')])
        Delta4=Matrix([s('delta_xx'),s('delta_yx'),s('delta_zx'),s('epsilon_xx'),s('epsilon_yx')+s('S_zx'),s('epsilon_zx')])
        Delta5=Matrix([s('delta_xy'),s('delta_yy'),s('delta_zy'),s('epsilon_xy')+s('S_zy'),s('epsilon_yy'),s('epsilon_zy')+s('S_xy')])
        Delta6=zeros(6,1)
    else:
        print('method输入不正确，请输如Z或F')
        exit()

    # 输出 所有Delata矩阵
    prefix_str='Delta'
    suffix_str='2 1 0 3 4 5 6'
    names=suffix_str.split(' ')
    for name in names:
        varname=prefix_str+name
        myprint(varname,locals()[varname])

    # ========计算 中间坐标系到末端坐标系的变换矩阵Tx8
    T56=T56
    T46=T45*T56
    T36=T34*T46
    T06=T03*T36
    # T16=getInvHTM(T01)*T06
    # T26=getInvHTM(T12)*T16

    # 输出所有Tx6矩阵
    prefix_str='T'
    suffix_str='56 46 36 06'
    names=suffix_str.split(' ')
    for name in names:
        varname=prefix_str+name
        myprint(varname,locals()[varname])

    # ======== 计算 J矩阵
    J65=Jze(T56)
    J64=Jze(T46)
    J63=Jze(T36)
    J60=Jze(T06)
    # J61=Jze(T16)
    # J62=Jze(T26)

    # 输出 J6x矩阵
    prefix_str='J'
    suffix_str='65 64 63 60'
    names=suffix_str.split(' ')
    for name in names:
        varname=prefix_str+name
        myprint(varname,locals()[varname])

    # ======== 计算每个轴的误差矢量在末端坐标系下的矢量
    JD6=Delta6
    JD5=J65*Delta5
    JD4=J64*Delta4
    JD3=J63*Delta3
    JD0=J60*Delta0
    # JD1=J61*Delta1
    # JD2=J62*Delta2
    # 输出 J6x矩阵
    prefix_str='JD'
    suffix_str='6 5 4 3 0'
    names=suffix_str.split(' ')
    for name in names:
        varname=prefix_str+name
        myprint(varname,locals()[varname])

    # ========末端坐标系：所有误差矢量转换到末端坐标系求和:gE_V_s:global errror vector in Sensor 坐标系
    gE_V_s=JD6+JD5+JD4+JD3+JD0
    myprint('gE_V_s:末端坐标系_综合误差矢量',gE_V_s)

    # ========末端坐标系：综合误差矢量==>综合误差矩阵
    gE_M_s=getDeltaforFu(gE_V_s[0],gE_V_s[1],gE_V_s[2],gE_V_s[3],gE_V_s[4],gE_V_s[5])
    myprint('[gE_M_s:末端坐标系_综合误差矩阵]',gE_M_s)

    # ========综合误差变换矩阵：末端==>工件
    dT=expand(T06*gE_M_s)
    myprint('[dT:末端==>工件：综合误差变换矩阵]',dT)

    # ========工件坐标系：综合误差各个分量结果
    print('[====method===]:',method)
    Pt=Matrix([0,0,0,1])
    Ot=Matrix([0,0,1,0])

    gPE=dT*Pt
    gOE=dT*Ot
    # 输出结果
    syms=[x,y,z,x_s,y_s,z_s]
    myprint('工件坐标系：综合几何误差-方向误差',gOE,simplify=False)
    myprint('gOx 工件坐标系:综合几何误差-O方向误差-x分量',collect(simplify(gOE[0]),syms))
    myprint('gOy 工件坐标系:综合几何误差-O方向误差-y分量',collect(simplify(gOE[1]),syms),simplify=False)
    myprint('gOz 工件坐标系:综合几何误差-O方向误差-z分量',collect(simplify(gOE[2]),syms),simplify=False)

    myprint('工件坐标系：综合几何误差-位置误差',gPE,simplify=False)
    myprint('gPx 工件坐标系：综合几何误差-P位置误差-X分量',collect(simplify(gPE[0]),syms),simplify=False)
    myprint('gPy 工件坐标系：综合几何误差-P位置误差-Y分量',collect(simplify(gPE[1]),syms),simplify=False)
    myprint('gPz 工件坐标系：综合几何误差-P位置误差-Z分量',collect(simplify(gPE[2]),syms),simplify=False)

# 改进付国强方法，建立通用利用微分多体系统理论(PIGE和PDGEs单独处理），推导机械结构误差模型:
# Input:xx.xlsx表格;method:diff/full,微分模型/全误差简化模型
# Output：6自由度误差公式
def getErrorsByDMBS(xlsx_file_name,method='diff'):
    # ======定义各种矩阵在表格/数组中的的起始
    global glmethod,glerr_flags,glfilename
    glfilename=xlsx_file_name
    glmethod=method #定义使用的方法全局变量，在mypprint()的时候使用
    glerr_flags=['h_','S_','epsilon_','delta_','O_'] # 定义误差前缀标志位，在使用IgnHighOrder()时需要用
    col_i=0 #低序体的列位置
    col_j=1 #特征体的列位置
    col_name_j=2 #特征体名称的列位置
    col_inv_j=3 #特征体inv的列位置
    col_s=4 #体间初始相对位姿在表格中的初始列位置（0开始）
    # 计算其他矩阵在行中开始的位置
    col_se=col_s+6
    col_m=col_se+6
    col_me=col_m+6
    starttime = time.time()
    workbook = xlrd.open_workbook(xlsx_file_name)
    print(workbook.sheet_names())  # 查看所有sheet
    booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
    cols = booksheet.ncols
    rows = booksheet.nrows
    # ========把有用的建模数据导入ds数组中,并定义sympy变量
    ds=[]
    varnames=[]
    for r in range(2,rows):
        arr_col=[]
        for c in range(cols):
            cell_val=booksheet.cell_value(r, c) #如果数据为空，那么就设定为“0”
            if cell_val=='':
                cell_val=0
            if c>=col_s and isinstance(cell_val,str):#定义sympy变量，后面eval()的时候好用
                varnames.append(cell_val)
            arr_col.append(cell_val)  #将单元格数据存入行数组
        ds.append(arr_col) # 构造数据的二维数组
    var(varnames) #构造SymPy变量
    print('[vars]:',varnames)
    ds.reverse() #数据数组逆序，因为计算T/J时需从最后一个矩阵开始计算，这样方便后面计算中间件到末端的各种矩阵
    # **********微分建模方法************#
    if method=='diff':
        # ======遍历数据，计算各种Delta、T、J矩阵等
        gEV_tool=z61() # gEV_tool（工具坐标系下的综合微分误差向量）的初值
        T_i_tool = zhtm() #工具末端到中间件的HTM
        T_j_tool_me = zhtm() #工具末端到中间件的HTM
        T_j_tool_se = zhtm() #工具末端到中间件的HTM
        for index,d in enumerate(ds): #从表格尾部到头部循环数据：!!注意：ds是excel表倒序的，从最后一行倒序过去
            # ===========定义特征体变量=========== #
            i=str(int(d[col_i])) #低序体
            j=str(int(d[col_j])) #特征体
            name_j=str(d[col_name_j]) # 特征体的名称
            isinv_j=bool(ds[index][col_inv_j])
            # ===========Delta_j=========== #
            dse = zeros(6, 1)
            dme = zeros(6, 1)
            for id, val in enumerate(d[col_se:col_se + 6]):
                dse[id] = eval(str(val))
            for id, val in enumerate(d[col_me:col_me + 6]):
                dme[id] = eval(str(val))
            # Delta_j = dse + dme
            if isinv_j:# 如果Inv为1，那么微分运动要取负值
                dse = -dse
                dme = -dme

            # ====计算T_j_tool(4x4)矩阵==>J_tool_j(6x6)矩阵==>EV_tool(6x1)向量==== #
            print("[******Process: {}({})**is_inv:{}******]".format(j,name_j,isinv_j))
            mypprint('before : T_i_tool',T_i_tool)
            if not isinv_j:# 如果Inv项为空,且低序体不是基体0，那么在表格中，产生Delta_j的矩阵T_ij在特征体j的下一行，在ds.reverse数据上一行
                T_j_tool_me=T_i_tool # 计算me误差项到工具坐标系之间的影响矩阵
                T_j_tool_se=getHTMByArray(d[col_m:col_m+6])*T_i_tool # 计算se误差项到工具坐标系之间的影响矩阵
                T_i_tool=getHTMByArray(d[col_s:cols+6])*getHTMByArray(d[col_m:col_m+6])*T_i_tool#T_i_tool:计算前是j前的i到tool的理想变换矩阵连乘，计算后是包括当前构件j在内的理想变换矩阵连乘
            else:# 注意求逆
                T_j_tool_se = getInvHTM(getHTMByArray(d[col_s:col_s + 6])) * T_i_tool
                T_j_tool_me = getInvHTM(getHTMByArray(d[col_m:col_m + 6])) * T_j_tool_se
                T_i_tool = getInvHTM(getHTMByArray(d[col_m:col_m + 6]))*getInvHTM(getHTMByArray(d[col_s:col_s + 6]))*T_i_tool

            # 计算J矩阵
            J_tool_j_me=Jze(T_j_tool_me)
            J_tool_j_se=Jze(T_j_tool_se)
            jd_j_me=J_tool_j_me*dme
            jd_j_se=J_tool_j_se*dse
            gEV_tool=gEV_tool+jd_j_me+jd_j_se
            mypprint('after : T_i_tool',T_i_tool)
            mypprint('T_{}({})_tool_me'.format(j,name_j),T_j_tool_me)
            mypprint('dme_{}({})'.format(j,name_j),dme)
            mypprint('T_{}({})_tool_se'.format(j,name_j),T_j_tool_se)
            mypprint('dse_{}({})'.format(j,name_j),dse)
            # mypprint('J_tool_{}({})'.format(j,name_j),(J_PDGEs_tool_j))
            # mypprint('JD_{}({})'.format(j,name_j),JD_PDGEs_j)
        # ======计算dT T_wp_tool*gE_tool
        gEM_tool = getDeltaforFu(gEV_tool[0], gEV_tool[1], gEV_tool[2], gEV_tool[3], gEV_tool[4], gEV_tool[5])# 综合误差矢量==>综合误差矩阵
        mypprint('[gE_M_tool:综合误差矩阵@末端坐标系]', gEM_tool)
        dT=expand(T_i_tool*gEM_tool) #误差变换矩阵
        mypprint('[gE_M_workpiece:综合误差变换矩阵dT:工具相对于工件]',dT)
        gPE=zeros(4,1)
        gOE=zeros(4,1)
        Pt=Matrix([0,0,0,1])
        Ot=Matrix([0,0,1,0])
        gPE=dT*Pt
        gOE=dT*Ot
    # ************全误差建模方法************#
    elif method=='full':
        T_ideal=zhtm()
        T_real=zhtm()
        for index,d in enumerate(ds): #从表格尾部到头部循环数据：!!注意：ds是excel表倒序的，从最后一行倒序过去
            T_ideal_ij=(getHTMByArray(d[col_s:col_s+6])*getHTMByArray(d[col_m:col_m+6]))
            T_real_ij=(getHTMByArray(d[col_s:col_s+6])*getDeltaByArray(d[col_se:col_se+6])*getHTMByArray(d[col_m:col_m+6])*getDeltaByArray(d[col_me:col_me+6]))
            mypprint('T_ideal_{}_{}({})'.format(str(int(d[col_i])),str(int(d[col_j])),d[col_name_j]),T_ideal_ij)
            mypprint('T_real_{}_{}({})'.format(str(int(d[col_i])),str(int(d[col_j])),d[col_name_j]),T_real_ij)
            if  d[col_inv_j]:
                T_ideal_ij=expand(getInvHTM(T_ideal_ij))
                T_real_ij=expand(getInvHTM(T_real_ij))
                mypprint('T_ideal_{}_{}({})_reverse'.format(str(int(d[col_i])),str(int(d[col_j])),d[col_name_j]),T_ideal_ij)
                mypprint('T_real_{}_{}({})_reverse'.format(str(int(d[col_i])),str(int(d[col_j])),d[col_name_j]),T_real_ij)
            T_ideal=expand(T_ideal_ij*T_ideal)
            T_real=(T_real_ij*T_real)
            mypprint('T_ideal',T_ideal)
            mypprint('T_real',T_real)
            print(varnames)
            print(var)

        # ======输出位置误差和姿态误差
        mypprint('T_ideal',T_ideal)
        mypprint('T_real',T_real)
        # =======计算位置误差和姿态误差，下面这样单独计算，可以比4x4大矩阵相减更少耗费资源，提高效率
        print('开始计算px')
        px=(expand(T_real[0,3])-expand(T_ideal[0,3]))
        print('开始计算py')
        py=(expand(T_real[1,3])-expand(T_ideal[1,3]))
        print('开始计算pz')
        pz=(expand(T_real[2,3])-expand(T_ideal[2,3]))
        mypprint('px',px)
        mypprint('py',py)
        mypprint('pz',pz)

        print('开始计算ox')
        ox=(expand(T_real[0,2])-expand(T_ideal[0,2]))
        print('开始计算oy')
        oy=(expand(T_real[1,2])-expand(T_ideal[1,2]))
        print('开始计算oz')
        oz=(expand(T_real[2,2])-expand(T_ideal[2,2]))
    else:
        print('△！！method参数输入错误，只能为：diff或full')

    # =======如果使用full方法，忽略其高次项
    if method=='diff':
        [px,py,pz,ox,oy,oz]=[gPE[0],gPE[1],gPE[2],gOE[0],gOE[1],gOE[2]]
    elif method=='full':
        ox=eval(IgnHighOrder(ox,'ox'))
        oy=eval(IgnHighOrder(oy,'oy'))
        oz=eval(IgnHighOrder(oz,'oz'))
        px=eval(IgnHighOrder(px,'px',isexpand=False),globals())
        py=eval(IgnHighOrder(py,'py',isexpand=False),globals())
        pz=eval(IgnHighOrder(pz,'pz',isexpand=False),globals())
    else:
        print('method参数设置错误')
    # =======设置提取公因式的公式
    # FXYZ、FZXY三轴
    try:
        syms=[Xt,Yt,Zt,X,Y,Z]
        # AFZXY 四轴
        # syms=[sin(alpha),cos(alpha),Xt,Yt,Zt,X,Y,Z]
        # CAFYXZ五轴
        # syms=[sin(alpha)*sin(gamma),sin(alpha)*cos(gamma),cos(alpha)*sin(gamma),cos(alpha)*cos(gamma),
        #       sin(alpha),sin(gamma),cos(alpha),cos(gamma),X,Y,Z]

        print('开始合并Ox/Oy/Oz的同类项操作,请耐心等待...')
        mypprint('ox 工件坐标系:综合几何误差-O方向误差-x分量',collect(simplify(ox),syms))
        mypprint('oy 工件坐标系:综合几何误差-O方向误差-y分量',collect(simplify(oy),syms))
        mypprint('oz 工件坐标系:综合几何误差-O方向误差-z分量',collect(simplify(oz),syms))
        print('开始合并Tx/Ty/Tz的同类项操作,请耐心等待...')
        mypprint('px 工件坐标系:综合几何误差-P位置误差-x分量',collect(simplify(px),syms))
        mypprint('py 工件坐标系:综合几何误差-P位置误差-y分量',collect(simplify(py),syms))
        mypprint('pz 工件坐标系:综合几何误差-P位置误差-z分量',collect(simplify(pz),syms))
    finally:
        endtime = time.time()
        print('[Time Consuming:]',endtime-starttime)
        print('T_ideal')
        printLatForMathType(T_ideal)
        return [px,py,pz,ox,oy,oz]

def printLatForMathType(expr):
    print('------Sympy Original Latex for MathType==>]')
    lat = latex(expr)
    print(lat)
    # mathtype里面的epsilon实际上是varepsilon
    res=getModLatFromStr(lat)
    print('------Precessed Latex for MathType==>]')
    print(res)
    return res

def getModLatFromStr(str):
    # mathtype里面的epsilon实际上是varepsilon
    modlat = re.sub(r'epsilon', "varepsilon", str)

    # 把小脚标的斜体改成正体:Xa,X和a默认都是斜体，但是在科学出版中，a应该是正体的
    sub_text = r'_\{(.*?)\}' # ?：表示非贪婪模式
    pattern = re.compile(sub_text)
    result = re.sub(pattern, u'_{{\\\\rm{\\1}}}', modlat).strip()
    return result

if __name__ == '__main__':
    '''测试LaTeX输出处理'''
    res=getHTM('x','y','z','a','b','c')
    a=Symbol('alpha_hs')
    b=Symbol('y_hs')
    z=a+b
    printLatForMathType(res)
    '''将原始的LaTeX处理后再输出'''
    # print(getModLatFromStr(latex(str)))
    # 测试DMBS（微分多体系统建模方法）
    # ！！！！！！！使用前修改约1209行的公因式公式！！！！！！！
    # getErrorsByDMBS(xlsx_file_name='xlsx/FZXY.xlsx',method='diff')
    # getErrorsByDMBS(xlsx_file_name='xlsx/FZXY.xlsx',method='full')
    # getErrorsByDMBS(xlsx_file_name='xlsx/AFZXY.xlsx',method='diff')
    # getErrorsByDMBS(xlsx_file_name='xlsx/AFZXY.xlsx',method='full')
    # getErrorsByDMBS(xlsx_file_name='xlsx/CAFYXZ.xlsx',method='diff')
    # getErrorsByDMBS(xlsx_file_name='xlsx/CAFYXZ.xlsx',method='full')
    # 成功：测试其次坐标变换矩阵
    # print(getHTM('x',0,0,0,0,0))
    # 成功：测试其次微分坐标变换矩阵
    # print(getDiffHTM('dx','dy','dz','ex','ey','ez'))
    # 成功：正向其次坐标变换矩阵的J矩阵推导
    # Ji=JzeInv()
    # 成功：忽略高阶项
    # IgnHighOrder()
    # 成功：验证两个微分运动相乘
    # twoDelta()
    # 成功：测试XYZ三轴CMM误差公式推导
    # getErrorsofXYZCMMByMethod('F')
    # 成功：测试XYZ三轴CMM Full全部误差公式推导
    # getFullErrorsofXYZCMM()
    # 成功：验证五轴CAFYXZ
    # getErrorsofCAFYXZbyMethod(method='F')
    # 成功：测试五轴CAFYXZ五轴全误差模型，运算时间较长
    # getFullErrorsofCAFYXZCMM()
    # 成功：验证课题四轴测量机误差模型
    # getErrorsofAFZXYZbyMethod(method='F')
    # 成功：但和上面差别，验证课题四轴测量机全误差模型
    # getFullErrorsofAFZXYCMM()
    # 成功：验证课题四轴简化成3轴的全误差模型
    # getFullErrorsof_FZXY_CMM()
    # 成功：验证课题四轴简化成3轴的微分误差模型
    # getErrorsof_FZXYZ_byMethod(method='F')
