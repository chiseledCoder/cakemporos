$(document).ready(function() {
    
    /*Calulating various dates and time formats for timepicker*/
    var weekday = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    var d1 = new Date ();
    var d2 = new Date ( d1 );
    d2.setHours ( d1.getHours() + 6 );
    var x = weekday[d1.getDay()];
    var n = d1.getDate();
    var m = d1.getMonth() + 1;
    var y = d1.getFullYear();
    if (n<10 && m<10) {
      var d3 = x+', '+'0'+n+'/0'+m+'/'+y;
    }
    else if (n>10 && m<10){
      var d3 = x+', '+n+'/0'+m+'/'+y;
    } else if(n<10 && m>=10) {
      var d3 = x+', '+n+'0/'+m+'/'+y;
    }
    else{
      var d3 = x+', '+n+'/'+m+'/'+y;
    }
    var h1 = d1.getHours();
    var h2 = 11+3;
    hstring = h2.toString()
    var h3 = hstring.concat(":00pm");
    var h4 = h1 + 3;
    $('#delivery-date').datepicker({
      startDate:d2,
      autoclose: true,
      format:"DD, dd/mm/yyyy"
    });
    $('#delivery-date').on('change',function(){
      var deliDate = $(this).val();
      if (deliDate == d3 && h1<11) {
        $('#ifToday').show();
        $('#delivery-time').timepicker({
          'minTime': h2.toString(),
          'maxTime': '08:00pm'
        });
            $('#delivery-time').timepicker('setTime', h2.toString());
      } 
      else if(deliDate == d3 && h1>=11 ){
        $('#ifToday').show();
        $('#delivery-time').timepicker({
          'minTime': h4.toString(),
          'maxTime': '08:00pm'
        });
            $('#delivery-time').timepicker('setTime', h4.toString());

      }
        else if (deliDate != d3 && h4<11) {
        $('#ifToday').show();
        $('#delivery-time').timepicker({
          'minTime': '11:00am',
          'maxTime': '08:00pm'
        });
        $('#delivery-time').timepicker('setTime', '11:00am');


      } 
      else {
          $('#ifToday').show();
          $('#delivery-time').timepicker({
          'minTime': '11:00am',
          'maxTime': '08:00pm'
        });
        $('#delivery-time').timepicker('setTime', '11:00am');
        }
    });
    $('#delivery-time').keypress(function(event) {
          event.preventDefault();
         return false;
     });
    $('input[name="payment_method"]').click(function(){
      if($(this).val() == "Cash On Delivery"){
        $('#mobile_verification').css('display', 'block');
      }
    });
    $(".addrs").change(function(){
        $("#new_ship_address").val($("#flatno").val() + "," + $("#buildno").val() + "," + $("#landmark").val()+ "," + $("#locality").val());
        $('#newAddrProceedBtn2').prop('disabled', false);
        
    });
    // SO TEXAREA WOULD NOT COPY ANY EMPTY LINES??
    $('.btn-number').click(function(e){
    e.preventDefault();
    
    fieldName = $(this).attr('data-field');
    type      = $(this).attr('data-type');
    var input = $("input[name='"+fieldName+"']");
    var currentVal = parseInt(input.val());
    if (!isNaN(currentVal)) {
        if(type == 'minus') {
            
            if(currentVal > input.attr('min')) {
                input.val(currentVal - 1).change();
            } 
            if(parseInt(input.val()) == input.attr('min')) {
                $(this).attr('disabled', true);
            }

        } else if(type == 'plus') {

            if(currentVal < input.attr('max')) {
                input.val(currentVal + 1).change();
            }
            if(parseInt(input.val()) == input.attr('max')) {
                $(this).attr('disabled', true);
            }

        }
    } else {
        input.val(0);
    }
  });
    $('.input-number').focusin(function(){
       $(this).data('oldValue', $(this).val());
    });
    $('.input-number').change(function() {
        
        minValue =  parseInt($(this).attr('min'));
        maxValue =  parseInt($(this).attr('max'));
        valueCurrent = parseInt($(this).val());
        
        name = $(this).attr('name');
        if(valueCurrent >= minValue) {
            $(".btn-number[data-type='minus'][data-field='"+name+"']").removeAttr('disabled')
        } else {
            alert('Sorry, the minimum value was reached');
            $(this).val($(this).data('oldValue'));
        }
        if(valueCurrent <= maxValue) {
            $(".btn-number[data-type='plus'][data-field='"+name+"']").removeAttr('disabled')
        } else {
            alert('Sorry, the maximum value was reached');
            $(this).val($(this).data('oldValue'));
        }
        
        
    });
    $(".input-number").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) || 
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });
    $('input[id^="photoCakeCheck"').iCheck({
      checkboxClass: 'icheckbox_square-yellow',
      radioClass: 'iradio_square-yellow',
      increaseArea: '20%' // optional
    });
    $('input[id^="addon"').iCheck({
      checkboxClass: 'icheckbox_square-yellow',
      radioClass: 'iradio_square-yellow',
      increaseArea: '20%' // optional
    });
    $('input[id^="photoCakeCheck"').on('ifChecked', function () { 
      $('div[id^="photoUploadField"').css('display','block');
     });
    $('input[id^="photoCakeCheck"').on('ifUnchecked', function () { 
      $('div[id^="photoUploadField"').css('display','none');
     });
    
