# copyright 2003-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-common.
#
# logilab-common is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option) any
# later version.
#
# logilab-common is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-common.  If not, see <http://www.gnu.org/licenses/>.
"""
unit tests for module logilab.common.tree
squeleton generated by /home/syt/bin/py2tests on Jan 20 at 10:43:25
"""

from logilab.common.testlib import TestCase, unittest_main
from logilab.common.tree import (
    Node,
    NodeNotFound,
    post_order_list,
    PostfixedDepthFirstIterator,
    pre_order_list,
    PrefixedDepthFirstIterator,
)

tree = (
    "root",
    (
        ("child_1_1", (("child_2_1", ()), ("child_2_2", (("child_3_1", ()),)))),
        ("child_1_2", (("child_2_3", ()),)),
    ),
)


def make_tree(tuple):
    n = Node(tuple[0])
    for child in tuple[1]:
        n.append(make_tree(child))
    return n


class Node_ClassTest(TestCase):
    """a basic tree node, caracterised by an id"""

    def setUp(self):
        """called before each test from this class"""
        self.o = make_tree(tree)

    def test_flatten(self):
        result = [r.id for r in self.o.flatten()]
        expected = [
            "root",
            "child_1_1",
            "child_2_1",
            "child_2_2",
            "child_3_1",
            "child_1_2",
            "child_2_3",
        ]
        self.assertListEqual(result, expected)

    def test_flatten_with_outlist(self):
        resultnodes = []
        self.o.flatten(resultnodes)
        result = [r.id for r in resultnodes]
        expected = [
            "root",
            "child_1_1",
            "child_2_1",
            "child_2_2",
            "child_3_1",
            "child_1_2",
            "child_2_3",
        ]
        self.assertListEqual(result, expected)

    def test_known_values_remove(self):
        """
        remove a child node
        """
        self.o.remove(self.o.get_node_by_id("child_1_1"))
        self.assertRaises(NodeNotFound, self.o.get_node_by_id, "child_1_1")

    def test_known_values_replace(self):
        """
        replace a child node with another
        """
        self.o.replace(self.o.get_node_by_id("child_1_1"), Node("hoho"))
        self.assertRaises(NodeNotFound, self.o.get_node_by_id, "child_1_1")
        self.assertEqual(self.o.get_node_by_id("hoho"), self.o.children[0])

    def test_known_values_get_sibling(self):
        """
        return the sibling node that has given id
        """
        self.assertEqual(self.o.children[0].get_sibling("child_1_2"), self.o.children[1], None)

    def test_raise_get_sibling_NodeNotFound(self):
        self.assertRaises(NodeNotFound, self.o.children[0].get_sibling, "houhou")

    def test_known_values_get_node_by_id(self):
        """
        return node in whole hierarchy that has given id
        """
        self.assertEqual(self.o.get_node_by_id("child_1_1"), self.o.children[0])

    def test_raise_get_node_by_id_NodeNotFound(self):
        self.assertRaises(NodeNotFound, self.o.get_node_by_id, "houhou")

    def test_known_values_get_child_by_id(self):
        """
        return child of given id
        """
        self.assertEqual(
            self.o.get_child_by_id("child_2_1", recurse=1), self.o.children[0].children[0]
        )

    def test_raise_get_child_by_id_NodeNotFound(self):
        self.assertRaises(NodeNotFound, self.o.get_child_by_id, nid="child_2_1")
        self.assertRaises(NodeNotFound, self.o.get_child_by_id, "houhou")

    def test_known_values_get_child_by_path(self):
        """
        return child of given path (path is a list of ids)
        """
        self.assertEqual(
            self.o.get_child_by_path(["root", "child_1_1", "child_2_1"]),
            self.o.children[0].children[0],
        )

    def test_raise_get_child_by_path_NodeNotFound(self):
        self.assertRaises(NodeNotFound, self.o.get_child_by_path, ["child_1_1", "child_2_11"])

    def test_known_values_depth_down(self):
        """
        return depth of this node in the tree
        """
        self.assertEqual(self.o.depth_down(), 4)
        self.assertEqual(self.o.get_child_by_id("child_2_1", True).depth_down(), 1)

    def test_known_values_depth(self):
        """
        return depth of this node in the tree
        """
        self.assertEqual(self.o.depth(), 0)
        self.assertEqual(self.o.get_child_by_id("child_2_1", True).depth(), 2)

    def test_known_values_width(self):
        """
        return depth of this node in the tree
        """
        self.assertEqual(self.o.width(), 3)
        self.assertEqual(self.o.get_child_by_id("child_2_1", True).width(), 1)

    def test_known_values_root(self):
        """
        return the root node of the tree
        """
        self.assertEqual(self.o.get_child_by_id("child_2_1", True).root(), self.o)

    def test_known_values_leaves(self):
        """
        return a list with all the leaf nodes descendant from this task
        """
        self.assertEqual(
            self.o.leaves(),
            [
                self.o.get_child_by_id("child_2_1", True),
                self.o.get_child_by_id("child_3_1", True),
                self.o.get_child_by_id("child_2_3", True),
            ],
        )

    def test_known_values_lineage(self):
        c31 = self.o.get_child_by_id("child_3_1", True)
        self.assertEqual(
            c31.lineage(),
            [
                self.o.get_child_by_id("child_3_1", True),
                self.o.get_child_by_id("child_2_2", True),
                self.o.get_child_by_id("child_1_1", True),
                self.o,
            ],
        )


