"""程序启动时加载/检查的内容"""

import os
import Modules.Log as logging

def loading():
    if os.path.exists("Logs/log.log"):
        with open("Logs/log.log", "w", encoding="utf-8") as f:
            f.write('') # 重置 Log
        logging.info('[Thread] "Modules.Loading.loading" 线程已启动')
        logging.info("[System] Log 已重置")
    
    if not os.path.exists("Download"):
        os.mkdir("Download")
        logging.info("[System] 已创建 Download 文件夹")
    
    if not os.path.exists("Download/Temp"):
        os.mkdir("Download/Temp")
        logging.info("[System] 已创建 Download/Temp 文件夹")
    
    if not os.path.exists("Server"):
        os.mkdir("Server")
        logging.info("[System] 已创建 Server 文件夹")    
    """检查 Java"""
    try:
        os.getenv("GGBond")
    except Exception as e:
        print(e)
    logging.info("[Loading] 初始化完毕")

        
        