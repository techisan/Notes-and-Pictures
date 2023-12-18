from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from . import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from .models import Notes, Image
import os, json, datetime
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/', methods=['GET', 'POST']) # Main page of the website
@login_required
def home():
    if request.method == 'POST':
        
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Notes(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

            if 'file' not in request.files:
                flash('No image file')
            file_s = request.files.getlist('file')
            for file in file_s:
                if file.filename == '':
                    flash('No selected file')
                if file and allowed_file(file.filename):
                    from main import app
                    filename = secure_filename(file.filename)
                    NOW = datetime.datetime.now()
                    new_filename = file.filename.rsplit('.',1)[0] + '_' + NOW.strftime("%d_%m_%Y_%H_%M_%S") + '.' + file.filename.rsplit('.',1)[1]
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                   
                    #note_ = Notes.query.filter_by(user_id=current_user.id).first()
                    new_image = Image(name=new_filename, notes_id=new_note.id)
                    db.session.add(new_image)
                    db.session.commit()
                flash('Image added!', category='success')
            
    return render_template("home.html", user = current_user)

@views.route('/add-img', methods=['POST'])
def add_images():
    note_id = request.form.get('noteId')
    note_object = Notes.query.get(note_id)

    if note_object:
        img_list = request.files.getlist('btnAddImage')

        if len(img_list) < 1:
            flash('No image to be added', category='error')
        else:
            # Process each file in img_list
            for img in img_list:
                if img and allowed_file(img.filename):
                    # Do something with the file, e.g., save it
                    from main import app
                    NOW = datetime.datetime.now()
                    new_filename = img.filename.rsplit('.',1)[0] + '_' + NOW.strftime("%d_%m_%Y_%H_%M_%S") + '.' + img.filename.rsplit('.',1)[1]
                    img.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                    new_image = Image(name=new_filename, notes_id=note_object.id)
                    
                    db.session.add(new_image)
                    db.session.commit()
            flash('Images added successfully!', category='success')
    return jsonify({})

@views.route('/edit-note', methods=['POST'])
def edit_note():
    note_id = request.form.get('noteId')
    note_object = Notes.query.get(note_id)
    
    if note_object:
        note = request.form.get('txtEdit')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            note_object.data = note
            db.session.commit()
            flash('Note Edited!', category='success')
    return jsonify({})

@views.route('/delete-img', methods=['POST'])
def delete_img():
    data = json.loads(request.data)
    imgId = data['imgId']
    img = Image.query.get(imgId)
    noteId = data['noteId']
    if img:
        if img.notes_id == int(noteId):
            image_name = img.name 
            image_path = os.path.join(UPLOAD_FOLDER, image_name)
            if os.path.exists(image_path):
                os.remove(image_path)
            db.session.delete(img)
            db.session.commit()
    return jsonify({})

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Notes.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            for image in note.images:
                image_name = image.name 
                image_path = os.path.join(UPLOAD_FOLDER, image_name)
                if os.path.exists(image_path):
                    os.remove(image_path)
                db.session.delete(image)
        db.session.delete(note)
        db.session.commit()
    return jsonify({})
