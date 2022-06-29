const url = window.location.href.split('/');
const protocol = url[0];
const domain = url[2];

disease_payload = [];
payload = {
                'tag': null,
                'followup_questions': null,
                'number_of_questions': null,
                'current_question': 0
            }

// onload message
$( document ).ready(function() {
     $('#chat-container').append(
        `
            <div class="col mb-2">
                <div class="row">
                    <div class="col col-2 col-sm-1 ">
                        <i class="fa fa-user-circle-o fa-2x" aria-hidden="true"></i>
                    </div>
                    <div class="col col-10 col-sm-10 rounded-pill p-2 make-light1 text-light">
                       <div class="ms-2">
                             I'm MediBot, your medical assistant...
                       </div>
                    </div>
                </div>
            </div>
        `
    );
});

// trigger click on enter
$(document).keypress(function(e){
    if (e.which == 13){
        e.preventDefault();
        $("#send-btn, #answer-btn").click();
    }
});



// send message
$(document).on('click', '#send-btn', function() {
    let pattern = $('#send').val();
    // display message
    displayMessage(pattern);

    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    let payload = {
        "url": `${$(location).attr('protocol')}//${domain}/api/v1.0/medibot/`,
        "method": "POST",
        "timeout": 0,
        "dataType": "json",
        "data": {
            "csrfmiddlewaretoken": csrf_token,
            'pattern': pattern,
        }
    };

    callChatBotEndPoints(payload);
});


// questioning mechanism
$(document).on('click', '#answer-btn', function() {
    answer = $('#send').val();
    if (answer === ''){
        response = {
            'response': 'Please answer the question.'
        }
        displayChatBotResponse(response);
    }
    else {
        disease_payload.push(answer);
        //display answer
        displayMessage(answer);
        // console.log('HD payload: ', disease_payload);

        // ask next question
        askQuestions(payload);
    }

});

// call chatbot end points
function callChatBotEndPoints(payload) {
    $.ajax(payload).done(function (response) {
        console.log(response);
        displayChatBotResponse(response);
        // updateCartIcon(response['Item Count'])
    });
}

// display user message
function displayMessage(msg){
    $('#chat-container').append(
        `
            <div class="col mb-2">
                <div class="row">
                    <div class="col col-10 col-sm-11 make-light2 rounded-pill p-2 text-light">
                       <div class="ms-2">
                            ${msg}
                       </div>
                    </div>
                    <div class="col col-2 col-sm-1">
                        <i class="fa fa-user-circle-o fa-2x" aria-hidden="true"></i>
                    </div>
                </div>
            </div>
        `
    );
    $('#send').focus();
}

// display chatbot response
function displayChatBotResponse(response){
    $('#send').val(null);

    $('#chat-container').append(
        `
            <div class="col mb-2">
                <div class="row">
                    <div class="col col-2 col-sm-1 ">
                        <i class="fa fa-user-square-o fa-2x" aria-hidden="true"></i>
                    </div>
                    <div class="col col-10 col-sm-10 rounded-0 p-2 make-light1 text-light">
                       <div class="ms-2 rounded-0">
                             ${response['response']}
                       </div>
                    </div>
                </div>
            </div>
        `
    );
    if (!(response['followup_questions'] == null)){
        payload['tag'] = response['tag'];
        payload['followup_questions'] = response['followup_questions'];
        payload['number_of_questions'] = response['followup_questions'].length;

        // change the send button
        removeSendButton();

        askQuestions(payload);
    }
    $('#send').focus();
}

// call diagnose endpoint
function callDiagnoseEndpoint(data) {
    // add send button
    addSendButton();
    // console.log('lol', data)
     let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        let payload = {
            "url": `${$(location).attr('protocol')}//${domain}/api/v1.0/diagnose/`,
            "method": "POST",
            "timeout": 0,
            "dataType": "json",
            "data": {
                "csrfmiddlewaretoken": csrf_token,
                'payload':JSON.stringify(data),
            }
        }

        $.ajax(payload).done(function (response) {
            displayChatBotResponse(response);
            // appointment cards
            displayDoctorList(response['doctors_list']);
        });
}



