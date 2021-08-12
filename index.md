## 簡介

我們利用**語音辨識（speech recognition）**、**場景辨識（scene recognition）** 的人工智慧模型，加上**顏色辨識（color recognition）** 和**方位辨識（orientation recognition）** 的演算法，結合裝置內的**三軸加速器（tri-axial accelerometer）**，建立一個能在台北捷運內輔助 GPS 系統以增加自身定位精準度的系統，並利用 **Flask** 和 **React** 建立一個能讓使用者能輕易使用的網站。

## 動機

在搭乘台北捷運的時候，往往會發現自己在 Google Map 上的定位與自己實際所在的位置具有相當大的落差，甚至當捷運行駛在地底下時，手機會完全接收不到 GPS 的信號而造成自己的定位一直停留在某個捷運站。
而原本想以「一日生活Vlog」作為專題題目的我們，在記錄了一天的生活足跡後也發現了這個問題的嚴重性，因此決定改以「改進捷運內 GPS 定位」作為研究的方向。

## 系統架構

![System Structure](https://user-images.githubusercontent.com/31942629/128692283-1cb2b308-ca9a-4438-a96e-3ec3806fdbf2.jpg)

## 系統原理

### 語音辨識 Speech Recognition

捷運行駛時，每當抵達下一站前，車廂內皆會以國語、台語、客家語和英文廣播捷運站的站名。我們將由 client 端裝置錄音下來的音訊片段傳給 server，server 利用 python 套件 speech_recognition，查看辨識出來的句子中是否有任一捷運站的名稱。若有，則將使用者的經緯度位置更新成被辨認出的捷運站經緯度，並傳回 client 端更新使用者在自己裝置地圖上的位置。

### 場景辨識 Scene Recognition

當使用者於搭乘捷運中途下車轉車或是因搭過頭而搭回去的狀況，我們利用 Google Teachable Machine 訓練出來的模型，辨別 client 端裝置拍攝並傳回給 server 的照片，判斷使用者此時位於捷運站裡或是捷運車廂內。

### 顏色辨識 Color Recognition

當使用者被辨別為在車站內，此時我們已知使用者位於某一捷運站內，也知道此捷運站有哪些轉乘線，因此我們利用 OpenCV 計算 client 端裝置拍攝並傳回給 server 的照片裡哪一條線代表的顏色的 pixel 數量較多（我們假設使用者此時面對自己即將要搭乘的車廂，且照片有拍攝到此條線），藉以判斷使用者接下來將搭乘的線路。

### 方位辨識 Orientation Recognition

承接上面，此時僅知道使用者欲搭乘的線路，但無法得知搭乘的方向，因此我們透過讀取使用者裝置內的三軸加速感應器的讀數，得到使用者此時面對的方位，再對應到已知捷運站各個線路相對應的方位表，藉此判斷使用者欲搭乘車廂行駛的方向。


### 測試 Testing

資料連結： [link](https://drive.google.com/drive/folders/1OgLQpNjG0bWfe8qfvyGSzIl5n7Z6d7b-?usp=sharing)

測試結果：
- 語音辨識：
  - 從台大醫院到蔡寮8站，共辨識出0站，準確率0%
  - 差，捷運雜音太大，導致廣播聲音過小，偵測不出車站名稱
- 場景辨識：
  - 未準確統計，但相同model使用google teachable machine皆可辨識出來。
  - 優，手動測試大部分照片都有辨別出捷運上與車站內
- 顏色辨識：
  - 未準確統計
  - 跟圖片清楚程度有關
  - 佳，只有特別挑選的圖片才有辨識出顏色
- 方位辨識：
  - 每秒紀錄數十筆資料，每次皆緩慢調整bearing
  - 經友人建議可以用websocket的方式實時傳送數據給server，不須多次重複傳送資料
  - 優，經過測試方位辨識非常精準

## Welcome to GitHub Pages

You can use the [editor on GitHub](https://github.com/momo1106github/GPS_Improvement_System_inside_Taipei_MRT/edit/gh-pages/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/momo1106github/GPS_Improvement_System_inside_Taipei_MRT/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
