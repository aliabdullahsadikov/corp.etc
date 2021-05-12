(function($){

    $('.update-userinfo-btn a').on('click', function(e){
        e.preventDefault();
        $('.section-one').addClass('hide').removeClass('show');
        $('.section-two').removeClass('hide').addClass('show');
    });

    // for search input, when input will chang this function will execute
    $('form #search').on('change', function(){
        var val = $(this).val();
//        console.log(val);
        $.getJSON("/static/js/employees.json", function(data){
//            console.log(data);
            $('.tweets').empty();
            counter = 0;
            $(data.users).each(function(index, value){
                var firstname = value['firstname'].toLowerCase();
                    lastname = value['lastname'].toLowerCase();
                    needed = val.toLowerCase();
//                    console.log(needed);
//                firstname.toLowerCase();
//                lastname.toLowerCase();

                if (firstname.includes(needed) || lastname.includes(needed)){

                    if(value['photo'] == '' || value['photo'] == 'user_default.png'){
                        var photo = "/static/images/user_default.png";
                    }else {
                        var photo = "/static/images/profile/"+value['photo'];
                    }
//                    console.log(value['firstname']);
//                    $(".tweets").append('<div class="item"><div class="tweet-img" style="width: 70px;"><img style="width:100%;" src="/static/images/user_default.png" alt="Zola"></div><div class="tweet-content" style="width: 80%;"><i class="fa fa-twitter"></i><h5 style="font-size: 18px;" class="font"> <a class="name"  id="'+value["id"]+'">'+ value['firstname']+' '+ value['lastname'] +'</a><a href="https://t.me/'+ value['firstname'] +'"><span style="font-size:13px;" class="font">@'+ value['firstname'] +'</span></a></h5><p>'+ value['department'] +'<span> контакты</span></p></div></div>');
                    item = '<div class="item">';
                        item += '<div class="tweet-img" style="width: 70px;">';
                            item += '<img style="width:100%;" src="'+ photo +'" alt="Zola"></div>';
                        item += '<div class="tweet-content" style="width: 80%;">';
                            if(value['telegram'] != null){
                                item += '<i class="fa fa-telegram"></i>';
                            }
                            item += '<h5 style="font-size: 18px;" class="font lolo">';
                                item += '<a class="employee-name" id="'+value["id"]+'">'+ value['firstname']+' '+ value['lastname'] +'</a>';
                                item += '<a target="_blank" href="https://t.me/'+ value['telegram'] +'">';
                                if(value['telegram'] != null){
                                    item += '<span style="font-size:13px;" class="font">@'+ value['telegram'] +'</span></a></h5>';
                                }
                    item += '<p>'+ value['department'] +'<span class="employee-name" style="cursor:pointer;"></span></p></div></div>'
                    $(".tweets").append(item);

                    counter++;
                }

            });
            $('#count').empty();
            $('#count').append(counter+' сотрудников');
        }).fail(function(){
            console.log("An error has occurred.");
        });
    });

    // for search input, when entering on input this function will execute
    $('form').keypress(function(e) { // Attach the form handler to the keypress event
        if (e.keyCode == 13) { // If the the enter key was pressed.
            e.preventDefault();
            var val = $('form #search').val();
            $.getJSON("/static/js/employees.json", function(data){
                $('.tweets').empty();
                counter = 0;
                $(data.users).each(function(index, value){
                    var firstname = value['firstname'].toLowerCase();
                        lastname = value['lastname'].toLowerCase();
                        needed = val.toLowerCase();

                    if (firstname.includes(needed) || lastname.includes(needed)){

                        if(value['photo'] == '' || value['photo'] == 'user_default.png'){
                            var photo = "/static/images/user_default.png";
                        }else {
                            var photo = "/static/images/profile/"+value['photo'];
                        }
    //                    console.log(value['firstname']);
    //                    $(".tweets").append('<div class="item"><div class="tweet-img" style="width: 70px;"><img style="width:100%;" src="/static/images/user_default.png" alt="Zola"></div><div class="tweet-content" style="width: 80%;"><i class="fa fa-twitter"></i><h5 style="font-size: 18px;" class="font"> <a class="name"  id="'+value["id"]+'">'+ value['firstname']+' '+ value['lastname'] +'</a><a href="https://t.me/'+ value['firstname'] +'"><span style="font-size:13px;" class="font">@'+ value['firstname'] +'</span></a></h5><p>'+ value['department'] +'<span> контакты</span></p></div></div>');
                        item = '<div class="item">';
                            item += '<div class="tweet-img" style="width: 70px;">';
                                item += '<img style="width:100%;" src="'+ photo +'" alt="Zola"></div>';
                            item += '<div class="tweet-content" style="width: 80%;">';
                                if(value['telegram'] != null){
                                    item += '<i class="fa fa-telegram"></i>';
                                }
                                item += '<h5 style="font-size: 18px;" class="font lolo">';
                                    item += '<a class="" id="'+value["id"]+'">'+ value['firstname']+' '+ value['lastname'] +'</a>';
                                    item += '<a href="https://t.me/'+ value['telegram'] +'">';
                                    if(value['telegram'] != null){
                                        item += '<span style="font-size:13px;" class="font">@'+ value['telegram'] +'</span></a></h5>';
                                    }
                        item += '<p>'+ value['department'] +'<span class=""> контакты</span></p></div></div>'
                        $(".tweets").append(item);

                        counter++;
                    }

                });
                $('#count').empty();
                $('#count').append(counter+' сотрудников');
            }).fail(function(){
                console.log("An error has occurred.");
            });
        }
    });

    // for department selection
    $('.depart .user-menu ul li').on('click', function(){
        var val = $(this).text();
//        console.log(val);
        $.getJSON("/static/js/employees.json", function(data){
//            console.log(data);
            $('.tweets').empty();
            counter = 0;
            $(data.users).each(function(index, value){
                var department = value['department']; // from json file
                    needed = val; // from selected list

                if (department.includes(needed)){
                    if(value['photo'] == '' || value['photo'] == 'user_default.png'){
                        var photo = "/static/images/user_default.png";
                    }else {
                        var photo = "/static/images/profile/"+value['photo'];
                    }
//                    console.log(value['firstname']);
//                    $(".tweets").append('<div class="item"><div class="tweet-img" style="width: 70px;"><img style="width:100%;" src="/static/images/user_default.png" alt="Zola"></div><div class="tweet-content" style="width: 80%;"><i class="fa fa-twitter"></i><h5 style="font-size: 18px;" class="font"> <a class="name"  id="'+value["id"]+'">'+ value['firstname']+' '+ value['lastname'] +'</a><a href="https://t.me/'+ value['firstname'] +'"><span style="font-size:13px;" class="font">@'+ value['firstname'] +'</span></a></h5><p>'+ value['department'] +'<span> контакты</span></p></div></div>');
                    item = '<div class="item">';
                        item += '<div class="tweet-img" style="width: 70px;">';
                            item += '<img style="width:100%;" src="'+ photo +'" alt="Zola"></div>';
                        item += '<div class="tweet-content" style="width: 80%;">';
                            if(value['telegram'] != null){
                                item += '<i class="fa fa-telegram"></i>';
                            }
                            item += '<h5 style="font-size: 18px;" class="font lolo">';
                                item += '<a class="employee-name" id="'+value["id"]+'">'+ value['firstname']+' '+ value['lastname'] +'</a>';
                                item += '<a target="_blank" href="https://t.me/'+ value['telegram'] +'">';
                                if(value['telegram'] != null){
                                    item += '<span style="font-size:13px;" class="font">@'+ value['telegram'] +'</span></a></h5>';
                                }
                    item += '<p>'+ value['department'] +'<span class="employee-name" style="cursor:pointer;"></span></p></div></div>'
                    $(".tweets").append(item);

                    counter++;
                }

            });
            $('#count').empty();
            $('#count').append(counter+' сотрудников');
        }).fail(function(){
            console.log("An error has occurred.");
        });
    });


    $(document).on('click', ".lolo .employee-name", function(e){
        e.preventDefault();
        id = $(this).attr('id');
        $.getJSON("/static/js/employees.json", function(data){
            $('.info-detail .left').empty();
            $(data.users).each(function(index, value){
//            console.log(value);
                var firstname = value['firstname'].toLowerCase();
                    lastname = value['lastname'].toLowerCase();

                if (value['id'] == id){

                    if(value['photo'] == '' || value['photo'] == 'user_default.png'){
                        var photo = "/static/images/user_default.png";
                    }else {
                        var photo = "/static/images/profile/"+value['photo'];
                    }
//                    console.log(value['firstname']);
//                    $(".tweets").append('<div class="item"><div class="tweet-img" style="width: 70px;"><img style="width:100%;" src="/static/images/user_default.png" alt="Zola"></div><div class="tweet-content" style="width: 80%;"><i class="fa fa-twitter"></i><h5 style="font-size: 18px;" class="font"> <a class="name"  id="'+value["id"]+'">'+ value['firstname']+' '+ value['lastname'] +'</a><a href="https://t.me/'+ value['firstname'] +'"><span style="font-size:13px;" class="font">@'+ value['firstname'] +'</span></a></h5><p>'+ value['department'] +'<span> контакты</span></p></div></div>');
                    detail = '<div class="thumbnail-img">';
					detail +=   '<img class="img-fluid" src="'+ photo +'" alt="Zola">';
					detail +='</div>';
				    detail += '<div class="name" style="    padding: 4px 0 0 15px; float: left;width: 72%;">';
					detail += '<span class="font" style="font-size:23px;">'+ value['firstname']  +' '+ value['lastname'] +'</span>';
					detail += '<br><span class="font" style="font-size:17px;">'+ value['department'] +'</span>';
					detail += '<br><span class="font" style="font-size:15px; color: grey;">'+ value['position'] +'</span>';
                    detail += '</div>';
				    detail += '<div class="details" style="padding: 0 0px; margin-top:15px; width: 100%;">';
                    detail += '<div class="followers-post">';
 					detail += '<div class="item" style="width:100%;">';
					detail += '<p class="font" style="font-family: revert !important;">Contacts</p>';
					detail += '<a href="tel:'+ value['phone'] +'">';
					detail += '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-phone" viewBox="0 0 16 16"><path d="M11 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h6zM5 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H5z"></path><path d="M8 14a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"></path></svg>';
					detail += '<span class="font" style="font-family: sans-serif !important;">'+ value['phone'] +' </span></a></div>';

					detail += '<div class="item" style="width:100%;">';
					detail += '<a href="#">';
					detail += '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-at" viewBox="0 0 16 16"><path d="M13.106 7.222c0-2.967-2.249-5.032-5.482-5.032-3.35 0-5.646 2.318-5.646 5.702 0 3.493 2.235 5.708 5.762 5.708.862 0 1.689-.123 2.304-.335v-.862c-.43.199-1.354.328-2.29.328-2.926 0-4.813-1.88-4.813-4.798 0-2.844 1.921-4.881 4.594-4.881 2.735 0 4.608 1.688 4.608 4.156 0 1.682-.554 2.769-1.416 2.769-.492 0-.772-.28-.772-.76V5.206H8.923v.834h-.11c-.266-.595-.881-.964-1.6-.964-1.4 0-2.378 1.162-2.378 2.823 0 1.737.957 2.906 2.379 2.906.8 0 1.415-.39 1.709-1.087h.11c.081.67.703 1.148 1.503 1.148 1.572 0 2.57-1.415 2.57-3.643zm-7.177.704c0-1.197.54-1.907 1.456-1.907.93 0 1.524.738 1.524 1.907S8.308 9.84 7.371 9.84c-.895 0-1.442-.725-1.442-1.914z"></path></svg>';
					detail += '<span class="font" style="font-family: sans-serif !important;">'+ value['email'] +'</span></a></div>';

					/* Facebook */
					detail += '<div class="item" style="width:100%;">';
					detail += '<a href="https://www.facebook.com/'+ value['facebook'] +'" target="_blank">';
					detail += '<i class="fa fa-facebook fa-lg" style="margin-right: 11px; margin-left: 5px;"></i>';
					detail += '<span class="font" style="font-family: sans-serif !important;">'+ value['facebook'] +'</span></a></div>';

					/* Instagram */
					detail += '<div class="item" style="width:100%;">';
					detail += '<a href="https://www.instagram.com/'+ value['instagram'] +'" target="_blank">';
					detail += '<i class="fa fa-instagram fa-lg" style="margin-right: 7px; margin-left: 4px;"></i>';
					detail += '<span class="font" style="font-family: sans-serif !important;">'+ value['instagram'] +'</span></a></div>';

					/* Telegram */
					detail += '<div class="item" style="width:100%;">';
					detail += '<a href="https://t.me/'+ value['telegram'] +'" target="_blank">';
					detail += '<i class="fa fa-telegram fa-lg" style="margin-right: 7px; margin-left: 3px;"></i>';
					detail += '<span class="font" style="font-family: sans-serif !important;">'+ value['telegram'] +'</span></a></div></div>';

//					detail += '<p class="font">Здесь размещен текст для информации о сотрудника.</p>';
					detail += '</div>';
//                    console.log(detail);
                    $(".info-detail .left").append(detail);
                }

            });
        }).fail(function(){
            console.log("An error has occurred.");
        });
    });

    var readURL = function(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.profile-pic').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }

    $(".file-upload").on('change', function(){
        readURL(this);
    });

    $(".upload-button").on('click', function() {
       $(".file-upload").click();
    });

//    $('.img-fluid').croppie(opts);
//    // call a method via jquery
//    $('.img-fluid').croppie(method, args);
//    $('.file-upload').on('change', function(){
//        val = $(this).val();
//        filename = val.match(/[^\\/]*$/)[0];
//        console.log(filename);
////        $('.img-fluid').croppie();
//    });


    // Start upload preview image
    $(".gambar").attr("src", "/static/images/user_default.png");
        var $uploadCrop,
        tempFilename,
        rawImg,
        imageId;
        function readFile(input) {
            if (input.files && input.files[0]) {
              var reader = new FileReader();
                reader.onload = function (e) {
                    $('.upload-demo').addClass('ready');
                    $('#cropImagePop').modal('show');
                    rawImg = e.target.result;
                }
                reader.readAsDataURL(input.files[0]);
            }
            else {
                swal("Sorry - you're browser doesn't support the FileReader API");
            }
        }

        $uploadCrop = $('#upload-demo').croppie({
            viewport: {
                width: 130,
                height: 130,
            },
            enforceBoundary: false,
            enableExif: true
        });
        $('#cropImagePop').on('shown.bs.modal', function(){
            // alert('Shown pop');
            $uploadCrop.croppie('bind', {
                url: rawImg
            }).then(function(){
                console.log('jQuery bind complete');
            });
        });

        $('.item-img').on('change', function () { imageId = $(this).data('id'); tempFilename = $(this).val();
                                                                                         $('#cancelCropBtn').data('id', imageId); readFile(this); });
        $('#cropImageBtn').on('click', function (ev) {
            $uploadCrop.croppie('result', {
                type: 'base64',
                format: 'jpeg',
                size: {width: 130, height: 130}
            }).then(function (resp) {
                $('#item-img-output').attr('src', resp);
                $('#cropImagePop').modal('hide');
            });
        });
// End upload preview image


    // Comment form scripts
    $('#comment_form').submit(handleSubmit);

    function handleSubmit(e){
        var form = $(this);
        var data = {
            "news_id" : form.find('#news_id').val(),
            "parent_id" : form.find('#parent_id').val(),
            "message" : form.find('#message').val()
        }

        postComment(data);

        return false;
    }

    function postComment(data){
//    console.log(data);
        $.ajax({
            method: "POST",
            url: "/comment",
            data: data,
//            headers: {
//              'X-Requested-With': 'XMLHttpRequest'
//            },
            success: postSuccess,
            error: postError
        })
    }

    function postSuccess(data, textStatus, jqXHR) {
        addToComment(data);
    }

    function postError(jqXHR, textStatus, errorThrown) {
        console.log(textStatus);
    }

    function addToComment(data){
//        $('#')
    }

    // comment answer:
    $('.comment-answer').on('click', function(){
        var news_id = $(this).data('news-id');
            parent_id = $(this).attr('id');
            user_photo = $(this).data('user-photo');
        checking = $('#replay-answer-'+parent_id).length;
        if($('#replay-answer-'+parent_id).length == 0){
            var form = '';
            form += '<div class="media" style="border-top:none;" id="replay-answer-'+ parent_id +'">';
            form +=    '<div class="img-frame1">';
            form +=         '<img class="mr-3" src="/static/images/profile/'+ user_photo +'" alt="Zola">';
            form +=     '</div>';
            form +=     '<div class="media-body" style="margin: 0 0 20px 2px;">';
            form +=         '<form action="/comment" id="comment_form" name="comment" method="post">';
            form +=             '<input type="hidden" name="news_id" id="news_id" value="'+ news_id +'">';
            form +=             '<input type="hidden" name="parent_id" id="parent_id" value="'+ parent_id +'">';
            form +=             '<input type="text" name="message" id="message" placeholder="Оставить комментарий" style="width: 87%; background: #fbfbfb; border-bottom: 1px solid #eeeeee !important; line-height: 2;">';
            form +=             '<input type="submit" name="submit" style="border-radius: 50%; width:30px; height:30px; cursor:pointer; color: white;" class="bg-orange font" value=">">';
            form +=         '</form>';
            form +=     '</div>';
            form += '</div>';
        }

        $(this).after(form);
//        console.log(user_photo);
//        console.log(checking);
    })


})(jQuery);