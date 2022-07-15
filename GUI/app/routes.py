#################
import time
from flask import Flask, render_template, request, session, url_for, send_from_directory, send_file, redirect, flash
import os
import shutil
from werkzeug.utils import secure_filename
from PIL import Image  # Python Image Library - Image Processing
from flask_login import login_required
# library for chipping function
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error
from ncempy.io import dm
from flask_login import current_user, login_user, logout_user
import pandas as pd
from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetPsswordRequestForm
from app.models import User
import hyperspy.api as hs
from model import stem_lstm as sl #lstm model lib
from keras.models import load_model
######### library not in use
import cv2
import json
import glob
############################

@app.route('/protected/<filename>')
def upload(filename):
    # username = session.get('username')
    file_path = os.path.join(app.config['UPLOAD_PATH'], 'username', filename)
    return send_from_directory(file_path)

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
# @login_required
def about():
    return render_template('about.html')


@app.route('/upload')
@login_required
def form():
    session.clear()
    return render_template('form.html')

@app.route('/download/<foldername>/<filename>')
def download(foldername, filename):
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "static/username/" + foldername + "/" + filename
    return send_file(path, as_attachment=True)

@app.route('/grid_select', methods=["GET", "POST"])
def create_grid():
    if request.method == 'POST':
        f = request.files['file']

        print(f.filename)

        cur_name = os.path.join(app.config['UPLOAD_FOLDER'], 'images', secure_filename(f.filename))

        if f.filename[-4:] == "tiff":
            f.save(cur_name)
            image = Image.open(cur_name)
            if image.mode not in ("L", "RGB"):  # rescale 16 bit tiffs to 8 bits
                image.mode = "I"
                image = image.point(lambda i: i * (1.0 / 256))
            new_image = image.convert("RGB")
            current_name = f.filename[:-4] + "jpg"
            new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'images', secure_filename(current_name)))
        elif f.filename[-3:] == "tif":
            f.save(cur_name)
            image = Image.open(cur_name)
            print(image.mode)
            if image.mode not in ("L", "RGB"):  # rescale 16 bit tiffs to 8 bits
                image.mode = "I"
                image = image.point(lambda i: i * (1.0 / 256))
            new_image = image.convert("RGB")
            current_name = f.filename[:-3] + "jpg"
            new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'images', secure_filename(current_name)))

        elif f.filename[-3:] == "dm4":
            f.save(cur_name)
            data = dm.dmReader(cur_name)['data']
            new_array = (data - np.min(data)) / (np.max(data) - np.min(data))
            im = Image.fromarray((255 * new_array).astype('uint8'))
            current_name = f.filename[:-3] + "jpg"
            im.save(os.path.join(app.config['UPLOAD_FOLDER'], 'images', secure_filename(current_name)))
        else:
            current_name = f.filename
            print(f)
            print("save address")
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'images', secure_filename(current_name)))
            #f.save("C:\Users\\rodr822\Desktop\Application\pychip_deploy\pychip\static\username\images\\"+current_name)

        session['file'] = current_name
        print(current_name)
        # load image and gets the image dimensions
        im_gray = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], 'images', secure_filename(session['file'])), cv2.IMREAD_GRAYSCALE)
        dim = {'height': im_gray.shape[0], 'width': im_gray.shape[1], 'image': secure_filename(session['file'])}

        session['dim'] = dim

        return render_template('index.html', dim=dim)

    # default image (if nothing is uploaded)
    # load image and gets the image dimensions
    # do we need this if the user is required to upload a file to move on?
    im_gray = cv2.imread(os.path.join(app.static_folder, "images/", "intensity.jpg"), cv2.IMREAD_GRAYSCALE)
    dim = {'height': im_gray.shape[0], 'width': im_gray.shape[1], 'image': "static/images/intensity.jpg"}
    session['dim'] = dim
    return render_template('index.html', dim=dim)


