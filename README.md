# 📜 Documentation back-end

## ⚙ Architecture globale

Le back-end s'architecture en 3 parties
<a href="https://ibb.co/LkkRfvn"><img src="https://i.ibb.co/1vvQxb8/Untitled-document.png" alt="Untitled-document" border="0"></a>
- Les modèles sont des classes qui ont pour unique but de réaliser les requêtes à la base de données.
- Les contrôleurs sont des méthodes regroupées par classe de la même manière que les modèles (pour une classe User dans les modèles, on aura une classe User dans les contrôleurs). Les contrôleurs prennent en paramètre une requête HTTP, la traite (gestion d'erreurs : vérifier que les champs existent, qu'ils ont les valeurs attendus etc...) et renvoie une réponse au format JSON.
- Les routes sont des fonctions où l'on appelle le contrôleur qui lui est associé (une route ne devrait faire qu'une ligne). Ainsi il y a unu contrôleur par route.


> Pourquoi détaché les routes et les contrôleurs et ne pas simplement mettre directement l'implémentation des contrôleurs dans les routes ?
> 
> Afin de pouvoir réaliser des tests unitaires sur les routes sans avoir à exécuter de requêtes.

## 📖 Guide pour ajouter des fonctionnalités au back-end

1. Partir du besoin front. Par exemple : on a besoin d'une route pour récupérer la liste des fichiers de l'utilisateur afin de les afficher.
2. Définir le endpoint (ou route) permettant de récupérer cette information
	- La méthode HTTP (GET, POST, PUT, DELETE...)
	- L'URL
	- Le format de requête
	- Le format de réponse

> Attention à bien respecter la norme REST.
> - Le format de réponse doit être en JSON.
> - L'URL ne doit pas transparaître l'action CRUD de la route. Par exemple il est inutile de faire une route /user/create, /user/get et /user/delete. Il y aura plusieurs endpoints avec l'URL /user mais avec une méthode HTTP différente pour chaque.
3. Implémenter la méthode du contrôleur. Le contrôleur ne fait aucune récupération ou opération sur les données directement, c'est le travail du modèle. Il se charge simplement de vérifier la requête et de formater la réponse et fait bien-sûr entre les deux, il appelle le modèle correspondant pour récupérer ou modifier les données.
4. Implémenter la méthode du modèle. La méthode se charge d'effectuer les opérations ou récupération de données. Tout modèle crée doit obligatoirement hériter de la classe Model. Cette classe est un wrapper de requêtes SQL à la base, qui implémente des méthodes CRUD qui permettent de gagner du temps dans le développement des méthodes des modèles.

Pour les étapes 3 et 4 il s'agit de regrouper les méthodes par classe. Chaque classe doit correspondre à un modèle de données (par exemple la classe User va correspondre à l'inscription, la connexion et la suppression d'un utilisateur). Par conséquent lors de l'ajout d'une méthode d'un contrôleur ou d'un modèle, soit il faut créer une nouvelle classe (donc un nouveau contrôleur et un nouveau modèle) ou bien l'implémenter dans un contrôleur et un modèle déjà existant.

Merci de bien respecter ces quelques règles et bon dev 😀

