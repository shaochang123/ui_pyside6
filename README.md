# ui_pyside6
a ui platform for my program
打开方式：
dist文件下main/main.exe或运行main.py（确保安装了需要的库：pyserial,pyside6）
打包文件命令（确保安装pyinstaller库）：
```
pyinstaller --noconfirm --onedir --windowed --upx-dir="path\to\upx" --exclude-module torch --exclude-module pandas --exclude-module matplotlib --exclude-module PIL.GifImagePlugin --exclude-module scipy --add-data "Message.ui;." --add-data "Plot.ui;." --add-data "resource/img.png;resource" --add-data "resource/login.jpg;resource" --add-data "resource/broom.svg;resource" --add-data "resource/reset.svg;resource" --add-data "resource/white.jpg;resource" --add-data "resource/pause.svg;resource" --add-data "resource/icon.png;resource" --add-data "Menu.ui;." --add-data "Login.ui;." --add-data "userinfo.csv;." -i "./resource/icon.png" main.py
```
