from copy import copy
from traceback import format_exc

class RiskManager(object):
    """
    This class exists to have an easy way to attempt something(s) (run a function)
    serially and keep track of exceptions that may happen until we get a good
    outcome or run out of backups

    For instance, in pigeon we use the RiskManager to try different upload
    strategies. First we try batches, but if that "plan" raises an exception
    we go move on to a backup plan, tracking the exception and passing the
    exception to the next plan.

    This continues till we run out of plans or a plan completes without raising
    an exception.
    """
    def __init__(self, plan):
        self.plans = [plan]
        self.exceptions_encountered = []

    def add_backup(self, backup_plan):
        self.plans.append(backup_plan)

    def __call__(self):
        """
        Calling the RiskManager instance will execute the plans in order
        until we have a success.

        Returns any result and the index of the plan that worked
        """
        result = None
        successful_plan = None
        first_plan = self.plans[0]

        for attempted_plan, plan in enumerate( self.plans ):
            try:
                if attempted_plan == 0:
                    result = plan()
                else:
                    result = plan(self.exceptions_encountered[-1])
                successful_plan = attempted_plan
                break
            except Exception as ex:
                self.exceptions_encountered.append(format_exc())

        return ( result, successful_plan )


