## This is the abstract class that the students should implement  

from modesEnum import Modes
import numpy as np
import cv2 as cv


class ImageModel():

    """
    A class that represents the ImageModel"
    """

    def __init__(self):
        pass

    def __init__(self, imgPath: str):
        self.imgPath = imgPath
        ###
        # ALL the following properties should be assigned correctly after reading imgPath 
        ###
        self.imgByte = cv.cvtColor(cv.imread(self.imgPath),cv.COLOR_BGR2GRAY)
        self.dft =  np.fft.fft2(self.imgByte)
        self.real = np.real(self.dft)
        self.imaginary = np.imag(self.dft)
        self.magnitude = np.abs(self.dft)
        self.phase = np.angle(np.fft.fftshift(self.dft))


        self.shape  = self.imgByte.shape
   
    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
        """
        a function that takes ImageModel object mag ratio, phase ration 
        """
        ### 
        # implement this function
        ###
        
        if mode == Modes.magnitudeAndPhase :
            mix = (   ( magnitudeOrRealRatio    *  self.magnitude   ) +  ( (1-magnitudeOrRealRatio)*imageToBeMixed.magnitude)   ) * np.exp(1j*( phaesOrImaginaryRatio*self.phase    ) +( (1-phaesOrImaginaryRatio)*imageToBeMixed.phase   ) )  
        
        elif   mode == Modes.realAndImaginary :
            mix = (   (self.real * magnitudeOrRealRatio + imageToBeMixed.real *(1-magnitudeOrRealRatio)  )  + 1j*(self.imaginary*phaesOrImaginaryRatio + (1-phaesOrImaginaryRatio)*imageToBeMixed.phase )      )
            
        elif mode == Modes.magnitudeAndUniformPhase :
            mix = (   ( magnitudeOrRealRatio    *  self.magnitude   ) +  ( (1-magnitudeOrRealRatio)*imageToBeMixed.magnitude)   ) * np.exp( 1j*(np.zeros(self.imgByte.shape )   ) )

        elif mode == Modes.uniformMagnitudeAndPhase :
            mix = (np.ones(self.imgByte.shape)) * np.exp(1j*( phaesOrImaginaryRatio*self.phase    ) +( (1-phaesOrImaginaryRatio)*imageToBeMixed.phase   ) )
        
        elif mode == Modes.phaseAndMagnitude :
            mix = (   (  (magnitudeOrRealRatio-1)    *  self.magnitude   ) +  ( (magnitudeOrRealRatio)*imageToBeMixed.magnitude)   ) * np.exp(1j*( phaesOrImaginaryRatio*self.phase    ) +( (1-phaesOrImaginaryRatio)*imageToBeMixed.phase   ) ) 
        '''
        elif mode == Modes.imaginaryAndReal :
            mix = (   (imageToBeMixed.real * magnitudeOrRealRatio + self.real *(1-magnitudeOrRealRatio)  )  + 1j*( imageToBeMixed.phase*phaesOrImaginaryRatio + (1-phaesOrImaginaryRatio)*self.imaginary )      )
 
        elif mode == Modes.uniformPhaseAndMagnitude :
            mix = (   ( magnitudeOrRealRatio    *  imageToBeMixed.magnitude  ) +  ( (1-magnitudeOrRealRatio)*  self.magnitude)   ) * np.exp( 1j*(np.zeros(self.imgByte.shape )  ) )
        
        elif mode == Modes.phaseAndUniformMagnitude :
            mix = (np.ones(self.imgByte.shape)) * np.exp(1j*( phaesOrImaginaryRatio* imageToBeMixed.phase   ) +( (1-phaesOrImaginaryRatio)* self.phase   ) ) 
        '''   
        output = np.abs( np.fft.ifft2(mix) )

        return(output)
        

        

        
        
        
        
        #pass