import pickle
import os
os.chdir(r"/home/soumyachatterjee/Desktop/INFRAMIND/PROJECT/")
model_path = "model.sav"
model = pickle.load(open(model_path,"rb"))

def feedback(s):
    return(model.predict([s])[0])
