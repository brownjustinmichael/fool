

function start() {
	cardModal();
}

function cardModal() {
	$(".card").click(function() {
		var cardName = $(this).find(".card_title h2").html();
		var cardModifier = $(this).find(".card_level").html();
		var cardLink = $(this).find(".play_card").html();
		console.log(cardName)
		$('#card_modal .card_title h2').html(cardName);
		$('#card_modal .card_level').html(cardModifier);
		$('#card_modal #modal_play_card').html(cardLink);
		$('#card_modal').show();
	});
	$("#modal_cancel").click(function(){
		$('#card_modal').hide();
	})
}
