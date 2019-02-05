import matplotlib.pyplot as plt
import math

def angle(dx, dy):
    """Used for movement direction calculation. Returns atan2(dy,dx) in degrees between 0 and 360"""

    if dx is not None and dy is not None:
        return int(math.fmod(math.degrees(math.atan2(dy, dx)) + 360, 360))
    else:
        return None
def norm_angle(p1, p2):
    """Used for orientation calculation. Returns the degree of the normal vector between the two points in degrees between 0 and 360"""
    if p1 is not None and p2 is not None:
        dx = (p2[0] - p1[0]) * 1.0  # x2-x1
        dy = (p2[1] - p1[1]) * 1.0
        #  important: dx and dy are changed up (atan2(dx,dy) instead of atan2(dy,dx)) to have a 90 degrees turn (because it's a normal vector)
        #  +360 is added to avoid negative values
        #  mod 360 is applied to have a result between 0 and 360
        return int(math.fmod((360-(math.degrees(math.atan2(dy, dx)) + 90)), 360))
    else:
        return None

print "testing the angle calculation"

p1=(120, 45)
p2=(110, 55)
p3=(165, 270)
p4=(170, 260)

p5=(400, 270)
p6=(413, 270)

p7=(430, 105)
p8=(417, 95)

fig, ax = plt.subplots(1, figsize=(8, 6))
ax.plot(639,359, '*w')
ax.plot(0,359, '*w')
ax.plot(639,0, '*w')
ax.plot(0,0, '*w')

ax.plot(p1[0], p1[1], '*g')
ax.plot(p2[0], p2[1], '*r')
ax.annotate(str(norm_angle(p1, p2)), xy=p1)

ax.plot(p3[0],p3[1], '*g')
ax.plot(p4[0],p4[1], '*r')
ax.annotate(str(norm_angle(p3, p4)), xy=p3)

ax.plot(p5[0], p5[1], '*g')
ax.plot(p6[0], p6[1], '*r')
ax.annotate(str(norm_angle(p5, p6)), xy=p5)

ax.plot(p7[0], p7[1], '*g')
ax.plot(p8[0], p8[1], '*r')
ax.annotate(str(norm_angle(p7, p8)), xy=p7)

fig.gca().invert_yaxis()
print ("calculated normal vectors:")
print ("p1, p2:", norm_angle(p1, p2))
print ("p3, p4:", norm_angle(p3, p4))
print ("p5, p6:", norm_angle(p5, p6))
print ("p7, p8:", norm_angle(p7, p8))

#plt.grid(b=True, which='major', color='#666666', linestyle='-')
plt.show()
