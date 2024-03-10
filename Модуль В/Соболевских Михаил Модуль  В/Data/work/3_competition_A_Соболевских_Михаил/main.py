import csv 
import json

cols = [...] 
 
data = [ 
{'...'}
] 
path = "C:\Users\Profi Main\Desktop"
with open(path, 'w') as f: 
    wr = csv.DictWriter(f, fieldnames = cols) 
    wr.writeheader() 
    wr.writerows(data) 