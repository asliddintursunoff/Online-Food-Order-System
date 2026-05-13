from django.db import models

class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    WAITER = "waiter", "Waiter"
    CLIENT = "client","Client"
    DELIVERER = "deliverer","Deliverer"

class OrderStatus(models.TextChoices):

    PENDING = "pending","Pending"
    PREPARING = "preparing","Preparing"
    READY = "ready", "Ready for pickup/delivery"
    DELIVERING = "delivering","Delivering"
    DONE = "done","Done"
    CANCELED = "canceled","Cancelled"

class MassType(models.TextChoices):
    KG = 'kg',"kg"
    GR = 'gr','gr'
    LITR = 'litr','litr'