from django.utils.translation import gettext
from rest_framework.exceptions import NotFound

from commons.decorators import validate_requirements, validate_existance, str_to_boolean
from payment.models import Payment
from .models import Branch


class BranchService:
    """
    General services for branch
    """

    @validate_requirements("name", "current_balance")
    def insert(self, params):
        """
        Save a new Branch model

        Args:
            params: dict

        Returns: Branch instance

        """
        branch = Branch()
        branch.name = params["name"]
        branch.current_balance = params["current_balance"]

        branch.save()

        return branch

    @validate_existance((Branch, "id"), is_critical=True)
    @validate_requirements("name", "current_balance")
    def update(self, params):
        """
        Update a Branch model

        Args:
            params: dict

        Returns: Branch instance

        """
        branch_id = params["id"]
        name = params["name"]
        current_balance = params["current_balance"]

        branch = Branch(id=branch_id, name=name, current_balance=current_balance)

        branch.save(update_fields=["name", "current_balance"])

        return branch

    def find(self):
        """
        Return a list of branches

        Returns: Branch QuerySet

        """
        return Branch.objects.all()

    def find_by_id(self, branch_id):
        """
        Return a single Branch instance
        Args:
            branch_id: int

        Returns: Branch instance

        """
        try:
            return Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            raise NotFound(detail=gettext("Branch not found"))

    def delete(self, branch_id):
        """
        Delete a Branch instance

        Args:
            branch_id: int
        """
        try:
            Branch.objects.get(id=branch_id).delete()
        except Branch.DoesNotExist:
            raise NotFound(detail=gettext("Branch not found"))

    @validate_existance((Branch, "branch"), is_critical=True)
    @str_to_boolean("is_paid")
    def find_payments(self, params):
        """
        Find a list of branch payment

        Args:
            params: dict - filters

        Returns: Payment queryset

        """
        branch = params["branch"]
        is_paid = params.get("is_paid")

        query = Payment.objects.filter(branch_id=branch)

        if is_paid is not None:
            query = query.filter(is_paid=is_paid)

        return query
