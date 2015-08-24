$(function(){
	function onFormSubmit(event){
		var data = $(event.target).serializeArray();
		var thesis = {};

		for(var i = 0; i<data.length ; i++){
			thesis[data[i].name] = data[i].value;
		}

		var thesis_create_api = '/api/thesis';

		$.post(thesis_create_api, thesis, function(response){
			// read response from server
			if (response.status = 'OK') {
				var thesis_list = response.data.year + ' ' + response.data.thesisTitle + ' created by: ' + response.data.userName;
				$('.thesis-list').prepend('<li>' + thesis_list + '<a href=\"/thesis/delete/'+response.data.id+'\"><button type=\"submit\">DELETE</button></a>')
				$('input:text').val('');
				$('textarea[name=abstract]').val('');
				$('select[name=year]').val('2011');
				$('select[name=section]').val('1');
			} else {

			}
		});

		return false;
	}

	function loadThesis(){
		var thesis_list_api = '/api/thesis';
		$.get(thesis_list_api, {} , function(response) {
			console.log('.thesis-list', response)
			response.data.forEach(function(thesis){
				var thesis_list = thesis.year + ' ' + thesis.thesisTitle + ' created by: ' + thesis.userName;;
				$('.thesis-list').append('<li>' + thesis_list + '<a href=\"/thesis/delete/'+thesis.id+'\"><button type=\"submit\">DELETE</button></a>' + '</li>')
			});
		});
	}
	loadThesis();
    $('.create-form').submit(onFormSubmit);
});