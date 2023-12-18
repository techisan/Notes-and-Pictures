function EnableDisable(txtEdit, noteId) {
    var formData = new FormData();
    formData.append('noteId', noteId);
    //Reference the Button.
    var btnSubmit = document.getElementById("btnSubmit_"+noteId);

    //Verify the TextBox value.
    if (txtEdit.value.trim() != "") {
        //Enable the TextBox when TextBox has value.
        btnSubmit.disabled = false;
    } else {
        //Disable the TextBox when TextBox is empty.
        btnSubmit.disabled = true;
    }
};

function addImages(noteId){
    var formData = new FormData();
    formData.append('noteId', noteId);
    
    var input = document.getElementById('btnAddImage_' + noteId);
    
    for (var i = 0; i < input.files.length; i++) {
        formData.append('btnAddImage', input.files[i]);
    }
    
    fetch('/add-img', {
        method: 'POST',
        body: formData,
    }).then((_res) => {
        window.location.href = "/";
    });
}

function editNote(noteId){
    var formData = new FormData();
    formData.append('noteId', noteId);
    formData.append('txtEdit', document.getElementById('txtEdit_'+noteId).value);

    fetch('/edit-note', {
        method:'POST',
        body: formData,
    }).then((_res) => {
        window.location.href = "/";
    });
}

function deleteImg(imgId, noteId){
    fetch('/delete-img', {
        method:'POST',
        body:JSON.stringify( { imgId: imgId, noteId: noteId } )
    }).then((_res) => {
        window.location.href = "/";
    });
}
function deleteNoteandImages(noteId){
    fetch('/delete-note', {
        method:'POST',
        body:JSON.stringify( { noteId: noteId } )
    }).then((_res) => {
        window.location.href = "/";
    });
}