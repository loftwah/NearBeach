from __future__ import unicode_literals
from email.policy import default
from django.db import models
from .private_media import FileStorage
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import uuid

# ENUM choices
DISCOUNT_CHOICE = (
    ("Percentage", "Percentage"),
    ("Amount", "Amount"),
)

KANBAN_BOARD_STATUS_CHOICE = (
    ("Open", "Open"),
    ("Closed", "Closed"),
)

NOTIFICATION_LOCATION = (
    ("All", "All"),
    ("Login", "Login"),
    ("Dashboard", "Dashboard"),
)

PAGE_LAYOUT = (
    ("Landscape", "Landscape"),
    ("Portrait", "Portrait"),
)

PERMISSION_LEVEL = (
    (0, "No Permission"),
    (1, "Read Only"),
    (2, "Edit Only"),
    (3, "Add and Edit"),
    (4, "Full Permission"),
)

PERMISSION_BOOLEAN = (
    (0, "No Permission"),
    (1, "Has Permission"),
)

PROJECT_STATUS_CHOICE = (
    ("New", "New"),
    ("Backlog", "Backlog"),
    ("Blocked", "Blocked"),
    ("In Progress", "In Progress"),
    ("Test/Review", "Test/Review"),
    ("Closed", "Closed"),
)


RATING_SCORE = (
    (1, "1 Star"),
    (2, "2 Star"),
    (3, "3 Star"),
    (4, "4 Star"),
    (5, "5 Star"),
)

RFC_APPROVAL = (
    (1, "Waiting"),
    (2, "Approved"),
    (3, "Rejected"),
    (4, "Cancel"),
)

RFC_IMPACT = (
    (3, "High"),
    (2, "Medium"),
    (1, "Low"),
)

RFC_PRIORITY = (
    (4, "Critical"),
    (3, "High"),
    (2, "Medium"),
    (1, "Low"),
)

RFC_RISK = (
    (5, "Very High"),
    (4, "High"),
    (3, "Moderate"),
    (2, "Low"),
    (1, "None"),
)

RFC_STATUS = (
    (1, "Draft"),
    (2, "Waiting for approval"),
    (3, "Approved"),
    (4, "Started"),
    (5, "Finished"),
    (6, "Rejected"),
)

RFC_TYPE = (
    (4, "Emergency"),
    (3, "High"),
    (2, "Medium"),
    (1, "Low"),
)

WANT_CHOICE = (
    ("0", "Do not want to do"),
    ("1", "Want to do"),
)
SKILL_CHOICE = (
    ("0", "Can not do"),
    ("1", "Willing to learn"),
    ("2", "Knows a little"),
    ("3", "Knows a lot"),
    ("4", "Proficient"),
)

WEBSITE_SOURCE = (
    ("Twitter", "Twitter"),
    ("Facebook", "Facebook"),
    ("Github", "Github"),
    ("Gitlab", "Gitlab"),
    ("Website", "Website"),
    ("LinkedIn", "LinkedIn"),
    ("Staff Page", "Staff page"),
    ("Other", "Other"),
)


# List of tables - in alphabetical order
class AboutUser(models.Model):
    about_user_id = models.AutoField(primary_key=True)
    about_user_text = models.TextField(
        blank=True,
        default="",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "about_user"


"""
Contact History is a simple form that user will fill out every time they
have some form of contact with the customer. This table will store both
contact history for customer and Organisations. The customer field in
this instance is not required, and implies that the contact history is
applied to the organisation. The organisation field will fill out automatically
when a user applies it to a customer. :)
"""


class ContactHistory(models.Model):
    contact_history_id = models.AutoField(primary_key=True)
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    customer = models.ForeignKey(
        "customer", on_delete=models.CASCADE, blank=True, null=True
    )
    contact_type = models.ForeignKey(
        "ListOfContactType",
        on_delete=models.CASCADE,
    )
    contact_date = models.DateTimeField()
    contact_history = models.TextField("contact_history")
    document_key = models.ForeignKey(
        "document",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "contact_history"


class Bug(models.Model):
    bug_id = models.AutoField(primary_key=True)
    bug_client = models.ForeignKey(
        "BugClient",
        on_delete=models.CASCADE,
    )
    # Just stores the code of the bug
    bug_code = models.CharField(max_length=255)
    bug_description = models.TextField()
    bug_status = models.CharField(max_length=50)  # Updated manually?
    project = models.ForeignKey(
        "project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        "task",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    requirement = models.ForeignKey(
        "requirement",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name='%(class)s_change_user',)
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.bug_description)

    class Meta:
        db_table = "bug"


class BugClient(models.Model):
    bug_client_id = models.AutoField(primary_key=True)
    bug_client_name = models.CharField(max_length=50)
    list_of_bug_client = models.ForeignKey(
        "ListOfBugClient",
        on_delete=models.CASCADE,
    )
    bug_client_url = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name='%(class)s_change_user',
                                    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.bug_client_name)

    class Meta:
        db_table = "bug_client"


