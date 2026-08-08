# 簡介 
幫你的裝備計算最佳鐵砧敲裝順序，拒絕敲爛裝備從你我做起

<img width="480" alt="image" src="https://github.com/user-attachments/assets/112d91cb-295c-4c4b-a048-4dc7c664ad15" />
<br>

# 如何下載和打開
方案A: 直接下載原代碼
  - clone這個專案
  - 安裝python(此專案寫於Python 3.12.4)
  - pip install 這個專案有用到的套件
  - 打開main.py

~~方案B: 下載exe~~ (還沒發布 sor mate)
  - ~~去[這邊](https://github.com/Remintonnn/waveDoc/releases)把exe檔案抓下來(只有windows的)~~
  - ~~點下載下來的檔案兩下~~

# 使用流程
1. 於UI中選擇想敲的目標裝備
2. 選擇想敲上去的目標附魔 (預設是從頭敲起)
3. 如果不是從頭敲起或有想使用敲過的書則使用"自定義合成內容"按鈕加入自訂物品
4. 按"計算鐵砧組合方式"
6. 根據UI指示敲出你的裝 (若無解請考慮使用裝備胚胎或拆魔，更多資訊請見程式內附之說明書)
7. 📈📈📈

### 注意:
- 裝備的物品和合成步驟是分開儲存的
- 計算裝備合成步驟時間複雜度是約O=3^n, 所以要敲的書種太多可能會害計算時間炸裂


## 重要檔案簡介 (你想fork的話)
main.py - 程式入口(點這開程式)  
compileQT.bat - 用來把 QT 的 .ui 壓成 .py  
~~README.MD - Hey that's me!~~  
  
calc/calc.py - 後臺演算法  
calc/enchantments.py - 定義附魔的 data class  
calc/enchJsonGen/Ench.json - 儲存附魔資訊  
calc/enchJsonGen/enchJsonGen.py - 生成上面那個檔案用，若需新加/修改附魔的話改這個  
  
ui/mainWindow.py - 主視窗檔案  
ui/resources/QtFiles/* - Qt Designer 使用的.ui檔，和他compile出來的.py (用 Qt Designer 改完.ui後記得compile)  
