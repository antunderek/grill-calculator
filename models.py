class Meat:
    def __init__(self, name, weight, price):
        self.name = name
        self.weight = weight
        self.price = price


class GrillSpecial:
    def __init__(self, name, meats, price):
        self.name = name
        self.meats = meats
        self.weight = self.calc_weight()
        self.price = price
    
    def calc_weight(self):
        weight = 0
        for meat in self.meats:
            weight += meat.weight
        return weight


class Group:
    def __init__(self, name, size, meats, avg_consumption):
        self.name = name
        self.size = size
        self.meats = meats
        self.avg_consumption = avg_consumption

    # how much of each meat will group consume
    def each_meat_weight(self):
        return (self.size * self.avg_consumption)//len(self.meats)


class ReceiptItem:
    def __init__(self, meat, amount, price):
        self.meat = meat
        self.amount = amount
        self.price = price


class Receipt:
    def __init__(self, receipt_items, total_price):
        self.receipt_items = receipt_items
        self.total_price = total_price
