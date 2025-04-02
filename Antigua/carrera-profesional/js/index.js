var info = {
	'name': 'Emilio Rodríguez',
	'subtitle': 'SEO / Programador / Analista',
	'bio': 'Mejor una solución aproximada a un problema correcto que una solución correcta a un problema aproximado - John Tukey.',
	'contact_links': [{
		'name': 'Inicio',
		'link': 'https://emirodgar.com' },
	{
		'name': 'consultor SEO',
		'link': 'https://emirodgar.com/consultor-seo/' },
	{
		'name': 'linkedin.com',
		'link': 'https://es.linkedin.com/in/emirodgar' },
	{
		'name': 'twitter.com',
		'link': 'https://twitter.com/emirodgar' }],

	'work_history': [{
		'title': 'Jefe de Proyecto',
		'location': 'Smartup',
		'date': '2017 - actual',
		'text': 'A cargo de la coordinación y control de los diferentes proyectos digitales tanto de marketing como Big Data.' },
	{
		'title': 'Director SEO',
		'location': 'Internet Advantage',
		'date': '2013 - 2017',
		'text': 'Liderando el equipo SEO formado por siete consultores. Búsqueda de soluciones estratégicas para los diferentes clientes.' },
	{
		'title': 'Consultor SEO',
		'location': 'Traffic4U',
		'date': '2009 -2013',
		'text': 'Desarrollo y ejecución de estrategias de marketing digital para el mercado español e internacional.' },
	{
		'title': 'Programador web',
		'location': 'Indra',
		'date': '2005 - 2009',
		'text': 'Diseño y desarrollo de una plataforma web para la gestión de servicios internos de Renfe.' }],



	'projects': [{
		'name': 'Proyectos SEO',
		'desc': 'Incremento del tráfico orgánico de calidad. Auditorías técnicas y de contenido.',
		'tags': [
		'SEO Onpage', 'SEO offpage'],

		'colors': [
		'#E30613', '#00698C', '#737373', '#5CB4EB'],

		'image_type': 'tall',
		'images': [
		'https://i.imgur.com/T8eWelh.jpg',
		'https://i.imgur.com/eZvnW5Y.jpg',
		'https://i.imgur.com/kWKsmIF.png'] },

	{
		'name': 'Ecommerce',
		'desc': 'Análisis orientados a la captación de leads y posterior conversión.',
		'tags': [
		'CRO', 'CLV' , 'Analítica'],

		'colors': [
		'#E87722', '#222222'],

		'image_type': 'tall',
		'images': [
		'https://i.imgur.com/muJBoB9.png',
		'https://i.imgur.com/h7XaS7S.png',
		'https://i.imgur.com/tnpykL1.png'] },

	{
		'name': 'Profesor',
		'desc': 'Colaboro como docente en diferentes empresas e instituciones.',
		'tags': [
		'MBA', 'Máster digital', 'Big Data'],

		'colors': [
		'#976BBA', '#00BCD4', '#A6C0DC', '#3B3B3A'],

		'image_type': 'tall',
		'images': [
		'https://i.imgur.com/c4hb5Aq.png',
		'https://i.imgur.com/oVemzE7.png',
		'https://i.imgur.com/gnIHN1b.png'] },

	{
		'name': 'Desarrollos propios',
		'desc': 'Growth Hacking para obtener el máximo rendimiento a mis estrategias.',
		'tags': [
		'PHP', 'FireHTML', 'Inbound'],

		'colors': [
		'#3B3B3A', '#58585A', '#B4B4B4'],

		'image_type': 'wide',
		'images': [
		'https://i.imgur.com/AdMmG1F.jpg',
		'https://i.imgur.com/TforndA.png',
		'https://i.imgur.com/Fj9mkyn.png'] },

	{
		'name': 'Certificaciones',
		'desc': 'Me he certificado en diferentes aplicaciones e instituciones.',
		'tags': [
		'Hubspot', 'Google', 'Webtrekk'],

		'colors': [
		'#DC002E', '#02678E', '#37454E'],

		'image_type': 'tall',
		'images': [
		'https://i.imgur.com/aQCILvy.png',
		'https://i.imgur.com/pPPlNew.png',
		'https://i.imgur.com/UnLFs14.png'] }] };




