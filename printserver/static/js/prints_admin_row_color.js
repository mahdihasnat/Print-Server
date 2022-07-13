(function($) {
    $(document).ready(function() {
		table = document.getElementById("result_list");
		for (var i = 1; i < table.rows.length; i++) {
			row = table.rows[i];
			val = row.cells[6].childNodes[0].value;
			if (val == 1) // queued
				row.style.backgroundColor = "#4d2322";
			else if(val == 2) // printing
				row.style.backgroundColor = "#22334d";
		}
    });
})(django.jQuery);