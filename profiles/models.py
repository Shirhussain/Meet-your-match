from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _ 
from django.urls import reverse
from django.contrib.auth.signals import user_logged_in

import stripe
from conf.stripe_info import Secret_key, Publishable_key

# here i didn't hide so you have to make sure that use decupal or enve to hide this sensitive info
stripe.api_key = Secret_key



class Address(models.Model):
    """Model definition for Address."""

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    street_address = models.CharField(_("Street Address"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    state = models.CharField(_("State"), max_length=50)
    zipcode = models.IntegerField(_("Zip Code"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated "), auto_now=True, auto_now_add=False)
    active = models.BooleanField(_("Active"), default=True)


    class Meta:
        """Meta definition for Address."""

        verbose_name = 'Address'
        verbose_name_plural = 'Addresess'

    def __str__(self):
        """Unicode representation of Address."""
        return self.city 


class Job(models.Model):
    """Model definition for Job."""

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    position = models.CharField(_("Position"), max_length=50)
    employer = models.CharField(_("Employer"), max_length=50)
    employer_address = models.CharField(_("Employer Address"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    state = models.CharField(_("State"), max_length=50)
    zipcode = models.IntegerField(_("Zipe Code"))
    phone = models.CharField(_("Phone"), max_length=13, null=True, blank=True)
    start_date = models.DateTimeField(_("Start Date"), auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(_("End date"), auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=False, auto_now_add=False)
    active = models.BooleanField(_("Active"), default=True)

    class Meta:
        """Meta definition for Job."""

        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

    def __str__(self):
        """Unicode representation of Job."""
        return self.position


class UserPicture(models.Model):

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to="Profiles/", height_field=None, width_field=None, max_length=None)
    timestamp = models.DateTimeField(_("Timstamp"), auto_now=False, auto_now_add=True)
    active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("UserPicture")
        verbose_name_plural = _("UserPictures")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("UserPicture_detail", kwargs={"pk": self.pk})


CHOICES = (
    ('Regular', 'Regular'),
    ('Staff', 'Staff'),
    ('Premium', 'Premium'),
)

class UserRole(models.Model):
    """Model definition for UserRole."""

    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)
    role = models.CharField(_("Role"), max_length=8, default="Regular", choices=CHOICES)

    class Meta:
        """Meta definition for UserRole."""

        verbose_name = 'UserRole'
        verbose_name_plural = 'UserRoles'

    def __str__(self):
        """Unicode representation of UserRole."""
        return self.role



class UserStripe(models.Model):
    """Model definition for UserStripe."""

    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)
    stripe_id = models.CharField(_("Stripe id"), max_length=50, null=True, blank=True)

    def get_stripe_id(self):
        return self.stripe_id 

    class Meta:
        """Meta definition for UserStripe."""

        verbose_name = 'UserStripe'
        verbose_name_plural = 'UserStripes'

    def __str__(self):
        """Unicode representation of UserStripe."""
        return self.user.username

def CreateStripeId(sender, user, request, **kwargs):
    new_id, created = UserStripe.objects.get_or_create(user=user)
    if created:
        print(created)
        # add user's email to stripe, then set the stripe ID
        stripe_customer = stripe.Customer.create(email=user.email, description=f"Stripe customer email is: {user.email}")
        print("This is Stripe customer id", stripe_customer.id)
        new_id.stripe_id = stripe_customer.id
        new_id.save()
    else:
        print("Not Created stripe id")

user_logged_in.connect(CreateStripeId)

