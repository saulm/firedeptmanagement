function get_used_ids(){
	var ids = new Array();
	$.each($("input[name$='lead']"), function(index, Element){
		ids.push($(Element).val());
	});
	$.each($("input[name$='driver']"), function(index, Element){
		ids.push($(Element).val());
	});
	$.each($("li.member_li"), function(index, Element){
		ids.push($(Element).attr("member_id"));
	});
	
	return ids;
}

function update_crew_list(id){
	var $form = $("div#"+id);
	var lis = $("div#"+id+" li");
	var ids = new Array();
	$.each(lis, function(index, Element){
		ids.push($(Element).attr("member_id"));
	});
	$form.find("input[name$='crew_ids']").attr("value", ids.join());
}

function fill_patient_form($form, data){
	$form.find("input[name$='first_name']").val(data.first_name);
	$form.find("input[name$='first_name_2']").val(data.first_name_2);
	$form.find("input[name$='last_name']").val(data.last_name);
	$form.find("input[name$='last_name_2']").val(data.last_name_2);
	$form.find("select[name$='gender']").val(data.gender);
	$form.find("input[name$='primary_email']").val(data.primary_email);
}

function insert_service_ready(settings){
	var static_url = settings["static_url"];
	
	//TODO: Revisar porque no sirve
	$("input.datePicker").datepicker("option", "maxDate", 0);
	
	$("input#id_time").mask("9999");
	
	$('tabs_nav').click(function (e) {
  		e.preventDefault();
  		$(this).tab('show');
	});
		
	$("a.delete_patient").click(function(){
		$(this).parent().hide();
		$(this).parent().find("input, select").val("");
	});
	
	$("a.delete_vehicle").click(function(){
		$(this).parent().hide();
		$(this).parent().find("input, select").val("");
	});
	
	$("a#add_patient").click(function(){
		$("h3#nopatients").hide();
		$(".patient_form:hidden").filter(":first").show();
	});
	
	$("a#add_vehicle").click(function(){
		$(".vehicle_form:hidden").filter(":first").show();
	});
	
	$("input[name$='driver_select']").each(function(index, Element){
		$(Element).closest(".control-group").hide();
	});
	
	$("select[name$='vehicle']").change(function(){
		var $driver_select =  $(this).closest(".vehicle_form").find("input[name$='driver_select']");
		var $driver_hidden =  $(this).closest(".vehicle_form").find("input[name$='driver']");
		var $driver_select_group = $driver_select.closest(".control-group");
		if($(this).val()==""){
			$driver_select.val("");
			$driver_hidden.val("");
			$driver_select_group.hide();
		} else {
			$driver_select_group.show();
		}
	});
	
	//Autocomplete Cedula
	$("input[name$='id_document']").autocomplete({
		source: function( request, response ) {
			$.ajax({
				url: "/gestion/personas/autocompletar/",
				dataType: "json",
				data: {
					term: request.term
				},
				success: function( data ) {
					response( $.map( data, function( item ) {
						return {
							label: item.fields.first_name +" "+item.fields.last_name,
							value: item.fields.id_document,
							first_name: item.fields.first_name,
							first_name_2: item.fields.first_name_2,
							last_name: item.fields.last_name,
							last_name_2: item.fields.last_name_2,
							gender : item.fields.gender,
							primary_email : item.fields.primary_email
						}
					}));
				}
			});
		},
		minLength: 3,
		select: function( event, ui ) {
				$form = $(event.target).closest(".patient_form");
				fill_patient_form($form, ui.item);
			}
	});
	
	//Autocomplete jefe comision
	$("input[name$='lead_select']").autocomplete({
		source: function( request, response ) {
			var element = this.element;
			$.ajax({
				url: "/gestion/bomberos/autocompletar/",
				dataType: "json",
				data: {
					term: request.term
				},
				success: function( data ) {
					response( $.map( data, function( item ) {
						var driver_id = $(element).closest(".vehicle_form").find("input[name$='driver']:hidden").val();
						//Permitir usar el conductor de la misma comision como jefe
						if(get_used_ids().indexOf(item.pk.toString()) < 0 || item.pk.toString()==driver_id){
							return {
								label: item.first_name +" "+item.last_name,
								value: item.first_name +" "+item.last_name,
								id: item.pk
							};
						}

					}));
				}
			});
		},
		minLength: 1,
		select: function( event, ui ) {
				$(event.target).closest(".vehicle_form").find("input[name$='lead']:hidden").val(ui.item.id);
			}
	});
	
	
	//Autocomplete Conductor
	$("input[name$='driver_select']").autocomplete({
		source: function( request, response ) {
			var element = this.element;
			$.ajax({
				url: "/gestion/bomberos/autocompletar/",
				dataType: "json",
				data: {
					term: request.term
				},
				success: function( data ) {
					response( $.map( data, function( item ) {
						var lead_id = $(element).closest(".vehicle_form").find("input[name$='lead']:hidden").val();
						//Permitir usar el jefe de la misma comision como conductor
						if(get_used_ids().indexOf(item.pk.toString()) < 0 || item.pk.toString()==lead_id){
							return {
								label: item.first_name +" "+item.last_name,
								value: item.first_name +" "+item.last_name,
								id: item.pk
							};
						}
					}));
				}
			});
		},
		minLength: 1,
		select: function( event, ui ) {
				$(event.target).closest(".vehicle_form").find("input[name$='driver']:hidden").val(ui.item.id);
			}
	});
	
	//Autocomplete de Miembro Comision
	$("input[name$='crew_select']").autocomplete({
		source: function( request, response ) {
			$.ajax({
				url: "/gestion/bomberos/autocompletar/",
				dataType: "json",
				data: {
					term: request.term
				},
				success: function( data ) {
					response( $.map( data, function( item ) {
						var used_ids = get_used_ids();
						if(used_ids.indexOf(item.pk.toString()) < 0){
							return {
								label: item.first_name +" "+item.last_name,
								value: item.first_name +" "+item.last_name,
								id: item.pk
							};
						}
					}));
				}
			});
		},
		minLength: 1,
		select: function( event, ui ) {
				var $form = $(event.target).closest(".vehicle_form");
				var content = "<li class='member_li' member_id="+ui.item.id+">"+ui.item.label+
								" <a onclick='$(this).parent().remove();update_crew_list(\""+
								$form.attr("id")+"\");'><img src='"+
								static_url+"img/remove_icon.png'></img></a></li>";
								 
				$form.find("ul.crew_group").append(content);				
				$(event.target).val("");
				update_crew_list($form.attr("id"));
				return false;
			}
	});
		
}
