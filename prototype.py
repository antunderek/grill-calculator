#! /usr/bin/env/python3

from models import Meat, GrillSpecial
from actions import GroupAction, FirstMayTime, MeatCalculator, ReceiptItemAction, ReceiptAction
import constants


meat_options = {
    'cevapcici': {
        '500': Meat('cevapcici', 500, 22),
        '1000': Meat('cevapcici', 1000, 35),
        '2000': Meat('cevapcici', 2000, 60),
    },
    'chicken': {
        '500': Meat('chicken', 500, 35),
        '1000': Meat('chicken', 1000, 60),
    },
    'sausage': {
        '400': Meat('sausage', 400, 15),
        '800': Meat('sausage', 800, 25),
    },
    'porkchop': {
        '500': Meat('porkchop', 500, 20),
        '1000': Meat('porkchop', 1000, 35),
    },
}

grill_specials = {
    GrillSpecial(
        'cevapcici-chicken-sausage',
        [
            meat_options['cevapcici']['500'], 
            meat_options['chicken']['500'], 
            meat_options['sausage']['400'],
        ], 65),
    GrillSpecial(
        'cevapcici-sausage',
        [
            meat_options['cevapcici']['1000'],
            meat_options['sausage']['800'],
        ], 55),
    GrillSpecial(
        'sausage-porkchop',
        [
            meat_options['sausage']['400'],
            meat_options['porkchop']['500'],
        ], 35),
}
   
# create GroupAction objects and ask for user input
men = GroupAction('men', meat_options.copy(), constants.MAN_AVG_CONSUMPTION)
men.information_input()

women = GroupAction('women', meat_options.copy(), constants.WOMAN_AVG_CONSUMPTION)
women.information_input()

children = GroupAction('children', meat_options.copy(), constants.CHILD_AVG_CONSUMPTION)
children.information_input()

groups_info = [men, children, women]

# return a list of Group objects
groups = GroupAction.create_groups(groups_info)

calculator = MeatCalculator()

# calculate how much weight of each meat is needed
calculator.weight_needed_by_meat(groups)

# calculate the best combination
items = calculator.calculate_best_options(meat_options, grill_specials)

# return a list of receipt items
receipt_items = ReceiptItemAction.create_receipt_items(items)

receipt_action = ReceiptAction()
# return a receipt object
receipt = receipt_action.create_receipt(receipt_items)

receipt_action.print_receipt(receipt)
print("Time left until first of May:", FirstMayTime.time_left_until_first_may())
