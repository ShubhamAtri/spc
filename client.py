import requests
import os
import pickle
import shutil
from bs4 import BeautifulSoup
import html , subprocess
import hashlib

myfile = 'login_details.txt'
if os.path.isfile(myfile) == False:
    print("You must login for performing this action")
    exit(0)

# url = 'http://192.168.2.1:8000/login/'
# d1url = "http://127.0.0.1:8000/files/download/?name=usrs.BookIndex/bytes/filename/mimetype/a.txt"
# durl = "http://127.0.0.1:8000/files/download/?name=usrs.BookIndex/bytes/filename/mimetype/Graph_and_Trees.pdf"

# client = requests.session()
# client.get(url)
# csrftoken1 = client.cookies['csrftoken']

# with open(myfile, 'r') as fr:
#     count = 1
#     for line in fr:
#         if count == 1:
#             u = line[:-1]
#         elif count == 2:
#             p = line[:-1]
#         count+=1

# print(u)
# print(p)

# login_data = dict(username=u, password=p, csrfmiddlewaretoken=csrftoken1)
# r1 = client.post(url, data=login_data)
# print(r1.url)

with open(myfile, 'rb') as fs:
    count = 1
    for line in fs:
        if count == 3 :
            url = line.decode('ascii')
        else:
            count+=1;

print(url)

l = []
inputd={}

fname = 'directory_path.txt'
with open(fname, 'rb') as fs:
    directory = fs.read().decode('ascii')

upload_file = 'upload_file.txt'

print(directory)
with open(upload_file, 'rb') as fs:
    upload_url = fs.read().decode('ascii')

# file = 'encodedmd5.pickle'
# with open(file,'wb') as fw:
#     inputd = pickle.load(fw)

