---
description: Guía de instalación para comenzar a trabajar con Python
lang: es_ES
author: Emirodgar
sitemap: 1
feed: 1
folder: programacion
date: 16/01/2020
image: https://emirodgar.com/cdn/images/og/marketing-digital.png
permalink: script-python-twitter-unfollow

---

# Script en Python para hacer unfollow de aquellos que no nos siguen

Si llevamos muchos años en Twitter y seguimos a mucha gente suele ser complicado atender a todos ellos y a menudo tenemos que recurrir a listas para estar al tanto de lo que realmente nos interesa.

Para poder hacer un poco de limpieza, podemos programar un script en Python que nos ayude a despejar nuestros seguidos de gente que no nos sigue de vuelta aunque este script se puede adaptar fácilmente para limpiar también nuestro *timeline* de aquelos perfiles que no publican, que no interactúan con nosotros o que tienen métricas *SPAM*. 

Una vez [instalado Python](https://emirodgar.com/instalar-python) en nuestro ordenador, creamos el script: unfollow.py.

Para este script usaremos la librería tweepy por lo que el primer paso será importarla y acto seguido preparar un array con los datos de acceso a nuestro perfil.

```python
import tweepy
config = {
        "screen_name": "Emirodgar",
        "CONSUMER_KEY": "XXXX",
        "CONSUMER_SECRET": "XXXXX",
        "ACCESS_TOKEN": "XXXX-XXXX",
        "ACCESS_SECRET": "XXXX"
}
```
El siguiente paso será crear la conexión de nuestro perfil con Twitter a través de su API.

```python
auth = tweepy.OAuthHandler(config["CONSUMER_KEY"], config["CONSUMER_SECRET"])
auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_SECRET"])

api = tweepy.API(auth)
```

Una vez que estemos conectamos, recuperamos el listado de los perfiles que nos siguen y a los que nosotros seguimos.

```python
followers = api.followers_ids(config["screen_name"])
following = api.friends_ids(config["screen_name"])
```

Y por último, definimos un bucle en el que dejamos de seguir a aquellos perfiles que no nos siguen. El criterio que he establecido para detener el script es **hacer *unfollow* a 25 perfiles**, de esta forma evitamos ser bloqueados por Twitter.

```python
no_followers = set(following) - set(followers)
total_unfollowed = 0
for f in no_followers:
    try:
        api.destroy_friendship(f)
        total_unfollowed += 1
        if total_unfollowed == 25:
            break
    except (tweepy.RateLimitError, tweepy.TweepError) as e:
        error_handling(e)
print(str(total_unfollowed) + ' unfollowed')
```

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTExNTU1ODkwLDY3NjgxNTg4MywxNTI4MT
A2MDUzLC00MjAwNDEyNDRdfQ==
-->