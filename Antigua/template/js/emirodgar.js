function getDate() {
	var d = new Date();
	var n = d.getFullYear();
	return n;
}
		
$(document).ready(function(){

	$('#side-panel').load('../template/html/sidebar.html');
	
	$("#footer").load("../template/html/footer.html", function() {
		$("#anno").html(getDate());
	});

});
