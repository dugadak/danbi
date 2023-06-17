from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator

class Team(models.Model):
    name = models.CharField(max_length=4, primary_key=True)


class UserAccountManager(BaseUserManager):
    def create_user(self, username, team_id, password):
        user = self.model(username=username, team_id=team_id, password=password)
        user.set_password(password)
        user.is_admin = False
        user.save(using = self._db)
        return user
    
    def create_superuser(self, username, team_id, password):
        user = self.create_user(username=username, team_id=team_id, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, id):
        return self.get(id=id)
    
    
class User(AbstractBaseUser):
    username = models.CharField(max_length=6, unique=True, validators=[MinLengthValidator(2)])
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    
    USERNAME_FIELD = 'username'
    
    objects = UserAccountManager()