# ui_pyside6
a ui platform for my program
打开方式：
dist文件下main.exe或main.py（确保安装了需要的库）
打包文件命令（确保安装pyinstaller库）：
```
pyinstaller --noconfirm --onefile --windowed --add-data "main.ui;." --add-data "resource/img.png;resource" --add-data "resource/broom.svg;resource" --add-data "resource/pause.svg;resource" -i "./resource/atom.png" main.py 
```
