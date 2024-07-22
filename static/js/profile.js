$(document).ready(function() {
    $('#edit-cover').click(function() {
        $('#cover-upload').click();
    });

    $('#cover-upload').change(function() {
        var formData = new FormData();
        formData.append('cover', $('#cover-upload')[0].files[0]);

        $.ajax({
            url: '/update_cover',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                $('#cover-image').attr('src', data.cover_url);
            }
        });
    });

    $('#edit-avatar').click(function() {
        $('#avatar-upload').click();
    });

    $('#avatar-upload').change(function() {
        var formData = new FormData();
        formData.append('avatar', $('#avatar-upload')[0].files[0]);

        $.ajax({
            url: '/update_avatar',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                $('#avatar-image').attr('src', data.photo_url);
            }
        });
    });

    $('#save-details').click(function() {
        var details = {
            name: $('#name').val(),
            surname: $('#surname').val()
        };

        $.ajax({
            url: '/update_details',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(details),
            success: function(data) {
                alert('Детали профиля обновлены');
            }
        });
    });

    $('#save-bio').click(function() {
        var bio = {
            bio: $('#bio').val()
        };

        $.ajax({
            url: '/update_bio',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(bio),
            success: function(data) {
                alert('Информация "О себе" обновлена');
            }
        });
    });

    $('#save-achievements').click(function() {
        var achievements = {
            achievements: $('#achievements').val()
        };

        $.ajax({
            url: '/update_achievements',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(achievements),
            success: function(data) {
                alert('Достижения обновлены');
            }
        });
    });

    $('#save-contact').click(function() {
        var contact = {
            contact: $('#contact').val()
        };

        $.ajax({
            url: '/update_contact',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(contact),
            success: function(data) {
                alert('Контакты обновлены');
            }
        });
    });
});
