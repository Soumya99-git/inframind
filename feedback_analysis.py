import pickle5 as pickle
import os
os.chdir(r"/home/soumyachatterjee/Desktop/INFRAMIND/PROJECT/")
model_path = "model.sav"
model = pickle.load(open(model_path,"rb"))

def feedback(s):
    return(model.predict([s])[0])


if __name__ == "__main__":
    print(feedback("this is a good problem"))