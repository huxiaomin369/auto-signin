## 环境搭建

```sh
# 安装chrome 浏览器和驱动
# 下载对应版本
# https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json
# 以Ubuntu24系统为例
wget https://storage.googleapis.com/chrome-for-testing-public/115.0.5776.0/linux64/chrome-linux64.zip
unzip chrome-linux64.zip
sudo mv chrome-linux64 /opt/google-chrome
sudo ln -s /opt/google-chrome/chrome /usr/bin/google-chrome
# 安装依赖
sudo apt update && sudo apt install -y libnss3 fonts-liberation libasound2t64
# 测试是否安装成功
google-chrome --version  # 查看版本
google-chrome --no-sandbox --headless --disable-gpu  # 无界面模式测试
# 安装驱动
wget https://storage.googleapis.com/chrome-for-testing-public/115.0.5776.0/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
sudo mv chromedriver /usr/local/bin/  # 移动文件到系统路径
sudo chmod +x /usr/local/bin/chromedriver  # 添加可执行权限
chromedriver --version # 验证安装成功

```

## 验证码识别开源库
```sh
# 验证码识别三方库依赖
git clone https://github.com/sml2h3/ddddocr.git
cd ddddocr
python setup.py install
```

## 运行
```sh
python testOcr.py
```