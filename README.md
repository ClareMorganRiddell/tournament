# tournament
My final project for the full-stack option  of the Udacity Nano Degree program "Introduction to Programming". 

### *Project Description* : *Tournament Planner*

_In this project, you’ll be writing a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament._

_The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible._

_This project has two parts: defining the database schema (SQL table definitions), and writing the code that will use it._

## Install

* Download and Install

    You will need to have [Vagrant] and [Virtual Box] installed on your computer in order  to  run this code

    All files required are in this repository, including the VM reqired.

- Naviagate

   Launch vagrant and cd to the location /vagrant/tournament

* Set up the Database

   Import the the .sql file into PostgreSQL

```sh
$vagrant@vagrant:/vagrant/tournament$ psql
$vagrant=> \i tournament.sql
```

* Run python code

    In CLI run tournament_test.py

```sh
$ python tournament_test.py
```


[Vagrant]: <https://www.vagrantup.com/>
[Virtual Box]: <https://www.virtualbox.org/>
[and this one]: <https://github.com/udacity/fullstack-nanodegree-vm>
