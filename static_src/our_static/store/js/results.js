$(document).ready(function() {
    if ($("div").find(".no-baker-in-locality-error")){
      $('.cd-fail-message').css('display','none');
    }
    wghtPriceUpdate();
    boxPriceUpdate();
    eggPriceUpdate();


    /*Upadte removeItem()*/
    removeItem();
    likeProduct();
    /*Quick Add product to cart */
    $('form[id^=quickadd-form]').submit(function(e) { // catch the form's submit event
        var formId = $(this).attr('id');
        var itemID = formId.substring(13);
        $('#productBoxDetails' + itemID).css('display','none');
        $('#spinner' + itemID).css('display', 'block');
        e.preventDefault();
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function(data) { // on success..
              var quick_cart = jQuery.parseJSON(data);
              $('#checkout__tbody').append('<tr class="new_item"><td>'+quick_cart.get_cart_item+'<span><br/><span class="text-lowercase"> by </span>'+ quick_cart.get_cart_item_baker+'</span></td><td id="item_total'+quick_cart.get_cart_item_slug+quick_cart.get_cart_item_id+'">&#8377;'+quick_cart.get_cart_item_total+'</td><td style="text-align:center"><a href="#" class="text-white" id="remove-item'+quick_cart.get_cart_id+'"><i class="fa fa-times"></i></a></td></tr>');
                $('#total_cart_items_count').html(quick_cart.get_total_items_count);
                $('#cart_total').html('&#8377;'+quick_cart.get_cart_total);
                removeItem();
                document.getElementById(formId).reset();
                $('#productInCart' + quick_cart.get_cart_item_id).css('display', 'block');
                $('#spinner' + quick_cart.get_cart_item_id).css('display', 'none');
            },
            error: function(data) {
                setTimeout(function() {
                  $('#errorModal').modal({backdrop:'static', keyboard:false,show:true});
                }, 1000);
            }/*  end of error */
        });
        return false;
    });
    /* one click remove product from cart */
    function removeItem(){
      $('a[id^=remove-item]').on("click", function(e) { // catch the form's submit event
        e.preventDefault();
        var aId = $(this).attr('id');
        var itemID = aId.substring(11);
        $(this).closest('tr').removeClass('new_item');
        $(this).closest('tr').addClass('remove');
        setTimeout(function() {$('.remove').css('display', 'none')}, 400);
        $.ajax({
          url:'/quick_cart/remove/'+itemID+'/',
          success: function(data) { // on success..
              var quick_remove = jQuery.parseJSON(data);
                $('#total_cart_items_count').html(quick_remove.get_total_items_count);
                $('#cart_total').html('&#8377;'+quick_remove.get_cart_total);
                $('#productInCart' + quick_remove.get_cart_item_id).css('display', 'none');
                $('#productBoxDetails' + quick_remove.get_cart_item_id).css('display', 'block');
            },
            
        });
    });
    };/* end of removeItem()*/
    function likeProduct(){
      $('a[id^=itemLike]').on("click", function(e) { // catch the form's submit event
        e.preventDefault();
        var aId = $(this).attr('id');
        var itemID = aId.substring(8);
        $.ajax({
          url:'/product/'+itemID+'/',
          success: function(data) { // on success..
              var rating_status = jQuery.parseJSON(data);
              if (rating_status.Success == "True") {
                $('a').find('#heart-icon' + itemID).removeClass('fa-heart-o text-not-liked').addClass('fa-heart text-liked');
                $('#like-count' + itemID).html(rating_status.count);
              } else if (rating_status.Removed == "True") {
                $('a').find('#heart-icon' + itemID).removeClass('fa-heart text-liked').addClass('fa-heart-o text-not-liked');
                $('#like-count' + itemID).html(rating_status.count);
              }
            },/* end of success */
            error: function(data) {
                setTimeout(function() {$('#errorModal').modal({backdrop:'static', keyboard:false,show:true});}, 1000);
            }/*  end of error */
        });/* end of ajax */
    });/* end of onclick*/
    };/* end of likeProduct()*/
});/*end of document.ready */    
$(document).ready(function(){
  /* lazy load */
  $("img.lazy").lazyload();
  
});/* End of document.ready */
/* content- checkbox */
(function() {
        [].slice.call( document.querySelectorAll( '.checkout' ) ).forEach( function( el ) {
          var openCtrl = el.querySelector( '.checkout__button' ),
            closeCtrls = el.querySelectorAll( '.checkout__cancel' );

          openCtrl.addEventListener( 'click', function(ev) {
            ev.preventDefault();
            classie.add( el, 'checkout--active' );
          } );

          [].slice.call( closeCtrls ).forEach( function( ctrl ) {
            ctrl.addEventListener( 'click', function() {
              classie.remove( el, 'checkout--active' );
            } );
          } );
        } );
      })();

function wghtPriceUpdate(){
  $("select[id^=addWeightSelect]").change(function(){
    var selectId = $(this).attr('id');
    var prodID = selectId.substring(15);
    var eggExtraPrice = $('#addEggSelect' + prodID).find(':selected').data('price')
    var price = parseFloat($('#price' + prodID).data('base-price'));
    $('#price' + prodID).tooltip('disable');
    $('#addWeightSelect' + prodID).each(function(i, el) {
        price = parseFloat($('option:selected', el).data('price')) + parseFloat($('#addEggSelect' + prodID).find(':selected').data('price'));
    });
    $('#price' + prodID).html("&#8377;" + price.toFixed(2));
    $('#price' + prodID).data('base-price', price);
  });/* end of weight price calulation. */
};
function boxPriceUpdate(){
  $('select[id^=addBoxSelect]').change(function(){
    var selectId = $(this).attr('id');
    var prodID = selectId.substring(12);
    var price = parseFloat($('#price' + prodID).data('base-price'));
    $('#price' + prodID).tooltip('disable');
    $('#addBoxSelect' + prodID).each(function(i, el) {
        price = parseFloat($('option:selected', el).data('price')) + parseFloat($('#addEggSelect' + prodID).find(':selected').data('price'));
    });
    $('#price' + prodID).html("&#8377;" + price.toFixed(2));
    $('#price' + prodID).data('base-price', price);
  });/* end of box price calulation. */
};
function eggPriceUpdate(){
  $('select[id^=addEggSelect]').change(function(){
    var selectId = $(this).attr('id');
    var prodID = selectId.substring(12);
    var price = parseFloat($('#price' + prodID).data('base-price'));
    $('#addEggSelect' + prodID).each(function(i, el) {
            if ($('#addWeightSelect' + prodID).length) {
              price = parseFloat($('option:selected', el).data('price')) + parseFloat($('#addWeightSelect' + prodID).find(':selected').data('price'));
            } else {
              price = parseFloat($('option:selected', el).data('price')) + parseFloat($('#addBoxSelect' + prodID).find(':selected').data('price'));
            }
            
    });
    $('#price' + prodID).html("&#8377;" + price.toFixed(2));
    $('#price' + prodID).data('base-price', price);
  });/* end of egg price calulation. */
};




  
  