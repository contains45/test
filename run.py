import os
import subprocess
import sys
import time

file_name = "xm"                          # 可执行程序名
log_file = "log.txt"                       # 日志文件路径
def println(text):
    try:
        if 'streamlit' not in sys.modules:
            import streamlit as st
        else:
            st = sys.modules['streamlit']
        st.write(text)
    except ImportError:
        print(text)

# 启动程序并记录日志
def start_program_with_logging(file_path):
    process = subprocess.Popen(
        [file_path],  # 执行的文件
        stdout=subprocess.PIPE,  # 捕获标准输出
        stderr=subprocess.PIPE,  # 捕获错误输出
        text=True,  # 输出以文本方式返回
        bufsize=1,  # 逐行刷新缓冲区
        universal_newlines=True,  # 确保输出是字符串形式
        start_new_session=True
    )
    
# 持续读取日志内容并显示
def read_log_file(log_path: str, interval: float = 0.5):
    """
    模拟 `tail -f`，持续读取日志文件内容并显示到 Streamlit。
    """
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
       # f.seek(0, os.SEEK_END)  # 移动到文件尾
        while True:
            line = f.readline()
            if not line:
                time.sleep(interval)  # 没有新内容，等待一会儿
                continue
            println(line)  # 显示到 Streamlit 界面

# 主逻辑
def main():
    file_path = os.path.join(os.getcwd(), file_name)
    log_path = os.path.join(os.getcwd(), log_file)
    println(f"日志文件路径：`{log_path}`")
    println(str(os.listdir('.')))
    # 确保赋予执行权限
    try:
        os.chmod(file_path, 0o755)
    except Exception as e:
        println(f"无法设置执行权限：{e}")
        return

    # 判断日志文件是否存在
    if os.path.exists(log_path):
        println("检测到日志文件存在，Nyako会直接读取它的内容喵～")
    else:
        println("日志文件不存在，Nyako会先启动程序并生成日志喵～")
        try:
            start_program_with_logging(file_path)
            println("程序启动成功，Nyako会开始读取日志内容喵～")
        except Exception as e:
            println(f"启动程序失败：{e}")
            return
    try:
        read_log_file(log_path)
    except Exception as e:
        println(f"读取日志文件失败：{e}")

if __name__ == "__main__":
    main()
