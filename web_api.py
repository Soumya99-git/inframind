from flask import Flask,redirect,session,render_template,request,flash,send_file
from pymongo import MongoClient
import os
import videotoaudio
import text_summariztion
        
client  = MongoClient("mongodb://localhost:27017/")
db = client["blogpost"]

coll = db["feedback"]
coll1 = db["login"]

app = Flask(__name__)
app.config["UPLOAD_FOLDER"]="/home/soumyachatterjee/Desktop/INFRAMIND/PROJECT/uploads"



@app.route("/",methods=["GET"])
def home():
    if "uname" in session:
        return render_template("home.html")
    else:
        return render_template("home_!sign.html")

@app.route("/signin",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        uname = request.form["uname"]
        password = request.form["password"]

        l = list(coll1.find({"uname":uname}))
        if (len(l)==0):
            flash("User does not exist")
            return redirect("/signin")
        else:
            a = l[0]
            if password!=a["password"]:
                flash("Wrong password")
                return redirect("/signin")
            else:
                session["uname"] = uname
                return redirect("/")
    else:
        return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        uname = request.form["uname"]
        password = request.form["password"]
        re_pass = request.form["password2"]
        email = request.form["email"]
        
        l = list(coll1.find({"uname":uname}))
        if(len(l)>0):
            flash("User already exists")
            return redirect("/signup")
        else:
            if password!=re_pass:
                flash("Retype password correctly")
                return redirect("/signup")
            else:
                new_user={
                    "uname": uname,
                    "email": email,
                    "password": password
                }
                coll1.insert_one(new_user)
                session["uname"] = uname
                return redirect("/")
    else:
        return render_template("signup.html")


@app.route("/feed",methods=["GET","POST"])
def feeds():
    if "uname" in session:
        import feedback_analysis
        if request.method=="POST":
            uname = request.form["uname"]
            feed = request.form["feed"]
            polarity = feedback_analysis.feedback(feed)
            new_feed = {
                "uname": uname,
                "feedback": feed,
                "polarity": polarity
            }
            print(new_feed)
            coll.insert_one(new_feed)
            #coll.remove({})
            return redirect("/feed")
        else:
            feed_all  = list(coll.find())
            return render_template("feedback.html",feeds = feed_all)
    else:
        flash("Please Sign in")
        return redirect("/signin")

@app.route("/vid_aud",methods=["GET","POST"])
def video():
    if "uname" in session:
        if request.method=="POST":
            if 'f' not in request.files:
                flash("Give some input file")
                return render_template("video.html")
            upload_file = request.files["f"]
            file_name = upload_file.filename.replace(" ","")
            upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name))
            print(upload_file.filename)
            
            new_path = videotoaudio.spliter_audio_text(os.path.join(app.config['UPLOAD_FOLDER'], file_name),file_name)
            
            return send_file(new_path,as_attachment=True)
        else:
            return render_template("video.html")
    else:
        flash("Please Sign in")
        return redirect("/signin")
@app.route("/text",methods=["GET","POST"])
def text():
    if "uname" in session:
        
        if request.method=="POST":
            if 'file' not in request.files:
                flash("Give some input file")
                return render_template("text.html")
            upload_file = request.files["file"]
            file_name = upload_file.filename.replace(" ","_")
            upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name))
            
            path = text_summariztion.summarization(os.path.join(app.config['UPLOAD_FOLDER'], upload_file.filename))
            
            return send_file(path,as_attachment=True)
        else:
            return render_template("text.html")
    else:
        flash("Please Sign in")
        return redirect("/signin")


@app.route("/youtube",methods=["GET","POST"])
def youtube():
    if "uname" in session:
        if request.method == "POST":
            if request.form["base_url"] == None:
                flash("Give an youtube url")
                return redirect("/youtube")
            base_url = request.form["base_url"]
            path  = videotoaudio.you_to_audio(base_url)  
            return send_file(path,as_attachment=True)   
        else:
            return render_template("youtube.html") 
    else:
        flash("Please Sign in")
        return redirect("/signin")          

@app.route("/logout",methods=["GET"])
def logout():
    session.pop("uname",None)
    return render_template("home_!sign.html")



if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True)