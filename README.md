# Ecommerce website
A CRUD website for selling products built by the Django framework and Django rest framework.

## Installation
* Create a virtual environment for this project.
* Use ```pip install -r requirements.txt``` install dependencies packages.
* Sign up in [Stripe](https://stripe.com/) and add your **SECRET_KEY**, **PUBLIC_KEY** and **ENDPOINT_SECRET** in **.env** file.
* Run ```python manage.py makemigrations``` then ```python manage.py migrate```.
* Create super user ```python manage.py createsuperuser```.
* Run server ```python manage.py runserver```.
* For Stripe payments to work you need to first login with ```stripe login``` then to listen to webhook run ```stripe listen --forward-to localhost:8000/payment/webhook/```.

## Features
- User Authentication
- Cart management with AJAX requests
- Payment with Stripe
- CRUD operations for Addresses
- View orders
- All operations can be done via API endpoints

## Photos
- ### Index page
  ![Screenshot_21-5-2024_6122_127 0 0 1](https://github.com/farshadz1997/Django-Ecommerce-Project/assets/60227955/706e1dde-1387-4945-ad06-fd7b5eaa662c)
- ### Product page
  ![Screenshot_21-5-2024_6241_127 0 0 1](https://github.com/farshadz1997/Django-Ecommerce-Project/assets/60227955/88e676c4-f866-4830-acc0-6f9d31dd2dfb)
- ### Shopping cart page
  ![Screenshot_21-5-2024_6355_127 0 0 1](https://github.com/farshadz1997/Django-Ecommerce-Project/assets/60227955/06d59530-13a7-4f3d-82c2-6a29afef09e6)
- ### User dashboard page
  ![Screenshot_21-5-2024_6234_127 0 0 1](https://github.com/farshadz1997/Django-Ecommerce-Project/assets/60227955/e2f30140-5094-4a20-83ea-1e6fa0c07f4c)
