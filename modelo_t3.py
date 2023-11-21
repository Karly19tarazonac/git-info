import os
import pydicom
import matplotlib.pyplot as plt

class Servicio(object):
    def __init__(self):
        self.__usuarios = {}
        #se crea un usuario inicial para arrancar el sistema
        self.__usuarios['bio12345'] = 'medicoAnalitico'
    
    def verificarUsuario(self, u, c):
        try:
            #Si existe la clave se verifica que sea el usuario
            if self.__usuarios[c] == u:
                return True
            else:
                return False
        except: #si la clave no existe se genera KeyError
            return False
        
    def leerDicom(self,imagen):
        ds = pydicom.dcmread(imagen)
        slice = str(ds["SliceLocation"])
        image_type = str(ds["ImageType"])
        study_description = str(ds["StudyDescription"])
        series_decription = str(ds["SeriesDescription"])
        modality = str(ds["Modality"])
        dcm_info = f"{image_type}\n{study_description}\n{series_decription}\n{modality}\n{slice}"
        return dcm_info
        
    def pictureMaker(self,imagen):
        dcm_data = pydicom.dcmread(imagen)
        im = dcm_data.pixel_array
        if (len(im.shape))==3:
            slice_index = im.shape[0] // 2
            selected_slice = im[slice_index, :, :]
            plt.imshow(selected_slice, cmap=plt.cm.bone)
        else:
            plt.imshow(im, cmap = plt.cm.bone)
        plt.axis('off')
        plt.savefig("temp_image.png")