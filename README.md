# Udacity Tournament

This project is to complete Udacity's *Intro Into Relation Databases* section of the Full Stack Engineering Nanodegree course. The objective of this project is to create a database schema and develop Python functions to simulate a [Swiss System Tournament](https://en.wikipedia.org/wiki/Swiss-system_tournament).

## Installation

To install Udacity Tournament [VirtualBox](https://www.virtualbox.org/) is required and Vagrant.
```bash
sudo apt-get install vagrant
git clone https://github.com/JAmedeo/udacity-tournament.git
cd udacity-tournament/FSND-Virtual-Machine/vagrant
vagrant up
vagrant ssh
cd /vagrant/tournament
python tournament_test.py
```

That's it!
