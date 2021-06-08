function getBathValue() {
  var uiBA = document.getElementsByName("uiBA");
  for(var i in uiBA) {
    if(uiBA[i].checked) {
      return parseInt(i)+1;
    }
  }
  return -1; // Invalid Value
}
  
function getBRValue() {
  var uiBR = document.getElementsByName("uiBR");
  for(var i in uiBR) {
    if(uiBR[i].checked) {
      return parseInt(i)+1;
    }
  }
  return -1; // Invalid Value
}

function getGDValue() {
  var uiGD = document.getElementsByName("uiGD");
  for(var i in uiGD) {
    if(uiGD[i].checked) {
      return parseInt(i)+1;
    }
  }
  return -1; // Invalid Value
}
  
function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");
  var city = document.getElementById("uiCity");
  var district = document.getElementById("uiDistrict");
  var sqft = document.getElementById("uiSqft");
  var bedrooms = getBRValue();
  var bathrooms = getBathValue();
  var garage = getGDValue();
  var lot_size = document.getElementById("uiAcres");
  var yr_built = document.getElementById("uiYR")
  var estPrice = document.getElementById("uiEstimatedPrice");
  // var url = "/api/predict_home_price"; when running on a production server
  var url = "http://127.0.0.1:5000/predict_home_price";

  $.post(url, {
    city: city.value,
    district: district.value,
    total_sqft: parseFloat(sqft.value),
    bedrooms: bedrooms,
    bathrooms: bathrooms,
    lot_size: parseFloat(lot_size.value),
    yr_built: parseInt(yr_built.value),
    garage: garage
  },function(data, status) {
    console.log(data.estimated_price);
    estPrice.innerHTML = `<h2>${data.estimated_price.toString()}</h2>`;
    console.log(status);
  });
}
  
function onPageLoad() {
  console.log( "document loaded" );
  //var url = "/api/get_city_names";
  var url= "http:127.0.0.1:5000/get_city_names";
  $.get(url,function(data, status) {
      console.log("got response for get_city_names request");
      if(data) {
        var city = data.city;
        var uiCity = document.getElementById("uiCity");
        $('#uiCity').empty();
        for(var i in city) {
            var opt = new Option(city[i]);
            $('#uiCity').append(opt);
        }
      }
  });
}
  
window.onload = onPageLoad;
