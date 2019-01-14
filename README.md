# replace

### 需要配置几个环境变量
    
    export REDSHIFT_DB_URL='xxx'  
    export SERVERDB_DB_URL='xxx'  
    export MODE='xxx' (PRODUCTION 或者 DEVELOPMENT)

### 创建 venv 虚拟环境：

    python3 -m venv venv 

### 进入虚拟环境工作：

    source venv/bin/active


### 安装依赖包
    
    pip install -r requirements.txt

### 启动服务

    python manager.py runserver(测试)
    gunicorn -c  gunicorn.py -b 0.0.0.0:5000 wsgi:application (正式)
    
