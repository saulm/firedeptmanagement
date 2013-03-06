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

function fill_patient_form($form, data){
	$form.find("input[name$='first_name']").val(data.first_name);
	$form.find("input[name$='first_name_2']").val(data.first_name_2);
	$form.find("input[name$='last_name']").val(data.last_name);
	$form.find("input[name$='last_name_2']").val(data.last_name_2);
	$form.find("select[name$='gender']").val(data.gender);
	$form.find("input[name$='primary_email']").val(data.primary_email);
}

function set_vehicle_form_behavior(settings){
	var static_url = settings["static_url"];
	
	
	$("a.delete_vehicle").click(function(){
		$(this).parent().remove();
		var total_forms = parseInt($("div#vehicles_forms input#id_form-TOTAL_FORMS").val()) - 1;
		$("div#vehicles_forms input#id_form-TOTAL_FORMS").val(total_forms);
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

function set_affected_form_behavior(){
	$("a.delete_patient").click(function(){
			$(this).parent().remove();
			var total_forms = parseInt($("div#patients_forms input#id_form-TOTAL_FORMS").val()) - 1;
			$("div#patients_forms input#id_form-TOTAL_FORMS").val(total_forms);
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
}

function get_next_index(selector){
	var index = 0;
	var indexes = [];
	$(selector).each(function() {
		indexes.push(parseInt($(this).attr('index')));
	});

	if(indexes.length > 0){
		indexes = indexes.sort( function (a,b) { return b-a });
		index = indexes[0]+1;
	}
	return index;
}

function set_total_forms(selector){
	var new_total = parseInt($(selector).val()) + 1;
	$(selector).val(new_total);
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

function fill_crews(settings){
	var static_url = settings["static_url"];
	var crew_data = jQuery.parseJSON(settings["crew_data"]);
	
	$("div.vehicle_form").each(function(){ 
		var $form = $(this);
		
		var ids = $form.children().filter("input[name$='crew_ids']").val().split(",");
		$.each(ids, function(index, Element){
			var id = parseInt(Element);
			var label = crew_data[id];
			if (label != undefined){
				var content = "<li class='member_li' member_id="+id+">"+label+
								" <a onclick='$(this).parent().remove();update_crew_list(\""+
								$form.attr("id")+"\");'><img src='"+
								static_url+"img/remove_icon.png'></img></a></li>";
				$form.find("ul.crew_group").append(content);	
			}
							
		});
		
		var vehicles = $form.find("select[name$='vehicle']");
		$.each(vehicles, function(index, vehicle){
			if ($(this).val()!=""){
				var $driver_select =  $form.find("input[name$='driver_select']");
				var $driver_select_group = $driver_select.closest(".control-group");
				$driver_select_group.show();
			}
		});
	});
}

function insert_service_ready(settings){
	var static_url = settings["static_url"];
	var crew_data = jQuery.parseJSON(settings["crew_data"]);
	var default_affected_form = settings["default_affected_form"];
	var default_vehicle_form = settings["default_vehicle_form"];
	
	$("input#id_date").change(function(){
		if($("input#id_scene_arrival_date").val() ==""){
			$("input#id_scene_arrival_date").val($(this).val());
		}
		if($("input#id_end_date").val() ==""){
			$("input#id_end_date").val($(this).val());
		}
		
	});
	
	$("input#id_time").change(function(){
		if($("input#id_scene_arrival_time").val() ==""){
			$("input#id_scene_arrival_time").val($(this).val());
		}
		if($("input#id_end_time").val() ==""){
			$("input#id_end_time").val($(this).val());
		}
		
	});
	
	$("input.datePicker").datepicker({"maxDate": 0});
	$("input#id_time").mask("9999");
	$("input#id_end_time").mask("9999");
	$("input#id_scene_arrival_time").mask("9999");
	
	
	
	$('tabs_nav').click(function (e) {
  		e.preventDefault();
  		$(this).tab('show');
	});
	
	set_vehicle_form_behavior(settings);
	set_affected_form_behavior();
	fill_crews(settings);
	
	$("a#add_patient").click(function(){
		var index = get_next_index("div.patient_form");
		var form = default_affected_form.replace(/__prefix__/g, index);
		
		set_total_forms("div#patients input#id_affected-TOTAL_FORMS");
		$("div#patients_forms").append('<div class="patient_form well" index="'+index+
						'"><a class="btn btn-danger delete_patient" style="float: right;">Eliminar</a>'+
						form+'</div>');
		set_affected_form_behavior();
	});
	
	$("a#add_vehicle").click(function(){
		var index = get_next_index("div.vehicle_form");	
		var form = default_vehicle_form.replace(/__prefix__/g, index);
				
		set_total_forms("div#vehicles input#id_vehicles-TOTAL_FORMS");
		$("div#vehicles_forms").append('<div id="vehicle_vehicles-'+index+
						'" class="vehicle_form well" index="'+index+
						'"><a class="btn btn-danger delete_vehicle" style="float: right;">Eliminar</a>'+
						form+'<ul class="crew_group"></ul></div>');
		set_vehicle_form_behavior(settings);
	});
}
