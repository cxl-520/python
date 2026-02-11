import logging

from logs import logs


def test_logging_demo():
    logs.setup_logging(
        level=logging.DEBUG,
        report_file="report.log",
        report_level=logging.INFO,
    )
def test_logging_demo2():
    # 使用try,except.else,finally
    List_data=['北京','1','2']
    try:
        res=List_data[4]
        print(res)
        print("没有出现异常")
    except Exception as e:
        print(f"出现了未知异常。原因是:{e}")
    else:
        print("没有出现异常")
    finally:
        print("不管有没有出现异常，都打印")
    logs.debug("debug message")
    logs.info("info message")
    logs.warning("warning message")
    logs.error("error message")
    logs.critical("critical message")
