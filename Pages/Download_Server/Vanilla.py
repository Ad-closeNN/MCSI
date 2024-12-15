"""下载原版服务端"""
# 使用了 bangbang93 的镜像服务 https://bmclapidoc.bangbang93.com
# 使用了 BetaCraft 的镜像服务 https://files.betacraft.uk/server-archive

import requests
import Modules.Log as logging
import json
import os
import shutil
import time
import hashlib

def vanilla():
    """获取版本信息"""
    logging.info("[Page] DownloadServer.vanilla 页面已加载")
    os.system("cls")
    print("正在获取版本列表")
    for retry in range(3):
        logging.info("[Net] 正在获取原版版本列表：https://bmclapi2.bangbang93.com/mc/game/version_manifest_v2.json")
        MCVersionList = requests.get("https://bmclapi2.bangbang93.com/mc/game/version_manifest_v2.json")
        if MCVersionList.status_code == 200:
            logging.info("[Net] 获取原版版本列表JSON成功，长度："+str(len(str(MCVersionList.content.decode('utf-8')))))
            break
        else:
            logging.error(f"[Net] 第{retry+1}/3次下载原版版本列表失败："+str(MCVersionList.status_code))
            print(f"获取原版版本列表失败，尝试 {retry+1}/3 次，每次间隔3秒")
            time.sleep(3)
    else:
        logging.error("[Net] 3次重试失败，返回上一级")
        print("获取失败，返回上一级")
        print("")
        input("按回车继续...")
        import Pages.DownloadServer
        Pages.DownloadServer.download_server()

    MCVersionList = json.loads(MCVersionList.content.decode('utf-8'))

    """做中文翻译"""
    # reversed() 是用来做倒序的，因为 json 里是正序（高版本->中版本->低版本）
    os.system("cls")
    MCType = input("请选择你需要展示的版本类型（全部/正式版/快照版）：\n> ")
    if "all" in MCType.lower() or "全部" in MCType.lower() or MCType == "1":
        print("")
        print("注意：> 带有“无服务端”字样的代表无服务端可下载 <")
        input("将列出所有版本（倒序，最下面为新版本），按回车继续...")
        logging.info("[System] 展示全部原版版本")
        for ver in reversed(MCVersionList["versions"]):
            if ver["type"] == "snapshot":
                type = "快照版"
            elif ver["type"] == "release":
                type = "正式版"
            elif ver["type"] == "old_beta":
                type = "无服务端" # 不想维护这么多的 old beta version 服务端，所以干脆就直接写无服务端就行了()
            elif ver["type"] == "old_alpha":
                type = "无服务端"
            print("[*] "+ver["id"]+" "+"("+type+")")
        print("请选择你需要下载的版本，需要完整的版本号（如 1.21.4-rc3 ）：")
        DownloadVersion = input("> ")
    
    elif "release" in MCType.lower() or "正式版" in MCType.lower() or MCType == "2":
        input("将列出正式版版本（倒序，最下面为新版本），按回车继续...")
        logging.info("[System] 展示仅正式版的原版版本")
        for ver in reversed(MCVersionList["versions"]):
            if ver["type"] == "release":
                print("[*]", ver["id"])
        print("请选择你需要下载的版本，需要完整的版本号（如 1.20.1 ）:")
        DownloadVersion = input("> ")
    
    elif "snapshot" in MCType.lower() or "快照版" in MCType.lower() or MCType == "3":
        input("将列出快照版版本（倒序，最下面为新版本），按回车继续...")
        logging.info("[System] 展示仅快照版的原版版本")
        for ver in reversed(MCVersionList["versions"]):
            if ver["type"] == "snapshot":
                print("[*]", ver["id"])
        print("请选择你需要下载的版本，需要完整的版本号（如 24w46a ）:")
        DownloadVersion = input("> ")
        
    else: # 不输入就执行 all
        print("")
        print("注意：> 带有“无服务端”字样的代表无服务端可下载 <")
        input("将列出所有版本（倒序，最下面为新版本），按回车继续...")
        logging.info("[System] 展示全部原版版本")
        for ver in reversed(MCVersionList["versions"]):
            if ver["type"] == "snapshot":
                type = "快照版"
            elif ver["type"] == "release":
                type = "正式版"
            elif ver["type"] == "old_beta":
                type = "远古版"
            elif ver["type"] == "old_alpha":
                type = "无服务端"
            print("[*] "+ver["id"]+" "+"("+type+")")
        print("请选择你需要下载的版本，需要完整的版本号（如 1.21.4-rc3 ）：")
        DownloadVersion = input("> ")
    DownloadVersion = DownloadVersion.strip() # 去除前后空格
    
    if not DownloadVersion == "" or DownloadVersion.startswith("a") or DownloadVersion.startswith("c") or DownloadVersion.startswith("rd") or DownloadVersion.startswith("inf"):
        betacraft_Server_jar_URL = f"https://files.betacraft.uk/server-archive/release/{DownloadVersion[:3]}/{DownloadVersion}.jar"
        bangbang93_Server_jar_URL = f"https://bmclapi2.bangbang93.com/version/{DownloadVersion}/server" # 使用 bangbang93 的 BMCLAPI
        """判断使用的 URL"""
        try:
            if int(DownloadVersion.replace(".", "")) <= 125:
                DownloadLink = betacraft_Server_jar_URL
                logging.info(f"[System] 检测的版本号（{DownloadVersion.replace(".", "")} <= 1.2.5（125）），将使用 BetaCraft 路线进行下载")
            if int(DownloadVersion.replace(".", "")) == 10: # 1.0
                DownloadLink = "https://files.betacraft.uk/server-archive/release/1.0/1.0.0.jar" # 1.0.1 的是服务器更新，client version json 里面没有，BetaCraft 分了个 1.0.0.jar 和 1.0.1.jar 出来...
            else:
                DownloadLink = bangbang93_Server_jar_URL
                logging.info(f"[System] 检测的版本号（{DownloadVersion.replace(".", "")} > 1.2.5（125）），将使用 bangbang93 路线进行下载")
        except Exception as e:
            DownloadLink = bangbang93_Server_jar_URL
            logging.info(f"[System] 检测的版本号（{DownloadVersion.replace(".", "")} > 1.2.5（125）），将使用 bangbang93 路线进行下载")            
            logging.debug(f"[Easter-Egg] 不是 Bug，判断版本号失败：{e}") # 彩蛋，不是bug
        """Retry"""
        for retry in range(3): # 3次重试
            logging.info(f'[Net] 正在下载原版服务端 {DownloadVersion}（{DownloadVersion.replace(".", "")}）："{DownloadLink}"') # 加冒号的原因：点名表扬愚人节快照版本id(比如版本 "3D Shareware v1.34" 会把 URL 分节而不能在 VS Code 里面打开)
            print(f"正在下载[原版]服务端：[{DownloadVersion}]，请稍等...")
            with requests.get(DownloadLink, stream=True) as Get_jar: # 用流式传输，因为后面的.jar可能会很大，现在的 1.21 都接近 50MB 了 
                if Get_jar.status_code == 200:
                    with open(f"Download/Temp/Vanilla_{DownloadVersion}.jar", "wb") as jar:
                        for chunk in Get_jar.iter_content(chunk_size=81920):
                            jar.write(chunk) # 以块+二进制的方式写入到文件里
                        Jar_size = int(os.path.getsize(f"Download/Temp/Vanilla_{DownloadVersion}.jar"))/1048576 # 转换为 MB 单位(/1024/1024 = /1024*1024)
                        logging.info(f"[Net] 获取 {DownloadVersion}.jar 成功，大小：{Jar_size} MB")
                        print(f"{DownloadVersion}.jar 下载成功，大小：{Jar_size:.1f}MB")
                    with open(f"Download/Temp/Vanilla_{DownloadVersion}.jar", "rb") as f:
                        logging.info(f"[System] {DownloadVersion}.jar 的 MD5 哈希值：" + hashlib.md5(f.read()).hexdigest())

                    """判断文件夹"""
                    if not os.path.exists("Server/[原版]"+ DownloadVersion):
                        os.mkdir("Server/[原版]"+ DownloadVersion)

                    """移动服务器.jar文件"""
                    shutil.move(f"Download/Temp/Vanilla_{DownloadVersion}.jar", f"Server/[原版]{DownloadVersion}/[原版]{DownloadVersion}.jar") # 特意删的空格，至少减少了有空格导致的bug的发生...
                    logging.info(f"[System] {DownloadVersion}.jar 剪切完毕，新命名：[原版]{DownloadVersion}.jar")
                    logging.info(f"[System] 原版服务端 {DownloadVersion} 下载完毕")
                    break
                else:
                    logging.error(f"[Net] 获取 {DownloadVersion}.jar 失败，返回值：{Get_jar.status_code}，正在重试{retry+1}/3，每次3s...")
                    print(f"下载 {DownloadVersion}.jar 失败，HTTP 错误代码：{Get_jar.status_code}\n正在重试{retry+1}/3，每次隔3秒...")
                    time.sleep(3) # 3秒一次
            logging.error("[Net] 三次重试次数已用完")
            print("")
            print("三次重试均为失败，请检查网络设置并重试")
    
    else: # 不输入就最新版
        MCLatestVersion = str(MCVersionList["latest"]["release"]) # 强制转换 List -> Str，因为 VS Code 不认 MCLatestVersion 是 Str（.replace 不会有代码高亮）
        logging.info(f"[Net] 最新的正式版服务端：{MCLatestVersion}")
        bangbang93_Server_jar_URL = f"https://bmclapi2.bangbang93.com/version/{MCLatestVersion}/server" # 使用 bangbang93 的 BMCLAPI
        DownloadLink = bangbang93_Server_jar_URL
        
        news = input(f"是否下载最新的正式版：[{MCLatestVersion}]？(Y/n):")
        if "n" in news.lower() or "否" in news.lower() or "不" in news.lower():
            os.system("cls")
            return # 直接退出函数，返回上一级

        """Retry"""
        for retry in range(3): # 3次重试
            logging.info(f'[Net] 正在下载原版服务端 {MCLatestVersion}："{DownloadLink}"') # 加冒号的原因：点名表扬愚人节快照版本id(比如 3D Shareware v1.34 会把 URL 分节而不能在 VS Code 里面打开)
            os.system("cls")
            print(f"正在下载[原版]服务端：[{MCLatestVersion}]，请稍等...")
            with requests.get(DownloadLink, stream=True) as Get_jar: # 用流式传输，因为后面的.jar可能会很大，现在的 1.21 都接近 50MB 了 
                if Get_jar.status_code == 200:
                    with open(f"Download/Temp/Vanilla_{MCLatestVersion}.jar", "wb") as jar:
                        for chunk in Get_jar.iter_content(chunk_size=81920):
                            jar.write(chunk) # 以块+二进制的方式写入到文件里
                        Jar_size = int(os.path.getsize(f"Download/Temp/Vanilla_{MCLatestVersion}.jar"))/1048576 # 转换为 MB 单位(/1024/1024 = /1024*1024)
                        logging.info(f"[Net] 获取 {MCLatestVersion}.jar 成功，大小：{Jar_size} MB")
                        print(f"{MCLatestVersion}.jar 下载成功，大小：{Jar_size:.1f}MB")
                    with open(f"Download/Temp/Vanilla_{MCLatestVersion}.jar", "rb") as f:
                        logging.info(f"[System] {MCLatestVersion}.jar 的 MD5 哈希值：" + hashlib.md5(f.read()).hexdigest())
                    """判断文件夹"""
                    if not os.path.exists("Server/[原版]"+ MCLatestVersion):
                        os.mkdir("Server/[原版]"+ MCLatestVersion)

                    """移动服务器.jar文件"""
                    shutil.move(f"Download/Temp/Vanilla_{MCLatestVersion}.jar", f"Server/[原版]{MCLatestVersion}/[原版]{MCLatestVersion}.jar") # 特意删的空格，至少减少了有空格导致的bug的发生...
                    logging.info(f"[System] {MCLatestVersion}.jar 剪切完毕，新命名：[原版]{MCLatestVersion}.jar")
                    logging.info(f"[System] 原版服务端 {MCLatestVersion} 下载完毕")
                    break
                else:
                    logging.error(f"[Net] 获取 {MCLatestVersion}.jar 失败，返回值：{Get_jar.status_code}，正在重试{retry+1}/3，每次3s...")
                    print(f"下载 {MCLatestVersion}.jar 失败，HTTP 错误代码：{Get_jar.status_code}\n正在重试{retry+1}/3，每次隔3秒...")
                    time.sleep(3) # 3秒一次
            logging.error("[Net] 三次重试次数已用完")
            print("")
            print("三次重试均为失败，请检查网络设置并重试")
    
    input("按回车返回...")
    os.system("cls")