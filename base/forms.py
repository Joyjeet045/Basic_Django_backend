from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
  class Meta:
    model=Room
    #so on form.save() the object is saved in the database
    fields='__all__'
    exclude=['host','participants']
 