;

( function ( document, window, index )
{
  var inputs = document.querySelectorAll( '.photoCakeUpload' );
  Array.prototype.forEach.call( inputs, function( input )
  {
    var label  = input.nextElementSibling,
      labelVal = label.innerHTML;

    input.addEventListener( 'change', function( e )
    {
      var fileName = '';
      if( this.files && this.files.length > 1 )
        fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
      else
        fileName = e.target.value.split( '\\' ).pop();

      if( fileName )
        label.querySelector( 'span' ).innerHTML = fileName;
      else
        label.innerHTML = labelVal;
    });

    // Firefox bug fix
    input.addEventListener( 'focus', function(){ input.classList.add( 'has-focus' ); });
    input.addEventListener( 'blur', function(){ input.classList.remove( 'has-focus' ); });
  });
}( document, window, 0 ));



       
  });/* end of document.ready*/
  $(document).ready(function () {

    var navListItems = $('div.setup-panel div a'),
            allWells = $('.setup-content'),
            allNextBtn = $('.nextBtn'),
            allPrevBtn = $('.prevBtn');

    allWells.hide();

    navListItems.click(function (e) {
        e.preventDefault();
        var $target = $($(this).attr('href')),
                $item = $(this);

        if (!$item.hasClass('disabled')) {
            navListItems.removeClass('btn-cakemporos').addClass('btn-default');
            $item.removeClass('btn-default').addClass('btn-cakemporos');
            allWells.hide();
            $target.show();
        }
    });
    allNextBtn.click(function(){
        var curStep = $(this).closest(".setup-content"),
            curStepBtn = curStep.attr("id"),
            nextStepWizard = $('div.setup-panel div a[href="#' + curStepBtn + '"]').parent().next().children("a"),
            curInputs = curStep.find("input[type='text']"),
            isValid = true;
/*input[type='text'],input[type='url'], input[type='radio']*/
            
        $(".form-group").removeClass("has-error");
        for(var i=0; i<curInputs.length; i++){
            if (!curInputs[i].validity.valid){
                isValid = false;
                $(curInputs[i]).closest(".form-group").addClass("has-error");
            }
        }
        var no_address = $('#address_select').val();
        var no_delivery_date = $('#delivery-date').val();
        var lets_go = false
        if(curStepBtn == "step-2" && no_address == null){
              $('#enterAddressError').css('display','block');
              $('#enterDeliveryDateError').css('display','none');
              $('#enterDeliveryTimeError').css('display','none');
              isValid = false;
            }
            else if(curStepBtn == "step-2" && no_delivery_date.length === 0){
              $('#enterAddressError').css('display','none');
              isValid = false; 
            }
            else{
              isValid = true;
              lets_go = true;
            }
        if(curStepBtn == "step-2"){
          var del_address = $('#address_select').val();
          var del_date = $('#delivery-date').val();
          var del_time = $('#delivery-time').val();
          $('#final_delivery_address').html(del_address);
          $('#final_delivery_date').html(del_date);
          $('#final_delivery_time').html(del_time);
          if (lets_go == true){
              $('.payment-options').css('display','none');
              $('#spinner').css('display', 'block');
              var add_id = $('select[name="prev_shipping_address"]').find(':selected').data('id');
              $.ajax({
                  url: "/calculate_delivery_charge/"+add_id, // the file to call
                  success: function(data){
                    var calc_response = jQuery.parseJSON(data);
                    console.log(calc_response);
                    $('#spinner').css('display', 'none');
                    $('.payment-options').css('display','block');
                    $('#updateDeliveryCost').html(calc_response.delivery_total);
                    $('#updateCartTotal').html(calc_response.cart_sub_total);
                    $('#updateCouponDetails').html(calc_response.coupon);
                    $('#updateAmountPayable').html(calc_response.cart_total);
                    if (calc_response.no_delivery == "True"){
                      $('#noDeliveryModal').modal({backdrop:'static', keyboard:false,show:true});
                    }
                  },/*./success*/
                  error: function(xhr, status, error) {
                      $('#errorModal').modal({backdrop:'static', keyboard:false,show:true});
                    }/*  end of error */
                  });
          }
        }
        if (isValid){
            nextStepWizard.removeClass('disabled');
            nextStepWizard.removeAttr('disabled').trigger('click');
          }

    });
    
    allPrevBtn.click(function(){
        var curStep = $(this).closest(".setup-content"),
            curStepBtn = curStep.attr("id"),
            prevStepWizard = $('div.setup-panel div a[href="#' + curStepBtn + '"]').parent().prev().children("a");

        $(".form-group").removeClass("has-error");
        prevStepWizard.removeAttr('disabled').trigger('click');
    });
    $('div.setup-panel div a.btn-cakemporos').trigger('click');
});/*end of document.ready */