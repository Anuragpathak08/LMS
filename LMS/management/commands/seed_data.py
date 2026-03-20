from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import timedelta
from django.utils import timezone

from account.models import Department, User
from LMS.models import LeaveRequest


fake = Faker()


class Command(BaseCommand):

    help = "Generate fake LMS data"

    def handle(self, *args, **kwargs):

        # Create Departments
        departments = ["Engineering", "HR", "Finance", "Marketing"]

        dept_objects = []

        for dept in departments:
            obj, created = Department.objects.get_or_create(name=dept)
            dept_objects.append(obj)

        self.stdout.write(self.style.SUCCESS("Departments created"))

        # Create Users
        users = []

        for i in range(50):

            department = random.choice(dept_objects)

            user = User.objects.create_user(
                username=fake.user_name() + str(i),
                email=fake.email(),
                password="1234",
                department=department
            )

            users.append(user)

        self.stdout.write(self.style.SUCCESS("Users created"))

        # Create Leave Requests
        for user in users:

            start_date = fake.date_between(start_date="-30d", end_date="+30d")

            end_date = start_date + timedelta(days=random.randint(0, 5))

            LeaveRequest.objects.create(
                user=user,
                start_date=start_date,
                end_date=end_date,
                reason=fake.sentence(),
                status=random.choice(["pending", "approved", "rejected"])
            )

        self.stdout.write(self.style.SUCCESS("Leave requests created"))