class Campus(models.Model):
    campus_id = models.AutoField(primary_key=True)
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    customer = models.ForeignKey(
        "customer",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default="",
    )
    campus_nickname = models.CharField(max_length=100)
    campus_phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        default="",
    )
    campus_fax = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        default="",
    )
    campus_address1 = models.CharField(
        max_length=255, 
        null=True,
        blank=True,
        default="",
    )
    campus_address2 = models.CharField(
        max_length=255, 
        null=True,
        blank=True,
        default="",
    )
    campus_address3 = models.CharField(
        max_length=255, 
        null=True,
        blank=True,
        default="",
    )
    campus_suburb = models.CharField(
        max_length=50
    )
    campus_region = models.ForeignKey(
        "ListOfCountryRegion",
        on_delete=models.CASCADE,
    )
    campus_postcode = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    campus_country = models.ForeignKey(
        "ListOfCountry",
        on_delete=models.CASCADE,
    )
    campus_longitude = models.DecimalField(
        decimal_places=13,
        max_digits=16,
        null=True,  # If use has no mapping software, we want to leave this blank
        blank=True,
    )
    campus_latitude = models.DecimalField(
        decimal_places=13,
        max_digits=16,
        null=True,  # If use has no mapping software, we want to leave this blank
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.campus_nickname)

    class Meta:
        db_table = "campus"


class ChangeTask(models.Model):
    change_task_id = models.AutoField(primary_key=True)
    request_for_change = models.ForeignKey(
        "RequestForChange",
        on_delete=models.CASCADE,
    )
    change_task_title = models.CharField(
        max_length=255,
    )
    change_task_description = models.TextField(
        blank=True,
        null=True,
        default="",
    )
    change_task_start_date = models.DateTimeField()
    change_task_end_date = models.DateTimeField()
    change_task_seconds = models.BigIntegerField(
        default=0,
    )
    change_task_assigned_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="change_assigned_user",
    )
    change_task_qa_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="change_qa_user",
    )
    change_task_required_by = models.CharField(
        max_length=255,
        default="Stakeholder(s)",
    )
    change_task_status = models.IntegerField(
        choices=RFC_STATUS,  # Similar FLOW to RFC
    )
    is_downtime = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
    )
    creation_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_creation_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str("$" + str(self.change_task_title))

    class Meta:
        db_table = "change_task"


class ChangeTaskBlock(models.Model):
    change_task_blocks = models.ForeignKey(
        ChangeTask,
        on_delete=models.CASCADE,
        related_name="change_task_blocks",
    )
    blocked_change_task = models.ForeignKey(
        ChangeTask,
        on_delete=models.CASCADE,
        related_name="blocked_change_task",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
    )
    creation_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_creation_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str("$" + str(self.change_task_title))

    class Meta:
        db_table = "change_task_block"


