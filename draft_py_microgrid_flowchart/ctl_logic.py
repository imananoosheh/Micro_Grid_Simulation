class Microgrid:
    def __init__(self, total_pwr_consump, pwr_load, pwr_battery, pwr_pv, soc, start_node):
        self.total_pwr_consump = total_pwr_consump
        self.pwr_load = pwr_load
        self.pwr_battery = pwr_battery
        self.pwr_pv = pwr_pv
        self.soc = soc
        self.nodes = []
        self.next_node = None
        
    def set_pwr_load(number):
        self.pwr_load = number

    def get_pwr_load():
        return self.pwr_load

    def set_pwr_battery(number):
        self.pwr_battery = number

    def get_pwr_battery():
        return self.pwr_battery

    def set_pwr_pv(number):
        self.pwr_pv = number

    def get_pwr_pv():
        return self.pwr_pv

    def set_soc(number):
        self.soc = number
    
    def get_soc():
        return self.soc

    def set_total_pwr_consump(number):
        self.total_pwr_consump = number
    
    def get_total_pwr_consump():
        return self.total_pwr_consump

    def add_node(n):
        self.nodes.append(n)

    def delete_node(n):
        if n in self.nodes:
            self.nodes.remove(n)

    def set_next_node(n):
        self.next_node = n

    def charge_battery (*args):
        for num in args:
            self.pwr_battery += num
    
    def supply_load (*args):
        pass
    def sell_load (*args):
        pass
    def grid_state_mode():
        pass

class Node:
    def __init__(self, id_number, microgrid):
        self.microgrid = microgrid
        self.id_number = id_number
    def goto(number):
        for n in self.microgrid.nodes:
            if n.id_number == number:
                self.microgrid.next_node = n
                break
    def function(self):
        raise NotImplementedError()

class Node1(Node):
    def functions(self):
        if self.microgrid.pwr_load > 0:
            self.goto(3)
        else:
            self.goto(2)

class Node2(Node):
    def function(self):
        if self.microgrid.pwr_pv > 0:
            self.goto(4)
        else:
            self.goto(9)

class Node3(Node):
    def function(self):
        if self.microgrid.pwr_pv >= self.microgrid.pwr_load:
            self.microgrid.supply_load(self.microgrid.pwr_pv)
            self.goto(4)
        else:
            self.goto(16)

class Node4(Node):
    def function(self):
        state = self.microgrid.grid_state_mode
        if state == buying:
            self.goto(7)
        elif state == selling:
            self.goto(5)
        elif state == normal:
            self.goto(6)

class Node5(Node):
    def function(self):
        if self.microgrid.soc > 70:
            self.microgrid.sell_load(self.microgrid.pwr_pv, self.microgrid.pwr_battery)
        else:
            self.microgrid.sell_load(self.microgrid.pwr_pv)
        self.goto(1)

class   Node6(Node):
    def function(self):
        if self.microgrid.soc > 90:
            self.microgrid.sell_load(self.microgrid.pwr_battery)
            self.goto(1)
        else:
            self.microgrid.charge_battery(self.microgrid.pwr_pv)
            self.goto(8)

class Node7(Node):
    def function(self):
        if self.microgrid.soc == 100:
            self.microgrid.sell_load(self.microgrid.pwr_battery)
            self.goto(1)
        else:
            self.microgrid.charge_battery(self.microgrid.pwr_pv, self.microgrid.pwr_battery)
            self.goto(8)

class Node8(Node):
    def function(self):
        if self.microgrid.pwr_pv > 0:
            self.microgrid.sell_load(self.microgrid.pwr_battery)
            self.goto(1)
        else:
            self.goto(1)

class Node9(Node):
    def function(self):
        state = self.microgrid.grid_state_mode
        if state == buying:
            self.goto(10)
        elif state == selling:
            self.goto(11)
        elif state == normal:
            self.goto(1)

class Node10(Node):
    def function(self):
        if self.microgrid.soc == 100:

        else:
            self.microgrid.charge_battery(self.microgrid.pwr_load)
        self.goto(1)

class Node11(Node):
    def function(self):
        if self.microgrid.soc > 70:
            self.microgrid.sell_load(self.microgrid.pwr_battery)
        else:

        self.goto(1)

class Node12(Node):
    def function(self):
        if self.microgrid.pwr_battery => (self.microgrid.pwr_load - self.microgrid.pwr_pv):
            self.microgrid.sell_load(self.microgrid.pwr_battery)
        else:
            self.microgrid.supply_load(self.microgrid.pwr_pv, self.microgrid.pwr_battery, self.microgrid.pwr_load)
        self.goto(1)

class Node13(Node):
    def function(self):
        if self.microgrid.pwr_battery => (self.microgrid.pwr_load - self.microgrid.pwr_pv):
            self.microgrid.supply_load(self.microgrid.pwr_pv, self.microgrid.pwr_battery)
        else:
            self.microgrid.supply_load(self.microgrid.pwr_pv, self.microgrid.pwr_battery, self.microgrid.pwr_load)
        self.goto(1)

class Node14(Node):
    def function(self):
        if self.microgrid.soc > 70:
            self.goto(12)
        else:
            self.microgrid.supply_load(self.microgrid.pwr_pv, self.microgrid.pwr_battery, self.microgrid.pwr_load)
            self.goto(1)

class Node15(Node):
    def function(self):
        if self.microgrid.soc > 0:
            self.goto(13)
        else:
            self.microgrid.supply_load(self.microgrid.pwr_pv, self.microgrid.pwr_load)
            self.goto(1)

class Node16(Node):
    def function(self):
        state = self.microgrid.grid_state_mode
        if state == buying:
            self.goto(17)
        elif state == selling:
            self.goto(14)
        elif state == normal:
            self.goto(15)

class Node17(Node):
    def function(self):
        if self.microgrid.soc == 100:
            self.microgrid.supply_load(self.microgrid.pwr_pv, self.microgrid.pwr_load)
        else:
            self.microgrid.charge_battery(self.microgrid.pwr_load)
        self.goto(1)
