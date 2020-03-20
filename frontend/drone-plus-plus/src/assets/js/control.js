window.addEventListener("DOMContentLoaded",()=>{
  const floatContainers = document.getElementsByClassName("float-container");
  for(let fc of floatContainers){
    let floatField = fc.getElementsByClassName("float-field");
    for (ff of floatField) {
      ff.addEventListener('focus', ()=>{
        fc.classList.add('active');
      });
    }
    ff.addEventListener('blur', ()=>{
      if (ff.innerHTML == null)
        fc.classList.remove('active');
    });
  }
});

function profileOptions(){
  event.stopPropagation();
  document.getElementById("profile-dropdown").classList.toggle("inactive");
}

window.onclick = function(event) {
  try {
    document.getElementById("profile-dropdown").classList.add("inactive");
  } catch {

  };

}
