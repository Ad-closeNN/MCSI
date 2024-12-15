"""主程序页面"""

import threading
import os
import Modules.Log as logging
import Modules.Loading

def main():
    logging.info("[Page] 主页面已加载")
    while True:
        os.system("cls")
        print("欢迎使用 Minecraft Server Installer！")
        print("请用数字选择使用的功能，使用回车确认：")
        print("1. 下载服务端")
        print("2. 启动服务端")
        print("3. 停止服务端")
        print("4. 重启服务端")
        print("5. 退出程序")
        
        Main_Page = input("> ")
        if Main_Page == "1": # 下载服务端
            import Pages.DownloadServer
            os.system("cls")
            Pages.DownloadServer.download_server()
        if Main_Page == "2": # 启动服务端
            ...
        if Main_Page == "3": # 停止服务端
            ...
        if Main_Page == "4": # 重启服务端
            ...
        if Main_Page == "5": # 退出程序
            os.system("cls")
            import sys
            logging.info("[System] 程序已退出")
            sys.exit()
            

if __name__ == "__main__":
    os.system("cls")
    load = threading.Thread(target=Modules.Loading.loading) # 加载/初始化线程
    load.start()
    logging.info('[Thread] "Modules.Loading.loading" 线程已启动')
    print("欢迎使用 MCServer Installer！")
    print("正在初始化...请稍等...")
    load.join()
    logging.info('[Thread] "Modules.Loading.loading" 线程已结束')
    
    main()
    logging.info("[System] 程序已退出")