# ShopApp
This app has been developed using Django Rest Framework and PostgreSQL for database. 
I have used JWT for token authentication and authorization. 
The app consists of 5 models and the USER model from django. 
To activate env:
    run comman env\Scripts\activate

Change the database settings as per your database credentials in settings.py.

The basic working of the app is:
  It will create a data entry in the model CART
  The model CARTITEM will also be populated with data. 
  This means that the user has added 1 item to the cart.  
  On hitting the api again, it will check if the cart model has the data entry for the logged in user and also checks if there is an item of that product in the CARTITEM model
  If yes, then it will increment the quantity by 1 or if ‘quantity’ is passed in the body, it will increment by that number + 1
  If it is the same user, but different product, it will add a new entry in the CARTITEM model for that product
  If it is a new user, then the CART model will be populated followed by the Cartitem model
  Here, the order_checkout field is TRUE only when the cartitems are finalized and moved to ORDER model. Else it is false
  Authentication is needed to hit this api. It checks if the logged in user is Customer. If seller, then returns 400_BAD_REQUEST
