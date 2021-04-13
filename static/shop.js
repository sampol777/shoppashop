

$(document).ready(function(){
    let products=[];
    function loadProducts(){
       
     $.getJSON('/products', function(data, status, xhr){
        for (let i = 0; i < data.length; i++ ) {
       products.push(data[i].name);
     }
    });
    };
    loadProducts();
    $('#product').autocomplete({
     source: products 
    }); 
    
   }); 



   $(document).ready(function() {
   
   $('.container-fluid').on("click", ".quantity-btn", function (evt) {
      
      form = $(evt.target).closest("form")
      
      $('#cart-items').text(String(Number(form.find("#quantity").val()) + Number($('#cart-items').text())))
      
      form.submit(function (e) {
         e.preventDefault();
         
         const csrf_token = "{{ csrf_token() }}";
         
       $.ajaxSetup({
         beforeSend: function(xhr, settings) {
             if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                 xhr.setRequestHeader("X-CSRFToken", csrf_token)
             }
           }
        });

       $.ajax({
            type: "POST",
            url: '/addtocart',
            data: form.serialize(), // serializes the form's elements.
            success: function (data) { 
               
            }
        });
        
        setTimeout(function(){
             $(form)[0].reset()
          }, 200);
      }); 
   })
});

//edit product
$("#seller-products").on("click", "#edit-button",  function (evt) {
   evt.preventDefault();
   
   let product = $(evt.target).closest("div");
   let productId = product.attr("data-product-id");
   let productName = product.find('h5').attr("data-product-name")
   let productColor= product.find('h5').attr("data-product-color")
   let productPrice = product.find('p').attr("data-product-price")
   let productStock = product.find('p').attr("data-product-stock")

   $('#sellerproduct_id').val(productId)
   $('#name').val(productName)
   $("#color").val(productColor)
   $('#price').val(productPrice)
   $('#stock').val(productStock)
   

 });

////delete seller-product
 $("#seller-products").on("click", "#delete-button", async function (evt) {
   evt.preventDefault();
   console.log('pressed')
   let product = $(evt.target).closest('div');
   let productCard = $(evt.target).closest('div .card');
   let productId = product.attr("data-product-id");

   $.ajax({
         type: "DELETE",
         url: `/deleteproduct/${productId}`,
         success: function (data) {
               console.log(data)  // display the returned data in the console.
         }
      });

   productCard.remove()
   

 });

 $("#cart-table").on("click", "#cart-delete-button", async function (evt) {
   evt.preventDefault();
   console.log('pressed')
   let product = $(evt.target).closest('tr');
   
   let productId = product.attr("id");
   
   $.ajax({
         type: "DELETE",
         url: `/removefromcart/${productId}`,
         success: function (data) {
               console.log(data)  // display the returned data in the console.
         }
      });

        
      location.replace(location.pathname)     
       

 });