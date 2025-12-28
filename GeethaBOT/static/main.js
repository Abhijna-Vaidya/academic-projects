/**
 * Returns the current datetime for the message creation.
 */
function getCurrentTimestamp() {
	return new Date();
}

/**
 * Renders a message on the chat screen based on the given arguments.
 * This is called from the `showUserMessage` and `showBotMessage`.
 */
function renderMessageToScreen(args) {
	// local variables
	let displayDate = (args.time || getCurrentTimestamp()).toLocaleString('en-IN', {
		month: 'short',
		day: 'numeric',
		hour: 'numeric',
		minute: 'numeric',
	});
	let messagesContainer = $('.messages');

	// init element
	let message = $(`
	<li class="message ${args.message_side}">
		<div class="avatar"></div>
		<div class="text_wrapper" style="width: fit-content;">
			<div class="text">${args.text}</div>
			<div class="timestamp">${displayDate}</div>
		</div>
	</li>
	`);

	// add to parent
	messagesContainer.append(message);

	// animations
	setTimeout(function () {
		message.addClass('appeared');
	}, 0);
	messagesContainer.animate({ scrollTop: messagesContainer.prop('scrollHeight') }, 300);
}

/* Sends a message when the 'Enter' key is pressed.
 */
$(document).ready(function() {
    $('#msg_input').keydown(function(e) {
        // Check for 'Enter' key
        if (e.key === 'Enter') {
            // Prevent default behaviour of enter key
            e.preventDefault();
			// Trigger send button click event
            $('#send_button').click();
        }
    });
});

/**
 * Displays the user message on the chat screen. This is the right side message.
 */
function showUserMessage(message, datetime) {
	renderMessageToScreen({
		text: message,
		time: datetime,
		message_side: 'right',
	});
}

/**
 * Displays the chatbot message on the chat screen. This is the left side message.
 */
function showBotMessage(message, datetime) {
	renderMessageToScreen({
		text: message,
		time: datetime,
		message_side: 'left',
	});
}

