"""下载服务端"""
# 这里只包括选择页面，比如可选择下载的服务端类型（比如 Spigot 等）

import Modules.Log as logging

def download_server():
    logging.info('[Page] DownloadServer 页面已加载')
    print("下载 服务端")
    print("")
    print("1. 下载 原版 服务端") # Download_Server/Vanilla.py
    print("2. 下载 第三方 插件服务端（如 Spigot, Pager 等）") # Download_Server/Plugin.py
    print("3. 下载 Forge/Fabric 之类的服务端") # Download_Server/Vanilla.py
    print("4. 返回上一级")
    
    
    while True:
        Download_Page = input("> ")
        if Download_Page == "1":
            import Pages.Download_Server.Vanilla
            Pages.Download_Server.Vanilla.vanilla()
            break
        if Download_Page == "2":
            import Pages.Download_Server.Plugin
            Pages.Download_Server.Plugin.plugin()
            break
        if Download_Page == "3":
            import Pages.Download_Server.ModLoader
            Pages.Download_Server.ModLoader.modloader()
            break
        if Download_Page == "4":
            import MCSI
            MCSI.main()
            break