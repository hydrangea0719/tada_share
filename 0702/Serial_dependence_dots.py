# coding:utf-8
# editor : Mizuki Tada
# date : 2021/07/02

from __future__ import division
from psychopy import core, data, event, gui, logging, visual
from psychopy.hardware import keyboard
import numpy as np
import pandas as pd
import csv, os
import random

# send experiment to ruuner から走らせると，走らせている途中でコードを編集してしまうことがない
# http://www.s12600.net/psy/python/pyexp/newver.html


############################
# -- dialogbox -- #
############################

# present dialogbox & get subjectID
subj_info = {"subj_id": ""}
dialogue_box = gui.DlgFromDict(subj_info, order = ["subj_id"])

if dialogue_box.OK:
    subj_id = subj_info["subj_id"]
else:
    core.quit()

# get date
exp_date = data.getDateStr("%Y%m%d%H%M%S")

# make data folder & file
try:
    os.makedirs("data/csv")
    os.makedirs("data/log")
# フォルダが既にある場合は何もしない
except OSError:
    pass

# make file name
file_name = subj_id + "_" + exp_date
file_name_csv = os.path.join("data/csv/" + file_name + ".csv")
file_name_log = os.path.join("data/log/" + file_name + ".log")

# log file setting
file_log = logging.LogFile(file_name_log, level = logging.EXP)

# datafilesetting
with open(file_name_csv, "a", encoding = "cp932") as f:
    writer = csv.writer(f, lineterminator = "\n")
    writer.writerow([
        "subj_id","trial_N","dot_N","stim_time"])

# 表示する画面 win の設定
# http://www.s12600.net/psy/python/pyexp/api/html/visual/window.html
win = visual.Window(size=(800, 600), pos=(0, 0), color=(0, 0, 0), # pos=None を変更
colorSpace='rgb', rgb=None, dkl=None, lms=None, fullscr=None,
allowGUI=None, monitor=None, bitsMode=None, winType=None, units=None,
    gamma=None, blendMode='avg', screen=0, viewScale=None, viewPos=None,
    viewOri=0.0, waitBlanking=True, allowStencil=False, multiSample=False,
    numSamples=2, stereo=False, name='window1', checkTiming=True,
    useFBO=False, autoLog=True) # 画面を表示する
    # useFBO=False, useRetina=False, autoLog=True) 
    # ここ修正したらエラーが消えて実行できるようになった

mouse = event.Mouse()
#invisible mouse carsol
mouse.setVisible(False)

# 総試行回数．画像を何枚表示するか
trial_N = 10;

# 試行開始
ii=0
for ii in range(trial_N):

    # dot の個数．画像の枚数．
    dots_NR = random.randint(6,15) 
    # dots_NR = 1  # debug 用．画像を1枚だけ表示する．

    timer = core.Clock()
    t = timer.getTime()
    
    # 各画像の位置を1つずつ設定
    i=0
    for i  in range(dots_NR):
        # 極座標 r, theta を使用
        # random.uniform(a, b) は a, b 間の float 型の乱数を生成
        r = np.sqrt(40000*random.uniform(0, 1)); #一般に、区間 (a,b) の N 個の乱数は、式 r = a + (b-a).*rand(N,1) を使って生成できる
        theta = np.rad2deg(random.uniform(-1, 1)*np.pi); #-pi_pi random
        jitterx = random.uniform(-40,40);  # 配置にランダム性を持たせる 
        jittery = random.uniform(-40,40);
        x = r * np.cos(theta) + jitterx;  # 最終的な画像の座標
        y = r * np.sin(theta) + jittery;
        
        # dot の情報
        # dot = visual.Circle(win, radius=6, edges=60, units='pix', lineWidth=0.5, lineColor=None,
        # lineColorSpace=None, fillColor="black", fillColorSpace=None,
        # pos=(x, y), size=1.0, ori=0.0, opacity=None, contrast=1.0,
        # depth=0, interpolate=True, lineRGB=False, fillRGB=False,
        # name=None, autoLog=None, autoDraw=False, color=None, colorSpace='rgb') # 形状
        # dot.draw() # 2. 刺激の描画
        
        # 画像（硬貨）の種類
        # どの硬貨を上限何枚まで表示するか List を作り，順番をシャッフルする．先頭から順に表示する．
        image_type = ['1yen.png'] * 16 + ['5yen.png'] * 3  + ['10yen.png'] * 16  # + ['50yen.png'] * 0  + ['100yen.png'] * 0 + ['500yen.png'] * 0
        random.shuffle(image_type)
        
        # 画像の設定．
        # http://www.s12600.net/psy/python/pyexp/api/html/visual/imagestim.html
        # pop() を使って，List の要素を取り出している．
        image = visual.ImageStim(
        win, image=image_type.pop(), mask=None, units='pix',
        pos=(x, y), size=100.0, ori=0.0, color=(1.0, 1.0, 1.0),  # pos は刺激の中心の座標，ori は回転角度，size は要調整
        colorSpace='rgb', contrast=1.0, opacity=None, depth=0,  
        interpolate=False, flipHoriz=False, flipVert=False, texRes=128,  
        name=None, autoLog=None, maskParams=None)
        
        # 画像の名前
        stim_name = "Stim_"+str(ii) +".png"
        
        # 画像を描画する
        image.draw()
        
    # end for
    

    t2 = timer.getTime()
    win.flip();
    win.getMovieFrame(buffer="front")
    win.saveMovieFrames(stim_name,clearFrames=True)  # 刺激を画像形式で保存

    s_t = timer.getTime(); #  画面に反映 start time
    core.wait(0.75) # 表示時間 0.5 ~ 0.75 くらいが適切？
    win.flip()
    e_t = timer.getTime(); # 画面を閉じる end time
    stim_time = e_t - s_t;
    core.wait(1.0) # 試行と試行の間の時間

    with open(file_name_csv, "a", encoding = "cp932") as f:
            writer = csv.writer(f, lineterminator = "\n")
            writer.writerow([subj_id,ii,dots_NR,stim_time])
logging.flush()

win.close()
core.quit()


# error 
# -> self.backend.close()  # moved here, dereferencing the window prevents
# AttributeError: 'NoneType' object has no attribute 'close'
# self (?) の type が None になりえて，その場合に落ちてしまう？
# 例外処理を追加するとうまくいくかも

# window.py 
# if sys.platform == 'win32':
#   def close(self):
#       self.backend.close()  # moved here, dereferencing the window prevents
#       # backend specific actions to take place
