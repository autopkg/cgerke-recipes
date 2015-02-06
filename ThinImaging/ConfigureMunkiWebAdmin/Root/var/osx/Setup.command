#!/bin/bash

path_root="$3"; if [ -z "${path_root}" ] || [ "${path_root}" = "/" ]; then path_root=""; fi #++ fix //
formatted_date=$(date +"%Y%m%d%H%M%S") #++ date to string

# it's awesome, its here https://github.com/munki/munkiwebadmin
# make this smarter eventually...not enough checks

# MunkiWebAdmin
easy_install virtualenv
cd /Volumes/Data/www/
virtualenv munkiwebadmin_env
cd munkiwebadmin_env
source ./bin/activate
pip install django==1.5.1
pip install django-wsgiserver==0.8.0beta
git clone https://github.com/munki/munkiwebadmin/ munkiwebadmin
cd munkiwebadmin
cp settings_template.py settings.py

# permissions
sudo chown -R root:osx /Volumes/Data/www/munkiwebadmin_env
sudo chmod -R 775 /Volumes/Data/www/munkiwebadmin_env

# script edit this eventually settings.py
# https://github.com/munki/munkiwebadmin/wiki/MunkiWebAdmin-OSX-Setup

exit 0