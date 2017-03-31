var groups = new vis.DataSet();
var id_assoc_group = {};

$(document).ready(function(){

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrf);
          }
      }
  });

  //Dat nesting doe
  if (jQuery.isEmptyObject(groups._data)){
    for (var i = 0; i < courses.length; i++) {
      groups.add({"id": i, "content": courses[i]})
      if (!(courses[i] in id_assoc_group)){
        id_assoc_group[courses[i]] = i;
      }
    }
  }

  setBottomRowHeight();
  drawTimeline();
  setCourses();
  setUpNext();
  setNotes();
  initPopUps();
});


function drawTimeline() {
  $('#visualization').empty();

  var dataSet = [];
  for (i = 0; i < events.length; i++) {
    dataSet.push({
      "id": events[i].id,
      "content": events[i].name,
      "start": events[i].due_date,
      "group": id_assoc_group[events[i].course]
    });
  }

    var container = document.getElementById('visualization');
    var items = new vis.DataSet(dataSet);
    var options = {
      height: '300px',
      editable: {
        remove: true
      },
      onRemove: function(item, callback) {

        //TODO: Show alert to confirm delete.
        $.ajax({
          url: "http://127.0.0.1:8000/delete_event/",
          type: 'DELETE',
          data: {eventID: item.id, csrfmiddlewaretoken: csrf},
          // dataType: 'json',
          success: function(resp) {
            callback(item)
          },
          error: function(resp) {
            callback(null);
          }
        });
      }//End 'onRemove'
    }
    var timeline = new vis.Timeline(container, items, options);
    timeline.setGroups(groups);
}


//I have to do this because the data is sent as json and i can't use django templates
function setCourses(){
  var container = $('#courses');
  var eventPopContainer = $('#event-pop-course')
  for (var i = 0; i < courses.length; i++) {
    container.append('<div class="course"><h4>' + courses[i] + '</h4></div>');
    eventPopContainer.append('<option value="'+courses[i]+'">'+courses[i]+'</option>')
  }
}


//Again, data passed as json, django templates won't work for population
function setUpNext() {
  var previousDate = new Date(1970, 0, 1);
  var eventDate = null;
  var container = $('#up-next-container');
  var dateContainer = null;

  for (var i = 0; i < events.length; i++) {
    eventDate = new Date(events[i].due_date);
    if (eventDate.getDate() > previousDate.getDate()){
      dateContainer = container.append('<div class="listViewDay"><h4>' + eventDate.toDateString()+ '</h4></div>');
      previousDate = eventDate
    }
    dateContainer.append('<div class="event"><h6>' + events[i].name + '</h6></div>')
  }
}


function setNotes() {
  var container = $('#notes-container')
  container.empty
  for (var i = 0; i < notes.length; i++) {
    container.append('<div class="note"><h4>'+notes[i].title+'</h4><h6>'+notes[i].text+'</h6></div>')
  }
}


function initPopUps() {
  //- - - - - - - - - - NOTES POPUP - - - - - - - - - - -
  var addNotePopup = $('#add-note-popup');
  var addNoteButton = $('#add-note-image');
  var noteCancel = $('#note-cancel');

  addNoteButton.click(function() {
      addNotePopup.css('display', 'block');
  });

  noteCancel.click(function() {
    addNotePopup.css('display', 'none');
  });

  $('#new-note-form').ajaxForm({
    success: function(resp){
      var note_obj = JSON.parse(resp)
      notes.push(note_obj)
      addNotePopup.css('display', 'none');
      setNotes();
    }
  });

  //- - - - - - - - - - TASK POPUP - - - - - - - - - - -
  var addTaskPopup = $('#add-task-popup');
  var addTaskButton = $('#add-task-image');
  var taskCancel = $('#task-cancel');

  addTaskButton.click(function() {
      addTaskPopup.css('display', 'block');
  });

  taskCancel.click(function() {
    addTaskPopup.css('display', 'none');
  });

  window.onclick = (function(event) {
      if (event.target == addTaskPopup[0]) {
          addTaskPopup.css('display', 'none');
      }
      if (event.target == addNotePopup[0]) {
          addNotePopup.css('display', 'none');
      }
  });

  $('#new-task-form').ajaxForm({
    success: function(resp){
      var task_obj = JSON.parse(resp)
      events.push(task_obj)
      addTaskPopup.css('display', 'none');
      setUpNext();
      drawTimeline();
    },
    error: function(resp){
      addTaskPopup.css('display', 'none')
    }
  });
}


function setBottomRowHeight() {
  var theHeight = $(window).height() - 445;
      $('.scroller').css({"height":theHeight+"px"});

  $('.selector').click(function(){
    $(this).addClass('active').siblings().removeClass('active');
  });

  $('.course').click(function(){
    $(this).addClass('courseActive').siblings().removeClass('courseActive');
  });

  $('.category').click(function(){
    $(this).addClass('categoryActive').siblings().removeClass('categoryActive');
  });
}


//Ayyy girl! OMG !!!!!Kevin, you are the bomb diggity;
