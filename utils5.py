import ast 

def transfo_liste(x):
  if isinstance(x, str):
    return ast.literal_eval(x)
  else:
    return x