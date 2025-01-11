"""下载 Paper 服务端"""
# 使用了 PaperMC 的 API 服务：https://api.papermc.io
import os
import requests
import Modules.Log as logging
import hashlib
import shutil
import time

def paper():
    api = "https://api.papermc.io/v2/projects/paper"
    for times in range(3):
        try:
            logging.info(f"[Net] 正在获取 Paper API，第 {times+1} 次，共3次：{api}。")
            json = requests.get(f"{api}")
            if json.status_code == 200:
                logging.info("[Net] 获取 Paper 服务端 API 成功。返回值 200。")
                break
            logging.warning("[Net] 获取 Paper 服务端 API 未成功。返回值 "+json.status_code+"。")
            retry = input("服务器返回了一个 "+json.status_code+" 状态。是否重新尝试获取？(y/n)：\n> ")
            if retry.lower() == "y":
                pass
            if retry.lower() == "n":
                break
                
        except TimeoutError:
            logging.error(f"[Net] 连接 API 超时：{api}。")
            print("连接 PaperMC API 超时，请检查网络设置。")
            time.sleep(3)
        except Exception as e:
            logging.error(f"[System] {e}")
            print(f"错误。请重试：{e}")
            time.sleep(2)

    json = json.json()
    paper_versions = json["versions"]
    os.system("cls" if os.name == "nt" else "clear")
    input("按下回车键列出 Paper 服务端 [所有] 版本：")
    for p_v in paper_versions:
        print("[*] " + p_v)
    version = input("请选择需要下载的版本，只会下载所选版本的最新稳定版，请勿输入列表中没有的版本号：\n> ")
    logging.info(f"[Report] 即将下载 Paper 服务端 jar：{version}")
    build_api = f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds"
    logging.info(f"[Net] 正在通过API获取 paper.{version}.builds ，重试次数 3/3：{build_api}")
    for times in range(3):
        try:
            build_json = requests.get(build_api)
            if build_json.status_code == 200:
                logging.info(f"[Net] 获取JSON paper.{version}.builds 成功。返回值 200。")
                build_json = build_json.json()
                break
            logging.error(f"[Net] 获取JSON paper.{version}.builds 失败。返回值 {build_json.status_code}。")
        except TimeoutError:
            logging.info(f"[Net] 获取JSON paper.{version}.builds 失败：连接超时，正在重试 {times+1}/3：{build_api}")
            time.sleep(3)
        except Exception as e:
            logging.info(f"[Net] {e}")
            print(e)
            time.sleep(2)

    latest_build = None
    for build in build_json.get("builds", []):
        if build.get("channel") == "default":
            latest_build = build.get("build") # 最新的 Paper {version} 稳定版版本构建号，如 130
            channel = "default"
        if build.get("channel") == "experimental":
            latest_build = build.get("build") # 最新的 Paper {version} experimental 版版本构建号，如 131
            channel = "exp"
    if channel == "default":
        logging.info("[Report] 将使用稳定版本进行下载。")
    if channel == "exp":
        logging.warning("[Report] 将使用实验版（experimental）下载。")
        print("\n注意：当前版本目前没有稳定版可供下载，将下载体验版（experimental），体验版可能会有风险，请悉知。")
    logging.info(f"[Report] 最新的 Paper {version} 服务端版本构建号为：{latest_build}")            
    file_name = f"paper-{version}-{latest_build}.jar"
    latest_download_api = f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{latest_build}/downloads/{file_name}"
    logging.info("[Report] 将要下载如下配置的 Paper 服务端 jar 文件：")
    logging.info(f"[Report] 服务端版本：{version}")
    logging.info(f"[Report] 服务端最新构建号：{latest_build}")
    logging.info(f"[Report] 服务端 .jar 文件名：paper-{version}-{latest_build}.jar")
    print("将要下载如下配置的 Paper 服务端 jar 文件：")
    print(f"服务端版本：{version}")
    print(f"服务端构建号：{latest_build}")
    print(f"服务端 .jar 文件名：{file_name}")
    logging.info(f"[Net] 即将下载 {file_name}：{latest_download_api}")
    continue_or_exit = input("按下回车键开始下载，按其他键取消：\n> ")
    if continue_or_exit != "":
        main()
    with requests.get(latest_download_api, stream=True) as Get_jar: # 用流式传输，因为后面的.jar可能会很大，现在的 1.21 都接近 50MB 了 
        if Get_jar.status_code == 200:
            with open(f"Download/Temp/{file_name}", "wb") as jar:
                for chunk in Get_jar.iter_content(chunk_size=81920):
                    jar.write(chunk) # 以块+二进制的方式写入到文件里
                Jar_size = int(os.path.getsize(f"Download/Temp/{file_name}"))/1048576 # 转换为 MB 单位(/1024/1024 = /1024*1024)
                logging.info(f"[Net] 下载 {file_name} 成功，大小：{Jar_size} MB。")
                print(f"{file_name} 下载成功，大小：{Jar_size:.1f}MB")
            with open(f"Download/Temp/{file_name}", "rb") as f:
                local_sha256_value = hashlib.sha256(f.read()).hexdigest()
                logging.info(f"[Report] {file_name} 的 本地文件 Sha-256 哈希值：" + local_sha256_value)
        if Get_jar.status_code != 200:
            print(f"远程服务器返回结果 {Get_jar.status_code} 而并非 200。请检查网络再试一次。")
            logging.warning(f"[Net] 远程服务器返回 {Get_jar.status_code}。")
    
    """哈希校验"""
    logging.info("[System] 开始进行哈希校验。")
    remote_sha256_value = None
    for item in build_json["builds"]: # 遍历下载过的 api-json
        if item["build"] == int(latest_build):
            remote_sha256_value = item["downloads"]["application"]["sha256"]
            break
    logging.info(f"[Report] {file_name} 的 远程服务器文件 Sha-256 哈希值：" + remote_sha256_value)
    
    if local_sha256_value != remote_sha256_value:
        logging.warning("[Report] 本地文件与远程服务器文件的 Sha-256 哈希不一致。")
        logging.warning(f"[Report] 远程服务器文件 Sha-256 哈希值：{remote_sha256_value} 。")
        logging.warning(f"[Report] 本地文件 Sha-256 哈希值：{local_sha256_value} 。")
        print("本地文件与远程服务器文件的 Sha-256 哈希不一致，这代表文件可能不完整。造成此原因一般是由于网络问题导致的，你可以再次尝试下载一次。\n如果你需要查看这两个哈希（远程和本地），查看日志即可。")
    if local_sha256_value == remote_sha256_value:
        logging.info(f"[Report] {file_name} 的哈希检验已通过，本地文件与远程服务器文件一致。")
    
    logging.info("[System] 哈希校验已结束。")
    
    """移动服务器.jar文件"""
    times = 1
    while times <= 2:
        try:
            if not os.path.exists(f"Server/[Paper]{version}"):
                os.mkdir(f"Server/[Paper]{version}")
            shutil.move(f"Download/Temp/{file_name}", f"Server/[Paper]{version}/[Paper]{version}.jar") # 特意删的空格，至少减少了有空格导致的bug的发生...
            logging.info(f"[System] {file_name} 剪切完毕，新命名：[Paper]{version}.jar")
            logging.info(f"[System] 第三方 Paper 服务端 {version} 下载完毕。")
            result = 0
            break
        except PermissionError as e:
            logging.error(f"[System] 权限错误：{e}")
            print("权限错误。请检查权限后按下回车重试。")
            result = 1
            times = times + 1
        except Exception as e:
            logging.error(f"[System] {e}")
    if result == 0:
        print("")
        print("√ 下载完毕。")
    if result == 1:
        if os.path.exists(f"Server/[Paper]{version}"):
            logging.info(f"[Report] Server/[Paper]{version} 文件夹存在。")
        else:
           logging.info(f"[Report] Server/[Paper]{version} 文件夹不存在。")
           
        if os.path.exists(f"Server/[Paper]{version}/[Paper]{version}.jar"):
            logging.info(f"[Report] Server/[Paper]{version}/[Paper]{version}.jar 文件存在。")
        else:
            logging.info(f"[Report] Server/[Paper]{version}/[Paper]{version}.jar 文件不存在。")
        
        print("")
        print("看起来你的文件并没有放到 Server 内。")
        print(f"不过你的服务端 .jar 初始文件仍然还在 Download/Temp/{file_name} 。所以你还有机会手动剪切出来使用。")

    input("按下回车键返回...")

def main():
    logging.info("[Page] DownloadServer.plugin.paper 页面已加载")
    os.system("cls" if os.name == "nt" else "clear")
    print("Paper 是一个基于 Spigot 的 Minecraft 游戏服务端，旨在大幅提高性能并提供更高级的功能和 API。")
    print("为了保护你的服务器，让你的服务器变得更加稳定和安全，MCSI 只会提供你所选的版本对应的最新稳定版下载。如需下载旧的构建版本，请前往 https://papermc.io/downloads/all 。")
    input("按下回车键继续...")
    os.system("cls" if os.name == "nt" else "clear")
    print("海内存知己，天涯若比邻\n        请稍等...") # 跟微软学的(x
    paper()
    os.system("cls" if os.name == "nt" else "clear")