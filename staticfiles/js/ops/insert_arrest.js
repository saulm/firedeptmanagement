function insert_arrest_ready(settings){
    var ff_autocomplete_url = settings["ff_autocomplete_url"];
	$("input.datePicker").datepicker({"maxDate": 0});
	$("input[name$='arrested_select']").autocomplete({
		source: function( request, response ) {
			var element = this.element;
			$.ajax({
				url: ff_autocomplete_url,
				dataType: "json",
				data: {
					term: request.term
				},
				success: function( data ) {
					response( $.map( data, function( item ) {
						return {
							label: item.first_name +" "+item.last_name,
							value: item.first_name +" "+item.last_name,
							id: item.pk
						};
					}));
				}
			});
		},
		minLength: 1,
		select: function( event, ui ) {
				$("input[name$='arrested']:hidden").val(ui.item.id);
				$(event.target).attr('readonly', 'readonly');
			}
	});
}

function insert_arrest_payment_ready(settings){
    var ff_autocomplete_url = settings["ff_autocomplete_url"];
	$("input#id_start_time_time").mask("9999");
	$("input#id_end_time_time").mask("9999");
	$("input#id_start_time_date").datepicker({"maxDate": 0});
	$("input#id_end_time_date").datepicker({"maxDate": 0});
	
	$("input[name$='payer_select']").autocomplete({
		source: function( request, response ) {
			var element = this.element;
			$.ajax({
				url: ff_autocomplete_url,
				dataType: "json",
				data: {
					term: request.term
				},
				success: function( data ) {
					response( $.map( data, function( item ) {
						return {
							label: item.first_name +" "+item.last_name,
							value: item.first_name +" "+item.last_name,
							id: item.pk
						};
					}));
				}
			});
		},
		minLength: 1,
		select: function( event, ui ) {
				$("input[name$='payer']:hidden").val(ui.item.id);
				$(event.target).attr('readonly', 'readonly');
			}
	});
}
