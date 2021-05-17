class CompoundResult:
    monthly_returns = [None]*101
    for i in range(101):
        monthly_returns[i] = (1 + (i/100)) ** (1 / float(12))

    def __init__(self, parent, annual_return, months, monthly_deposit=0, initial_amount=None):
        self.parent = parent
        self.annual_return = annual_return
        self.months = months
        self.monthly_deposit = monthly_deposit
        if initial_amount:
            self.result = initial_amount
        else:
            temp_result = parent.result
            monthly_return = CompoundResult.monthly_returns[annual_return]
            for m in range(months):
                # TODO think about multiplying first, then adding deposit after
                temp_result = (temp_result + monthly_deposit) * monthly_return
            self.result = int(temp_result)

    def has_parent(self):
        return self.parent is not None

    def get_compoundresults(self):
        results = []
        pointer = self
        results.insert(0, pointer)
        while pointer.has_parent():
            pointer = pointer.parent
            results.insert(0, pointer)
        return results


class Period:
    def __init__(self, months, monthly_deposit=0):
        self.months = months
        self.monthly_deposit = monthly_deposit


def make_initial_compoundresult(initial_amount):
    return CompoundResult(parent=None, annual_return=None, months=None, monthly_deposit=None, initial_amount=initial_amount)


def generate_compound_possibilities(initial_amount, periods, min_rate, max_rate):
    base = [make_initial_compoundresult(initial_amount=initial_amount)]
    results = []
    for p in periods:
        for res in base:
            for r in range(min_rate, max_rate+1):
                results.append(CompoundResult(parent=res, annual_return=r, months=p.months, monthly_deposit=p.monthly_deposit))
        base = results
        if p != periods[-1]:
            results = []

    for res in results:
        compound_results = res.get_compoundresults()
        row = str(compound_results[0].result)
        for i in range(1, len(compound_results)):
            row = row + f" --{compound_results[i].annual_return}--> {compound_results[i].result}"
        print(row)


# testing the code:
test_periods = [Period(months=24, monthly_deposit=1250), Period(months=50, monthly_deposit=1000), Period(months=75), Period(months=75), Period(months=75)]
test_min_rate = 11
test_max_rate = 11
test_initial_amount = 20000
generate_compound_possibilities(test_initial_amount, test_periods, test_min_rate, test_max_rate)
