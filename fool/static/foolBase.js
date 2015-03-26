function start() {
	roundHand();
	cardModal();
	handShift();
	scrollBottom();
	animateCardHover();
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

function roundHand(){
	var cardWidth = $('.card_slot').width();
	$('#card_bin').width(Math.floor($('#card_bin').width()/cardWidth)*(cardWidth + 3));
	$('#cards').width(Math.floor($('#card_bin').width()/cardWidth)*(cardWidth + 3) + 80);
	$('.card_button[value=back]').css('background','grey');
	if(Math.floor($('#card_bin').width()/cardWidth) >= $('.card_slot').length){
		$('.card_button[value=next]').css('background','grey');
	}

}

function handShift(){
	var cardWidth = $('.card_slot').width();
	$('.card_button').click(function(){
		var shiftCount = -(parseInt($('#card_slots').css('left'))/cardWidth);
		var handCount = $('#card_bin').width()/cardWidth;
		if($(this).attr('value') == 'next' && shiftCount < $('.card_slot').length - handCount){
			$('#card_slots').animate({left:'-=' + cardWidth + 'px'}, 50);
			shiftCount += 1;
		}else if($(this).attr('value') == 'back' && shiftCount > 0){
			$('#card_slots').animate({left:'+=' + cardWidth + 'px'}, 50);
			shiftCount -= 1;
		}
		if(shiftCount >= $('.card_slot').length - handCount){
			$('.card_button[value=back]').css('background','red');
			$('.card_button[value=next]').css('background','grey');
		}else if(shiftCount <= 0){
			$('.card_button[value=back]').css('background','grey');
			$('.card_button[value=next]').css('background','red');
		}else{
			$('.card_button[value=back]').css('background','red');
			$('.card_button[value=next]').css('background','red');
		}
	})
}

function scrollBottom(){
	$("#content_main").prop({ scrollTop: $("#content_main").prop("scrollHeight") });
}

function animateCardHover(){
	$(".card").mouseenter(function(){
		$(this).animate({
			top: "5"
		}, {duration: 200, 
			queue:false});
	});
	$(".card").mouseleave(function(){
			$(this).animate({
			top: "150"
		}, {duration: 200, 
			queue:false});
	});
}