@app.route('/support_select', methods=["GET", "POST"])
def save_file():
    if request.method == 'POST':
        current_file = session.get('file')
        print(current_file)

        # dim = {'height': height, 'width' : width, 'image': "protected/username/" + current_file}

        path_to_im = os.path.join(app.config['UPLOAD_FOLDER'], 'images', secure_filename(session['file']))
        print("this is the path!")

        query_path = os.path.join(app.config['UPLOAD_FOLDER'], 'query', 'all_chips')

        try:
            shutil.rmtree(query_path)
            print("removed previous query set")
        except:
            print('There were no previous query sets')
        finally:
            os.mkdir(query_path)

        # Get the chip size from the slider
        chip_size = int(request.form["mySlider"])
        session["chip_size"] = chip_size
        # chipping image
        img = cv2.imread(path_to_im)
        width = int(img.shape[1])
        height = int(img.shape[0])
        size_of_img = chip_size
        num_crops_x = math.floor(width / size_of_img)
        num_crops_y = math.floor(height / size_of_img)
        total_num_crops = num_crops_x * num_crops_y

        pixels_ignored_in_x = width % size_of_img
        pixels_ignored_in_y = height % size_of_img
        print("Pixels ignored in x: last " + str(pixels_ignored_in_x))
        print("Pixels ignored in y: last " + str(pixels_ignored_in_y))

        #crop out unused part
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], 'images', secure_filename(session['file'])))
        im1 = image.crop((0, 0, width - pixels_ignored_in_x, height - pixels_ignored_in_y))
        im1.save(os.path.join(app.config['UPLOAD_FOLDER'], 'images', secure_filename(session['file'])))
        img = cv2.imread(path_to_im)


        x_coords = list(range(0, width, size_of_img))
        y_coords = list(range(0, height, size_of_img))
        img_names = []

        crops = np.zeros((total_num_crops, size_of_img, size_of_img))
        count = 0

        for i in range(num_crops_x):
            for j in range(num_crops_y):
                x = x_coords[i]
                y = y_coords[j]
                new_img = img[y:y + size_of_img, x:x + size_of_img, 0]
                crops[count, :, :] = new_img

                count = count + 1
                name = "cropX_" + str(i) + "_Y_" + str(j) + ".jpg"

                img_names.append(name)
                plt.imsave(os.path.join(query_path, name), new_img, vmin=0, vmax=255)
        dim = session.get('dim')
        dim["num_crops_x"] = num_crops_x
        dim["num_crops_y"] = num_crops_y
        return render_template('predict.html', dim=dim)

    dim = session.get('dim')

    return render_template('predict.html', dim=dim)


@app.route('/results', methods=["GET", "POST"])
def send_supports():
    if request.method == 'POST':

        return render_template('results.html')
    return render_template('results.html')

###########Updated GUI###############
# Login routes, detail see models.py, check the username and password
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('about'))
    return render_template('login.html', title='Sign In', form=form)

# Logout routes, do the logout_user() function built in flask, and clear the session
@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    g = os.walk(r"./flask_session/")
    for path,dir_list,file_list in g:
        for file in file_list:
            file_path = os.path.join(r"./flask_session/" + file)
            print(file_path)
            os.remove(file_path)
    # redirect to login page
    return redirect(url_for('login'))

# Register routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Reset password request route, currently not work, need to set up the official email
@app.route('/reset_password_request',methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = ResetPsswordRequestForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data).first()
    #     if user:
    #         send_password_reset_email(user)
    #     flash(_('Check your email for the instructions to reset your password'))
    #     return redirect(url_for('login'))
    return render_template('reset_password_request.html',title='Reset Password',form=form)

# Learning History routes, send the filename under ../static/username/images/ to the frontend
@app.route('/hisory')
@login_required
def history():
    file_list = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'images'))
    file_dict = {}
    for i, file in enumerate(file_list):
        if file != '.gitkeep':
            date = time.ctime(os.path.getctime(os.path.join(app.config['UPLOAD_FOLDER'], 'images', file)))
            result = file[:-4] + "_lstm_result.jpg"
            cur = {'date':date,'file':file,'result':result}
            file_dict[i] = cur
    return render_template('history.html', file_dict=file_dict)

# Delete file routes, needs filename as parameter
@app.route('/delete/<filename>',methods=["GET", "POST"])
def delete(filename):
    # delete the source file, usually .dm4 format
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'images', filename)
    if os.path.exists(file_path):
        print(1)
        try:
            os.remove(file_path)
            print('success to delete')
        except:
            print('fail to delete')
    # delete the result file, usually .jpg format
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result', filename[:-4]+'_lstm_result.jpg')
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print('success to delete')
        except:
            print('fail to delete')
    return redirect(url_for('history'))

# showDetail route, redirect to the download routes
@app.route('/showDetail/<filename>')
def showDetail(filename):
    return redirect(url_for('download', foldername="result", filename=filename[:-4]+'_lstm_result.jpg'))

# Lstm index page routes
@app.route('/lstm')
@login_required
def lstm():
    return render_template('lstm.html')

