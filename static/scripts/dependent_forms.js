
$(document).ready(function() {
    $('#brand').on('change', function() {
      $('.dependency').hide();
      
      if (this.value==="bmw"){
        $('#bmw').show()
      }else if(this.value==="audi"){
        $('#audi').show()
      }else if(this.value==="mercedes"){
        $('#mercedes').show()
      }else if(this.value==="ford"){
        $('#ford').show()
      }else if(this.value==="mazda"){
        $('#mazda').show()
      }else if(this.value==="volvo"){
        $('#volvo').show()
      }else if(this.value==="chevrolet"){
        $('#chevrolet').show()
      }else if(this.value==="dodge"){
        $('#dodge').show()
      }else if(this.value==="seat"){
        $('#seat').show()
      }
    });
  });

/*
  $(document).ready(function() {
    $('#brand').on('change', function() {
      $('.dependency').hide();
  
      if (this.value==="car1"){
        $('#pieces_for_car_1').show()
      }else if(this.value==="car2"){
        $('#pieces_for_car_2').show()
      }else if(this.value==="car3"){
        $('#pieces_for_car_3').show()
      }else if(this.value==="all_cars"){
        $('#pieces_for_all_cars').show()
      }
    });
  });
  */