---
title: Función JavaScript para validar fechas
description: Sencilla función para validar cualquier formato de fecha lista para incluir en tus proyectos
lang: es_ES
author: Emirodgar
sitemap: 1
feed: 1
folder: programacion
date: 17/05/2019
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
permalink: funcion-javascript-para-validar-fechas

---
# Función JavaScript para validar fechas

Esta función en JavaScript nos permitirá de una forma rápida validar una fecha. Devolverá ```true``` o ```false``` dependiendo de si el formato es correcto o no. Para que sea más reutilizable la fecha se pasará como parámetro.  

## Validaciones

- Esta función valida que el formato introducido sea ```dd/mm/yyyy```, aunque se puede modificar de una forma sencilla para adaptarse a otros formatos.  
- Valida que todos los parámetros introducidos a excepción de las barras de separación ```/``` sean números.  
- También valida que el día y el mes se correspondan entre ellos, por ejemplo, en Abril no permitir introducir días mayores de 30.  
- Esta función también tiene en cuenta que cada 4 años es bisiesto.

```javascript
    function validarFecha(fecha) {  
      
     try{        
	     var fecha = fecha.split("/");        
	     var dia = fecha[0];        
	     var mes = fecha[1];        
	     var ano = fecha[2];        
	     var estado = true;  
	      
	     if ((dia.length == 2) && (mes.length == 2) && (ano.length == 4)) {        
		     switch (parseInt(mes)) {        
			     case 1:dmax = 31;break;        
			     case 2: if (ano % 4 == 0) dmax = 29; else dmax = 28;        
			     break;        
			     case 3:dmax = 31;break;        
			     case 4:dmax = 30;break;        
			     case 5:dmax = 31;break;        
			     case 6:dmax = 30;break;        
			     case 7:dmax = 31;break;        
			     case 8:dmax = 31;break;        
			     case 9:dmax = 30;break;        
			     case 10:dmax = 31;break;       
			     case 11:dmax = 30;break;      
			     case 12:dmax = 31;break;       
		     }  
	           
		     dmax!=""?dmax:dmax=-1;if ((dia >= 1) && (dia <= dmax) && (mes >= 1) && (mes <= 12)) {        
		     for (var i = 0; i < fecha[0].length; i++) {         
			     diaC = fecha[0].charAt(i).charCodeAt(0);        
			     (!((diaC > 47) && (diaC < 58)))?estado = false:'';       
			     mesC = fecha[1].charAt(i).charCodeAt(0);        
			     (!((mesC > 47) && (mesC < 58)))?estado = false:'';       
		     }  
	      
	     } for (var i = 0; i < fecha[2].length; i++) {  
	      
	     anoC = fecha[2].charAt(i).charCodeAt(0);  
	      
	     (!((anoC > 47) && (anoC < 58)))?estado = false:'';        
	     }} else estado = false;        
	     return estado;    
         
    }catch(err){  
     alert("Error fechas");    
}
```
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE4NzM2Njk5MzFdfQ==
-->