// ask question
function askQuestions(payload){
    response = {
        'response': payload['followup_questions'][payload['current_question']]
    }

    console.log('res', payload);

    if(payload['current_question'] === payload['number_of_questions']){
        if(payload['tag'] === 'diagnose'){
            console.log('Diagnose payload:', disease_payload);
            callDiagnoseEndpoint(disease_payload)
        }
        else {
            callHeartDiseaseEndPoint(disease_payload);
            // console.log('sending', disease_payload)
        }
    }
    else {
        displayChatBotResponse(response);
        payload['current_question'] += 1;
    }
}


// call heatdisease endpoint
function callHeartDiseaseEndPoint(data) {
    // add send button
    addSendButton();
    // console.log('lol', data)
     let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        let payload = {
            "url": `${$(location).attr('protocol')}//${domain}/api/v1.0/heart-disease-model/`,
            "method": "POST",
            "timeout": 0,
            "dataType": "json",
            "data": {
                "csrfmiddlewaretoken": csrf_token,
                'payload':JSON.stringify(data),
            }
        }

        $.ajax(payload).done(function (response) {
            displayChatBotResponse(response);
            // appointment cards
            displayDoctorList(response['doctors_list']);
        });
}

// display doctor list
function displayDoctorList(doctors_list){
    doctors_list.forEach(function(doctor){
        console.log(doctor)
        $('#chat-container').append(
          `
            <div class="card mb-2" id="${ doctor['id'] }">
              <h5 class="card-header">${ doctor['__str__'] }</h5>
              <div class="card-body">
                <h5 class="card-title">${ doctor['specialty'] }</h5>
                <p class="card-text">
                    <strong>First Name: </strong>${ doctor['first_name'] }<br>
                    <strong>Last Name: </strong>${ doctor['last_name'] }<br>
                    <strong>Experience: </strong>${ doctor['get_experience'] }<br>
                </p>
                <div class="row">
                    <div class="col">
                        <a href="${ doctor['link'] }" target="_blank">
                            <i class="fa fa-eye" aria-hidden="true"></i> see profile
                        </a>
                    </div>
                    <div class="col">
                         <button class="btn btn-success float-end appointment-btn" id="${ doctor['id'] }">
                            <i class="fa fa-bookmark-o" aria-hidden="true"></i>
                            Put an appointment
                        </button>
                    </div>
                </div>
              </div>
            </div>
          `
        );
        $('#send').focus();
    });
}

// appointment
$(document).on('click', '.appointment-btn', function(event) {
    let doctor_id = $(this).attr('id');
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    let payload = {
        "url": `${$(location).attr('protocol')}//${domain}/api/v1.0/appointment/`,
        "method": "POST",
        "timeout": 0,
        "dataType": "json",
        "data": {
            "csrfmiddlewaretoken": csrf_token,
            'doctor': doctor_id,
        }
    }

        $.ajax(payload).done(function (response) {
            displayAppointmentDetails(response);
            console.log(response);
        });
});

// display appointment details
function displayAppointmentDetails(response){
    $('#send').val(null);

    $('#chat-container').append(
        `
            <div class="col mb-2">
                <div class="row">
                    <div class="col col-2 col-sm-1 ">
                        <i class="fa fa-user-circle-o fa-2x" aria-hidden="true"></i>
                    </div>
                    <div class="col col-10 col-sm-10 rounded-pill bg-success p-2 text-light">
                       <div class="ms-2">
                             Your appointment is at ${parseISOString(response['date_time']) }
                       </div>
                    </div>
                </div>
            </div>
        `
    );
    $('#send').focus();
}

function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
}

// remove send button
function removeSendButton(){
    $('#send-btn').remove();
    $('#send-form').append(
        `
            <div class="col col-2 col-sm-2" id="answer-btn">
                  <button type="button" class="btn btn-primary mb-3">
                    <i class="fa fa-paper-plane" aria-hidden="true"></i>
                  </button>
                </div>
        `
    );
    $('#send').focus();
}

// add send button
function addSendButton(){
    $('#answer-btn').remove();
    $('#send-form').append(
        `
            <div class="col col-2 col-sm-2" id="send-btn">
                  <button type="button" class="btn btn-primary mb-3">
                    <i class="fa fa-paper-plane" aria-hidden="true"></i>
                  </button>
                </div>
        `
    );

}

function showAppointmentCard(doctors){
    $('#chat-container').append(
        `
            <div class="card">
              <h5 class="card-header">Featured</h5>
              <div class="card-body">
                <h5 class="card-title">Special title treatment</h5>
                <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                <a href="#" class="btn btn-primary">Go somewhere</a>
              </div>
            </div>
        `
    );
}

