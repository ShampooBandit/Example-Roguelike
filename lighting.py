
# xx, xy, yx, yy
OCTANT_TRANSFORM = [
    (1, 0, 0, 1),
    (0, 1, 1, 0),
    (0, -1, 1, 0),
    (-1, 0, 0, 1),
    (-1, 0, 0, -1),
    (0, -1, -1, 0),
    (0, 1, -1, 0),
    (1, 0, 0, -1)
]

def computeVisibility(dungeon, position, radius):
    dungeon.visible[position[0]][position[1]] = 1

    for i in range(8):
        castLight(dungeon, position, radius, 1, 1, 0, OCTANT_TRANSFORM[i])

def castLight(dungeon, position, radius, row, start, end, transform):
    if start < end:
        return
    
    radius_squared = radius * radius

    for j in range(row, radius+1):
        dx, dy = -j-1, -j
        blocked = False
        while dx <= 0:
            dx += 1

            xpos = position[0] + dx * transform[0] + dy * transform[1]
            ypos = position[1] + dx * transform[2] + dy * transform[3]

            l_slope, r_slope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)

            if start < r_slope:
                continue
            elif end > l_slope:
                break
            else:
                if dx*dx + dy*dy < radius_squared:
                    dungeon.setVisible(xpos, ypos)
                if blocked:
                    if dungeon.checkSolid(xpos, ypos):
                        new_start = r_slope
                        continue
                    else:
                        blocked = False
                        start = new_start
                else:
                    if dungeon.checkSolid(xpos, ypos) and j < radius:
                        blocked = True
                        castLight(dungeon, position, radius, j+1, start, l_slope, transform)
                        new_start = r_slope
        if blocked:
            break