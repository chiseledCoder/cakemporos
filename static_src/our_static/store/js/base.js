        /* OPEN REGISTER MODAL*/
        function openRegister() {
            $('#login-modal').modal('hide');
            $('#register-modal').modal({backdrop:'static', keyboard:false,show:true});
        };
        /* OPEN LOGIN MODAL*/
        function openLogin() {
            $('#register-modal').modal('hide');
            $('#login-username').focus();
            $('#login-modal').modal({backdrop:'static', keyboard:false,show:true});
        };
        /* SEND OTP ON FORGOT PASSWORD CLICKED MODAL*/
        $(document).ready(function(){
            /* TOOLTIP INITIALIZATION*/
            $("[data-toggle=tooltip]").tooltip();

            /* RELOAD THE PAGE ON CLOSING OF ERROR MODAL */
            $('#errorModal').on('hidden.bs.modal', function () {
                location.reload();
            });
            $('#noDeliveryModal').on('hidden.bs.modal', function () {
                $('div#step-2.row.setup-content').show();
                $('div#step-3.row.setup-content').hide();
                $('a[href="#step-2"]').addClass('btn-cakemporos').removeClass('btn-default disabled');
                $('a[href="#step-3"]').removeClass('btn-cakemporos').addClass('btn-default disabled');
            });
            /*  LOGIN VALIDATION*/
            $("#loginform" ).validate( {
                rules: {
                    phone: {
                        required: true,
                        minlength: 10
                    },
                    password: {
                        required: true,
                        minlength: 5
                    },
                },
                messages: {
                    phone: "Please enter valid phone number",
                    password: "Please enter password"
                },
                errorElement: "em",
                errorPlacement: function ( error, element ) {
                    // Add the `help-block` class to the error element
                    error.addClass( "help-block" );

                    // Add `has-feedback` class to the parent div.form-group
                    // in order to add icons to inputs
                    element.parents( ".form-group" ).addClass( "has-feedback" );

                    if ( element.prop( "type" ) === "checkbox" ) {
                        error.insertAfter( element.parent( "label" ) );
                    } else {
                        error.insertAfter( element );
                    }

                    // Add the span element, if doesn't exists, and apply the icon classes to it.
                    if ( !element.next( "span" )[ 0 ] ) {
                        $( "<span class='fa fa-times form-control-feedback'></span>" ).insertAfter( element );
                    }
                },
                success: function ( label, element ) {
                    // Add the span element, if doesn't exists, and apply the icon classes to it.
                    if ( !$( element ).next( "span" )[ 0 ] ) {
                        $( "<span class='fa fa-check form-control-feedback'></span>" ).insertAfter( $( element ) );
                    }
                },
                highlight: function ( element, errorClass, validClass ) {
                    $( element ).parents( ".form-group" ).addClass( "has-error" ).removeClass( "has-success" );
                    $( element ).next( "span" ).addClass( "fa-times" ).removeClass( "fa-check" );
                },
                unhighlight: function ( element, errorClass, validClass ) {
                    $( element ).parents( ".form-group" ).addClass( "has-success" ).removeClass( "has-error" );
                    $( element ).next( "span" ).addClass( "fa-check" ).removeClass( "fa-times" );
                }
            } );

        });

        $(document).ready(function(){
            /*$(window).load(function(){
                $('#preloader').fadeOut('slow',function(){$(this).remove();});
            });*/
             /* REGISTRATION VALIDATION */ 
            $( "#signupForm" ).validate( {
                rules: {
                    name: {
                        required: true,
                        minlength: 6
                    },
                    phone: {
                        required: true,
                        minlength: 10
                    },
                    password: {
                        required: true,
                        minlength: 5
                    },
                    confirm_password: {
                        required: true,
                        minlength: 5,
                        equalTo: "#password"
                    },
                    email: {
                        required: true,
                        email: true
                    }
                },
                messages: {
                    name: "Please enter full name",
                    phone: "Please enter valid phone number",
                    password: {
                        required: "Please provide a password",
                        minlength: "Your password must be at least 5 characters long"
                    },
                    confirm_password: {
                        required: "Please provide a password",
                        minlength: "Your password must be at least 5 characters long",
                        equalTo: "Please enter the same password as above"
                    },
                    email: "Please enter a valid email address"
                },
                errorElement: "em",
                errorPlacement: function ( error, element ) {
                    // Add the `help-block` class to the error element
                    error.addClass( "help-block" );

                    // Add `has-feedback` class to the parent div.form-group
                    // in order to add icons to inputs
                    element.parents( ".form-group" ).addClass( "has-feedback" );

                    if ( element.prop( "type" ) === "checkbox" ) {
                        error.insertAfter( element.parent( "label" ) );
                    } else {
                        error.insertAfter( element );
                    }

                    // Add the span element, if doesn't exists, and apply the icon classes to it.
                    if ( !element.next( "span" )[ 0 ] ) {
                        $( "<span class='fa fa-times form-control-feedback'></span>" ).insertAfter( element );
                    }
                },
                success: function ( label, element ) {
                    // Add the span element, if doesn't exists, and apply the icon classes to it.
                    if ( !$( element ).next( "span" )[ 0 ] ) {
                        $( "<span class='fa fa-check form-control-feedback'></span>" ).insertAfter( $( element ) );
                    }
                },
                highlight: function ( element, errorClass, validClass ) {
                    $( element ).parents( ".form-group" ).addClass( "has-error" ).removeClass( "has-success" );
                    $( element ).next( "span" ).addClass( "fa-times" ).removeClass( "fa-check" );
                },
                unhighlight: function ( element, errorClass, validClass ) {
                    $( element ).parents( ".form-group" ).addClass( "has-success" ).removeClass( "has-error" );
                    $( element ).next( "span" ).addClass( "fa-check" ).removeClass( "fa-times" );
                }
            } );
            

        });