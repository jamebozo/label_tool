from PIL import Image
import cairocffi as cairo
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

################################
def process( image_paths: list=None, image_titles: list=None, fig=None) -> None:
    """
    Show Matrix subplots
    Arg:
       image_paths - (list) image_paths to show
    """
    #print(filename)
    if len(image_paths) == 0:
        return
    
    if fig == None:
        plt.figure(figsize=(15,15))
    # Generate sub-image matrix
    img_num = len(image_paths)
    row_num = np.ceil(np.sqrt(img_num))

    for index in range(img_num):
        plt.subplot(row_num, row_num, index+1)

        # add sub titles
        if image_titles != None and index < len(image_titles):
            plt.gca().set_title(image_titles[index])

        # read and show sub-images
        image = mpimg.imread(image_paths[index])
        plt.imshow(image, cmap='gray')
        plt.axis('off')

    # scipy.misc.imsave(str(index)+".png", featur
    plt.show()




# set shown image size

##############################
#fig.canvas.mpl_connect('key_press_event', press)


names = ["1", "2", "3", "4"]
files = ["/home/share/datasets/ImageNet/ILSVRC2015/ILSVRC2012_img_train/images/n02127052/n02127052_4626.JPEG"] * 25 #16
#process(files, names)