class post_order_list_FunctionTest(TestCase):
    def setUp(self):
        """called before each test from this class"""
        self.o = make_tree(tree)

    def test_known_values_post_order_list(self):
        """
        create a list with tree nodes for which the <filter> function returned true
        in a post order foashion
        """
        L = [
            "child_2_1",
            "child_3_1",
            "child_2_2",
            "child_1_1",
            "child_2_3",
            "child_1_2",
            "root",
        ]
        li = [n.id for n in post_order_list(self.o)]
        self.assertEqual(li, L, li)

    def test_known_values_post_order_list2(self):
        """
        create a list with tree nodes for which the <filter> function returned true
        in a post order foashion
        """

        def filter(node):
            if node.id == "child_2_2":
                return 0
            return 1

        L = ["child_2_1", "child_1_1", "child_2_3", "child_1_2", "root"]
        li = [n.id for n in post_order_list(self.o, filter)]
        self.assertEqual(li, L, li)


class PostfixedDepthFirstIterator_ClassTest(TestCase):
    def setUp(self):
        """called before each test from this class"""
        self.o = make_tree(tree)

    def test_known_values_next(self):
        L = ["child_2_1", "child_3_1", "child_2_2", "child_1_1", "child_2_3", "child_1_2", "root"]
        iter = PostfixedDepthFirstIterator(self.o)
        o = next(iter)
        i = 0
        while o:
            self.assertEqual(o.id, L[i])
            o = next(iter)
            i += 1


class pre_order_list_FunctionTest(TestCase):
    def setUp(self):
        """called before each test from this class"""
        self.o = make_tree(tree)

    def test_known_values_pre_order_list(self):
        """
        create a list with tree nodes for which the <filter> function returned true
        in a pre order fashion
        """
        L = [
            "root",
            "child_1_1",
            "child_2_1",
            "child_2_2",
            "child_3_1",
            "child_1_2",
            "child_2_3",
        ]
        li = [n.id for n in pre_order_list(self.o)]
        self.assertEqual(li, L, li)

    def test_known_values_pre_order_list2(self):
        """
        create a list with tree nodes for which the <filter> function returned true
        in a pre order fashion
        """

        def filter(node):
            if node.id == "child_2_2":
                return 0
            return 1

        L = ["root", "child_1_1", "child_2_1", "child_1_2", "child_2_3"]
        li = [n.id for n in pre_order_list(self.o, filter)]
        self.assertEqual(li, L, li)


class PrefixedDepthFirstIterator_ClassTest(TestCase):
    def setUp(self):
        """called before each test from this class"""
        self.o = make_tree(tree)

    def test_known_values_next(self):
        L = ["root", "child_1_1", "child_2_1", "child_2_2", "child_3_1", "child_1_2", "child_2_3"]
        iter = PrefixedDepthFirstIterator(self.o)
        o = next(iter)
        i = 0
        while o:
            self.assertEqual(o.id, L[i])
            o = next(iter)
            i += 1


if __name__ == "__main__":
    unittest_main()
