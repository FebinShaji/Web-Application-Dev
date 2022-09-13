function mySave() {
  var notes = document.getElementById("Textbox").value;
  localStorage.setItem("notes", notes);
}
function myLoad() {
  var notes = localStorage.getItem("notes");
  document.getElementById("Textbox").value = notes;
}
function clear()  {
  var notes = localStorage.getItem("notes");
  localStorage.clear();
}
