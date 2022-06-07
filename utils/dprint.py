import inspect
import re

def varname(p):
  for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
    m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
      return m.group(1)

def dprint(var):
    vname=varname(var)
    print(vname)

def get_variable_name(x)->str:
    for k,v in locals().items():
        if v is x:
            return k
def p(var):
    print(var)

def print1(var):
    print(get_variable_name(var))
    print(var)

if __name__ == '__main__':
    a=1
    dprint(a)