def convert(text): 
    content = ""
    if isinstance(text,str):
        content = text
    elif isinstance(text,tuple) or isinstance(text,list):
        content = "".join('%s' %i for i in text) 
    return content