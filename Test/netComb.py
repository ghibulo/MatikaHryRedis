import itertools

(north, east, south, west) = (0, 1, 2, 3)



"""
1  2  3  4
5  6  7  8
9  10 11 12
13 14 15 16
"""

netmap = {1:[2,5], 2:[1,6,3], 3:[2,7,4], 4:[3,8],
          5:[1,6,9], 6:[2,5,10,7], 7:[3,6,11,8], 8:[4,7,12],
          9:[5,10,13], 10:[6,9,14,11], 11:[7,10,15,12], 12:[8,11,16],
          13:[9,14], 14:[13,10,15], 15:[14,11,16], 16:[15,12]}


def update_netmap():
    """ add coord to every number"""
    lst = []
    for x in range(4):
        for y in range(4):
            lst.append((x, y))
    global netmap
    for i in range(16):
        netmap[i+1] = [netmap[i+1], lst[i]]
    return


def is_only_one_group(hx):
    """ is every number a neighbour of any other?"""
    stack = [hx[0]]
    other = list(hx[1:])
    while True:
        again = False
        for i in other:
            for j in stack:
                if i in netmap[j]:
                    other.remove(i)
                    stack.append(i)
                    again = True
                    break
        if not again:
            break
    return len(stack) == 6


def vecplus(v1, v2):
    return tuple(map(lambda x: x[0]+x[1],list(zip(v1, v2))))

def rotation(lst, direction = 1):
    """lst -> list
   direction: 1 -> clockwise, (-1) -> anticlockwise"""
    while direction > 0:
        direction -= 1
        lst.insert(0,lst[-1])
        lst.pop()
        if direction == 0:
            return lst
    while direction < 0:
        direction += 1
        lst.append(lst[0])
        lst.pop(0)
        if direction == 0:
            return lst


class Cube:

    def __init__(self, scheme):
        # {face: [[neighbours], visited]}
        self.cube_faces = {1: [[2, 3, 5, 4], 1], 2: [[6, 3, 1, 4], 1], 3: [[2, 6, 5, 1], 1],
                           5: [[1, 3, 6, 4], 1], 4: [[2, 1, 5, 6], 1], 6: [[5, 3, 2, 4], 1]}
        # list of (number of face, [coords])
        # bottom face
        self.bottom = 0
        self.place = None
        self.scheme = dict(map(lambda x: (x,-1), scheme))
        self.scheme_keys = list(self.scheme)
        self.solved = False
        self.isCube = False

    def put_cube(self, side=1, place = None):
        """put cube on the side and write the first frame to the net """
        self.cube_faces[side][1] = 0
        self.bottom = side
        if place == None:
            self.place = self.scheme_keys[0]
        else:
            self.place = place
        self.scheme[self.place] = self.bottom


    def get_future_bottom_place(self, course):
        """ input -> course, output -> (future_bottom, [coords of place])"""
        fb = self.cube_faces[self.bottom][0][course]
        if course == 0:
            return fb, vecplus(self.place, [0, -1])
        elif course == 1:
            return fb, vecplus(self.place, [1, 0])
        elif course == 2:
            return fb, vecplus(self.place, [0, 1])
        elif course == 3:
            return fb, vecplus(self.place, [-1, 0])

    def _turn(self, course):
        """to change "cube_faces" along the course"""
        if course == 0:
            rs = self.cube_faces[self.bottom][0][east]
            ls = self.cube_faces[self.bottom][0][west]
            rotation(self.cube_faces[rs][0], -1)
            rotation(self.cube_faces[ls][0], 1)
        elif course == 1:
            ns = self.cube_faces[self.bottom][0][north]
            ss = self.cube_faces[self.bottom][0][south]
            ws = self.cube_faces[self.bottom][0][west]
            rotation(self.cube_faces[ns][0], 1)
            rotation(self.cube_faces[ss][0], -1)
            rotation(self.cube_faces[ws][0], 2)
            rotation(self.cube_faces[7-self.bottom][0], 2)
        elif course == 2:
            rs = self.cube_faces[self.bottom][0][east]
            ls = self.cube_faces[self.bottom][0][west]
            rotation(self.cube_faces[rs][0], 1)
            rotation(self.cube_faces[ls][0], -1)
        elif course == 3:
            ns = self.cube_faces[self.bottom][0][north]
            ss = self.cube_faces[self.bottom][0][south]
            es = self.cube_faces[self.bottom][0][east]
            rotation(self.cube_faces[ns][0], -1)
            rotation(self.cube_faces[ss][0], 1)
            rotation(self.cube_faces[es][0], 2)
            rotation(self.cube_faces[7-self.bottom][0], 2)

    def turn_cube(self, course):
        """turn cube to the 0->north, 1->east, 2->south, 3->west """
        if not (course in [0, 1, 2, 3]):
            raise Exception()
        # future bottom and future place?
        (fb, fp) = self.get_future_bottom_place(course)
        if not fp in self.scheme_keys:
            return False
        if self.cube_faces[fb][1] == 0 and self.scheme[fp] == -1:
            self.solved = True
            return False
        if self.cube_faces[fb][1] > 0 and (self.scheme[fp] > -1):
            self.solved = True
            return False
        self._turn(course)
        self.bottom = fb
        self.cube_faces[fb][1] = 0
        self.place = fp
        self.scheme[fp] = self.bottom
        if self.is_net_complete():
            self.solved = True
            self.isCube = True
        return True


    def is_net_complete(self):
        """every face of cube was already bottom?"""
        return not any(x > 0 for x in [self.cube_faces[y][1] for y in self.cube_faces])



    def solve_course(self,  course):
        """
        :param cb: Cube
        :param net: list of [(1,2),-1] elements - first: coords, second: never be there
        :return:
        """
        back = (course+2)%4
        if self.turn_cube(course):
            for i in range(4):
                if self.solved:
                    break
                if i != back:
                    self.solve_course(i)
        else:
            return
        self.turn_cube(back)

    def solve(self):
        """
        :return: is a net of the cube? -> True/False
        """
        for i in range(4):
            self.solve_course(i)
            if self.solved:
                return
        if not self.solved:
            self.solved = True
            self.isCube = self.is_net_complete()
        return self.isCube


