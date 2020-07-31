from show import *
import csv
import cairocffi as cairo
import matplotlib
#matplotlib.use('GTK3CairoTkAgg')
#matplotlib.use('GTK3Cairo')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os
import csv
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input",  type=str, default="",help="input_file")
parser.add_argument("-o", "--outfile", type=str, default="",help="Output directory")
parser.add_argument("-s", "--start",  type=int, default=0, help="Start frame")
args = parser.parse_args()

img_size = 4
cc_label = ['boxes', 'pets', 'car', 'person']

class LabelTool():

    def __init__(self):
        # init var
        self.out_dic = defaultdict(list)         
        self.file_dic = {}

        # init func
        self.init_dic()
        self.init_input()
        
        return

    #############################################################
    def init_input(self):
        # check input txt
        _path = args.input
        assert(os.path.exists(_path))

        _file = open(_path, "r")
        paths, labels = self.read_file(_file)
        #print(paths)
        self.press_to_show_next(paths, labels)

    #############################################################
    def init_dic(self):       
        out_file = args.outfile #"myout.txt"
        out_file = os.path.split(out_file)[-1].split('.')
        try:
            print("==> file exists, read paths and labels")
            for _level in ["easy", "midd", "hard"]:

                # open existing file
                _file = open(f'{out_file[0]}_{_level}.txt', "r+")
                self.file_dic[_level] = _file
                print("add") 
                # read paths,labels and add to dic
                paths, labels = self.read_file(_file)
                print("get paths")
                for p, l in zip(paths, labels):
                    
                    self.out_dic[_level].append(f'{p},{l}\n')
                    print("found")
            #print(self.out_dic)

        except:            
            print("==> file not found, create new")
            self.file_dic['easy'] = open(out_file[0]+"_easy."+out_file[1], "w+")
            self.file_dic['midd'] = open(out_file[0]+"_midd."+out_file[1], "w+")
            self.file_dic['hard'] = open(out_file[0]+"_hard."+out_file[1], "w+")



    ###############################################################
    def read_file(self, inp):
        fieldnames = ['path', 'label']
        reader = csv.DictReader(inp, fieldnames=fieldnames)
        #writer = csv.DictWriter(out, fieldnames=fieldnames)
        #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #labels = []
        #for row in reader:
        #    labels.append(row['label'])
        paths, labels = [], [] 
        for row in reader:
            paths.append(row['path'])
            labels.append(row['label'])
        return paths, labels
        

    ###############################################################
    def press_to_show_next(self, paths: list=None, labels: list=None):

        # paths, labels = paths
        if paths == None:
            print("xxxxx paths")
            return
        
        # global cnt
        cnt = [args.start]
        lst_show = [""]
        lst_save = []

        fig, ax = plt.subplots()
        # print(paths[args.start])
        image = mpimg.imread(paths[args.start])
        #im = ax.imshow(image, vmin=0, vmax=1, cmap='gray')
        #ax.text(0.3, 0.3, "hhhhhh")
        im = ax.imshow(image,  cmap='gray')
        lst_show[0] = f'{paths[cnt[0]]},{labels[cnt[0]]}\n'
        fig.suptitle(f'lab: {labels[cnt[0]]}  cnt: {cnt[0]}\n')
        fig.text(0.0, 0.02, ' Shortcut \n (j): easy  (k) midd,  (l) hard  (u) undo (y) save (n) just preview', fontsize=8)
        fig.set_size_inches(img_size,img_size)
        print("show: ", cnt[0], paths[cnt[0]])

        
        out_dic = defaultdict(list)
        ################################
        def dump_all():
            # write to easy 
            for line in out_dic['easy']: # list
                self.file_dic['easy'].write(line)
            out_dic['easy'] = []
            
            # write to midd 
            for line in out_dic['midd']: # list
                self.file_dic['midd'].write(line)
            out_dic['midd'] = []

            # write to hard 
            for line in out_dic['hard']: # list
                self.file_dic['hard'].write(line)
            out_dic['hard'] = []

        ################################
        def next_image(evt=None):
            # show next image every keystroke
            n = evt.key
            print("========================")
            print("You pressed {}".format(n))
            key_dic = {'easy':'j', 'midd':'k', 'hard':'l', 'undo':'u', 'save':'y', 'next': 'n'}
            if n not in key_dic.values():
                return
            # press keys to action
            if n == key_dic['easy']: 
                # write to ok
                print(f"add easy: {lst_show[0][:-1]}")
                lst_save.append(lst_show[0])
                out_dic['easy'].append(lst_show[0])

            if n == key_dic['midd']: 
                # add to ok
                print(f"add midd: {lst_show[0][:-1]}")
                lst_save.append(lst_show[0])
                out_dic['midd'].append(lst_show[0])

            elif n == key_dic['hard']:
                print(f"add hard: {lst_show[0][:-1]}")
                # write to not
                lst_save.append(lst_show[0])
                out_dic['hard'].append(lst_show[0])
            
            elif n == key_dic['undo']:    
                # undo last label
                print("*****undo*****")
                #print(f'lst: {lst_show[0]}')
                #print(out_dic)
                if len(lst_save) == 0:
                    print("nothing to undo xxxx")
                    return
                _lst_save = lst_save.pop()
                if len(out_dic['easy']) > 0 and (_lst_save in out_dic['easy']):
                    print("last easy pop")
                    print(out_dic['easy'].pop(), _lst_save)
                if len(out_dic['midd']) > 0 and (_lst_save in out_dic['midd']):
                    print("last midd pop")
                    print(out_dic['midd'].pop(), _lst_save)
                elif len(out_dic['hard']) > 0 and (_lst_save in out_dic['hard']):
                    print("last hard pop")
                    print(out_dic['hard'].pop(), _lst_save)

                # rewind cnt
                cnt[0]-=2

            elif n == key_dic['save']:
               # dump and pop all
               dump_all()
               return       
                                    
            # show next image
            #print("You pressed {}".format(n))
            fig.set_size_inches(img_size,img_size)
            if cnt[0] < len(paths)-1:
                cnt[0] += 1
                print("show: ", cnt[0], paths[cnt[0]])
                lst_show[0] = f'{paths[cnt[0]]},{labels[cnt[0]]}\n'
                assert(os.path.exists(paths[cnt[0]]))
                image = mpimg.imread(paths[cnt[0]])
                im.set_array(image)

                # show title if available
                if labels != None and cnt[0] < len(labels):
                    print("add title..........")
                    fig.suptitle(f'lab: {labels[cnt[0]]}  cnt: {cnt[0]}')
          
                print("draw..........")
                fig.canvas.draw_idle()
            else:
                dump_all()
                plt.close()

        fig.canvas.mpl_connect("key_press_event", next_image)
        plt.show()

##############################
#print(paths)
LabelTool()



# open outfile

#print(list(reader['path']))


#for 
#
#for line in inp:
#    sp = line.split(",")
 #   print(sp[0], sp[1])
#


                                                                        

