"""下载第三方插件服务端"""

import Modules.Log as logging
import os

def plugin():
    logging.info("[Page] DownloadServer.plugin 页面已加载")
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("下载第三方服务端")
        print("1. 下载[Paper]服务端") #Plugin/Paper.py
        print("2. 下载[Leaves]服务端") #Plugin/Leaves.py
        print("3. 下载[Spigot]服务端") #Plugin/Spigot.py
        print("4. 返回上一级")
        
        Download_Page = input("> ")
        if Download_Page == "1":
            os.system("cls" if os.name == "nt" else "clear")
            print("海内存知己，天涯若比邻\n        请稍等...") # 跟微软学的(x
            import Pages.Download_Server.Plugin_.Paper
            logging.info("[Page] 已从 DownloadServer.plugin 加载到 DownloadServer.plugin.paper")
            Pages.Download_Server.Plugin_.Paper.main()
            logging.info("[Page] 已从 DownloadServer.plugin.paper 返回到 DownloadServer")

        if Download_Page == "2":
            import Pages.Download_Server.Plugin_.Leaves
        
        if Download_Page == "3":
            import Pages.Download_Server.Plugin_.Spigot
        
        if Download_Page == "4":
            os.system("cls" if os.name == "nt" else "clear")
            return