

$(document).ready(function () {



    function startTimer(duration, display) {
        const timerElement = document.getElementById(display);
        const otpInputFieldContainer = document.getElementById('otp-field');
        const otpButtonContainer = document.getElementById('get-otp');

        otpInputFieldContainer.classList.toggle('d-none');
        otpButtonContainer.classList.toggle('d-none');
        function updateTimer() {
            const minutes = Math.floor(duration / 60);
            const seconds = duration % 60;
            const secondsStr = seconds < 10 ? '0' + seconds : seconds;
            timerElement.textContent = `Time Remaining: ${minutes}:${secondsStr}`;
            if (duration < 0) {
                clearInterval(timerInterval);
                otpInputFieldContainer.classList.toggle('d-none');
                otpButtonContainer.classList.toggle('d-none');
                timerElement.textContent = 'Resend Otp!';
            }
            duration--;

            let otpInputField = $('#id_otp').val()
            if (otpInputField.length == 6){
                clearInterval(timerInterval);
                timerElement.textContent= ""
            }
        }

        updateTimer(); // Call updateTimer immediately to prevent initial delay
        const timerInterval = setInterval(updateTimer, 1000);
    }

    
    // Call the function to start the timer
    // TODO GET OTP
    $('#get_otp-button').click(function () {
        let email = $('#id_email').val().trim()
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val().trim(); 

        console.log(email)
        if (email){
            startTimer(120, 'timer');
        }
        $.ajax({
            type: "POST",
            headers: {
                'X-CSRFToken': csrfToken 
            },
            url: "/api/getOTP/",
            data: {
                email: email,
            },
            dataType: "json",
            success: function (response) {
                console.log(response);
                
            }
        });
    });

    
    // TODO SEARCH SERVICES 
    $('#search_button').click(function () {
        let service = $('#search_input').val().trim()
        $('#data_pagination').addClass('d-none')

        if(service)
        {    
            $.ajax({
                type: "GET",
                url: "/",
                data: {
                    service: service
                },
                dataType: "json",
                success: function (response) {
                    console.log(response);
                    let data = response.page_obj
                    let str = ``
                    if(data.length > 0){
                        for (let i = 0; i < data.length; i++) {
                            str += ` <a href=${data[i].id} class="card m-4 position-relative" style="width: 23rem;text-decoration:none;">
                                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-${data[i].is_active===true?"success":"danger"} p-2">${data[i].is_active===true?"Active":"In-Active"}</span>
                                <img src="${data[i].image?"http://localhost:8000/"+data[i].image:''}" class="card-img-top" alt="...">
                                <div class="card-body">
                                    <h5 class="card-title">${data[i].name}</h5>
                                    <p class="card-text">Price: ${data[i].price}/-</p>
                                </div>
                            </a>`
                        }
                    }else{
                        str += `<h1>No Service Available</h>`
                    }

                    $('#service-cards').html(str);
                },
                error: function() {
                    location.reload();
                }
            });
        }
    });


    $('#update-service').click(function () {
        let service_id = $('#service_id').val().trim()
        console.log(service_id)

        $.ajax({
            type: "GET",
            url: "/updateService/",
            data: {
                id: service_id,
            },
            dataType: "json",
            success: function (response) {
                console.log(response);
                
            }
        });
    });

    $('#delete-service').click(function () {
        let service_id = $('#service_id').val().trim()
        console.log(service_id)

        $.ajax({
            type: "DELETE",
            url: "/api/service/",
            data: {
                id: service_id,
            },
            dataType: "json",
            success: function (response) {
                console.log(response);
                
            }
        });
    });
});