md5 = {}
def fillinputd():
    for (dirpath, dirnames, filenames) in os.walk(directory):
        print(filenames)
        for filename in filenames:
            reldir = os.path.relpath(dirpath, directory)
            print(reldir)
            if reldir != ".":
                relFile = os.path.join(reldir, filename)
            else:
                relFile = filename
            hash_md5 = hashlib.md5()
            with open(relFile, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
                md5[relFile] = hash_md5.hexdigest()
            if filename[0]!='.':
                inputd[relFile]=0

    
def sync():
    client = requests.session()
    with open('somefile', 'rb') as f:
        client.cookies.update(pickle.load(f))
    u = 'sed5'
    p = 'A123456!'
    client.auth = (u,p)
    client.headers.update({'x-test': 'true'})
    # g = client.get(upload_url,cookies=client.cookies, headers={'x-test2': 'true'})
    # client.get(upload_url)
    # csrftoken = client.cookies['csrftoken']
    csrftoken = client.cookies['csrftoken']
    # files = {'index': open(filename,'rb')}
    # values = {'ownr': 1, 'name': filename,'md5s': 'vsdhabhja', 'username': 'sed4','csrfmiddlewaretoken': csrftoken,'password': 'Shubham123', 'deb': 1}
    r = client.get(url)
    soup = BeautifulSoup(r.content,features="html.parser")
    # print(1)
    tables = soup.findChildren('table')
    if len(tables)!=0:
        # print(2)
        # print(tables)
        my_table = tables[0]
        # print(3)
        # print(my_table)
        rows = my_table.findChildren('tr')
        # print(4)
        # print(rows)
        for row in rows:
         # print(row)
         cells = row.findChildren('td')
         k1 = cells[0].find('a').contents[0]
         k2 = cells[1].find('a')['href']
         k3 = cells[4].text
         k3 = k3[1:-1]
         # p = k2[0].find('a',href=True)
         print(cells[1].find('a'))
         print(k1)
         # print(k2)
         print(k3)
         print("")
         temp = []
         temp.append(k1)
         temp.append(k2)
         temp.append(k3)
         l.append(temp)

def download():
    for item in l:
        if os.path.isfile(item[0]) == False:
            client = requests.session()
            with open('somefile', 'rb') as f:
                client.cookies.update(pickle.load(f))
            u = 'sed5'
            p = 'A123456!'
            client.auth = (u,p)
            client.headers.update({'x-test': 'true'})
            # g = client.get(upload_url,cookies=client.cookies, headers={'x-test2': 'true'})
            # client.get(upload_url)
            # csrftoken = client.cookies['csrftoken']
            csrftoken = client.cookies['csrftoken']
            values = {'username': 'sed5','csrfmiddlewaretoken': csrftoken,'password': 'A123456!', 'check1': 1}    
            t = client.post("http://10.42.0.133:8000"+item[1], data=values)
            print(item[0])
            with open(item[0]+'.gpg','wb') as f:
                f.write(t.content)
                f.close()
            subprocess.call(['gpg', '--yes', '--batch', '--passphrase="a"', item[0]+'.gpg'])
            subprocess.call(['rm', item[0]+'.gpg'])
        else:
            print(type(md5[item[0]]))
            print(type(item[2]))
            print(md5[item[0]])
            print(len(item[2]))
            if md5[item[0]] == item[2]:
                inputd[item[0]] = 1
            else:
                print('File with name'+ item[0] + 'exist both on server and client' )
                print('If you want to keep both files, then terminate the sync process and change file name')
                print('Warning : If you continue then one file content name are lost')
                print('S(For overloading your file with server file)')
                print('C(For overloading server file with your file)')
                k = input()
                if k == 'S':
                    inputd[item[0]] = 1
                    client = requests.session()
                    os.remove(item[0])
                    with open('somefile', 'rb') as f:
                        client.cookies.update(pickle.load(f))
                    u = 'sed5'
                    p = 'A123456!'
                    client.auth = (u,p)
                    client.headers.update({'x-test': 'true'})
                    # g = client.get(upload_url,cookies=client.cookies, headers={'x-test2': 'true'})
                    # client.get(upload_url)
                    # csrftoken = client.cookies['csrftoken']
                    csrftoken = client.cookies['csrftoken']
                    values = {'username': 'sed5','csrfmiddlewaretoken': csrftoken,'password': 'A123456!', 'deb': 1}    
                    t = client.post("http://10.42.0.133:8000"+item[1], data=values)
                    print(item[0])
                    with open(item[0]+'.gpg','wb') as f:
                        f.write(t.content)
                        f.close()
                    subprocess.call(['gpg', '--yes', '--batch', '--passphrase="a"', item[0]+'.gpg'])
                    subprocess.call(['rm', item[0]+'.gpg'])
                elif k != 'C':
                    print('The option you entered is invalid')
                    exit(0)




def upload():
    for key,values in inputd.items():
        if values == 0:           
            client = requests.session()
            with open('somefile', 'rb') as f:
                client.cookies.update(pickle.load(f))
            u = 'sed5'
            p = 'A123456!'
            client.auth = (u,p)
            client.headers.update({'x-test': 'true'})
            # g = client.get(upload_url,cookies=client.cookies, headers={'x-test2': 'true'})
            # client.get(upload_url)
            # csrftoken = client.cookies['csrftoken']
            csrftoken = client.cookies['csrftoken']
            print(key)
            subprocess.call(['gpg', '--yes', '--batch', '--passphrase="a"', '-c', key])
            hash_md5 = hashlib.md5()
            with open(key+'.gpg', "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            temp = hash_md5.hexdigest()
            print(temp)
            print(len(temp))
            files = {'index': open(key+'.gpg','rb')}
            values = {'ownr': 4,'encpt_key': 'wvdehj','md5se':temp ,'en_schm':"dsf",'sharing': 'sdfs', 'name': key,'md5so': md5[key], 'username': 'sed5','csrfmiddlewaretoken': csrftoken,'password': 'A123456!', 'check1': 1}    
            r = client.post(upload_url, files=files, data=values)
            subprocess.call(['rm', key+'.gpg'])
# def md5_sum()
   
fillinputd()
print(inputd)
sync()
print(l)
download()
upload()


# def upload_file(filename):
#     if os.path.isfile(filename) == False:
#         print("No such file exist")
#         print("Terminating")
#         exit(0)
#     client = requests.session()
#     with open('somefile', 'rb') as f:
#         client.cookies.update(pickle.load(f))
#     u = 'sed4'
#     p = 'A123456!'
#     client.auth = (u,p)
#     client.headers.update({'x-test': 'true'})
#     # g = client.get(upload_url,cookies=client.cookies, headers={'x-test2': 'true'})
#     # client.get(upload_url)
#     # csrftoken = client.cookies['csrftoken']
#     csrftoken = client.cookies['csrftoken']
#     files = {'index': open(filename,'rb')}
#     values = {'ownr': 4, 'name': filename,'md5s': 'vsdhabhja', 'username': 'sed4','csrfmiddlewaretoken': csrftoken,'password': 'A123456!', 'deb': 1}
#     t = client.post(durl, data=values)

#     with open("dow_file",'wb') as f:
#         f.write(t.content)

#     r = client.post(upload_url, files=files, data=values)
#     # print(r.status_code)
#     soup = BeautifulSoup(r.content,features="html.parser")
#     # print(1)
#     tables = soup.findChildren('table')
#     # print(2)
#     # print(tables)
#     my_table = tables[0]
#     # print(3)
#     # print(my_table)
#     rows = my_table.findChildren('tr')
#     # print(4)
#     # print(rows)
#     for row in rows:
#      # print(row)
#      cells = row.findChildren('td')
#      k1 = cells[0].find('a').contents[0]
#      k2 = cells[1].find('a')['href']
#      # p = k2[0].find('a',href=True)
#      print(k1)
#      print(k2)
#      print("")
#      temp = []
#      temp.append(k1)
#      temp.append(k2)
#      l.append(temp)
#     print(r.content)
#     if r.status_code == 200:
#         print("Uploaded file successfully")
#     else:
#         print("Some error ocurred while uploading file")

# def upload_directory():
#     for filename in os.listdir(directory):
#         filename = directory + filename
#         print(filename)
#         upload_file(filename)

# directory_path = 'directory_path.txt'

# if os.path.isfile(directory_path):
#     print("If you want to upload all files in your observing directory, enter 1")
#     print("(If some file is already uploaded then it will not get reuploaded even if some changes are made)")
#     print("If you want to upload a particular file, enter 2")
#     t = int(input(">> "))
#     if t == 1:
#         with open(directory_path, 'rb') as fs:
#             directory = fs.read().decode('ascii')
#         upload_directory()
#     else:
#         filename = input("Enter the path of file to be uploaded: ")
#         filename = os.path.abspath(filename)
#         upload_file(filename)
# else:
#     filename = input("Enter the path of file to be uploaded: ")
#     filename = os.path.abspath(filename)
#     upload_file(filename)



# text_file = 'login_details.txt'

# with open(text_file, 'rb') as fs:
#     count = 1
#     for line in fs:
#         if count == 3 :
#             csrftoken = line.decode('ascii')
#         else:
#             count+=1;

# print(csrftoken)



# def directory_server():
#     r = requests.get(url_for_sending_back_csv_containing_files_with_their_md5sum)

# directory_server()

# compare r with the directory structure of the client and then sync

# for root, dirs, files in os.walk(directory):
#     level = root.replace(os.getcwd(), '').count(os.sep)
#     indent = ' ' * 4 * (level)
#     str1 += '{}{}/'.format(indent, os.path.basename(root))
#     str1 += '\n'
#     subindent = ' ' * 4 * (level + 1)
#     for f in files:
#         str1 += '{}{}'.format(subindent, f)
#         str1 += '\n'
#     data = bytes(str1, 'utf-8')
#     csFT.sendall(data)

# upload_url = 'http://0.0.0.0:8000/model_files/add/'


# client = requests.session()
# client.get(upload_url)  # sets the cookie
# csrftoken = client.cookies['csrftoken']

# with open(text_file, 'wb') as fw:
#         fw.write(bytes(u, 'utf-8'))
#         fw.write(bytes("\n", 'utf-8'))
#         fw.write(bytes(p, 'utf-8'))
#         fw.close()

# files = {'Index': open(directory + 'login_details.txt','rb')}
# files = {'index': open('ssl-quiz3/RMO.pdf','rb')}
# values = {'ownr': 2, 'name': 'RMO', 'csrfmiddlewaretoken': csrftoken}
# r = client.post(upload_url, files=files, data=values)
# # print(r.status_code)
# # print(r.content)
# if r.status_code == 200:
#     print("Uploaded file successfully")
# else:
#     print("Some error ocurred while uploading file")

# download_url = 'http://192.168.2.1:8000/model_files/add/'





# str1 =""
# for root, dirs, files in os.walk(directory):
#     level = root.replace(os.getcwd(), '').count(os.sep)
#     indent = ' ' * 4 * (level)
#     str1 += '{}{}/'.format(indent, os.path.basename(root))
#     str1 += '\n'
#     subindent = ' ' * 4 * (level + 1)
#     for f in files:
#         str1 += '{}{}'.format(subindent, f)
#         str1 += '\n'
#     data = bytes(str1, 'utf-8')
#     csFT.sendall(data)

# #Send file
# with open(text_file, 'rb') as fs:
#     #Using with, no file close is necessary,
#     #with automatically handles file close
#     #csFT.send(b'BEGIN')
#     while True:
#         data = fs.read(1024)
#         print('Sending data', data.decode('utf-8'))
#         csFT.send(data)
#         print('Sent data', data.decode('utf-8'))
#         if not data:
#             print('Breaking from sending data')
#             break
#     csFT.sendall(b'exit')
#     fs.close()
 
# #Receive file
# print("Receiving..")
# with open(text_file, 'wb') as fw:
#     while True:
#         data = csFT.recv(1024)
#         if not data:
#             break
#         fw.write(data)
#     fw.close()
# print("Received..")
 
# csFT.close()



# files = {'upload_file': open('file.txt','rb')}
# values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}

# r = requests.post(url, files=files, data=values)