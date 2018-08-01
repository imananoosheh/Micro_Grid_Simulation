from ctl_logic import *
import random

test_pv = PV()
test_battery = Battery(random.randrange(0,101),random.randrange(0,101))
test_load = Load(random.randrange(0,101))
test_grid = Grid(random.randrange(0,101))
test_ac = AC_Hub(test_grid,test_load)
test_dc = DC_Hub(test_battery,test_pv)

test_microgrid = Microgrid(0,0,test_ac,test_dc)


#creating and adding nodes

n1 = Node1(1,test_microgrid)
test_microgrid.add_node(n1)

n2 = Node2(2,test_microgrid)
test_microgrid.add_node(n2)

n3 = Node3(3,test_microgrid)
test_microgrid.add_node(n3)

n4 = Node4(4,test_microgrid)
test_microgrid.add_node(n4)

n5 = Node5(5,test_microgrid)
test_microgrid.add_node(n5)

n6 = Node6(6,test_microgrid)
test_microgrid.add_node(n6)

n7 = Node7(7,test_microgrid)
test_microgrid.add_node(n7)

n8 = Node8(8,test_microgrid)
test_microgrid.add_node(n8)

n9 = Node9(9,test_microgrid)
test_microgrid.add_node(n9)

n10 = Node10(10,test_microgrid)
test_microgrid.add_node(n10)

n11 = Node11(11,test_microgrid)
test_microgrid.add_node(n11)

n12 = Node12(12,test_microgrid)
test_microgrid.add_node(n12)

n13 = Node13(13,test_microgrid)
test_microgrid.add_node(n13)

n14 = Node14(14,test_microgrid)
test_microgrid.add_node(n14)

n15 = Node15(15,test_microgrid)
test_microgrid.add_node(n15)

n16 = Node16(16,test_microgrid)
test_microgrid.add_node(n16)

n17 = Node17(17,test_microgrid)
test_microgrid.add_node(n17)

test_microgrid.set_next_node(n1)

def func(num):
    first = True
    while(num > 0):
        if test_microgrid.next_node == n1:
            test_microgrid.dc_hub.battery.set_pwr_battery(random.randrange(0,101))
            test_microgrid.ac_hub.load.set_pwr_load(random.randrange(0,101))
            test_microgrid.dc_hub.pv.set_pwr_pv()
            test_microgrid.dc_hub.battery.set_soc(random.randrange(0,101))
        print("-------------------------------------------------------------")
        print("Current Node is : " + str(test_microgrid.next_node.id_number))
        print("SoC is : " + str(test_microgrid.dc_hub.battery.get_soc()) + "%")
        print("battery power is : " + str(test_microgrid.dc_hub.battery.get_pwr_battery()) )
        print("PV power is : " + str(test_microgrid.dc_hub.pv.get_pwr_pv()))
        print("Load / Grid is :" + str(test_microgrid.ac_hub.load.get_pwr_load()))
        test_microgrid.next_node.function()
        num -= 1
        print("-------------------------------------------------------------")
        
func(50)
