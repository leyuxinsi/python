import os,stat

os.makedirs('yanying')
os.chmod('yanying',stat.S_IRWXU | stat.S_IRWXG|stat.S_IRWXO)