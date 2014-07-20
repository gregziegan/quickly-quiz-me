var source = $('body').html()

var errored_posts = 0;

$(function() {
    var content = $('textarea').val();

    $('textarea').keyup(function(e) { 
        answer_element = $(e.currentTarget)
        if (answer_element.val() != content) {
            save_response(answer_element)
        }
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

function save_response(answer_element) {
    var content = answer_element.val();
    var url_base = location.href.substring(0, location.href.lastIndexOf("/")+1)
    var post_url = url_base + 'auto-save/?question_id=' + /\d+/.exec(answer_element.attr('id'))

    $.ajax({
      url : post_url,
      type : 'POST',
      data : {'answer': content},
      success: function(data, testStatus, errorThrown)
      {
          errored_posts = 0;
          if (new_url) {
            window.location.replace(new_url)
          }
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

$(document).ready(function() {
    var answers = {{ answers|safe }}
    var re = /id="response-\d+/g
    var responses = source.match(re)
    var response_id;
    for (var i = 0; i < responses.length; i++) {
        response_id = /\d+/.exec(responses[i]);
        var answer = answers[response_id.toString()];
        $('#response-' + response_id).val(answer['essay']);
        $('#question-' + response_id + '-choice-' + answer['mult_choice']).prop("checked", true)
    }
});

function save_all_responses(new_url) {
    var re = /id="response-\d+/g
    var responses = source.match(re)
    var response_id

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
