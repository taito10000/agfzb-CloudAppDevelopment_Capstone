try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid

from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(max_length=60)
    desc = models.CharField(max_length=300)

    def __str__(self):
        txt = f"CarMake Class: {self.name}, {self.desc}"
        return txt

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):

    carMake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    dealerId = models.IntegerField()
    carType = models.CharField(max_length=60)
    year = models.DateField()

    def __str__(self):
        txt = f"{self.carMake}, {self.name}, {self.carType}, {self.year}"
        return txt

class myOwnModel(models.Model):
    name = models.CharField(max_length=60)
    age = models.IntegerField()


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