/**
 * Get input from user and show it on screen on button click.
*/
 $('#contact_button').on('click', function (e) {
    // Get and show user message, then reset input
    const userInput = "Contact Us"
    showUserMessage(userInput);
    
    // Show bot response based on user input
      setTimeout(function () {
        showBotMessage("<p><b>Contact Information</b></p><p>Phone : 0821 - 4257304, 2581304, 2977306</p>e-mail : gsssengg@gmail.com</div>");
      }, 300);
    }
  );

  $('#department_button').on('click', function (e) {
    // Get and show user message, then reset input
    const userInput = "Our Departments"
    showUserMessage(userInput);
    
    // Show bot response based on user input
    setTimeout(function () {
      showBotMessage("<div><div id='cse_button' class='button'>CSE</div><div id='ise_button' class='button'>ISE</div><div id='aiml_button' class='button'>AI & ML</div><div><div id='ece_button' class='button'>ECE</div><div id='eee_button' class='button'>EEE</div><div id='aids_button' class='button'>AI & DS</div>")
    }, 300);
    }
  );

  $('#location_button').on('click', function (e) {
    // Get and show user message, then reset input
    const userInput = "Location"
    showUserMessage(userInput);
    
    // Show bot response based on user input
      setTimeout(function () {
        showBotMessage("<figure><img src='static//college.jpg' style='width:100%'><figcaption style='text-align:center'><b>Our Location</b></figcaption><a href='https://www.google.com/maps/place/GSSS+Institute+of+Engineering+and+Technology+for+Women+-+Mysuru/@12.361618,76.6265765,17z/data=!4m10!1m2!2m1!1sgsss+engineering+college+mysore+location!3m6!1s0x3baf7a4400000021:0x93637e6857ed9677!8m2!3d12.3615489!4d76.6286206!15sCihnc3NzIGVuZ2luZWVyaW5nIGNvbGxlZ2UgbXlzb3JlIGxvY2F0aW9ukgEHY29sbGVnZeABAA!16s%2Fg%2F11btydf5_z?entry=ttu' target='_blank'><p style='text-align:center'>GSSS Institute of Engineering and Technology for Women</p></a></div>");
      }, 300);
    }
  );

  $('#placement_button').on('click', function (e) {
    // Get and show user message, then reset input
    const userInput = "Placement Statistics"
    showUserMessage(userInput);
    
    // Show bot response based on user input
      setTimeout(function () {
        showBotMessage("<figure><img src='static//placement_numberOfPlacements.png' style='width:100%'><figcaption style='text-align:center'><b>Number Of Placement Offers</b></figcaption></figure><br><br><figure><img src='static//placement_totalNumberOfOffers.png' style='width:100%'><figcaption style='text-align:center'><b>Year Wise Total No. of Placement Offers</b></figcaption></figure><br><br><figure><img src='static//placement_dreamAndSuperDream.png' style='width:100%'><figcaption style='text-align:center'><b>Year Wise Total No. of Dream & Super Dream Offer</b></figcaption></figure>"
        );
        showBotMessage("To Know More Visit : <br><p><a href='https://geethashishu.in/departments/placements'><p>Placement Department<p></a></br>");
      }, 300);
    }
  );

  $('#hostel_button').on('click', function (e) {
    // Get and show user message, then reset input
    const userInput = "Hostel Details"
    showUserMessage(userInput);
    
    // Show bot response based on user input
    setTimeout(function () {
      showBotMessage("<figure><img src='static//block_A.png' style='width:100%'><figcaption style='text-align:center'><b>Hostel Blocks</b></figcaption></figure>");
      showBotMessage("<figure><img src='static//dormitory.png' style='width:100%'><figcaption style='text-align:center'><b>Dormitory</b></figcaption></figure>");
      showBotMessage("To Know More Visit : <br><p><a href='https://geethashishu.in/2021-09-20-11-41-18/hostels'><p>Hostel<p></a></br>");
    }, 300);
    }
  );

  $('#admission_button').on('click', function (e) {
    // Get and show user message, then reset input
    const userInput = "Admission Details"
    showUserMessage(userInput);
    
    // Show bot response based on user input
    setTimeout(function () {
      showBotMessage("<html><body>Admission to the GSSS Institute of Engineering and Technology for Women (GSSSIETW) in Mysore, Karnataka is based on entrance exam scores:<br><b>Undergraduate : <b> Admission to UG courses like BE and B. Tech is based on COMEDK UGET or KCET scores.<br><b>Postgraduate : <b>Admission to PG courses like M. Tech and MBA is based on Karnataka PGCET/GATE scores for engineering courses and PGCET/K-MAT for other courses. For example, to be eligible for admission to M. Tech, candidates must have an aggregate of 50% in graduation.</body></html>");
      showBotMessage("For more info, vist : <a href='https://geethashishu.in/admissions/'>Admission</a><p> Mail Us : admissions@gsss.edu.in</p></br>");
      }, 300);
    }
  );

  $('#cet_button').on('click', function (e) {
    // Get and show user message, then reset input
    const userInput = "KCET"
    showUserMessage(userInput);
    
    // Show bot response based on user input
    setTimeout(function () {
      showBotMessage("<figure><img src='static//1st_round.png' style='width:100%:height:400px'><figcaption style='text-align:center'><b>1st round CET cut-off (2023)</b></figcaption></figure>");
      showBotMessage("<figure><img src='static//2nd_round.png' style='width:100%:height:400px'><figcaption style='text-align:center'><b>2st round CET cut-off (2023)</b></figcaption></figure>");      
    }, 300);
    }
  );  
  
  $('#fees_button').on('click', function (e) {
    // Get and show user message, then reset input
    const userInput = "Fees Details"
    showUserMessage(userInput);
    
    // Show bot response based on user input
    setTimeout(function () {
      showBotMessage("Visit : <a href='https://geethashishu.in/admissions/'>Admission</a><p> Mail Us : admissions@gsss.edu.in</p></br>");
      }, 300);
    }
  );

  $('#more_button').on('click', function (e) {
    // Get and show user message, then reset input
    const userInput = "More"
    showUserMessage(userInput);
    
    // Show bot response based on user input
    setTimeout(function () {
      showBotMessage("<div><div id='admission_button' class='button'>Admission</div><div id='cet_button' class='button'>KCET</div><div id='comedk' class='button'>COMEDK</div><div id='brochure' class='button'>Brochure</div><div id='facility_button' class='button'>Facility</div>");

      $('#admission_button').on('click', function() {
        showUserMessage("Admission");
        Admission();
      });
      
      $('#cet_button').on('click', function() {
        showUserMessage("KCET");
        Cutoff();
      });
  
      $('#brochure').on('click', function() {
        showUserMessage("Fees");
        Brochure();
      });

      $('#facility_button').on('click', function() {
        showUserMessage("Fees");
        Facility();
      });

      $('#comedk').on('click', function() {
        showUserMessage("COMEDKS");
        Comedk();
      });

    },300);
    });

 $('#send_button').on('click', function (e) {
    // Get and show user message, then reset input

    const userInput = $('#msg_input').val();
    showUserMessage(userInput);
    $('#msg_input').val('');

    // Show bot response based on user input
    const Input = userInput.toLowerCase();

    try{
      if(userInput=='hi' || userInput=='hello' || userInput=='hey' || userInput=='Namaste'){
        setTimeout(showBotMessage("Hi I'm GeethaBOT, how can I help you. <br>select the query or type in your question</br>"));
      }
      else if(Input.includes("contact")){
        setTimeout(Contact(),300);
      }
      else if(Input.includes("department")){
        setTimeout(Department(),300);
      }
      else if(Input.includes("location")){
        setTimeout(Location(),300);
      }
      else if(Input.includes("placement")){
        setTimeout(Placement(),300);
      }
      else if(Input.includes("hostel")){
        setTimeout(Hostel(),300);
      }
      else if(Input.includes("admission")){
        setTimeout(Admission(),300);
      }
      else if(Input.includes("fee structure")|| Input.includes("fee")||Input.includes("fees")){
        setTimeout(FeeStructure(),300);
      }
      else if(Input.includes("courses")){
        setTimeout(Courses(),300);
      }
      else if(Input.includes("facility")|| Input.includes("facilities")){
        setTimeout(Facility(),300);
      }
      else if(Input.includes("cutoff") || Input.includes("cet") || Input.includes("kcet")){
        setTimeout(Cutoff(),300);
      }
      else if(Input.includes("better") ||Input.includes("why")||Input.includes("special")){
        setTimeout(Value(),300);
      }
      else if(Input.includes("board")||Input.includes("member")||Input.includes("members")){
        setTimeout(Member(),300);
      }
      else if(Input.includes("awards")||Input.includes("achievments")){
        setTimeout(Awards(),300);
      }
      else if(Input.includes("brochure")){
        setTimeout(Brochure(),300);
      }
      else if(Input.includes("value")){
        setTimeout(Value(),300);
      }
      else if(Input.includes("ranking")){
        showBotMessage("<html><body><p>Ranking and Achievements</p></body></html>");
        setTimeout(Ranking(),300);
      }
      else if(Input.includes("principal")){
        setTimeout(Principal(),300);
      }
      else if(Input.includes("founder")){
        setTimeout(Founder(),300);
      }
      else if(Input.includes("code")){
        setTimeout(function () {
          showBotMessage("<html><body>CET Code : E133</body></htlm>");
          showBotMessage("<html><body>COMEDK Code : E055</body></htlm>");
          }, 300);
      }
      else if(Input.includes("packages") || Input.includes("highest") || Input.includes("package")){
        setTimeout(function () {
          showBotMessage("<figure><img src='static//highest.jpg' style='width:100%'><figcaption style='text-align:center'></figure>");
          showBotMessage("Visit : <a href='https://geethashishu.in/departments/placements'>Placement Department</a>");
          }, 300);
      }
      else if(Input.includes("logo")){
        setTimeout(function () {
          showBotMessage("<figure><img src='static//logo.jpeg' style='width:100%'><figcaption style='text-align:center'></figure>");
        }, 300);
      }
      else{
        if(userInput== ' '){
          setTimeout(showBotMessage("Oops!! I did not understand that. can u pls type in your question again"),300)
        }
        else{
        showBotMessage("I do not have proper information regarding it");
        }
      }
    }
    
    catch(err){

    }
  });

/**
 * Set initial bot message to the screen for the user.
 */
$(window).on('load', function () {
	showBotMessage('Namaste!');
	showBotMessage('I am GeethaBOT, How can I help you');
});