function ProjectImages(props) {
	return (
		React.createElement('div', { className: 'project-images' },
			props.images.map(function (url, index) {
				return (
					React.createElement('div', { className: 'thumb' },
						React.createElement('img', { className: props.type + ' gallery-' + props.index, 'data-featherlight': url, src: url })));


			})));


}

function ProjectColors(props) {
	return null;
	return (
		React.createElement('div', { className: 'color-scheme' },
			props.colors.map(function (color, index) {
				return React.createElement('span', { style: { backgroundColor: color } });
			})));


}

function Project(props) {
	var tags = props.project_info.tags;
	var tag_list = tags.map(function (name, index) {
		var fname = index === 0 ? name : ' / ' + name;
		return fname;
	});
	return (
		React.createElement('div', { className: 'row' },
			React.createElement('div', { className: 'col-md-4' },
				React.createElement('div', { className: 'project-text' },
					React.createElement('div', null,
						tag_list),

					React.createElement('strong', null, props.project_info.name),
					React.createElement('p', null, props.project_info.desc))),


			React.createElement('div', { className: 'col-md-2' },
				React.createElement(ProjectColors, { colors: props.project_info.colors })),

			React.createElement('div', { className: 'col-md-6' },
				React.createElement(ProjectImages, { index: props.index, type: props.project_info.image_type, images: props.project_info.images }))));



}

function Projects(props) {
	return (
		React.createElement('div', { className: 'content-wrap' },
			React.createElement('div', { className: 'container' },
				React.createElement('h1', null, 'Experiencia digital'),
				React.createElement('hr', null),
				props.info.map(function (project, index) {
					return (
						React.createElement('div', null,
							React.createElement(Project, { index: index, project_info: project }),
							React.createElement('hr', null)));


				}))));



}

function WorkHistory(props) {
	return (
		React.createElement('div', { className: 'content-wrap' },
			React.createElement('div', { className: 'container' },
				React.createElement('h1', { 'class': '' }, getDate() + ' años trabajando en el mundo digital'),
				React.createElement('hr', null),
				props.work.map(function (work, index) {
					return (
						React.createElement('div', { className: 'work-history' },
							React.createElement('strong', null, work.title), ' / ', work.location, ' / ', React.createElement('strong', null, work.date),
							React.createElement('p', null, work.text),
							React.createElement('hr', null)));


				}))));



}

function Quote(props) {
	return (
		React.createElement('div', { className: 'content-wrap' },
			React.createElement('div', { className: 'container' },
				React.createElement('blockquote', { className: 'blockquote' },
					React.createElement('p', { className: 'mb-0' }, props.text)))));




}

function Header(props) {
	return (
		React.createElement('header', null,
			React.createElement('div', { className: 'container' },
				React.createElement('div', { className: 'row' },
					React.createElement('div', { className: 'col-md-6' },
						React.createElement('div', { className: 'header-left' },
							React.createElement('h1', { className: 'display-4' }, info.name),
							React.createElement('h2', null, info.subtitle))),


					React.createElement('div', { className: 'col-md-6' },
						React.createElement('div', { 'class': 'float-md-right' },
							React.createElement('a', { href: 'https://emirodgar.com' }, 'emirodgar.com'), ' / ', React.createElement('a', { href: 'https://es.linkedin.com/in/emirodgar' }, 'linkedin.com'), ' / ', React.createElement('a', { href: 'https://twitter/emirodgar' }, 'twitter.com'), ''))))));






}

ReactDOM.render(
React.createElement('div', null,
	React.createElement(Header, null),
	React.createElement(Quote, { text: info.bio }),
	React.createElement(WorkHistory, { work: info.work_history }),
	React.createElement(Projects, { info: info.projects })),

document.getElementById('app'));

function getDate() {
            var d = new Date();
            var n = d.getFullYear() - 2005;
            return n;
         }
		 
function getJub() {
            var d = new Date();
			return 2049 - d.getFullYear();
         }
document.getElementById('jub').innerHTML = getJub();