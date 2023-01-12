import streamlit as st
import os

st.title('Multiple Images')

#絶対パスを取得  自分の場合C:\Users\dy574\OneDrive\公開\デスクトップ\プログラミング練習\streamlit\images
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
print(PROJECT_PATH)

#画像保存フォルダのパスを取得
image_dir = os.path.join(PROJECT_PATH,'images')
print(image_dir)

# 画像ファイルのリストを取得
fName_list = os.listdir(image_dir)

#画像ファイル数
print(len(os.listdir(image_dir)))
img_file_num = len(os.listdir(image_dir))

#multiple images　Grid表示

idx = 0


# ---- memo -----------------------
# フォルダの中にある画像の中で
# 類似したものを見つける
# ---------------------------------


# pip install opencv-python-headless
from PIL import Image
import cv2
from sys import argv
from glob import glob
from itertools import combinations
import subprocess as sb
from os import environ

METHOD_NAME = ['Correlation', 'Chi-square', 'Intersection', 'Bhattacharyya distance']
THRESHOLD_DEF = [0.9, 100000, 1600000, 0.15]

# environment variable
METHOD = int(environ.get('METHOD', 3))
THRESHOLD = float(environ.get('THRESHOLD', THRESHOLD_DEF[METHOD]))


__doc__="""
Usage:
    [METHOD=(int)] [THRESHOLD=(float)] python3 {f} folder_name
    environment variable
    METHOD:
        0: Correlation
        1: Chi-square
        2: Intersection
        3: Bhattacharyya distance <- Default
    THRESHOLD:
        estimated THRESHOLD
        METHOD = 0 -> 0.88 ~ 1 (Default is 0.9)
        METHOD = 1 -> 80000 ~ 120000 (Default is 100000)
        METHOD = 2 -> 1200000 ~ 2000000 (Default is 1600000)
        METHOD = 3 -> 0.05 ~ 0.2 (Default is 0.15)
    exsample)
        METHOD=0 python3 {f} folder_name
        METHOD=3 THRESHOLD=0.2 python3 {f} folder_name
""".format(f=__file__)

def usage():
    # print('Usage:\n\t[THRESHOLD=(float)] [METHOD=(int)] python3 {f} folder_name'.format(f=__file__))
    print(__doc__)
    exit()

def matching():
    print('METHOD: {}'.format(METHOD_NAME[METHOD]))
    print('THRESHOLD: {}'.format(THRESHOLD))

    # 画像リストの作成(gifは除外)
    Pictures = glob('{folder}/*'.format(folder=FolderName))
    Pictures[:] = [pict for pict in Pictures if pict.split('.')[-1] != 'gif']
    
    # ヒストグラムの計算
    image_hists = dict()
    for picture in Pictures:
        im = cv2.imread(picture)
        image_hists[picture] = cv2.calcHist([im], [0], None, [256], [0, 256])
    
    # 類似度の計算
    result = list()
    for pictA, pictB in combinations(Pictures, 2):
        image_histA, image_histB = image_hists[pictA], image_hists[pictB]
        tmp = cv2.compareHist(image_histA, image_histB, METHOD)
        if METHOD in [1, 3]:
            if tmp < THRESHOLD:
                result.append((tmp, pictA, pictB))
        else:
            if tmp > THRESHOLD:
                result.append((tmp, pictA, pictB))


    # 連結成分の計算
    repr_dict = dict()
    pict2repr = dict()
    for _, nodeA, nodeB in result:
        is_A, is_B = nodeA in pict2repr, nodeB in pict2repr
        if not is_A and not is_B:
            repr_dict[nodeA] = [nodeA, nodeB]
            pict2repr[nodeA] = nodeA
            pict2repr[nodeB] = nodeA
        if is_A and not is_B:
            repr_dict[pict2repr[nodeA]].append(nodeB)
            pict2repr[nodeB] = pict2repr[nodeA]
        if not is_A and is_B:
            repr_dict[pict2repr[nodeB]].append(nodeA)
            pict2repr[nodeA] = pict2repr[nodeB]
        if is_A and is_B:
            if pict2repr[nodeA] == pict2repr[nodeB]:
                continue
            repr_dict[pict2repr[nodeA]] += repr_dict[pict2repr[nodeB]]
            for pict in repr_dict[pict2repr[nodeB]]:
                pict2repr[pict] = pict2repr[nodeA]

    # 結果の出力
    # 類似画像なし
    if len(result) == 0:
        print('Same pictures are not found.')
        exit()

    # 類似画像あり
    print('Maybe same pictures ...')
    for i, _repr in enumerate(set(pict2repr.values())):
        print('[{}] {}'.format(i, ' '.join(repr_dict[_repr])))

    # 画像をOpenするかどうか
    print('Open those?(y or n)')
    ans = input()
    if ans in ['y', 'yes']:
        for _repr in set(pict2repr.values()):
            component = repr_dict[_repr]
            sb.run(['open'] + component)

    return 1

if __name__ == '__main__':
    if len(argv) == 2 and argv[1] not in ['-h', '--help']:
        FolderName = argv[1] if argv[1][-1] != '/' else argv[1][:-1]
        matching()
    else:
        usage()

for _ in range(len(fName_list)-1):
    cols = st.columns(4)

    if idx < len(fName_list):
        cols[0].image(f'./images/{fName_list[idx]}',width=150, caption=fName_list[idx])
        print(os.path.join(image_dir, fName_list[idx]))
        idx += 1
    if idx < len(fName_list):
        cols[1].image(f'./images/{fName_list[idx]}',width=150, caption=fName_list[idx])
        idx += 1
    if idx < len(fName_list):
        cols[2].image(f'./images/{fName_list[idx]}',width=150, caption=fName_list[idx])
        idx += 1
    if idx < len(fName_list):
        cols[3].image(f'./images/{fName_list[idx]}',width=150, caption=fName_list[idx])
        idx += 1
    else:
        break
