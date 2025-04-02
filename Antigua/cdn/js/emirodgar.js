function getDate() {
	var d = new Date();
	var n = d.getFullYear();
	return n;
}

function getExperience() {
	return new Date().getFullYear() - 2007;
}
		
$(document).ready(function(){

	$('#side-panel-content').load('https://emirodgar.com/cdn/html/sidebar.html');
	
	/*$("#footer").load("https://emirodgar.com/cdn/html/footer.html", function() {
		$("#anno").html(getDate());
	});*/
	$("#anno").html(getDate());
	
	$(".erg_protfolio").load('https://emirodgar.com/cdn/html/portfolio.html');
	$("#section-services-seo").load('https://emirodgar.com/cdn/html/services.html');
	
	$("#section-experience").load("https://emirodgar.com/cdn/html/experience.html", function() {
		$("#anno_experience").html(getExperience());
	});
	
	$("#section-why").load("https://emirodgar.com/cdn/html/why.html", function() {
		$("#anno_why").html(getDate());
	});
	
	$('#section-about-me').load('https://emirodgar.com/cdn/html/about.html');
	$('#section-reasons-seo').load('https://emirodgar.com/cdn/html/reasons-seo.html');
	
	

});
