"""下载服务端"""
# 这里只包括选择页面，比如可选择下载的服务端类型（比如 Spigot 等）

import Modules.Log as logging
import os

def download_server():
    logging.info('[Page] DownloadServer 页面已加载')

    while True:
        print("下载服务端")
        print("1. 下载[原版]服务端") # Download_Server/Vanilla.py
        print("2. 下载[第三方]插件服务端（如 Spigot/Pager 等）") # Download_Server/Plugin.py
        print("3. 下载[Forge/Fabric]服务端") # Download_Server/Vanilla.py
        print("4. 返回上一级")

        Download_Page = input("> ")
        if Download_Page == "1":
            os.system("cls")
            print("海内存知己，天涯若比邻\n        请稍等...") # 跟微软学的(x
            import Pages.Download_Server.Vanilla
            Pages.Download_Server.Vanilla.vanilla()
            logging.info("[Page] 已从 DownloadServer.vanilla 返回到 DownloadServer")
        
        if Download_Page == "2":
            import Pages.Download_Server.Plugin
            Pages.Download_Server.Plugin.plugin()
        
        if Download_Page == "3":
            import Pages.Download_Server.ModLoader
            Pages.Download_Server.ModLoader.modloader()
        
        if Download_Page == "4":
            return