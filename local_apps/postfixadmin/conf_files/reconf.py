import os, re

def reconf():
    
    path = os.getcwd()

    hostname = ''
    username = ''
    password = ''
    port = ''
    

    replacements = [    ('__password__', password),
                        ('__username__', username),
                        ('__hostname__', hostname),
                        ('__port__', port)
                    ]

    for root, dirs, files in os.walk(path):

        for name in files:

            if name != 'reconf.py':

                f_in = file(root+'/'+name,'r')
                c = f_in.read()

                for search, replace in replacements:
                    p = re.compile(search)
                    c = p.sub(replace ,c)

                f_out = file(root+'/'+name,'w')
                f_out.write(c) 

if __name__ == "__main__":
    reconf()
