# Topology Morphing #

We start with the following simple star topology:

         h2        
         |
         |
h1 ----- s1 ----- h3 

# Task 1: Show everything works
We ping all the host to be sure that the controller works and everyone is connected.

# Task 2: Modify the topology of the network
First we disable all switch-host links. Then, we add new virtual links to connect h1 and h3 with h2 (who embedds a linux router) obtaining the following topology:

        s1

h1------h2------h3

# Task 3: Make sure that the router correctly delivers all the packets
We have to re-define the default gateway of other hosts so that they send packets to the router (h2) instead of sending them to the switch (s1). Then we ping all the hosts to show that everyone remains connected even without the switch.

# Run the example with:
- $sudo mn -c
- $ryu-manager topology_morphing.py &
- $sudo python3 star.py
