# coding: utf-8
# need: ffmpeg
import re
import subprocess
import sys
import os
import glob
import util

# ログ設定
logger = util.get_shared_logger()

# ルート配下の全mp4ファイルパスを取得
args = sys.argv
rootdir = args[1]
mp4files = glob.glob(rootdir + "/**/*.mp4", recursive=True)
logger.info("Start [add chapter]")
logger.info("mp4files:{}".format(mp4files))

for mp4file in mp4files:
    mp4dir = os.path.dirname(mp4file)
    mp4fname = os.path.basename(mp4file)
    mp4fnamenoext = os.path.splitext(mp4fname)[0]
    chapfname = mp4fnamenoext + ".chapters.txt"
    chapfile = os.path.join(mp4dir, chapfname)
    logger.debug("mp4dir:{}, mp4fname:{}, mp4fnamenoext:{}".format(mp4dir, mp4fname, mp4fnamenoext))

    # チャプター未登録か確認  /////////////////////////////////////////////////////////////////////
    command = 'mp4chaps -l \'{}\''.format(mp4file)
    logger.debug("get chapter cmd:{}".format(command))
    ret_str = subprocess.run(command, shell=True, capture_output=True, text=True).stdout
    if "Chapter" in ret_str:
        # すでにチャプターあり
        logger.info("already has chapter: {}".format(mp4file))
        next

    # チャプター登録のため<movie>.chapters.txt作成  /////////////////////////////////////////////////////
    ### 最大値を求める ###
    command = 'mp4info \'{}\' | grep "hvc1.*secs"'.format(mp4file)
    logger.debug("get duration cmd :{}".format(command))
    duration_str = subprocess.run(command, shell=True, capture_output=True, text=True).stdout
    logger.debug("got duration :{}".format(duration_str))
    x = re.search(r"hvc1, (\d+).(\d+) secs(.*)", duration_str)
        # 1	video	hvc1, 4595.591 secs, 636 kbps, 1280x720 @ 29.970030 fps

    secs = int(x.group(1))
    max_num = int(secs/300) + 1
    logger.debug("max_num ={}".format(max_num))

    ### movie.chapters.txt作成 ###
    with open(chapfile, mode="w") as f:
        for num in range(0, max_num):
            h = int(num / 12)
            mm = int(num *5 % 60)
            title = num + 1
            f.write("{:02d}:{:02d}:00.000 Chapter{}\n".format(h, mm, title))
                    #00:00:00.000 チャプター名1


    # チャプター登録  /////////////////////////////////////////////////////
    command = 'mp4chaps -i \'{}\''.format(mp4file)
    duration_str = subprocess.run(command, shell=True, capture_output=True, text=True).stdout

logger.info("End [add chapter]")
