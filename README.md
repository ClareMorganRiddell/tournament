# tournament
My final project for the full-stack option  of the Udacity Nano Degree program "Introduction to Programming". 

## Install

* Download and Install

    You will need to have [Vagrant] and [Virtual Box] installed on your computer in order  to  run this code

    Fork this repository to get the Database and python code, [and this one] to get the VM. 

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
