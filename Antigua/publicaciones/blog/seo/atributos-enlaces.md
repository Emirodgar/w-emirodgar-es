---
description: Además de nofollow ahora contamos con sponsored y ugc
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
date: 12/09/2019
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
folder: seo
permalink: atributos-enlaces-google

--- 

# Nuevos atributos para los enlaces de Google

Este semana Google ha anunciado en su blog oficial [nuevos atributos para los enlaces](https://webmasters.googleblog.com/2019/09/evolving-nofollow-new-ways-to-identify.html?m=1). A partir de ahora los enlaces -tanto internos como externos- podrán ser etiquetados como nofollow, sponsored o ugc. Estas son las características de cada uno de ellos:

  

-   **nofollow:** existe desde el 2005 e indica a los buscadores que el enlace no debe ser seguido ni tenido en cuenta para traspasar popularidad. A partir de ahora, podría aportar valor al posicionamiento y a partir de 2020 también al rastreo e indexación. Esto lo decidirá Google.    
-   **sponsored**: nuevo atributo diseñado para etiquetar los enlaces de pago/publicidad. Con esto Google pretende conocer mejor la naturaleza de aquellos enlaces obtenidos a cambio de una colaboración monetaria.     
-   **ugc**: nuevo atributo diseñado para los enlaces que aparezcan dentro de contenido generado por los usuarios (comentarios, foros, etc). De esta forma Google pretender discernir entre los enlaces originales de una publicación y los que han sido añadidos después por usuarios externos.    

Un ejemplo de cómo tendríamos que utilizar estos atributos sería el siguiente:

 ```html     
 <a href="https://emirodgar.com" rel="ugc">Emirodgar</a>
 <a href="https://emirodgar.com" rel="sponsored">Emirodgar</a>
 <a href="https://emirodgar.com" rel="nofollow">Emirodgar</a>
 ```  

En la siguiente imagen podemos ver un esquema de la evolución de los atributos y su impacto en las estrategias SEO.

<amp-twitter 
  width="375"
  height="472"
  layout="responsive"
  data-tweetid="1207679355150831620">
</amp-twitter>
    

## Conclusiones
  

-   No es obligatorio utilizar ninguno de los atributos. Si no lo hacemos, el enlace servirá para rastrear, indexar y posicionar la página de destino.       
-   Google no recomienda llevar a cabo ningún cambio en el enlazado actual, lo propone más bien para etiquetar de aquí en adelante. También ha dicho que no se esperan grandes cambios en los rankings.       
-   Actualmente ninguno de los tres atriburos sirve para rastrear ni indexar la URL de destino pero queda en manos de Google decidir si suman al posicionamiento web. A partir de marzo de 2020 todas las acciones -rastrear, indexar y posicionar- serán decisión de Google en función de cómo de relevante considere el enlace y la página de destino, independientemente del atributo que tenga el enlace.    
-   Podemos combinar los atributos como queramos, es decir, no estamos limitados a usar sólo uno.  
     

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEzMTYxOTk0MzgsNjI0OTI3OTk3LDE1Nj
I1MTcwOTAsLTIwMDgzMjc5NTAsLTE1NDc4MTIxMzgsNzk4MjYx
MTFdfQ==
-->