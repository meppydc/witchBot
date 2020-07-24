from threading import Timer

def mytimer(num):
      print(f"Timer {num} seconds")
my_timer = Timer(3.0, mytimer, [3.0])
my_timer.start()
my_timer2 = Timer(5.0, mytimer, [5.0]     )
my_timer2.start()
print("Bye\n")
