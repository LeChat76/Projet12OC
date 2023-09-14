# Projet12OC

* Page de login (user de test : cedric / Toto1234!)

* Menu 1 - 1 : creation client
* Menu 1 - 2 : vue/modification client
* Menu 1 - 3 : suppression client
* Menu 2 - 1 : creation contrat
* Menu 2 - 2 : vue/modification contract
* Menu 2 - 4 : signer contrat

c'est tout pour le moment

## CONFIGURATION:

* créer table epicevents sur mysql
   => `CREATE DATABASE epicevents;`

* créer groupe avec requete sql:
   => `INSERT INTO epicevents.department (name) VALUES ('superadmin'), ('management'), ('commercial'), ('support');`

* créer compte superadmin avec requete sql : 

   => `INSERT INTO epicevents.employee (username,password,`department_id`,status) VALUES ('cedric','$2y$10$IpoOpINijEvbie3PjdBzae/5SPTfoBnz7U27myUk3GBThO/fzGr2i','1','ENABLE');`

## EXECUTION:

* lancer l'application avec `python main.py`
