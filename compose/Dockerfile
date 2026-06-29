FROM python:3.11-slim

WORKDIR /app

# 由于飞牛UI隔离机制，我们只在构建时拷贝 requirements.txt
COPY requirements.txt .

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt

EXPOSE 11400

# 运行时通过 volume 挂载加载代码
CMD ["python", "compose/server.py"]
