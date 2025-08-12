from django.db import models
import hashlib


class MyUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()  # Поле для хранения возраста как целого числа
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def get_name(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def verify_age(age):
        # Преобразуем age в целое число, если это строка
        try:
            age = int(age)
        except ValueError:
            return False
        return 18 <= age <= 122

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        hashed_password = self.hash_password(password)
        return hashed_password == self.password

    @property
    def skills(self):
        return list(Skill.objects.filter(userskill__user=self).values_list('name', flat=True))

    class Meta:
        db_table = "my_user"


class Skill(models.Model):
    name = models.CharField(max_length=100)
 
    @classmethod
    def get_all_skills(cls):
        return [obj for obj in cls.objects.all()]
 
    class Meta:
        db_table = "skill"



class Vacancy(models.Model):
    name = models.CharField(max_length=255)
    salary = models.IntegerField()
    area_name = models.CharField(max_length=255)

    @property
    def skills(self):
        return list(Skill.objects.filter(vacancyskill__vacancy=self).values_list('name', flat=True))

    class Meta:
        db_table = "vacancy"


class UserSkill(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_skill"
        constraints = [
            models.UniqueConstraint(fields=['user', 'skill'], name='unique_user_skill')
        ]


class VacancySkill(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        db_table = "vacancy_skill"
        constraints = [
            models.UniqueConstraint(fields=['vacancy', 'skill'], name='unique_vacancy_skill')
        ]


class UserResponse(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        db_table = "user_response"