# Routes for choice of hyperParameter for lstm
@app.route('/time_step_select', methods=["GET", "POST"])
def create_time_step():
    if request.method == 'POST':
        f = request.files['file']

        cur_name = os.path.join(app.config['UPLOAD_FOLDER'], 'images', secure_filename(f.filename))
        if f.filename[-3:] == "dm4":
            f.save(cur_name)
            s = hs.load(cur_name)

            data1 = s[2].data
            scale = s[2].axes_manager[1].scale
            size = s[2].axes_manager[1].size
            offset = s[2].axes_manager[1].offset
            # Define energy scale
            e_min = offset
            e_max = offset + size * scale
            e = np.linspace(e_min, e_max, size)
            # save the data as csv file
            df2 = pd.DataFrame(columns=['TimeStep', 'X', 'Y'])
            appendlist = []
            timestep = len(data1)
            for step in range(timestep):
                for i, x in enumerate(e):
                    appendlist.append({'TimeStep': str(step), 'X': str(x), 'Y': str(data1[step][i])})

            df2 = df2.append(appendlist, ignore_index=True)
            current_csv_name = f.filename[:-4] + ".csv"
            df2.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'images', secure_filename(current_csv_name)), index=False)

        else:
            current_name = f.filename
            print(f)
            print("save address")
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'images', secure_filename(current_name)))

        dim = {'file':f.filename, 'csv':secure_filename(current_csv_name), 'slider_max':s[2].data.shape[0]}
        session['dim'] = dim
        return render_template('lstm-index.html', dim=dim)


    return render_template('lstm-index.html')


# LSTM predict routes
@app.route('/lstm_training', methods=["GET", "POST"])
def lstm_training():
    if request.method == 'POST':

        form_data = request.form
        print(form_data)
        current_file = session.get('dim')['file']
        # remove csv saved before
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'images', secure_filename(current_file)[:-3]+'csv')
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print('success to delete')
            except:
                print('fail to delete')

        # Load data
        s = hs.load(os.path.join(app.config['UPLOAD_FOLDER'], 'images', secure_filename(current_file))[:-3]+'dm4')
        # Load model
        saved_model = load_model('model/LSTM_0.4s.h5')
        # Scale data
        data_aligned = sl.align_spectra(s[2])
        data_scaled, scaler = sl.scale_spectra(data_aligned, return_scaler=True)
        # Format data
        window_back = 8
        window_forward = 8
        test_X_scaled, test_y_scaled = sl.LSTM_format(data_scaled, window_back, window_forward)

        pred_y_scaled = saved_model.predict(test_X_scaled)
        pred_y = scaler.inverse_transform(pred_y_scaled)
        test_y = scaler.inverse_transform(test_y_scaled)
        mse = int(mean_squared_error(pred_y,test_y))

        # Extract bin size, scale, and offset for accurate plotting
        scale = data_aligned.axes_manager[1].scale
        size = data_aligned.axes_manager[1].size
        offset = data_aligned.axes_manager[1].offset

        # Define energy scale
        e_min = offset
        e_max = offset + size * scale
        e = np.linspace(e_min, e_max, size)

        # Plot input sequence, real, and prediction
        for i, input_spec in enumerate(test_X_scaled[-1]):
            input_spec_us = scaler.inverse_transform(input_spec.reshape(1, -1))
            if i == 4:
                plt.plot(e, input_spec_us[0], ':', color='black', alpha=(i + 2) / 15, label='input_sequence')
            else:
                plt.plot(e, input_spec_us[0], ':', color='black', alpha=(i + 2) / 15)
        plt.plot(e, test_y[-1], label='real')
        plt.plot(e, pred_y[-1], label='prediction')
        plt.xlabel('Energy loss axis [eV]')
        plt.ylabel('Intensity [counts]')
        plt.title('LSTM Result for the '+str(current_file[:-4]) + ' MSE = ' + str(mse))
        plt.legend()
        current_name = current_file[:-4] + "_lstm_result.jpg"
        plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], 'result', secure_filename(current_name)))
        plt.close()

        im_gray = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], 'result', secure_filename(current_name)),
                             cv2.IMREAD_GRAYSCALE)
        dim = {'height': im_gray.shape[0], 'width': im_gray.shape[1], 'image': secure_filename(current_name)}
        session['dim'] = dim
        return render_template('lstm-predict.html', dim=dim, picture=secure_filename(current_name), mse=mse)

    dim = session.get('dim')
    return render_template('lstm-predict.html', dim=dim)


