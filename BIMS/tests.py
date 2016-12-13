from django.test import TestCase
from django.db import connection
import os
from BIMS.models import User

#alist = User.objects.all()
#print(alist)

# Create your tests here.
#Book_Info_Manager_System
os.environ['DJANGO_SETTINGS_MODULE'] = 'Book_Info_Manager_System.settings'
cursor = connection.cursor()


#test git