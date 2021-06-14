import datetime
import constants
from models import Receipt, ReceiptItem, Group


class GroupAction:
    def __init__(self, name, meat_options, avg_consumption):
        self.name = name
        self.meats = meat_options
        self.avg_consumption = avg_consumption
        self.number = 0
        self.wont_eat = []

    # ask for user information
    def information_input(self):
        while True:
            try:
                print(f'Number of {self.name}: ')
                self.number = int(input())
                break
            except ValueError:
                print('That was not a valid number. Try again ...')
        print(f"{self.name.capitalize()} won't eat: ")
        self.wont_eat = input().lower().split()

    # only select meats which group will eat
    def will_eat(self):
        for self.wont_eat in self.wont_eat:
            if self.wont_eat in self.meats:
                self.meats.pop(self.wont_eat)
        return self.meats

    # create Group objects
    @staticmethod
    def create_groups(groups_info):
        groups = []
        for group_info in groups_info:
            groups.append(Group(group_info.name, group_info.number, group_info.will_eat(), group_info.avg_consumption))
        return groups


class FirstMayTime:
    @staticmethod
    def time_left_until_first_may():
        current_time = datetime.datetime.now()
        this_year = current_time.year
        if current_time.month >= 5:
            this_year += 1
        first_may = datetime.datetime(this_year, 5, 1)
        time_left = first_may - current_time
        return time_left


class MeatCalculator:
    # calculate how much weight is needed
    def weight_needed_by_meat(self, groups):
        self.meat_needed = {'cevapcici': 0, 'chicken': 0, 'sausage': 0, 'porkchop': 0}
        for group in groups:
            for meat in group.meats:
                self.meat_needed[meat] += group.each_meat_weight()
        print(f'\nAmount of meat needed: {self.meat_needed}\n')

    # choose best meat options
    def optimal_meat_choice(self, options):
        for meat, weight in self.meat_needed.items():
            if weight <= constants.MEAT_DEVIATION_LOWER:
                continue

            meat_options = []
            for meat_option in self.meats[meat].values():
                meat_options.append(meat_option.weight)

            weight_choice = min(meat_options, key=lambda x: abs(x - weight))
            options[meat] = self.meats[meat][str(weight_choice)]

    def subtract_weight_from_weight_needed(self, options):
        meat_left = False
        for meat in options.values():
            if meat.name in self.meat_needed.keys():
                self.meat_needed[meat.name] -= meat.weight
                if self.meat_needed[meat.name] >= constants.MEAT_DEVIATION_UPPER:
                    meat_left = True
        return meat_left

    def combination_exists_in_grill_special(self, options):
        for grill_special in self.grill_specials:
            check = True
            for meat in grill_special.meats:
                if meat.name in options.keys():
                    if options[meat.name].weight != meat.weight:
                        check = False
                else:
                    check = False
                    break
            if check:
                for meat in grill_special.meats:
                    del options[meat.name]
                options[grill_special.name] = grill_special

    def add_to_receipt(self, options, result):
        for meat in options.values():
            if meat.name in result:
                if meat.weight in result[meat.name]:
                    result[meat.name][meat.weight]['amount'] += 1
                    result[meat.name][meat.weight]['price'] += meat.price
                else:
                    result[meat.name][meat.weight] = {'meat': meat, 'amount': 1, 'price': meat.price}

            else:
                result[meat.name] = {meat.weight: {'meat': meat, 'amount': 1, 'price': meat.price}}

    def calculate_best_options(self, meats, grill_specials):
        self.meats = meats
        self.grill_specials = grill_specials
        result = {}
        while True:
            options = {}
            self.optimal_meat_choice(options)
            meat_left = self.subtract_weight_from_weight_needed(options)
            self.combination_exists_in_grill_special(options)
            self.add_to_receipt(options, result)

            if not meat_left:
                break

        self.best_options = result
        return self.best_options


class ReceiptItemAction:
    @staticmethod
    def create_receipt_items(items):
        receipt_items = []
        for item in items:
            for meat in items[item]:
                receipt_item = ReceiptItem(items[item][meat]['meat'], items[item][meat]['amount'],
                                           items[item][meat]['price'])
                receipt_items.append(receipt_item)
        return receipt_items


class ReceiptAction:
    def create_receipt(self, items):
        return Receipt(items, self.total_price(items))

    def total_price(self, items):
        total_price = 0
        for item in items:
            total_price += item.price
        return total_price

    def print_receipt(self, receipt):
        for item in receipt.receipt_items:
            print(
                f"Item: {item.meat.name}"
                f"\tWeight: {item.meat.weight}{constants.WEIGHT_UNIT}"
                f"\t Amount: {item.amount}"
                f"\t Price: {item.price}{constants.CURRENCY}")

        print(f"Total price {receipt.total_price}{constants.CURRENCY}")
