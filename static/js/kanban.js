let relatedButton = null;
let form = $('#task-form').validate({
    rules: {
        total_hours: {
            required: true,
            min: 1
        },
        description: {
            required: true,
            minlength: 5,
            maxlength: 500
        }
    },
    messages: {
        total_hours: {
            required: "Este campo es obligatorio",
            min: "El numero debe ser mayor a cero"
        },
        description: {
            required: "La descripcion de la tarea es obligatoria",
            minlength: "Ingrese un minimo de 5 caracteres",
            maxLength: "Ingrese un maximo de 500 caracteres"
        }
    },
    errorElement: 'span',
    errorPlacement: function (error, element) {
        error.addClass('invalid-feedback');
        element.closest('.form-group').append(error);
    },
    highlight: function (element, errorClass, validClass) {
        $(element).addClass('is-invalid');
    },
    unhighlight: function (element, errorClass, validClass) {
        $(element).removeClass('is-invalid');
    }
});


$('#modal-default').on('shown.bs.modal', function (e) {
    //get related target element
    relatedButton = $(e.relatedTarget)
    //get and send user story id attr to the input hidden into the modal
    const userStoryId = relatedButton.data('user-story-id')
    $(this).find('input[name="user_story_id"]').val(userStoryId)
})

const btnSaveTask = document.getElementById('btn-add-task')
/**
 * store task
 * */
btnSaveTask.addEventListener('click', saveTask);

function saveTask(e) {
    e.preventDefault()
    if (form.form()) {
        const modal = $('#modal-default');
        const userStoryId = modal.find('input[name="user_story_id"]');
        const description = modal.find('input[name="description"]');
        const totalHours = modal.find('input[name="total_hours"]');
        const url = modal.data('url');
        const csrf_token = modal.data('csrf');
        console.log('users', userStoryId)
        $.ajax(url, {
            type: 'POST',
            data: {
                id_user_story: userStoryId.val(),
                description: description.val(),
                total_hours: totalHours.val(),
                csrfmiddlewaretoken: csrf_token
            },
            success: function (data, status, xhr) {
                //move card to the sprint backlog
                if (data?.status === 200) {
                    const li = document.createElement('li')
                    li.classList.add('text-black-50')
                    li.textContent = `- ${description.val()} | ${totalHours.val()} horas`
                    relatedButton.closest('.task-section').find('.task-container').append(li)

                    //clear inputs
                    userStoryId.val(null)
                    description.val(null)
                    totalHours.val(null)
                    modal.find('.btn-cancel').click()
                }
            },
            error: function (jqXhr, textStatus, errorMessage) {
                console.log(jqXhr)
                //fire alert success
                toastr.error("Error")
            }
        });
    }


}
