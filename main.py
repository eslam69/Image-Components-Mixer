from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox  
from gui import Ui_MainWindow
from imageModel import ImageModel
from modesEnum import Modes

import cv2 as cv
import numpy as np
import sys
import os
import qdarkgraystyle
import logging


logging.basicConfig(filename="D:\!Dsp\sbe309-2020-task3-eslam69\LogFileMixer.txt", format='%(asctime)s %(message)s', filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.msg = QMessageBox() 


       


        ################# control lists  ##################
        self.plots = [self.ui.widget , self.ui.widget_2 ,self.ui.widget_3 ,self.ui.widget_4 ,self.ui.widget_5 , self.ui.widget_6]
        self.combos = [self.ui.comboBox , self.ui.comboBox_2, self.ui.comboBox_3 , self.ui.comboBox_6 ,self.ui.comboBox_5]
        self.radioButtons = [self.ui.radioButton_2 , self.ui.radioButton ,self.ui.radioButton_3 , self.ui.radioButton_4]
        self.gains = [self.ui.horizontalSlider_3 , self.ui.horizontalSlider_2]
        self.gains[0].setEnabled(False)
        self.gains[1].setEnabled(False)
        for i in range(len(self.radioButtons)) :
            self.radioButtons[i].setEnabled(False)


        ####################################################


        for i in range(len(self.plots)) :
            self.plots[i].ui.histogram.hide()
            self.plots[i].ui.roiBtn.hide()
            self.plots[i].ui.menuBtn.hide()
            self.plots[i].ui.roiPlot.hide()

        self.pictureModes= ['','Magnitude','Phase','Real component','Imaginary component']
        self.mixModes = [ '','Magnitude', 'Phase', 'Real', 'Imaginary', 'uniform magnitude' , 'uniform phase']
        self.ui.comboBox.addItems(self.pictureModes)
        self.ui.comboBox_2.addItems(self.pictureModes) 
        self.ui.comboBox_5.addItems(self.mixModes)
        self.ui.comboBox_6.addItems(self.mixModes)

        
       
        ###### disable the 5 comboBoxes ##############
        

        for i in range(len(self.combos)) :
            self.combos[i].setEnabled(False)
        self.combos[2].addItems(['Output 1'  , 'Output 2'])

        ######### default radiobuttons #########
        #self.radioButtons[0].setChecked(True)
        #self.radioButtons[3].setChecked(True)

        ############# signals of first 3 combos  
        self.combos[0].currentIndexChanged.connect(lambda  : self.draw_component(0,1 , self.combos[0].currentText() ))
        self.combos[1].currentIndexChanged.connect(lambda  : self.draw_component(1,3, self.combos[1].currentText() )) 
        self.combos[2].currentIndexChanged.connect(lambda  : self.current_output() )
        #self.output_widget =self.plots[4] 

        for i in range(len(self.radioButtons)) :  ### radio buttons sources of coponents check
            self.radioButtons[i].toggled.connect(lambda : self.check_sources() )

        ###### Combo Box dynamic Ui 
        self.combos[3].currentIndexChanged.connect(lambda  : self.update_options(3,4) ) 
        #self.combos[4].currentIndexChanged.connect(lambda  : self.update_options(4,3) )




        self.ui.actionOpen.triggered.connect(lambda : self.open(1) )
        self.ui.actionLoad_Image_2.triggered.connect(lambda : self.open(2) )
        self.ui.actionLoad_Image_2.setDisabled(True)


        self.gains[0].sliderReleased.connect(lambda :self.draw()) 
        self.gains[1].sliderReleased.connect(lambda :self.draw()) 





    def open(self , number) :
        fname = QtGui.QFileDialog.getOpenFileName( self, 'choose the image', os.getenv('HOME') ,"Images (*.png *.xpm *.jpg)" )
        self.path = fname[0] 
        if self.path =="" :
            return
        self.read(self.path , number)

    def read(self, path , number) :
        image = ImageModel(path)

        if 1 == number : 
            self.current_size = image.shape
            self.image1= image
            self.plots[0].show()
            self.plots[0].setImage(self.image1.imgByte.T)
            self.ui.comboBox.setEnabled(True)
            self.combos[2].setEnabled(True)
            self.combos[3].setEnabled(True)
            self.combos[4].setEnabled(True)

            self.images = [self.image1 ]
            self.ui.actionLoad_Image_2.setDisabled(False)

            logger.info("image 1 read, from path:"+str(path))

        elif 2==number :
            if image.shape != self.current_size :
                print('error not the same size')
                logger.error("file 2 opened not the same size of file 1")
                self.msg.setWindowTitle("Error in Image Size")
                self.msg.setText("The 2 images must have the same size")
                self.msg.setIcon(QMessageBox.Warning)
                x = self.msg.exec_()
                return

            else:
                self.image2= image
                self.plots[2].show()
                self.plots[2].setImage(self.image2.imgByte.T)
                self.ui.comboBox_2.setEnabled(True)
                self.images = [self.image1 , self.image2 ]
                for i in range(len(self.radioButtons)) :
                    self.radioButtons[i].setEnabled(True)
                self.gains[0].setEnabled(True)
                self.gains[1].setEnabled(True) 
                logger.info("image 2 read, from path:"+str(path) )

            self.check_sources()
            self.current_output()



    def draw_component(self,imageOriginalNum,imageBoxNum , mode) :
        self.plots[imageBoxNum].show() 
        print(mode)


        if mode == self.pictureModes[1] :
            self.plots[imageBoxNum].setImage(20*np.log(self.images[imageOriginalNum].magnitude.T))
            logger.info(" plot Magnitude of image {} ".format(imageBoxNum) )

            #print(mode)
        elif mode == self.pictureModes[2] :
            self.plots[imageBoxNum].setImage(self.images[imageOriginalNum].phase.T)
            logger.info(" plot phase of image {} ".format(imageBoxNum) )
             
        elif mode == self.pictureModes[3] :
            self.plots[imageBoxNum].setImage(20*np.log(self.images[imageOriginalNum].real.T))
            logger.info(" plot real component of image {} ".format(imageBoxNum) )

        elif mode ==self.pictureModes[4] :
            self.plots[imageBoxNum].setImage(self.images[imageOriginalNum].imaginary.T) 
            logger.info(" plot imaginary componenet of image {} ".format(imageBoxNum) )


    def current_output(self) :
        if self.combos[2].currentText() == 'Output 1' :
            self.output_widget = self.plots[4]

        elif self.combos[2].currentText() == 'Output 2' :
            self.output_widget = self.plots[5]
    
    def check_sources(self) :
        if self.radioButtons[0].isChecked()==True :
            self.source1 = self.image1
        else :
            self.source1 =self.image2
        
        if self.radioButtons[3].isChecked() == True :
            self.source2 = self.image2 
        else :
            self.source2 =self.image1
 #self.mixModes = [ '','Magnitude', 'Phase', 'Real', 'Imaginary', 'uniform magnitude' , 'uniform phase']
    def update_options(self,first,second) :
        

        if self.combos[first].currentText() == "Magnitude"  : # options : phase 2 , uniform phase 6
            
            for i in range(1,len(self.combos[second])) : ##hide all options then we add acceptable options 
                self.combos[second].view().setRowHidden(i,True)
            self.combos[second].view().setRowHidden(2,False)
            self.combos[second].view().setRowHidden(6,False) 
        elif self.combos[first].currentText() == "Phase" : # options : Magnitude 1 , Uniform magnitude 5
            for i in range(1,len(self.combos[second])) : ##hide all options then we add acceptable options 
                self.combos[second].view().setRowHidden(i,True)
            self.combos[second].view().setRowHidden(1,False)
            self.combos[second].view().setRowHidden(5,False) 
            logger.info("select phase mode")
        elif self.combos[first].currentText() == "Real" : # options :imaginary 4
            for i in range(1,len(self.combos[second])) : ##hide all options then we add acceptable options 
                self.combos[second].view().setRowHidden(i,True)
            self.combos[second].view().setRowHidden(4,False)
            logger.info("select imaginary mode")
            
        elif self.combos[first].currentText() == "Imaginary" : # options :Real 3
            for i in range(1,len(self.combos[second])) : ##hide all options then we add acceptable options 
                self.combos[second].view().setRowHidden(i,True)
            self.combos[second].view().setRowHidden(3,False)
            logger.info("select real mode")
        elif self.combos[first].currentText() == "uniform magnitude" : # options :  phase 2 , uniform phase 6
            for i in range(1,len(self.combos[second])) : ##hide all options then we add acceptable options 
                self.combos[second].view().setRowHidden(i,True)
            self.combos[second].view().setRowHidden(2,False)
            self.combos[second].view().setRowHidden(6,False) 
            logger.info("select uniform magnitude mode")
        elif self.combos[first].currentText() == "uniform phase" : # options : Magnitude 1 , Uniform magnitude 5
            for i in range(1,len(self.combos[second])) : ##hide all options then we add acceptable options 
                self.combos[second].view().setRowHidden(i,True)
            self.combos[second].view().setRowHidden(1,False)
            self.combos[second].view().setRowHidden(5,False)
            logger.info("select uniform pahse mode")
        #elif self.combos[first].currentText() == '' : # show all options in the other combo if blanck is pressed
        #    for i in range(7) : ##show all
        #        self.combos[second].view().setRowHidden(i,False)
        #    for i in range(7) : ##show all 
        #            self.combos[first].view().setRowHidden(i,False)
 #self.mixModes = [ '','Magnitude', 'Phase', 'Real', 'Imaginary', 'uniform magnitude' , 'uniform phase']

    def draw(self) :
        ratio1= self.gains[0].value() /100
        ratio2= self.gains[1].value() /100
        logger.info("gain vlaues :" ,ratio1,ratio1)

        if self.combos[3].currentText() == 'Magnitude' and self.combos[4].currentText()  == 'Phase' :

            data = self.source1.mix(self.source2,ratio1,ratio2, Modes.magnitudeAndPhase )
            self.output_widget.show()
            self.output_widget.setImage(20*np.log(data.T))
            #self.output_widget.setImage(data.T)

        elif self.combos[3].currentText() == 'Real' and self.combos[4].currentText()  == 'Imaginary' :

            data = self.source1.mix(self.source2,ratio1,ratio2, Modes.realAndImaginary )
            self.output_widget.show()
            self.output_widget.setImage(20*np.log(data.T))

        elif self.combos[3].currentText() == 'Magnitude' and self.combos[4].currentText()  == 'uniform phase' :

            data = self.source1.mix(self.source2,ratio1,ratio2, Modes.magnitudeAndUniformPhase )
            self.output_widget.show()
            self.output_widget.setImage(20*np.log(data.T))
        
        elif self.combos[3].currentText() == 'uniform magnitude' and self.combos[4].currentText()  == 'Phase' :

            data = self.source1.mix(self.source2,ratio1,ratio2, Modes.uniformMagnitudeAndPhase )
            self.output_widget.show()
            self.output_widget.setImage(20*np.log(data.T))
        
        elif self.combos[3].currentText() == 'Phase' and self.combos[4].currentText()  == 'Magnitude' :

            data = self.source1.mix(self.source2,ratio2,ratio1, Modes.magnitudeAndPhase )
            self.output_widget.show()
            self.output_widget.setImage(20*np.log(data.T))

        elif self.combos[3].currentText() == 'Imaginary' and self.combos[4].currentText()  ==  'Real':

            data = self.source1.mix(self.source2,ratio2,ratio1, Modes.realAndImaginary )
            self.output_widget.show()
            self.output_widget.setImage(20*np.log(data.T))

        elif self.combos[3].currentText() =='uniform phase' and self.combos[4].currentText()  ==  'Magnitude' :

            data = self.source1.mix(self.source2,ratio2,ratio1, Modes.magnitudeAndUniformPhase )
            self.output_widget.show()
            self.output_widget.setImage(20*np.log(data.T))
        
        elif self.combos[3].currentText() =='Phase'  and self.combos[4].currentText()  ==  'uniform magnitude':

            data = self.source1.mix(self.source2,ratio2,ratio1, Modes.uniformMagnitudeAndPhase )
            self.output_widget.show()
            self.output_widget.setImage(20*np.log(data.T))
            





            


        






def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__))) # to load the directory folder
    app = QtWidgets.QApplication(sys.argv)
    
    application = ApplicationWindow()
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()








