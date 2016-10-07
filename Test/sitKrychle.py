import copy

(north, east, south, west) = (0, 1, 2, 3)

def vecplus(v1, v2):
    return list(map(lambda x: x[0]+x[1],list(zip(v1, v2))))

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
    result_positions = []
    start_faces = {1: [[2, 3, 5, 4], 1], 2: [[6, 3, 1, 4], 1], 3: [[2, 6, 5, 1], 1],
                   5: [[1, 3, 6, 4], 1], 4: [[2, 1, 5, 6], 1], 6: [[5, 3, 2, 4], 1]}

    def __init__(self, another_cube=None):
        if another_cube == None:
            # {face: [[neighbours], visited]}
            self.cube_faces = copy.deepcopy(Cube.start_faces)
            # list of (number of face, [coords])
            self.cube_net = []
            # bottom face
            self.bottom = 0
            self.place = None
        else:
            self.cube_faces = copy.deepcopy(another_cube.cube_faces)
            self.cube_net = copy.deepcopy(another_cube.cube_net)
            self.bottom = another_cube.bottom

    def _update_faces_along_net(self):
        self.cube_faces = copy.deepcopy(Cube.start_faces)
        for fc,pos in self.cube_net:
            self.cube_faces[fc[1]][1] -= 1

    def get_copy_position(self):
        """return position and orientation of the cube
        I'd like to bind this data to every explored face of net and so I could continue exploring from this
        face many times with different "cube_net"
        """
        return copy.deepcopy(self.cube_faces), self.bottom

    def set_copy_position(self, copy_pos):
        self.cube_faces = copy_pos[0]
        self.bottom = copy_pos[1]
        self._update_faces_along_net()

    def put_cube(self, side):
        """put cube on the side and write the first frame to the net """
        self.cube_faces[side][1] -= 1
        self.bottom = side
        self.place = [0, 0]
        self.cube_net.append((self.get_copy_position(), [0, 0]))

    def get_future_bottom_place(self, course):
        """ input -> course, output -> (future_bottom, [coords of place])"""
        fb = self.cube_faces[self.bottom][0][course]
        if course == 0:
            return fb, vecplus(self.cube_net[-1][1], [0, -1])
        elif course == 1:
            return fb, vecplus(self.cube_net[-1][1], [1, 0])
        elif course == 2:
            return fb, vecplus(self.cube_net[-1][1], [0, 1])
        elif course == 3:
            return fb, vecplus(self.cube_net[-1][1], [-1, 0])

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
            rotation(self.cube_faces[ns][0], 1)
            rotation(self.cube_faces[ss][0], -1)
            rotation(self.cube_faces[7-self.bottom][0], 2)
        elif course == 2:
            rs = self.cube_faces[self.bottom][0][east]
            ls = self.cube_faces[self.bottom][0][west]
            rotation(self.cube_faces[rs][0], 1)
            rotation(self.cube_faces[ls][0], -1)
        elif course == 3:
            ns = self.cube_faces[self.bottom][0][north]
            ss = self.cube_faces[self.bottom][0][south]
            rotation(self.cube_faces[ns][0], -1)
            rotation(self.cube_faces[ss][0], 1)
            rotation(self.cube_faces[7-self.bottom][0], 2)

    def return_cube(self, fromcourse):

        if len(self.cube_net) == 1:
            self.cube_net = []
            self.bottom = 0
            self.place = None
            return
        fb,fp = self.get_future_bottom_place((fromcourse+2)%4)
        # make place empty again
        self.cube_net = list(filter(lambda x:x[1] != self.place, self.cube_net))
        # build our cube to the right previous position
        self.place = fp
        self.set_copy_position((next(filter(lambda x: x[1] == self.place, self.cube_net)))[0])

    def turn_cube(self, course):
        """turn cube to the 0->north, 1->east, 2->south, 3->west """
        if not (course in [0, 1, 2, 3]):
            return False
        # future bottom and future place?
        (fb, fp) = self.get_future_bottom_place(course)
        # I have been there already
        if self.cube_faces[fb][1] == 0 or  not self.is_empty_place(fp):
            return False
        self._turn(course)
        self.bottom = fb
        self.cube_faces[fb][1] -= 1
        self.cube_net.append((self.get_copy_position(), fp))
        self.place = fp
        return True

    def solve_position(self, course):
        if not self.turn_cube(course):
            # we are on the same place
            return
        if self.is_net_complete():
            print(self.cube_net)
            self.result_positions.append(self.cube_net)
            self.return_cube(course)
            return
        # save my position
        my_position = self.get_copy_position()
        for pos, pl in self.cube_net:
            self.set_copy_position(pos)
            for crs in range(4):
                self.solve_position(crs)
        # get back my position
        self.set_copy_position(my_position)
        self.return_cube(course)
        return

    def is_net_complete(self):
        return not any(x > 0 for x in [self.cube_faces[y][1] for y in self.cube_faces])

    def is_face_on_net(self, fc):
        return any(x[0][1] == fc for x in self.cube_net)

    def is_empty_place(self, pl):
        return not any(x[1] == pl for x in self.cube_net)

k = Cube()
k.put_cube(1)
k.solve_position(north)

