import random
import datetime


class DC_Hub:
    def __init__(self,battery,pv):
        self.pv = pv
        self.battery = battery


class Battery:
    def __init__(self,pwr_battery,soc):
        self.pwr_battery = pwr_battery
        self.soc = soc
        self.max_battery_capacity = 10000 #watt
    
    def set_soc(self,arg):
        self.soc = arg

    def get_soc(self):
        return self.soc 
    
    def set_pwr_battery(self,arg):
        self.pwr_battery = arg
    
    def get_pwr_battery(self):
        return self.pwr_battery

    def get_max_battery_capacity(self):
        return self.max_battery_capacity

    def battery_health(self):
        pass
    def charge_battery (self,*args):
        temp = ""
        for num in args:
            if type(num) == int:
                temp += " " +  str(num) + " " 
        print("charge battery" + temp)
            

class PV:
    def __init__(self):
        self.pwr_pv = 0

    def get_pwr_pv(self):
        return self.pwr_pv
    def set_pwr_pv(self):
        localhour = datetime.datetime.now().hour
        localminute = datetime.datetime.now().minute
        if (localhour >= 0) & (localhour < 6 ):
            self.pwr_pv = 0 #watt (no sun)
        elif (localhour >= 6) & (localhour < 12 ):
            self.pwr_pv = ((1000*((localhour-6)*60+localminute)))/(6*60)
            #watt calculation in linear func of y=x which y[0watt:1000watt] and x[6am:12pm]
        elif (localhour >= 12) & (localhour < 18 ):
            self.pwr_pv = (1-(((localhour-12)*60+localminute)/(6*60)))*1000
            #watt calculation in linear func of y=-x which y[1000watt:0watt] and x[12pm:18pm]
        elif (localhour >= 18) & (localhour <= 23 ):
            self.pwr_pv = 0 #watt (no sun)

class AC_Hub:
    def __init__(self,grid,load):
        self.load = load
        self.grid = grid

class Grid:
    def __init__(self,pwr_grid):
        self.pwr_grid = pwr_grid
    
    def set_pwr_grid(self,pwr_grid):
        self.pwr_grid = pwr_grid
    
    def get_pwr_grid(self):
        return self.pwr_grid

    def grid_state_mode(self):
        localhour = datetime.datetime.now().hour
        #temp = random.randrange(0,3)
        if (localhour >= 0) & (localhour < 6 ):
            print ("buying")
            return "buying"
        elif (localhour >= 6) & (localhour < 18 ):
            print("normal")
            return "normal"
        elif (localhour >= 18) & (localhour <= 23 ):
            print("selling")
            return "selling"
        
class Load:
    def __init__(self,pwr_load):
        self.pwr_load = pwr_load

    def supply_load (self,*args):
        temp = ""
        for a in args:
            if type(a) == int:
                temp += " " +  str(a) + " "
        print("supply load" + temp)

    def set_pwr_load(self,arg):
        self.pwr_load = arg
    
    def get_pwr_load(self):
        return self.pwr_load

    def prediction(self):
        pass
    


class Microgrid:
    def __init__(self,e_sell,e_buy,ac_hub,dc_hub):
        self.ac_hub = ac_hub
        self.dc_hub = dc_hub
        self.nodes = []
        self.next_node = Node(0,self)
        self.e_sell = e_sell
        self.e_buy = e_buy

    def get_e_sell(self):
        return self.e_sell

    def set_e_sell(self,arg):
        self.e_sell = arg
    
    def get_e_buy(self):
        return self.e_buy

    def set_e_buy(self,arg):
        self.e_buy = arg

    def add_node(self, n):
        self.nodes.append(n)

    def delete_node(self, n):
        if n in self.nodes:
            self.nodes.remove(n)

    def set_next_node(self, n):
        self.next_node = n

    def sell_load (self,*args):
        temp = ""
        for a in args:
            if type(a) == int:
                self.e_sell += a
                temp +=  " " + str(a) + " "
        print("sell load" + temp)



class Node:
    def __init__(self, id_number, microgrid):
        self.microgrid = microgrid
        self.id_number = id_number
    def goto(self, number):
        for n in self.microgrid.nodes:
            if n.id_number == number:
                self.microgrid.next_node = n
                break
    def function(self):
        raise NotImplementedError()

class Node1(Node):
    def function(self):
        if self.microgrid.ac_hub.load.get_pwr_load() > 0:
            self.goto(3)
        else:
            self.goto(2)

class Node2(Node):
    def function(self):
        if self.microgrid.dc_hub.pv.get_pwr_pv() > 0:
            self.goto(4)
        else:
            self.goto(9)

class Node3(Node):
    def function(self):
        if self.microgrid.dc_hub.pv.get_pwr_pv() >= self.microgrid.ac_hub.load.get_pwr_load():
            self.microgrid.ac_hub.load.supply_load(self.microgrid.dc_hub.pv.get_pwr_pv)
            self.goto(4)
        else:
            self.goto(16)

class Node4(Node):
    def function(self):
        state = self.microgrid.ac_hub.grid.grid_state_mode()
        if state == "buying":
            self.goto(7)
        elif state == "selling":
            self.goto(5)
        elif state == "normal":
            self.goto(6)

