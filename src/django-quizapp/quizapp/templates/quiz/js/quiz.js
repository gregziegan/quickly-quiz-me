var source = $('body').html()

var errored_posts = 0;

$(function() {
    var content = $('textarea').val();

    $('textarea').keyup(function(e) { 
        var answer_element = $(e.currentTarget)
        if (answer_element.val() != content) {
            save_essay_response(answer_element)
        }
    });

    $('input.mult-choice').click(function(e) {
      var answer_element = $(e.currentTarget)
      save_response(answer_element, true)
    });
});

function show_question(question_id) {
    $('#overview').hide()
    hide_questions()
    $('#question-' + question_id).show()
}

function hide_questions() {
    var re = /id="question-\d+/g
    var questions = source.match(re)
    for (var i = 0; i < questions.length; i++) {
        $('#question-' + /\d+/.exec(questions[i])).hide()
    }
}

function show_overview() {
    hide_questions()
    $('#overview').show()
}

function save_mult_choice_response(post_url, letter) {

  $.ajax({
      url : post_url,
      type : 'POST',
      data : {'answer': letter},
      success: function(data, testStatus, errorThrown)
      {
          errored_posts = 0;
      },
      error: function(jqXHR, testStatus, errorThrown)
      {
          console.log('Error saving response');
      }
    });

}

function save_essay_response(post_url, content) {

  $.ajax({
      url : post_url,
      type : 'POST',
      data : {'answer': content},
      success: function(data, testStatus, errorThrown)
      {
          errored_posts = 0;
      },
      error: function(jqXHR, testStatus, errorThrown)
      {
          errored_posts += 1;
          if (errored_posts >= 3) {
              alert("We are having trouble saving your responses.");
              errored_posts = 0;
          }
          console.log('Error saving response');
      }
    });

}

function save_response(answer_element, is_multiple_choice) {
    var content = answer_element.val();
    var url_base = location.href.substring(0, location.href.lastIndexOf("/")+1)
    var post_url = url_base + 'auto-save/?question_id=' + /\d+/.exec(answer_element.attr('id'))

    if (is_multiple_choice) {
      save_mult_choice_response(post_url, content)
    } else {
      save_essay_response(post_url, content)
    }
  
}

$(document).ready(function() {
    var answers = {{ answers|safe }}
    var re = /id="response-\d+/g
    var responses = source.match(re)
    var response_id;
    for (var i = 0; i < responses.length; i++) {
        response_id = /\d+/.exec(responses[i]);
        var answer = answers[response_id.toString()];
        $('#response-' + response_id).val(answer['essay']);
    }
    var question_ids = {{ question_ids|safe }};
    for (var i = 0; i < question_ids.length; i++) {
      var question_id = question_ids[i].toString();
      var answer = answers[question_id];
      $('#question-' + question_id + '-choice-' + answer['mult_choice']).prop("checked", true)
    }
});

function save_all_responses(new_url) {
    var re = /id="response-\d+/g
    var responses = source.match(re)
    var response_id;

    for (var i = 0; i < responses.length; i++) {
        response_id = /\d+/.exec(responses[i])
        // Used to make sure the last ajax post redirects the user
        if (i == responses.length - 1) {
            save_response($('#response-' + response_id), new_url);
        } else {
            save_response($('#response-' + response_id));
        }
    }
}

function next_question(question_ordinal) {
    var new_question_ordinal = parseInt(question_ordinal) + 1
    $('#question-' + question_ordinal).hide()
    $('#question-' + new_question_ordinal).show()
}