class Cost(models.Model):
    cost_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        "project", on_delete=models.CASCADE, blank=True, null=True
    )
    task = models.ForeignKey("task", on_delete=models.CASCADE, blank=True, null=True)
    cost_description = models.CharField(
        max_length=255,
    )
    cost_amount = models.DecimalField(max_digits=19, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str("$" + str(self.cost_amount))

    class Meta:
        db_table = "cost"


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_title = models.ForeignKey(
        "ListOfTitle",
        on_delete=models.CASCADE,
    )
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    customer_email = models.CharField(max_length=200)
    customer_profile_picture = models.ForeignKey(
        "document",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(
            str(self.customer_id)
            + " - "
            + self.customer_first_name
            + " "
            + self.customer_last_name
        )

    class Meta:
        db_table = "customer"


class CustomerCampus(models.Model):
    customer_campus_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        "customer",
        on_delete=models.CASCADE,
    )
    campus = models.ForeignKey(
        "campus",
        on_delete=models.CASCADE,
    )
    customer_phone = models.CharField(max_length=20)
    customer_fax = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "customer_campus"


class Document(models.Model):
    document_key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    document_description = models.CharField(max_length=255)
    document_url_location = models.TextField(
        # Contains URLS
        null=True,
        blank=True,
        default="",
    )
    document = models.FileField(
        blank=True,
        null=True,
        storage=FileStorage(),
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "document"

    def __str__(self):
        return str(self.document_description)


class DocumentPermission(models.Model):
    document_permisssion_id = models.AutoField(primary_key=True)
    document_key = models.ForeignKey(
        "document",
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        "project",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        "task",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    organisation = models.ForeignKey(
        "organisation",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        "customer",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    requirement = models.ForeignKey(
        "requirement",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    requirement_item = models.ForeignKey(
        "RequirementItem",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    request_for_change = models.ForeignKey(
        "RequestForChange",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    folder = models.ForeignKey(
        "folder",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "document_permission"


class EmailContact(models.Model):
    email_contact_id = models.AutoField(primary_key=True)
    email_content = models.ForeignKey(
        "EmailContent",
        on_delete=models.CASCADE,
    )
    to_customer = models.ForeignKey(
        "customer",
        related_name="%(class)s_to_customer",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    cc_customer = models.ForeignKey(
        "customer",
        related_name="%(class)s_cc_customer",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    bcc_customer = models.ForeignKey(
        "customer",
        related_name="%(class)s_bcc_customer",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    project = models.ForeignKey(
        "project",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        "task",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    is_private = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "email_contact"


class EmailContent(models.Model):
    email_content_id = models.AutoField(primary_key=True)
    email_subject = models.CharField(max_length=255)
    email_content = models.TextField("email_content")
    is_private = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "email_content"


class Folder(models.Model):
    folder_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        "project", on_delete=models.CASCADE, blank=True, null=True
    )
    task = models.ForeignKey("task", on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(
        "customer",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement = models.ForeignKey(
        "requirement",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement_item = models.ForeignKey(
        "RequirementItem",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    request_for_change = models.ForeignKey(
        "RequestForChange",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    folder_description = models.CharField(max_length=255)
    parent_folder = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.folder_description)

    class Meta:
        db_table = "folder"


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(
        max_length=50,
    )
    parent_group = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def natural_key(self):
        return (self.group_id, self.group_name)

    def __str__(self):
        return str(self.group_name)

    class Meta:
        db_table = "group"


class GroupManager(models.Manager):
    def get_by_natural_key(self, group_id, group_name):
        return self.get(group_id=group_id, group_name=group_name)


class GroupPermission(models.Model):
    group_permission_id = models.AutoField(primary_key=True)
    permission_set = models.ForeignKey(
        "PermissionSet",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey("group", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.permission_set)

    class Meta:
        db_table = "group_permission"


class KanbanBoard(models.Model):
    kanban_board_id = models.AutoField(primary_key=True)
    kanban_board_name = models.CharField(max_length=255)
    requirement = models.ForeignKey(
        "requirement",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    kanban_board_status = models.CharField(
        max_length=10,
        choices=KANBAN_BOARD_STATUS_CHOICE,
        default="Open",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    creation_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_creation_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "kanban_board"

    def __str__(self):
        return str(self.kanban_board_name)


class KanbanCard(models.Model):
    kanban_card_id = models.AutoField(primary_key=True)
    kanban_card_text = models.CharField(max_length=255)
    kanban_card_description = models.TextField(
        blank=True,
        default="",
    )
    kanban_card_sort_number = models.IntegerField()
    kanban_level = models.ForeignKey(
        "KanbanLevel",
        on_delete=models.CASCADE,
    )
    kanban_column = models.ForeignKey(
        "KanbanColumn",
        on_delete=models.CASCADE,
    )
    kanban_board = models.ForeignKey(
        "KanbanBoard",
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        "project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        "task",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    requirement = models.ForeignKey(
        "requirement",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_archived = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "kanban_card"

    def __str__(self):
        return str(self.kanban_card_text)


class KanbanColumn(models.Model):
    kanban_column_id = models.AutoField(primary_key=True)
    kanban_column_name = models.CharField(max_length=255)
    kanban_column_sort_number = models.IntegerField()
    kanban_board = models.ForeignKey(
        "KanbanBoard",
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "kanban_column"

    def __str__(self):
        return str(self.kanban_column_name)


class KanbanLevel(models.Model):
    kanban_level_id = models.AutoField(primary_key=True)
    kanban_level_name = models.CharField(max_length=255)
    kanban_level_sort_number = models.IntegerField()
    kanban_board = models.ForeignKey(
        "KanbanBoard",
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "kanban_level"

    def __str__(self):
        return str(self.kanban_level_name)


class Kudos(models.Model):
    kudos_key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    kudos_rating = models.IntegerField(
        choices=RATING_SCORE,
        default=0,
    )
    improvement_note = models.TextField(
        blank=True,
        default="",
    )
    liked_note = models.TextField(
        blank=True,
        default="",
    )
    extra_kudos = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    submitted_kudos = models.BooleanField(
        default=False,
    )
    project = models.ForeignKey(
        "project",
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        "customer",
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "kudos"


class ListOfAmountType(models.Model):
    amount_type_id = models.AutoField(primary_key=True)
    amount_type_description = models.CharField(max_length=20)
    list_order = models.IntegerField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.amount_type_description)

    class Meta:
        db_table = "list_of_amount_type"
        ordering = ["list_order"]


class ListOfBugClient(models.Model):
    list_of_bug_client_id = models.AutoField(primary_key=True)
    bug_client_name = models.CharField(max_length=50)
    bug_client_api_url = models.CharField(max_length=255)

    # The different API commands
    api_open_bugs = models.CharField(max_length=255)  # Find all open bugs
    api_search_bugs = models.CharField(max_length=255)  # Search command

    # Get that particular bug information - direct link to bug
    api_bug = models.CharField(max_length=255)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.bug_client_name)

    class Meta:
        db_table = "list_of_bug_client"


class ListOfCurrency(models.Model):
    currency_id = models.AutoField(primary_key=True)
    currency_description = models.CharField(max_length=20)
    currency_short_description = models.CharField(max_length=4)
    list_order = models.IntegerField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.currency_description)

    class Meta:
        db_table = "list_of_currency"


class ListOfContactType(models.Model):
    contact_type_id = models.AutoField(primary_key=True)
    contact_type = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.contact_type)

    class Meta:
        db_table = "list_of_contact_type"


class ListOfCountry(models.Model):
    country_id = models.CharField(primary_key=True, max_length=2)
    country_name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.country_name)

    class Meta:
        db_table = "list_of_country"


class ListOfCountryRegion(models.Model):
    region_id = models.AutoField(primary_key=True)
    country = models.ForeignKey(
        "ListOfCountry",
        on_delete=models.CASCADE,
    )
    region_name = models.CharField(max_length=150)
    region_type = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        default="",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.region_name)

    class Meta:
        db_table = "list_of_country_region"


class ListOfRequirementItemStatus(models.Model):
    requirement_item_status_id = models.AutoField(primary_key=True)
    requirement_item_status = models.CharField(
        max_length=100,
    )
    status_is_closed = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_item_status)

    class Meta:
        db_table = "list_of_requirement_item_status"


class ListOfRequirementItemType(models.Model):
    requirement_item_type_id = models.AutoField(primary_key=True)
    requirement_item_type = models.CharField(
        max_length=100,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_item_type)

    class Meta:
        db_table = "list_of_requirement_item_type"


class ListOfRequirementStatus(models.Model):
    requirement_status_id = models.AutoField(primary_key=True)
    requirement_status = models.CharField(
        max_length=50,
    )
    requirement_status_is_closed = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_status)

    class Meta:
        db_table = "list_of_requirement_status"


class ListOfRequirementType(models.Model):
    requirement_type_id = models.AutoField(primary_key=True)
    requirement_type = models.CharField(
        max_length=100,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_type)

    class Meta:
        db_table = "list_of_requirement_type"


class ListOfRFCStatus(models.Model):
    rfc_status_id = models.AutoField(primary_key=True)
    rfc_status = models.CharField(
        max_length=100,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.rfc_status)

    class Meta:
        db_table = "list_of_rfc_status"


class ListOfTax(models.Model):
    tax_id = models.AutoField(primary_key=True)
    tax_amount = models.DecimalField(
        max_digits=6,
        decimal_places=4,
    )
    tax_description = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )  # Incase the customer wants to place a name against the tax
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        # No need to encode as it is a decimal point
        return str(self.tax_amount)

    class Meta:
        db_table = "list_of_tax"


class ListOfTitle(models.Model):
    title_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = "list_of_title"


class NearbeachOption(models.Model):
    """
    This table will store the options for NearBeach.
    These options will have a new row each time a new option is created
    There does not need to be a is_deleted function
    """

    nearbeach_option_id = models.AutoField(primary_key=True)
    story_point_hour_min = models.IntegerField(
        default=4,
    )
    story_point_hour_max = models.IntegerField(
        default=10,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.nearbeach_option_id)

    class Meta:
        db_table = "nearbeach_option"


class Notification(models.Model):
    """
    Administrator can utilise this field to store notifications to tell users.
    Notifications can appear on;
    - Login screen
    - Dashboard
    """

    notification_id = models.AutoField(primary_key=True)
    notification_header = models.CharField(
        blank=False,
        null=False,
        max_length=255,
    )
    notification_message = models.TextField(
        blank=True,
        default="",
    )
    notification_start_date = models.DateTimeField()
    notification_end_date = models.DateTimeField()
    notification_location = models.CharField(
        max_length=20,
        choices=NOTIFICATION_LOCATION,
        default="All",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "notification"


class ObjectAssignment(models.Model):
    """
    Object permissions is the centralised permissions for all objects
    - Requirement
    - Project
    - Task
    - Kanban board
    - Request for change
    - Card

    These permission are only "ACCESS" permissions.
    The user/group's over riding permissions determine if
    the user can add, edit etc.
    """

    object_assignment_id = models.AutoField(primary_key=True)
    assigned_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_assigned_user",
        null=True,
        blank=True,
    )
    group_id = models.ForeignKey(
        "group",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement = models.ForeignKey(
        "requirement",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement_item = models.ForeignKey(
        "RequirementItem",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    project = models.ForeignKey(
        "project",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        "task",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    kanban_board = models.ForeignKey(
        "KanbanBoard",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    kanban_card = models.ForeignKey(
        "kanban_card",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    request_for_change = models.ForeignKey(
        "RequestForChange",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    customer = models.ForeignKey(
        "customer",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    meta_object = models.BigIntegerField(
        blank=True,
        null=True,
    )
    meta_object_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    meta_object_status = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "object_assignment"


class ObjectNote(models.Model):
    object_note_id = models.AutoField(primary_key=True)
    object_note = models.TextField(
        blank=False,
        default="",
    )
    kanban_card = models.ForeignKey(
        "KanbanCard",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement = models.ForeignKey(
        "requirement",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement_item = models.ForeignKey(
        "RequirementItem",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    project = models.ForeignKey(
        "project",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        "task",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    request_for_change = models.ForeignKey(
        "RequestForChange",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "object_note"


class Organisation(models.Model):
    organisation_id = models.AutoField(primary_key=True)
    organisation_name = models.CharField(max_length=255)
    organisation_website = models.CharField(max_length=50)
    organisation_email = models.CharField(max_length=100)
    organisation_profile_picture = models.ForeignKey(
        "document",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.organisation_name)

    class Meta:
        db_table = "organisation"


class PermissionSet(models.Model):
    permission_set_id = models.AutoField(primary_key=True)
    permission_set_name = models.CharField(
        max_length=255,
    )
    # ADMINISTRATION PERMISSIONS
    administration_assign_user_to_group = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    administration_create_group = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    administration_create_permission_set = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    administration_create_user = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    bug_client = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    customer = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    kanban_board = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    kanban_card = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    organisation = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    project = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    request_for_change = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    requirement = models.IntegerField(choices=PERMISSION_LEVEL, default=0)
    task = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    """
    ADDITIVE permission
    ~~~~~~~~~~~~~~~~~~~~
    Designed to add on extra abilities to those user who have "READ ONLY" for certain modules.
    If a user has the ability to "EDIT" for any of these modules, then this section does not
    need to be populated with data.
    """
    document = models.IntegerField(
        choices=PERMISSION_BOOLEAN,
        default=0,
    )
    kanban_comment = models.IntegerField(
        choices=PERMISSION_BOOLEAN,
        default=0,
    )
    project_history = models.IntegerField(
        choices=PERMISSION_BOOLEAN,
        default=0,
    )
    task_history = models.IntegerField(
        choices=PERMISSION_BOOLEAN,
        default=0,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.permission_set_name)

    class Meta:
        db_table = "permission_set"


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    project_description = models.TextField("project_description")
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # Only fill this field out if there are no organisation
    customer = models.ForeignKey(
        "customer",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    project_start_date = models.DateTimeField()
    project_end_date = models.DateTimeField()
    project_status = models.CharField(
        max_length=15, choices=PROJECT_STATUS_CHOICE, default="New"
    )
    project_story_point_min = models.IntegerField(default=1)
    project_story_point_max = models.IntegerField(default=4)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    creation_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_creation_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.project_name)

    class Meta:
        db_table = "project"


class ProjectCustomer(models.Model):
    project_customer_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        "project",
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        "customer",
        on_delete=models.CASCADE,
    )
    customer_description = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "project_customer"


class RequestForChange(models.Model):
    """
    Due to the long and complicated name,
    request for change will be shortened to rfc for ALL fields.
    """

    rfc_id = models.AutoField(primary_key=True)
    rfc_title = models.CharField(
        max_length=255,
    )
    rfc_summary = models.TextField("rfc_summary")
    rfc_type = models.IntegerField(
        choices=RFC_TYPE,
    )
    rfc_implementation_start_date = models.DateTimeField()
    rfc_implementation_end_date = models.DateTimeField()
    rfc_implementation_release_date = models.DateTimeField()
    rfc_version_number = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )
    rfc_status = models.ForeignKey(
        "ListOfRfcStatus",
        on_delete=models.CASCADE,
    )
    rfc_lead = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="RfcLead",
    )
    rfc_priority = models.IntegerField(
        choices=RFC_PRIORITY,
        default=1,
    )
    rfc_risk = models.IntegerField(
        choices=RFC_RISK,
        default=1,
    )
    rfc_impact = models.IntegerField(
        choices=RFC_IMPACT,
        default=1,
    )
    rfc_risk_and_impact_analysis = models.TextField(
        "rfc_risk_and_impact_analysis",
    )
    rfc_implementation_plan = models.TextField(
        "rfc_implementation_plan",
    )
    rfc_backout_plan = models.TextField(
        "rfc_backout_plan",
    )
    rfc_test_plan = models.TextField(
        "rfc_test_plan",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    creation_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_creation_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.rfc_title)

    class Meta:
        db_table = "request_for_change"


class RequestForChangeGroupApproval(models.Model):
    rfc_group_approval_id = models.AutoField(primary_key=True)
    rfc = models.ForeignKey(
        "RequestForChange",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        "group",
        on_delete=models.CASCADE,
    )
    approval = models.IntegerField(
        choices=RFC_APPROVAL,
        default=1,  # Waiting
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.approval)

    class Meta:
        db_table = "request_for_change_group_approval"


class RequestForChangeNote(models.Model):
    rfc_note_id = models.AutoField(primary_key=True)
    rfc_note = models.TextField(
        blank=True,
        default="",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.rfc_note)

    class Meta:
        db_table = "request_for_change_note"


class RequestForChangeStakeholder(models.Model):
    """
    This model will store all the stakeholders for those request for changes. The stakeholders could be an organisation
    OR a customer.

    rfc = request for change. It is shortened to make it easier for the programmer.
    """

    rfc_stakeholder_id = models.AutoField(primary_key=True)
    request_for_change = models.ForeignKey(
        "RequestForChange",
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        "customer",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "request_for_change_stakeholder"


class Requirement(models.Model):
    requirement_id = models.AutoField(primary_key=True)
    requirement_title = models.CharField(
        max_length=255,
    )
    requirement_scope = models.TextField(
        blank=True,
        default="",
    )
    requirement_type = models.ForeignKey(
        "ListOfRequirementType",
        on_delete=models.CASCADE,
    )
    requirement_status = models.ForeignKey(
        "ListOfRequirementStatus",
        on_delete=models.CASCADE,
    )
    requirement_story_point_min = models.IntegerField(default=1)
    requirement_story_point_max = models.IntegerField(default=4)
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    creation_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_creation_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_title)

    class Meta:
        db_table = "requirement"


class RequirementCustomer(models.Model):
    requirement_customer_id = models.AutoField(primary_key=True)
    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_customer_id)

    class Meta:
        db_table = "requirement_customer"


class RequirementItem(models.Model):
    requirement_item_id = models.AutoField(primary_key=True)
    requirement = models.ForeignKey(
        "requirement",
        on_delete=models.CASCADE,
    )
    requirement_item_title = models.CharField(max_length=255)
    requirement_item_scope = models.TextField(
        blank=True,
        default="",
    )
    requirement_item_status = models.ForeignKey(
        "ListOfRequirementItemStatus",
        on_delete=models.CASCADE,
    )
    requirement_item_type = models.ForeignKey(
        "ListOfRequirementItemType",
        on_delete=models.CASCADE,
    )
    ri_story_point_min = models.IntegerField(default=4)
    ri_story_point_max = models.IntegerField(default=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_item_title)

    class Meta:
        db_table = "requirement_item"


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(
        max_length=50,
    )
    tag_colour = models.CharField(
        max_length=7,
        default="#651794",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.tag_name)

    class Meta:
        db_table = "tag"


class TagAssignment(models.Model):
    class ObjectEnum(models.TextChoices):
        REQUIREMENT = "requirement", _("Requirement")
        REQUIREMENT_ITEM = "RequirementItem", _("Requirement Item")
        PROJECT = "project", _("Project")
        TASK = "task", _("Task")
        KANBAN = "KanbanBoard", _("Kanban Board")
        CARD = "KanbanCard", _("Kanban Card")
        REQUEST_FOR_CHANGE = "RequestForChange", _("Request for Change")
        CUSTOMER = "customer", _("Customer")
        ORGANISATION = "organisation", _("Organisation")

    tag_assignment_id = models.AutoField(primary_key=True)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )
    object_enum = models.CharField(
        max_length=40,
        choices=ObjectEnum.choices,
        default=ObjectEnum.REQUIREMENT,
    )
    object_id = models.IntegerField(
        default=0,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "tag_assignment"


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_short_description = models.CharField(max_length=255)
    task_long_description = models.TextField()
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task_start_date = models.DateTimeField()
    task_end_date = models.DateTimeField()
    task_assigned_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    task_status = models.CharField(
        max_length=15, choices=PROJECT_STATUS_CHOICE, default="New"
    )
    task_story_point_min = models.IntegerField(default=4)
    task_story_point_max = models.IntegerField(default=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    creation_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_creation_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.task_short_description)

    class Meta:
        db_table = "task"


class TaskAction(models.Model):
    task_action_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(
        "task",
        on_delete=models.CASCADE,
    )
    task_action = models.TextField()
    submitted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "task_action"


class TaskCustomer(models.Model):
    task_customer_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(
        "task",
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        "customer",
        on_delete=models.CASCADE,
    )
    customer_description = models.CharField(max_length=155, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "task_customer"


class Timesheet(models.Model):
    timesheet_id = models.AutoField(primary_key=True)
    timesheet_description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    timesheet_date = models.DateField()
    timesheet_start_time = models.TimeField()
    timesheet_end_time = models.TimeField()
    project = models.ForeignKey(
        "project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        "task",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    requirement_item = models.ForeignKey(
        "RequirementItem",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    # Doubles up as the user inputting the time
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "timesheet"


class ToDo(models.Model):
    to_do_id = models.AutoField(primary_key=True)
    to_do = models.CharField(
        max_length=255,
    )
    to_do_completed = models.BooleanField(default=False)
    project = models.ForeignKey(
        "project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        "task",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "to_do"


class UserGroup(models.Model):
    user_group_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        "group",
        on_delete=models.CASCADE,
    )
    permission_set = models.ForeignKey(
        "PermissionSet",
        on_delete=models.CASCADE,
    )
    report_to = models.ForeignKey(
        User,
        related_name="report_to",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    group_leader = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "user_group"


class UserWant(models.Model):
    user_want_id = models.AutoField(
        primary_key=True,
    )
    want_choice = models.CharField(
        max_length=50,
        choices=WANT_CHOICE,
    )
    want_choice_text = models.CharField(
        max_length=50,
    )
    want_skill = models.CharField(
        max_length=50,
        choices=SKILL_CHOICE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.want_choice_text

    class Meta:
        db_table = "user_want"


class UserWeblink(models.Model):
    user_weblink_id = models.AutoField(primary_key=True)
    user_weblink_url = models.URLField(max_length=255)
    user_weblink_source = models.CharField(
        max_length=50,
        choices=WEBSITE_SOURCE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.user_weblinks_url

    class Meta:
        db_table = "user_weblink"
