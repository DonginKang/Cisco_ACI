#python reload.py 사용 불가, python 실행후 복사후 붙여넣기로 실행 

from pexpect import pxssh
import time

s=pxssh.pxssh()

def on_off(r_number,r_time):
    
    for i in range(0,r_number): # (0,150)일경우엔 150번 반복
        s.login('IP','USER','PASS')  

        time.sleep(2)  # 2초간 정지
        s.sendline('ssh leaf201')
        s.prompt()
        print (s.before.decode())
        s.sendline('PASS')
        s.prompt()
        print (s.before.decode())
        s.sendline('reload')
        s.prompt()
        print (s.before.decode())    
        s.sendline('y')
        s.prompt()
        print (s.before.decode())
    
        s.logout()

        time.sleep(r_time) # 600초간 정지 후 다시 반복

