# Ecommerce website
A website for selling products built by Django framework and you may see live demo of this project on heroku from the following link.
https://farshad-online-shop.herokuapp.com

## Installation
* Create virtual environment for this project.
* Use ```pip install -r requirements.txt``` install dependencies packages.
* Sign up in [Stripe](https://stripe.com/) and add your **SECRET_KEY**, **PUBLIC_KEY** and **ENDPOINT_SECRET** in **.env** file.
* Run ```python manage.py makemigrations``` then ```python manage.py migrate```.
* Create super user ```python manage.py createsuperuser```.
* Run server ```python manage.py runserver```.
* In order to Stripe payments works you need to first login with ```stripe login``` then for listening to webhook run ```stripe listen --forward-to localhost:8000/payment/webhook/```.
