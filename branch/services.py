from commons.decorators import validate_requirements
from .models import Branch


class BranchService:
    """
    General services for branch
    """

    @validate_requirements('name', 'current_balance')
    def insert(self, params):
        """
        Save a new Branch model

        Args:
            params: dict

        Returns: Branch instance

        """
        branch = Branch()
        branch.name = params['name']
        branch.current_balance = params['current_balance']

        branch.save()

        return branch
