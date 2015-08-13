$(function(){
	function onFormSubmit(event){
		var data = $(event.target).serializeArray();
		var thesis = {};

		for(var i = 0; i<data.length ; i++)
		{
			thesis[data[i].name] = data[i].value;
		}

		var thesis_create_api = '/api/thesis';

		$.post(thesis_create_api, thesis);/*, function(response){
			// read response from server
			if (response.status = 'OK') {
				var thesis_list = response.data.section + ' ' + response.data.thesisTitle;
				$('.thesis-list').prepend('<li>' + thesis_list + '</li>')
				//$('input[type=text], [type=number]').val('');
			} else {

			}
		});*/

		var list_element = $('<li>');
		list_element.html(thesis.year + ' ' + thesis.thesisTitle);
		$('.thesis-list').prepend(list_element);
		$('input:text').val('');
		$('input[type=number]').val('');
		return false;
	}
/*
	function loadThesis(){
		var thesis_list_api = '/api/thesis';
		$.get(thesis_list_api, {} , function(response) {
			console.log('.thesis-list', response)
			response.data.forEach(function(thesis){
				var thesis_list = response.data.year + ' ' + response.data.thesisTitle;
				$('.thesis-list').append('<li>' + thesis_list + '</li>')
			});
		});
	}*/
    $('.create-form').submit(onFormSubmit)
    //loadThesis();
});