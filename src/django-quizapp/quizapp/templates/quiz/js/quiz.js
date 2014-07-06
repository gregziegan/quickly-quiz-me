var source = $('body').html()

{% if candidate_exam.exam.time_limit %}
var time_limit = {{ candidate_exam.exam.time_limit }}; 
var start_datetime = new Date('{{ candidate_exam.started_at|date:"F d, Y H:i:s" }}');
var end_by_datetime = new Date(start_datetime.getTime() + time_limit * 60000);
  {% if candidate_exam.exam.time_limit > 60 %}
    $('#exam_time').countdown({until: end_by_datetime, layout: '{hn} {hl}, {mn} {ml} Remaining'});
  {% else %}
    $('#exam_time').countdown({until: end_by_datetime, layout: '{mn} {ml}, {sn} {sl} Remaining'});
  {% endif %}
var absolute_end_by_datetime = new Date(start_datetime.getTime() + time_limit * 2 * 60000);
var today = new Date()
{% endif %}

{% if not candidate_exam.exam.requires_answer_file %}
var errored_posts = 0;

function chevron_swap(section_id) {
    chevron_span = $('#chevron_span_' + section_id)
    current_chevron_class = chevron_span.attr('class').split(/\s+/)[1];
    chevron_span.removeClass(current_chevron_class)
    if (current_chevron_class == 'glyphicon-chevron-down') {
        chevron_span.addClass('glyphicon-chevron-up')
    } else {
        chevron_span.addClass('glyphicon-chevron-down')
    }
}

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

function save_response(answer_element, new_url) {
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
              window.location.href = new_url;
          }
      },
      error: function(jqXHR, testStatus, errorThrown)
      {
          errored_posts += 1;
          if (errored_posts >= 3) {
              alert("We are having trouble saving your responses.\nKeep your responses backed up elsewhere and contact screening-help@vertical-knowledge.com");
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
        $('#response-' + response_id).val(answers[response_id.toString()]);
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
{% endif %}

function confirm_submission() {
    var submit = confirm('Are you sure?\nAnswers will no longer be able to be edited.');
 
    console.log(submit)
    if (submit) {
        console.log('click')
        $('#submit_exam_btn').click();
    }
}
