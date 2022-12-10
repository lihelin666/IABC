'''sympy相关的函数'''
from sympy import latex,var,init_printing
import re
import sympy

def getLatForMathType(expr):
    lat = latex(expr,order='grlex') # grlex：高阶在前，lex：低阶在前
    if 'epsilon' in lat:  # 正则替换
        lat = re.sub(r'epsilon_\{(\S)(\S)\}', u'varepsilon_{\\1}(\\2)', lat)
    if 'delta' in lat:  # 正则替换
        lat = re.sub(r'delta_\{(\S)(\S)\}', u'delta_{\\1}(\\2)', lat)
    if 'cdot' in lat:
        lat=lat.replace('cdot','times')
    return lat