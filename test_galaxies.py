#!/usr/bin/env python3

import galaxies
import unittest
#import xmlrunner

class TestCalc(unittest.TestCase):


    def setUp(self):
        self.boards = {
            'b3': galaxies.galaxy_field(3,[(1,1)]),

            # 5x5 normal, ID = 1_758_394
            'b5': galaxies.galaxy_field(5,[(0.5,0), (3.5,0), (2.5,1), (0.5, 2.5), (4, 2.5), (2,3), (3,3.5)]),

            # 7x7 hard, ID = 3_240_019
            'b7': galaxies.galaxy_field(7, [(1.5,0), (4,0), (0,1), (2.5, 1.5), (5,2.5), (3.5, 3.5), (6, 3.5), (1.5, 4.5), (0, 5.5), (1,6), (4.5,6)]),

            # 7x7 hard, ID = 2_243_248
            'b7b': galaxies.galaxy_field(7, [(2,0), (4,0.5), (0,1), (5.5,1.5), (2.5,2), (2.5,3), (2.5,4), (6,4), (0,4.5), (1,5), (5,5), (6,5.5), (2.5,6)]),

            # 7x7 hard, ID = 381_831
            'b7c': galaxies.galaxy_field(7, [(1.5,0.5), (4.5,0.5), (6,0.5), (1,2), (3,2.5), (0,3), (5,3), (1,3.5), (4,4), (0.5,5), (3,5), (5,5), (0,6), (5.5,6)]),

            # 10x10 hard, ID = 2_851_686
            'b10': galaxies.galaxy_field(10, [(5,0.5), (3.5,1), (7,1), (0,1.5), (1.5,2.5), (4,2.5), (7.5,3), (9,3), (0,4), (5,4), (3,5), (8,5), (0.5,7), (4,7), (7,7), (2,7.5), (6,8), (8.5,8), (4,8.5), (0.5,9), (3,9)]),

            # 10x10 hard, ID = 9_710_141
            'b10b': galaxies.galaxy_field(10,[(0.5,0.5),(6,0.5), (9,1), (4,2), (7.5,2), (0.5,2.5), (2.5,3), (8,3), (2,4), (8.5,4), (5,5), (8,5.5), (0.5,6), (5.5,6), (2.5,6.5), (9,7), (6,7.5), (1,8), (0,9), (3,9), (8,9) ]),

            # 15x15 hard, ID: 8_351_812
            'b15': galaxies.galaxy_field(15, [(0.5,0), (5,0), (12,0), (9,0.5), (14,0.5), (2.5,1), (7,1), (11,1), (5.5,1.5), (4,2),  (12,2), (7.5,2.5), (7,4), (9.5,4), (12,4.5), (0.5,5), (4,5), (5.5,5.5), (7.5,5.5), (13,5.5), (3.5,6), (10,6), (14,7), (2.5,7.5), (8.5,7.5), (10.5,7.5), (2,9), (7,9), (13.5,9), (6,9.5), (1,10), (12,10), (3.5,10.5), (14,11), (7.5,11.5), (9,11.5), (11.5,11.5), (10,12), (13,12), (0.5,12.5), (4.5,12.5), (2,13.5), (8,13.5), (10.5,13.5), (13,13.5), (5.5,14) ]),

            # 15x15 hard, ID: 29_126
            'b15b': galaxies.galaxy_field(15,[(2,0), (8,0), (4.5,0.5), (13.5,0.5), (1,1.5), (6,1.5), (10.5,1.5), (3,2), (8,2.5), (13.5,2.5), (0.5,3.5), (4.5,3.5), (7.5,4), (10,4), (13.5,4.5), (4,5), (8,5), (12,5), (6.5,5.5), (9.5,5.5), (0,6), (4,6.5), (13.5,6.5), (1,7), (6,7), (7,8), (3.5,8.5), (8.5,8.5), (10.5,8.5), (12.5,8.5), (5,9), (14,9.5), (1.5,10), (7.5,10), (4.5,11), (8.5,11), (11,11), (0,12), (5,12), (10,12), (6.5,12.5), (13,12.5), (2,13), (4,13), (3,13.5), (9.5,13.5), (4.5,14), (12,14) ])

        }

        self.b3_wrong = galaxies.galaxy_field(3,[(0,0)])
        self.b7_wrong = galaxies.galaxy_field(7, [(1.5,0), (4,0), (0,1), (2.5, 1.5), (5,2.5), (3.5, 3.5), (6, 3.5), (1.5, 4.5), (0, 5.5), (1,6)])

    def test_get_neighbors(self):
        for x in range(5):
            for y in range(5):
                res = self.boards['b5'].get_neighbors(x,y)
                for rx, ry in res:
                    self.assertTrue(rx >= 0)
                    self.assertTrue(rx < 5)
                    self.assertTrue(ry >= 0)
                    self.assertTrue(ry < 5)
                self.assertTrue(len(res) > 1)
                self.assertTrue(len(res) < 5)

    def test_is_connected_galaxy3(self):
        self.boards['b3'].solve(level=2)
        for x in range(3):
            for y in range(3):
                self.assertTrue(self.boards['b3'].is_connected_galaxy(x,y,(1,1)))

    def test_is_connected_galaxy5(self):
        self.assertTrue(not self.boards['b5'].is_connected_galaxy(0,0,(0,2)))
        self.assertTrue(self.boards['b5'].is_connected_galaxy(0,0,(0.5,0)))
        self.assertTrue(not self.boards['b5'].is_connected_galaxy(0,1,(0.5,2.5)))
        self.assertTrue(not self.boards['b5'].is_connected_galaxy(4,4,(0.5,2.5)))

    def test_is_connected_galaxy7(self):
        self.assertTrue(not self.boards['b7'].is_connected_galaxy(1,1,(2.5,1.5)))
        self.boards['b7'].solve(level=2)
        self.assertTrue(self.boards['b7'].is_connected_galaxy(1,1,(2.5,1.5)))
        self.assertTrue(not self.boards['b7'].is_connected_galaxy(5,0,(5,2.5)))
        self.assertTrue(not self.boards['b7'].is_connected_galaxy(0,6,(1,6)))
        self.assertTrue(not self.boards['b7'].is_connected_galaxy(1,5,(1,6)))
        self.assertTrue(not self.boards['b7'].is_connected_galaxy(2,6,(1,6)))

    def test_get_reachable_centers(self):
        self.boards['b7'].solve(level=1)
        for cx, cy in self.boards['b7'].centers:
            cxr, cyr = int(cx), int(cy)
            self.assertTrue(self.boards['b7'].get_reachable_centers(cxr,cyr) == {(cx,cy)})
        self.assertTrue(self.boards['b7'].get_reachable_centers(0,3) == {(1.5, 0), (0, 1), (2.5, 1.5), (3.5, 3.5), (1.5, 4.5), (0, 5.5)})

    def test_get_reachable_and_possible_centers(self):
        self.boards['b7'].solve(level=1)
        self.assertTrue(self.boards['b7'].get_reachable_and_possible_centers(0,3) == { (2.5, 1.5), (1.5, 4.5)})

    def test_get_least_possibilities_position(self):
        self.boards['b7'].solve(level=1)
        self.assertTrue(self.boards['b7'].get_least_possibilities_position() == (0,0, {(0,1), (1.5,0)}))


    def test_simple_solve_phase_2(self):
        self.assertTrue(not self.boards['b3'].is_solved())
        #self.boards['b3'].show()
        self.boards['b3'].solve(level=2)
        #self.boards['b3'].show()
        self.assertTrue(self.boards['b3'].is_solved())

    def test_mark_point_and_mirror_point(self):
        self.boards['b7'].solve(level=1)

        self.boards['b7'].mark_point_and_mirror_point(0,0,(1.5,0))
        self.assertTrue(self.boards['b7'].board[0][0] == (1.5,0))
        self.assertTrue(self.boards['b7'].board[0][3] == (1.5,0))

        self.boards['b7'].mark_point_and_mirror_point(0,3,(1.5,4.5))
        self.assertTrue(self.boards['b7'].board[3][0] == (1.5,4.5))
        self.assertTrue(self.boards['b7'].board[6][3] == (1.5,4.5))

    def test_solve_all(self):
        i=0
        print()
        for b in self.boards.keys():
            with self.subTest("Message for this subtest", board=b):
                print(b)
                self.assertTrue(not self.boards[b].is_solved())
                self.assertTrue(not self.boards[b].unsolvable)
                self.boards[b].show(showgrid=True, showborder=False)
                self.boards[b].solve()
                self.boards[b].show(showgrid=False, showborder=True)
                self.assertTrue(self.boards[b].is_solved())
                self.assertTrue(not self.boards[b].unsolvable)
            i += 1

    def test_unsolvable(self):
        for b in [ self.b3_wrong, self.b7_wrong ]:
            self.assertTrue(not b.is_solved())
            self.assertTrue(not b.unsolvable)
            b.solve()
            self.assertTrue(not b.is_solved())
            self.assertTrue(b.unsolvable)

if __name__ == "__main__":

    #unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    unittest.main()

