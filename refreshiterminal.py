import sys,time

s = ["\\","|","/","-","|","-"]

while True:

    for i in s:

        sys.stdout.write("\r") # 清空终端并清空缓冲区

        sys.stdout.write(i) # 往缓冲区里写数据

        sys.stdout.flush() # 将缓冲区里的数据刷新到终端，但是不会清空缓冲区

        time.sleep(0.5)