class Node5(Node):
    def function(self):
        if self.microgrid.dc_hub.battery.get_soc() > 70:
            self.microgrid.sell_load(self.microgrid.dc_hub.pv.get_pwr_pv(), self.microgrid.dc_hub.battery.get_pwr_battery())
        else:
            self.microgrid.sell_load(self.microgrid.dc_hub.pv.get_pwr_pv())
        self.goto(1)

class   Node6(Node):
    def function(self):
        if self.microgrid.dc_hub.battery.get_soc() > 90:
            self.microgrid.sell_load(self.microgrid.dc_hub.battery.get_pwr_battery())
            self.goto(1)
        else:
            self.microgrid.dc_hub.battery.charge_battery(self.microgrid.dc_hub.pv.get_pwr_pv())
            self.goto(8)

class Node7(Node):
    def function(self):
        if self.microgrid.dc_hub.battery.get_soc() == 100:
            self.microgrid.sell_load(self.microgrid.dc_hub.battery.get_pwr_battery())
            self.goto(1)
        else:
            self.microgrid.dc_hub.battery.charge_battery(self.microgrid.dc_hub.pv.get_pwr_pv(), self.microgrid.ac_hub.grid.get_pwr_grid())
            self.goto(8)

class Node8(Node):
    def function(self):
        if self.microgrid.dc_hub.pv.get_pwr_pv() > 0:
            self.microgrid.sell_load(self.microgrid.dc_hub.battery.get_pwr_battery())
        else:
            pass
        self.goto(1)

class Node9(Node):
    def function(self):
        state = self.microgrid.ac_hub.grid.grid_state_mode()
        if state == "buying":
            self.goto(10)
        elif state == "selling":
            self.goto(11)
        elif state == "normal":
            self.goto(1)

class Node10(Node):
    def function(self):
        if self.microgrid.dc_hub.battery.get_soc() == 100:
            pass
        else:
            self.microgrid.dc_hub.battery.charge_battery(self.microgrid.ac_hub.grid.get_pwr_grid())
        self.goto(1)

class Node11(Node):
    def function(self):
        if self.microgrid.dc_hub.battery.get_soc() > 70:
            self.microgrid.sell_load(self.microgrid.dc_hub.battery.get_pwr_battery())
        else:
            pass
        self.goto(1)

class Node12(Node):
    def function(self):
        if self.microgrid.dc_hub.battery.get_pwr_battery() >= (self.microgrid.ac_hub.load.get_pwr_load() - self.microgrid.dc_hub.pv.get_pwr_pv()):
            self.microgrid.sell_load(self.microgrid.dc_hub.battery.get_pwr_battery())
        else:
            self.microgrid.ac_hub.load.supply_load(self.microgrid.dc_hub.pv.get_pwr_pv(), self.microgrid.dc_hub.battery.get_pwr_battery(), self.microgrid.ac_hub.grid.get_pwr_grid())
        self.goto(1)

class Node13(Node):
    def function(self):
        if self.microgrid.dc_hub.battery.get_pwr_battery() >= (self.microgrid.pwr_load - self.microgrid.dc_hub.pv.get_pwr_pv()):
            self.microgrid.ac_hub.load.supply_load(self.microgrid.dc_hub.pv.get_pwr_pv(), self.microgrid.dc_hub.battery.get_pwr_battery())
        else:
            self.microgrid.ac_hub.load.supply_load(self.microgrid.dc_hub.pv.get_pwr_pv(), self.microgrid.dc_hub.battery.get_pwr_battery(), self.microgrid.ac_hub.grid.get_pwr_grid())
        self.goto(1)

class Node14(Node):
    def function(self):
        if self.microgrid.dc_hub.battery.get_soc() > 70:
            self.goto(12)
        else:
            self.microgrid.ac_hub.load.supply_load(self.microgrid.dc_hub.pv.get_pwr_pv(), self.microgrid.dc_hub.battery.get_pwr_battery(), self.microgrid.ac_hub.grid.get_pwr_grid())
            self.goto(1)

class Node15(Node):
    def function(self):
        if self.microgrid.dc_hub.battery.get_soc() > 0:
            self.goto(13)
        else:
            self.microgrid.ac_hub.load.supply_load(self.microgrid.dc_hub.pv.get_pwr_pv(), self.microgrid.ac_hub.grid.get_pwr_grid())
            self.goto(1)

class Node16(Node):
    def function(self):
        state = self.microgrid.ac_hub.grid.grid_state_mode()
        if state == "buying":
            self.goto(17)
        elif state == "selling":
            self.goto(14)
        elif state == "normal":
            self.goto(15)

class Node17(Node):
    def function(self):
        if self.microgrid.dc_hub.battery.get_soc() == 100:
            self.microgrid.ac_hub.load.supply_load(self.microgrid.dc_hub.pv.get_pwr_pv(), self.microgrid.ac_hub.grid.get_pwr_grid())
        else:
            self.microgrid.dc_hub.battery.charge_battery(self.microgrid.ac_hub.grid.get_pwr_grid())
        self.goto(1)