def num_to_coord(lst):
    return list(map(lambda x: netmap[x][1], lst))


def solve_net(lst_coo):
    """
    :param list of coords
    :return if net-cube -> dictionary of signed faces, else original list
    """
    k = Cube(lst_coo)
    k.put_cube()
    k.solve()
    if k.isCube:
        return k.scheme
    else:
        return lst_coo


def normalize_coord(lst_c):
    """
    to move coords in list to top-left
    return: list of normalized coords
    """
    l = 5
    t = 5
    for x,y in lst_c:
        if x < l:
            l=x
        if y < t:
            t=y
    return [(x-l, y-t) for x,y in lst_c]


# all combination 16 over 6
all = list(itertools.combinations([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],6))

# filter only contained into one group
connected = list(filter(is_only_one_group,all))

# global netmap is a dictionary and contains for key 1, 2, ... 16 elements like [[1, 6, 3], (0, 1)]
# el[0] - neighbours of the element
# el[1] - coord of the element
update_netmap()

# global netmap help me to convert numbers into coords
concoo = list(map(num_to_coord, connected))

# all coords move to left-top
norm_concoo = list(map(normalize_coord, concoo))

# elements of norm_concoo into hashtable tuple and the list convert into set (remove duplicates)
all_connected_coord = set([tuple(x) for x in norm_concoo])

# filter only nets of cube
result = list(map(solve_net,all_connected_coord))

#  divide for net-cube and the other...
res_cubes = list(filter(lambda x: type(x) is dict, result))
# nocubes will be important for generate test question too...
res_nocubes = list(filter(lambda x: not type(x) is dict, result))

if __name__ == '__main__':
    print("res_cubes = ", res_cubes)
    print("len(res_cubes) = ", len(res_cubes))
    print(10*"-")
    print("res_nocubes = ", res_nocubes)
    print("len(res_nocubes) = ", len(res_nocubes))
    print(10*"-")

#result = list(filter(solve_net,concoo))
#print(len(result))
#print(result)
#k = Cube([(1,1), (2,0), (2,1), (3,1), (2,2), (2,3) ])
#k.put_cube(1,(2,1))
# k.turn_cube(1)
#k.solve()
#print(k.isCube)


