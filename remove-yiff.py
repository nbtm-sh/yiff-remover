import requests, os, hashlib, time

E621_DOMAIN = "static1.e621.net"
USER_AGENT = "yiff-remover (github.com/nbtm-sh)"
DIRECTORY = "./"

def get_files(directory):
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames if os.path.splitext(f)[1] == '.jpg' or os.path.splitext(f)[1] == '.png' or os.path.splitext(f)[1] == '.swf']
    return files

def get_file_hash(file):
    file_handler = open(file, 'rb')
    file_content = file_handler.read()
    file_hander.close()
    md5_sum = hashlib.md5(file_content)
    return md5_sum.hexdigest() 

def check_if_exists(file_hash, file_name):
    ext = os.path.splitext(file_name)[1]
    file_name = file_hash + ext

    path = f"{file_name[0:2]}/{file_name[2:4]}/{file_name}"
    x = requests.get(f"https://{E621_DOMAIN}/data/{path}", headers={"User-Agent": USER_AGENT})

    return x.status_code == 200

def scan(directory, remove=True, wait=1):
    file_list = get_files(directory)
    for i in file_list:
        i_hash = get_file_hash(i)
        if check_if_exists(i_hash, i):
            print("Remove", i, i_hash)
            if remove:
                os.remove(i)
        else:
            print("Skip", i, i_hash)
        
        time.sleep(wait)


scan(DIRECTORY)
