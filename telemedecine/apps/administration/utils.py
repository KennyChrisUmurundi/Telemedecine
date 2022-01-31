from telemedecine.apps.core.models.hospital_models import Patient, Institution
from telemedecine.apps.authentication.models import CustomUser
from telemedecine.apps.core.models.administration import Role


def get_institution(user):
    try:
        resp = Institution.objects.get(id=user)
    except Institution.DoesNotExist as err:
        logging.debug("INSTITUTION NOT FOUND:%s" % err)
        resp = None
    return resp


def create_patient(
    user, first_name, last_name, age, gender, address, phone_number, email=None
):
    user = None
    institution = get_institution(user.user_role.institution_id)
    if email:
        try:
            user = CustomUser.objects.get(email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except CustomUser.DoesNotExist:
            temp_password = uuid.uuid4().hex[:6].upper()
            user = CustomUser.objects.create_user(email, temp_password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            try:
                send_mail(
                    "Telemedecine Patient Creation",
                    "Hi dear"
                    + user.email
                    + " Your Generated Password is "
                    + temp_password
                    + " Use it to login to our platform",
                    " telemedecine@gmail.com",
                    [email],
                    fail_silently=False,
                )
            except BaseException:
                pass

        try:
            existing_role = Role.objects.get(user=user)
            return False
        except Role.DoesNotExist:
            pass

        try:
            role = Role.objects.get(
                user=user,
                institution=institution,
                role=Role.PATIENT,
            )
        except Role.DoesNotExist:
            role = Role.objects.create(
                user=user,
                institution=institution,
                role=Role.PATIENT,
            )
            role.save()
    patient_code = "PA-" + uuid.uuid4().hex[:6].upper()
    patient = Patient.objects.create(
        institution=institution,
        # user=user,
        patient_code=patient_code,
        first_name=first_name,
        last_name=last_name,
        age=age,
        country=institution.country,
        email=email,
        gender=gender,
        address=address,
        phone_number=phone_number,
    )
    if user:
        patient.user = user
    patient.save()

    return True, patient
