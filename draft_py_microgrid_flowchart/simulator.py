from ctl_logic import *

test_grid = Microgrid(100,100,100,100,100)


#creating and adding nodes

n1 = Node1(1,test_grid)
test_grid.add_node(n1)

n2 = Node2(2,test_grid)
test_grid.add_node(n2)

n3 = Node3(3,test_grid)
test_grid.add_node(n3)

n4 = Node4(4,test_grid)
test_grid.add_node(n4)

n5 = Node5(5,test_grid)
test_grid.add_node(n5)

n6 = Node6(6,test_grid)
test_grid.add_node(n6)

n7 = Node7(7,test_grid)
test_grid.add_node(n7)

n8 = Node8(8,test_grid)
test_grid.add_node(n8)

n9 = Node9(9,test_grid)
test_grid.add_node(n9)

n10 = Node10(10,test_grid)
test_grid.add_node(n10)

n11 = Node11(11,test_grid)
test_grid.add_node(n11)

n12 = Node12(12,test_grid)
test_grid.add_node(n12)

n13 = Node13(13,test_grid)
test_grid.add_node(n13)

n14 = Node14(14,test_grid)
test_grid.add_node(n14)

n15 = Node15(15,test_grid)
test_grid.add_node(n15)

n16 = Node16(16,test_grid)
test_grid.add_node(n16)

n17 = Node17(17,test_grid)
test_grid.add_node(n17)

test_grid.next_node(n1)

while(true):
    test_grid.next_node.function()
    