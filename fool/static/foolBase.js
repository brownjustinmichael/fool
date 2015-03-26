

function start() {
	handPrep();
	cardModal();
	scrollBottom();
	animateCardHover();
	deleteLocationContentDuplicates()
}

function cardModal() {
	$(".card").click(function() {
		var cardName = $(this).find(".card_title h2").html();
		var cardModifier = $(this).find(".card_level").html();
		var cardLink = $(this).find(".play_card").html();
		var cardDescription = $(this).find(".card_description").html();
		$('#card_modal .card_title h2').html(cardName);
		$('#card_modal .card_level').html(cardModifier);
		$('#card_modal #modal_play_card').html(cardLink);
		$('#card_modal .card_description').html(cardDescription);
		$('#card_modal').show();
	});
	$("#modal_cancel").click(function(){
		$('#card_modal').hide();
	})
}

function handPrep(){
	var handCount = 5;
	handShift(handCount);
}

function handShift(handCount){
	buttonToggle('back','off');
	if($('.card_slot').size() >= handCount){
		buttonToggle('next','on');
	}
	
	var cardHeight = 50;
	var shiftCount = 0;
	$('.card_button').click(function(){
		
		if($(this).attr('value') == 'next' && shiftCount < $('.card_slot').length - handCount){
			$('#card_slots').animate({top:'-=' + cardHeight + 'px'}, 200);
			$('.card_slot:nth-child(' + (shiftCount + 1) + ')').animate({opacity:0}, 200);
			shiftCount += 1;
		}else if($(this).attr('value') == 'back' && shiftCount > 0){
			$('#card_slots').animate({top:'+=' + cardHeight + 'px'}, 200);
			$('.card_slot:nth-child(' + (shiftCount) + ')').animate({opacity:1}, 200);
			shiftCount -= 1;
		}
		if(shiftCount >= $('.card_slot').length - handCount){
			buttonToggle('back','on');
			buttonToggle('next','off');
		}else if(shiftCount <= 0){
			buttonToggle('back','off');
			buttonToggle('next','on');
		}else{
			buttonToggle('back','on');
			buttonToggle('next','on');
		}
	});
	function buttonToggle(type, toggle){
		if(toggle == "on"){
			$('.card_button[value='+ type + ']').css('background','#c3beb9');
			$('.card_button[value='+ type + ']').html('O')
		}
		else{
			$('.card_button[value='+ type + ']').css('background','#554b40');
			$('.card_button[value='+ type + ']').html('-');
		}
	}
}

function scrollBottom(){
	$("#content_main").prop({ scrollTop: $("#content_main").prop("scrollHeight") });
}

function animateCardHover(){
	$(".card").mouseenter(function(){
		$(this).animate({
			top: "-120"
		}, {duration: 200, 
			queue:false});
	});
	$(".card").mouseleave(function(){
			$(this).animate({
			top: "0"
		}, {duration: 200, 
			queue:false});
	});
	
	$(".card_sidetab").mouseenter(function(){
		$(this).siblings('.card').animate({
			top: "-120"
		}, {duration: 200, 
			queue:false});
	});
	$(".card_sidetab").mouseleave(function(){
			$(this).siblings('.card').animate({
			top: "0"
		}, {duration: 200, 
			queue:false});
	});
}

function deleteLocationContentDuplicates(){
	var logLength = $('.log_entry').size();
	
	for(var i = 1; i <= logLength; i++){
		if($('.log_entry:nth-child(' + i + ') h2').html() == $('.log_entry:nth-child(' + (i - 1) + ') h2').html()){
			$('.log_entry:nth-child(' + i + ') h2').css("color","red");
			//$('.log_entry:nth-child(' + i + ') h2').hide();
			$('.log_entry:nth-child(' + (i-1) + ') .horiz_divider').hide();
		}
	}
}
